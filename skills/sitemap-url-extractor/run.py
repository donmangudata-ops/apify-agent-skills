#!/usr/bin/env python3
"""Run Sitemap URL Extractor API (conserving_celerytop/sitemap-url-extractor) on Apify from an agent skill.

Standard library only (Python 3.9+). The Apify token is read from the APIFY_TOKEN environment
variable and sent only in an Authorization header to Apify; it is never printed, stored or put in a URL.
Prices are read live from the public Actor record. Results are written as JSON and as a CSV whose
cells cannot run as spreadsheet formulas.

Run with --help for every flag.
"""
import argparse
import csv
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SKILL_NAME = "sitemap-url-extractor"
ACTOR_ID = "conserving_celerytop/sitemap-url-extractor"
DESCRIPTION = "Run Sitemap URL Extractor API (Sitemap URL extractor) on Apify and save the results as JSON and CSV."
PARAMS = [
    ["startUrls", "list", [], "Websites or sitemaps. Enter websites (example.com), whose sitemaps are found through robots.txt and the usual addresses, or sitemap addresses directly."],
    ["urlContains", "str", [], "URL contains. Keep only URLs that contain this text, for example /blog/ or /products/."],
    ["maxUrlsPerSite", "int", [], "URLs per website. Return at most this many URLs for each website or sitemap you enter."],
    ["maxSitemapsPerSite", "int", [], "Sitemaps per website. Read at most this many sitemap files per website, counting the files inside sitemap indexes."],
    ["maxResults", "int", [], "Maximum URLs. Stop after this many URLs in total."],
]
DEFAULTS = {"maxUrlsPerSite": 1000, "maxSitemapsPerSite": 50, "maxResults": 5000}
ESTIMATE = {"events": ["sitemap-url"], "unit": "URLs", "terms": [["startUrls", "maxUrlsPerSite"]], "cap": "maxResults"}
FILE_KEY = "startUrls"
REQUIRED = ["startUrls"]
LOCAL_FILES_KEY = None
DOWNLOAD_FIELDS = []
OUTPUT_COLUMNS = ["input", "url", "lastModified", "changeFrequency", "priority", "imageCount", "sitemapUrl", "status", "error"]

STORE_URL = "https://apify.com/" + ACTOR_ID
CSV_FORMULA_START = ("=", "+", "-", "@", "\t", "\r")


def api_base():
    return os.environ.get("APIFY_API_BASE_URL", "https://api.apify.com").rstrip("/")


def get_token():
    token = os.environ.get("APIFY_TOKEN", "").strip()
    if not token:
        sys.exit("Set APIFY_TOKEN in the environment first (Apify Console, Settings, API & Integrations). "
                 "Never write the token into a file, a URL or a chat.")
    return token


def http_json(method, url, body=None, token=None, timeout=120, accept="application/json"):
    """Send one HTTPS request and return (parsed JSON, response headers). The token goes only in a header."""
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Accept": accept, "User-Agent": "apify-agent-skills/" + SKILL_NAME}
    if data is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace")
            return (json.loads(raw) if raw.strip() else {}), r.headers
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        sys.exit(f"HTTP {e.code} from {urllib.parse.urlsplit(url).netloc}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {urllib.parse.urlsplit(url).netloc}: {e.reason}")


def live_prices(actor_id):
    """Free-plan price per event, read from the public Actor record (no token sent). None if unreadable."""
    url = f"{api_base()}/v2/acts/{actor_id.replace('/', '~')}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.load(r).get("data") or {}
    except (urllib.error.URLError, OSError, ValueError):
        return None
    infos = data.get("pricingInfos") or []
    info = infos[-1] if infos else (data.get("currentPricingInfo") or {})
    events = ((info.get("pricingPerEvent") or {}).get("actorChargeEvents")) or {}
    out = {}
    for name, ev in events.items():
        price = ((ev.get("eventTieredPricingUsd") or {}).get("FREE") or {}).get("tieredEventPriceUsd")
        if price is None:
            price = ev.get("eventPriceUsd")
        if price is not None:
            out[name] = float(price)
    return out or None


def money(x):
    """Dollar amount with enough digits for small prices: 0.00005, 0.0025, 1.25."""
    return f"{x:.2f}" if x >= 1 else f"{x:.6f}".rstrip("0").rstrip(".")


def total_str(x):
    return f"{x:.2f}" if x >= 0.01 else f"{x:.4f}"


