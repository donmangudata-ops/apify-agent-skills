#!/usr/bin/env python3
"""Check every skill folder here against the Agent Skills rules. Standard library only.

  python validate_skills.py          check all skills (folders starting with _ are skipped)

Works from the repo root (checks skills/) or from inside the skills folder. Each skill folder is
flat: SKILL.md, run.py and reference.md, with no subfolders.

Checks: frontmatter keys, name (lowercase letters, digits and single hyphens, 64 characters at most,
same as the folder, no reserved words), description (1 to 1024 characters, says "Use when", no XML
tags), SKILL.md under 500 lines, linked files exist, flags used in SKILL.md exist in the script,
run.py compiles, reference.md anchors exist, the folder is flat, one store link in a last "## Reference" section, and no em dashes, e-mail
addresses, API tokens or real names in any file.
"""
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / "skills" if (HERE / "skills").is_dir() else HERE
ALLOWED_KEYS = {"name", "description", "license", "metadata", "compatibility", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PROFILE = "https://apify.com/conserving_celerytop"
TOKEN_RES = [re.compile("apify" + r"_api_[A-Za-z0-9]{10,}"), re.compile(r"[?&]token=[A-Za-z0-9]")]
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
FORBIDDEN_WORDS = [w[::-1] for w in ("norod", "namrug")]  # stored reversed so this file passes its own check
TEXT = {".md", ".py", ".json", ".txt"}


def frontmatter(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    data, cur = {}, None
    for line in m.group(1).splitlines():
        if line.startswith("  ") and cur:
            k, _, v = line.strip().partition(":")
            data[cur][k.strip()] = v.strip().strip('"')
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if not v:
            data[k], cur = {}, k
        else:
            if len(v) >= 2 and v[0] == v[-1] == '"':
                v = v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            data[k], cur = v, None
    return data


def check(folder):
    errs = []
    md = folder / "SKILL.md"
    if not md.exists():
        return [f"{folder.name}: no SKILL.md"]
    text = md.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        return [f"{folder.name}: SKILL.md must start with YAML frontmatter"]
    if set(fm) - ALLOWED_KEYS:
        errs.append(f"unknown frontmatter keys {sorted(set(fm) - ALLOWED_KEYS)}")
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not NAME_RE.match(name) or len(name) > 64:
        errs.append(f"name '{name}' must be lowercase letters, digits and single hyphens, 64 characters at most")
    if name != folder.name:
        errs.append(f"name '{name}' differs from folder '{folder.name}'")
    if any(w in name for w in ("anthropic", "claude")):
        errs.append("name uses a reserved word")
    if not 1 <= len(desc) <= 1024:
        errs.append(f"description is {len(desc)} characters (1 to 1024)")
    if "Use when" not in desc:
        errs.append("description must say when to use the skill ('Use when ...')")
    if re.search(r"<[a-zA-Z/][^>]*>", desc):
        errs.append("description contains an XML tag")
    if len(text.splitlines()) >= 500:
        errs.append("SKILL.md is 500 lines or more")
    if text.count(PROFILE) != 1:
        errs.append(f"the store link must appear once (found {text.count(PROFILE)})")
    h2 = re.findall(r"(?m)^## (.+)$", text)
    if not h2 or h2[-1] != "Reference":
        errs.append("the last section must be '## Reference'")
    for link in re.findall(r"\]\(([^)#]+)\)", text):
        if not link.startswith("http") and not (folder / link).exists():
            errs.append(f"linked file {link} does not exist")
    sub = sorted(p.name for p in folder.iterdir() if p.is_dir() and p.name != "__pycache__")
    if sub:
        errs.append(f"not flat: subfolders {sub}")
    if re.search(r"scripts/|references/", text):
        errs.append("SKILL.md still mentions scripts/ or references/")
    ref = folder / "reference.md"
    if ref.exists():
        heads = {re.sub(r"[^a-z0-9 -]", "", h.strip().lower()).replace(" ", "-")
                 for h in re.findall(r"(?m)^#+ (.+)$", ref.read_text(encoding="utf-8"))}
        for anchor in sorted(set(re.findall(r"\]\(reference\.md#([^)]+)\)", text))):
            if anchor not in heads:
                errs.append(f"reference.md has no section #{anchor}")
    for script in sorted(set(re.findall(r"(?<![\w/.-])([a-z0-9_]+\.py)\b", text))):
        path = folder / script
        if not path.exists():
            errs.append(f"{script} does not exist")
            continue
        try:
            py_compile.compile(str(path), doraise=True, cfile=str(Path(tempfile.gettempdir()) / "vs_check.pyc"))
        except py_compile.PyCompileError as e:
            errs.append(f"{script} does not compile: {e.msg[:200]}")
            continue
        out = subprocess.run([sys.executable, str(path), "--help"], capture_output=True, text=True, timeout=60)
        known = set(re.findall(r"--[a-z][a-z0-9-]*", out.stdout))
        used = set(re.findall(r"(?<![\w-])--[a-z][a-z0-9-]*", text)) - {"--transport", "--header"}
        if out.returncode != 0:
            errs.append(f"{script} --help failed")
        elif used - known:
            errs.append(f"flags not accepted by {script}: {sorted(used - known)}")
    for f in folder.rglob("*"):
        if f.suffix not in TEXT or not f.is_file() or "__pycache__" in f.parts:
            continue
        body = f.read_text(encoding="utf-8")
        rel = f.relative_to(folder)
        if "\u2014" in body:
            errs.append(f"{rel}: contains an em dash")
        if any(r.search(body) for r in TOKEN_RES):
            errs.append(f"{rel}: contains something that looks like a token")
        if EMAIL_RE.search(body):
            errs.append(f"{rel}: contains an e-mail address")
        low = body.lower()
        if any(w in low for w in FORBIDDEN_WORDS):
            errs.append(f"{rel}: contains a real name; use the pen name only")
    return [f"{folder.name}: {e}" for e in errs]


def main():
    folders = sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(("_", ".")))
    errors = []
    for folder in folders:
        errors += check(folder)
    for e in errors:
        print("FAIL", e)
    print(f"{len(folders)} skills checked, {len(errors)} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
