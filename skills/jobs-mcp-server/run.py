#!/usr/bin/env python3
"""Run Jobs MCP Server (conserving_celerytop/jobs-mcp-server) on Apify from an agent skill.

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

SKILL_NAME = "jobs-mcp-server"
ACTOR_ID = "conserving_celerytop/jobs-mcp-server"
DESCRIPTION = "Run Jobs MCP Server (Jobs MCP server) on Apify and save the results as JSON and CSV."
PARAMS = [
]
DEFAULTS = {}
ESTIMATE = {"events": ["tool-call"], "unit": "tool calls", "terms": []}
FILE_KEY = None
REQUIRED = []
LOCAL_FILES_KEY = None
DOWNLOAD_FIELDS = []
OUTPUT_COLUMNS = ["companyName", "title", "department", "location", "workplaceType", "seniority", "salaryAnnualMin", "salaryAnnualMax", "salaryCurrency", "postedAt", "url", "applyUrl", "companyStatus", "rowType"]
MCP_URL = "https://conserving-celerytop--jobs-mcp-server.apify.actor/mcp"

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


MCP_ACCEPT = "application/json, text/event-stream"
TOOL_ACTORS = {
    "get_company_jobs": ("conserving_celerytop/live-career-page-jobs-api", "company-lookup"),
    "search_tech_jobs": ("conserving_celerytop/tech-jobs-search", "matching-job"),
}


def mcp_post(message, token, session=None):
    """POST one JSON-RPC message to the MCP endpoint (Streamable HTTP) and return (reply, session id)."""
    headers = {"Accept": MCP_ACCEPT, "Content-Type": "application/json",
               "Authorization": "Bearer " + token, "User-Agent": "apify-agent-skills/" + SKILL_NAME}
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(MCP_URL, data=json.dumps(message).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            session = r.headers.get("Mcp-Session-Id") or session
            raw = r.read().decode("utf-8", "replace")
            ctype = r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} from the MCP server: {e.read().decode('utf-8', 'replace')[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach the MCP server: {e.reason}")
    if not raw.strip():
        return None, session
    if "text/event-stream" in ctype:
        reply = None
        for line in raw.splitlines():
            if line.startswith("data:"):
                try:
                    msg = json.loads(line[5:].strip())
                except ValueError:
                    continue
                if msg.get("id") == message.get("id"):
                    reply = msg
        return reply, session
    return json.loads(raw), session


def mcp_session(token):
    init = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": SKILL_NAME, "version": "1.0.0"}}}
    reply, session = mcp_post(init, token)
    if not reply or "error" in reply:
        sys.exit(f"MCP initialize failed: {reply}")
    mcp_post({"jsonrpc": "2.0", "method": "notifications/initialized"}, token, session)
    return session


def find_rows(obj):
    """The first list of objects in a tool result (the jobs), searched breadth first."""
    queue = [obj]
    while queue:
        cur = queue.pop(0)
        if isinstance(cur, list) and cur and all(isinstance(x, dict) for x in cur):
            return cur
        if isinstance(cur, dict):
            queue.extend(v for v in cur.values() if isinstance(v, (dict, list)))
    return []


def tool_estimate(tool, args):
    tool_price = (live_prices(ACTOR_ID) or {}).get("tool-call")
    actor_id, event = TOOL_ACTORS[tool]
    unit = (live_prices(actor_id) or {}).get(event)
    if tool_price is None or unit is None:
        print(f"Could not read live prices. Check the Pricing tab: {STORE_URL}")
        return None
    if args.get("cursor"):
        count = 0
    elif tool == "get_company_jobs":
        count = len(args.get("companies") or [])
    else:
        count = int(args.get("maxResults") or 50)
    total = tool_price + count * unit
    print(f"Estimated charge on the free Apify plan: ${money(tool_price)} per tool call + {count} x {event} "
          f"(${money(unit)}) = about ${total_str(total)}, plus a little platform usage.")
    return total


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--list-tools", action="store_true", help="List the server's tools and their inputs, then exit.")
    parser.add_argument("--tool", choices=sorted(TOOL_ACTORS), help="Tool to call.")
    parser.add_argument("--companies", help="get_company_jobs: comma-separated job board links, websites or names (1 to 25).")
    parser.add_argument("--keywords", help="search_tech_jobs: comma-separated title keywords.")
    parser.add_argument("--title-includes", help="get_company_jobs: comma-separated title words.")
    parser.add_argument("--location", help="Country, US state or city.")
    parser.add_argument("--remote-only", action="store_true", help="Only remote jobs.")
    parser.add_argument("--posted-since", help="search_tech_jobs: such as '7 days'.")
    parser.add_argument("--max-results", type=int, help="search_tech_jobs: matching jobs to return (default 50, at most 500).")
    parser.add_argument("--cursor", help="Cursor from a previous result, for the next page or a search still running.")
    parser.add_argument("--args-json", help="Full tool arguments as a JSON string; flags override its keys.")
    parser.add_argument("--out", default=SKILL_NAME, help="Output path prefix (default: %(default)s).")
    parser.add_argument("--estimate", action="store_true", help="Print the cost estimate and exit.")
    parser.add_argument("--yes", action="store_true", help="Allow a call estimated above $1 (after the user agreed).")
    args = parser.parse_args()

    if args.list_tools:
        token = get_token()
        session = mcp_session(token)
        reply, _ = mcp_post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, token, session)
        print(json.dumps((reply or {}).get("result", reply), ensure_ascii=False, indent=2))
        return
    if not args.tool:
        parser.error("give --tool or --list-tools")
    tool_args = json.loads(args.args_json) if args.args_json else {}
    for key, value in (("companies", split_list(args.companies)), ("keywords", split_list(args.keywords)),
                       ("titleIncludes", split_list(args.title_includes)), ("location", args.location),
                       ("postedSince", args.posted_since), ("maxResults", args.max_results), ("cursor", args.cursor)):
        if value:
            tool_args[key] = value
    if args.remote_only:
        tool_args["remoteOnly"] = True
    total = tool_estimate(args.tool, tool_args)
    if args.estimate:
        return
    if (total is None or total > 1.0) and not args.yes:
        sys.exit("The cost is above $1 or unknown. Confirm with the user, then rerun with --yes.")
    token = get_token()
    session = mcp_session(token)
    call = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": args.tool, "arguments": tool_args}}
    reply, _ = mcp_post(call, token, session)
    if not reply or "error" in reply:
        sys.exit(f"Tool call failed: {reply}")
    result = reply.get("result") or {}
    payload = result.get("structuredContent")
    if payload is None:
        texts = [c.get("text", "") for c in result.get("content") or [] if c.get("type") == "text"]
        try:
            payload = json.loads(texts[0]) if len(texts) == 1 else {"text": "\n".join(texts)}
        except ValueError:
            payload = {"text": "\n".join(texts)}
    with open(args.out + ".json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    rows = find_rows(payload)
    if rows:
        write_outputs(rows, args.out, OUTPUT_COLUMNS)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2)[:3000])
    cursor = payload.get("nextCursor") if isinstance(payload, dict) else None
    if cursor:
        print(f"More results or a search still running: rerun with --cursor '{cursor}'")
    if result.get("isError"):
        print("The tool reported an error; see the message above.")


if __name__ == "__main__":
    main()