def csv_safe(value):
    """Make one CSV cell safe to open in Excel or Google Sheets.

    The data comes from other people's websites and files. A text cell that starts with
    = + - @ (or a tab or carriage return) would run as a formula, so it gets a leading
    single quote. Lists and objects are written as JSON text and checked the same way.
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    if isinstance(value, str) and value.startswith(CSV_FORMULA_START):
        return "'" + value
    return value


def write_outputs(rows, out_prefix, preferred=()):
    """Write rows to <out>.json (as returned) and <out>.csv (formula-safe)."""
    with open(out_prefix + ".json", "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    cols = [c for c in preferred if any(c in r for r in rows)]
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with open(out_prefix + ".csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([csv_safe(c) for c in cols])
        for r in rows:
            w.writerow([csv_safe(r.get(c)) for c in cols])
    print(f"Wrote {len(rows)} rows to {out_prefix}.json and {out_prefix}.csv")


def split_list(text):
    return [s.strip() for s in (text or "").split(",") if s.strip()]


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.lstrip().startswith("#")]


def kebab(name):
    return "".join("-" + c.lower() if c.isupper() else c for c in name)


def add_param_flags(parser):
    for key, kind, choices, help_text in PARAMS:
        flag = "--" + kebab(key)
        if kind == "bool":
            parser.add_argument(flag, dest=key, action=argparse.BooleanOptionalAction, default=None, help=help_text)
        elif kind == "list":
            parser.add_argument(flag, dest=key, default=None,
                                help=help_text + " Comma-separated." + (f" One or more of: {', '.join(choices)}." if choices else ""))
        elif kind == "int":
            parser.add_argument(flag, dest=key, type=int, default=None, help=help_text)
        elif kind == "num":
            parser.add_argument(flag, dest=key, type=float, default=None, help=help_text)
        else:
            parser.add_argument(flag, dest=key, default=None, choices=choices or None, help=help_text)


def build_input(args):
    run_input = {}
    if args.input_file:
        with open(args.input_file, encoding="utf-8") as f:
            run_input.update(json.load(f))
    if args.input_json:
        run_input.update(json.loads(args.input_json))
    for key, kind, choices, _ in PARAMS:
        value = getattr(args, key, None)
        if value is None:
            continue
        if kind == "list":
            value = split_list(value)
            bad = [v for v in value if choices and v not in choices]
            if bad:
                sys.exit(f"--{kebab(key)}: {bad} not allowed. Use: {', '.join(choices)}")
        run_input[key] = value
    if FILE_KEY and args.file:
        run_input[FILE_KEY] = list(dict.fromkeys((run_input.get(FILE_KEY) or []) + read_lines(args.file)))
    return run_input


def schema_default(key):
    return DEFAULTS.get(key)


def estimate_count(run_input):
    """Upper bound of billed units for the main event, or None when it cannot be known before the run."""
    spec = ESTIMATE
    if not spec:
        return None
    for key in spec.get("unknown_if", []):
        if run_input.get(key):
            return None
    total, any_term = 0, False
    for list_key, per_key in spec.get("terms", []):
        items = run_input.get(list_key) or []
        if items:
            any_term = True
            per = 1
            if per_key:
                per = run_input.get(per_key, schema_default(per_key)) or 1
            total += len(items) * int(per)
    cap_key = spec.get("cap")
    cap = run_input.get(cap_key, schema_default(cap_key)) if cap_key else None
    if not any_term:
        return int(cap) if cap is not None else None
    return min(total, int(cap)) if cap is not None else total


def estimate(run_input, actor_id=None):
    """Print the estimated ceiling from live prices and return it in USD (None if unknown)."""
    actor_id = actor_id or ACTOR_ID
    prices = live_prices(actor_id)
    events = ESTIMATE.get("events", [])
    for field, mapping in (ESTIMATE.get("event_by") or {}).items():
        chosen = mapping.get(str(run_input.get(field, schema_default(field))))
        if chosen:
            events = [chosen]
    print(f"Prices of {actor_id} on the free Apify plan (paid plans pay less), read live:")
    if not prices:
        print(f"  Could not read live prices. Check the Pricing tab: {STORE_URL}")
        return None
    for name, price in sorted(prices.items()):
        print(f"  {name}: ${money(price)}")
    count = estimate_count(run_input)
    unit = max((prices.get(e) or 0.0) for e in events) if events else 0.0
    if count is None or not unit:
        print(f"  The number of billed {ESTIMATE.get('unit', 'units')} is not known before the run.")
        return None
    total = count * unit + prices.get("apify-actor-start", 0.0)
    print(f"  Ceiling: up to {count} {ESTIMATE.get('unit', 'units')} x ${money(unit)} = about ${total_str(total)}")
    return total


def resolve_cap(user_cap, total):
    if user_cap is not None:
        return user_cap
    if total is None:
        sys.exit("The cost cannot be estimated before the run, so pass --max-charge (a hard cap in USD).")
    return max(0.05, math.ceil(total * 1.25 * 100) / 100)


def confirm_spend(cap, yes):
    if cap > 1.0 and not yes:
        sys.exit(f"The spending cap is ${cap:.2f}, above $1. Confirm with the user, then rerun with --yes.")


TERMINAL = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}


def run_actor(run_input, cap, token):
    """Start the Actor with a hard spending cap, wait for it, and return the run record."""
    act = ACTOR_ID.replace("/", "~")
    query = urllib.parse.urlencode({"maxTotalChargeUsd": f"{cap:.2f}", "waitForFinish": 60})
    print(f"Running {ACTOR_ID} with a spending cap of ${cap:.2f}...")
    run = http_json("POST", f"{api_base()}/v2/acts/{act}/runs?{query}", run_input, token)[0].get("data") or {}
    run_id = run.get("id")
    if not run_id:
        sys.exit("The run did not start.")
    print(f"  Run {run_id}: https://console.apify.com/actors/runs/{run_id}")
    while run.get("status") not in TERMINAL:
        time.sleep(2)
        run = http_json("GET", f"{api_base()}/v2/actor-runs/{run_id}?waitForFinish=60", token=token)[0].get("data") or {}
        print(f"  status: {run.get('status')}")
    print(f"  Finished: {run.get('status')}. Charged events: {run.get('chargedEventCounts') or 'none reported'}")
    if run.get("status") != "SUCCEEDED":
        print("  The run did not finish cleanly; rows may be partial. Rows past the cap are not returned.")
    return run


def dataset_items(dataset_id, token, page=1000):
    rows, offset = [], 0
    while True:
        q = urllib.parse.urlencode({"clean": "true", "format": "json", "offset": offset, "limit": page})
        url = f"{api_base()}/v2/datasets/{dataset_id}/items?{q}"
        batch = http_json("GET", url, token=token)[0]
        if not isinstance(batch, list) or not batch:
            break
        rows.extend(batch)
        offset += len(batch)
        if len(batch) < page:
            break
    return rows


def download_files(rows, folder, token):
    """Save the files the Actor produced (links in DOWNLOAD_FIELDS) into a local folder."""
    os.makedirs(folder, exist_ok=True)
    saved = 0
    for i, r in enumerate(rows, 1):
        for field in DOWNLOAD_FIELDS:
            link = r.get(field)
            if not isinstance(link, str) or not link.startswith("https://"):
                continue
            host = urllib.parse.urlsplit(link).netloc
            headers = {"User-Agent": "apify-agent-skills/" + SKILL_NAME}
            if host == urllib.parse.urlsplit(api_base()).netloc:
                headers["Authorization"] = "Bearer " + token  # only ever sent to the Apify API host
            name = os.path.basename(urllib.parse.urlsplit(link).path) or f"file-{i}"
            target = os.path.join(folder, f"{i:04d}-{name}")
            try:
                with urllib.request.urlopen(urllib.request.Request(link, headers=headers), timeout=120) as resp, \
                        open(target, "wb") as f:
                    f.write(resp.read())
                saved += 1
            except (urllib.error.URLError, OSError) as e:
                print(f"  could not download row {i} {field}: {e}")
    print(f"Saved {saved} files to {folder}/")


def add_local_files(run_input, paths):
    """Read local image files and pass them to the Actor as base64 data URIs."""
    import base64
    import mimetypes
    items = list(run_input.get(LOCAL_FILES_KEY) or [])
    for p in paths:
        mime = mimetypes.guess_type(p)[0] or "application/octet-stream"
        with open(p, "rb") as f:
            items.append(f"data:{mime};base64," + base64.b64encode(f.read()).decode("ascii"))
    run_input[LOCAL_FILES_KEY] = items


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    add_param_flags(parser)
    if FILE_KEY:
        parser.add_argument("--file", help=f"Text file with one {FILE_KEY} entry per line (# for comments).")
    if LOCAL_FILES_KEY:
        parser.add_argument("--local-files", help="Comma-separated local image files, sent as base64.")
    if DOWNLOAD_FIELDS:
        parser.add_argument("--download", metavar="FOLDER", help="Also save the produced files into this folder.")
    parser.add_argument("--input-json", help="Full Actor input as a JSON string; flags override its keys.")
    parser.add_argument("--input-file", help="Full Actor input as a JSON file; flags override its keys.")
    parser.add_argument("--out", default=SKILL_NAME, help="Output path prefix for .json and .csv (default: %(default)s).")
    parser.add_argument("--max-charge", type=float, help="Hard spending cap for the run in USD.")
    parser.add_argument("--estimate", action="store_true", help="Print the cost ceiling from live prices and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print the Actor input and exit. No token needed.")
    parser.add_argument("--yes", action="store_true", help="Allow a spending cap above $1 (after the user agreed).")
    args = parser.parse_args()

    run_input = build_input(args)
    if LOCAL_FILES_KEY and args.local_files:
        add_local_files(run_input, split_list(args.local_files))
    if REQUIRED and not any(run_input.get(k) for k in REQUIRED):
        parser.error("give at least one of: " + ", ".join("--" + kebab(k) for k in REQUIRED))
    if args.dry_run:
        print(json.dumps(run_input, ensure_ascii=False, indent=2)[:4000])
        return
    total = estimate(run_input)
    if args.estimate:
        return
    cap = resolve_cap(args.max_charge, total)
    confirm_spend(cap, args.yes)
    token = get_token()
    run = run_actor(run_input, cap, token)
    rows = dataset_items(run.get("defaultDatasetId"), token)
    write_outputs(rows, args.out, OUTPUT_COLUMNS)
    if DOWNLOAD_FIELDS and getattr(args, "download", None):
        download_files(rows, args.download, token)


if __name__ == "__main__":
    main()
