#!/usr/bin/env python3
"""repo_probe.py - verify candidate repos before judging them (stdlib + `gh` CLI).

Usage: python repo_probe.py repos.txt [--json out.json]
  repos.txt: one repo per line: owner/name or github.com/owner/name or a github URL (# comments ok)
Reports per repo: exists, stars, license (SPDX) + class, closed-app verdict, last push, archived,
language bytes, number of files in the tree, and FLAGS:
  NO_SOURCE   - almost no code (README-only / binary-release repo)  -> feature spec, not a donor
  ARCHIVED, STALE(>2y), NO_LICENSE, COPYLEFT, NONCOMMERCIAL, UNKNOWN_LICENSE, NOT_FOUND
  README_SAYS_<X> - API found no license but the README mentions one (e.g. GPL): treat the README as the stricter signal
Requires `gh auth login` (uses the user's own session; no tokens are read or printed).
"""
import datetime
import json
import re
import subprocess
import sys

PERMISSIVE = {"MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Zlib", "Unlicense", "CC0-1.0", "Apache-2.0", "0BSD", "BSL-1.0"}
WEAK = {"MPL-2.0", "LGPL-2.1", "LGPL-3.0", "LGPL-2.1-only", "LGPL-3.0-only", "EPL-2.0"}
COPYLEFT = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "GPL-2.0-only", "GPL-3.0-only", "AGPL-3.0-only", "GPL-3.0-or-later", "GPL-2.0-or-later", "AGPL-3.0-or-later"}


def gh(path, jq=None):
    cmd = ["gh", "api", path] + (["--jq", jq] if jq else [])
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=40)
    return p.returncode, p.stdout


def norm(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    m = re.search(r"github\.com[/:]([^/\s]+)/([^/\s#?]+)", line)
    if m:
        return f"{m.group(1)}/{m.group(2).removesuffix('.git')}"
    return line if re.fullmatch(r"[\w.-]+/[\w.-]+", line) else None


def classify(spdx):
    if not spdx or spdx == "none":
        return "none", "no (ideas only)"
    if spdx in PERMISSIVE:
        return "permissive", "yes"
    if spdx in WEAK:
        return "weak-copyleft", "conditional"
    if spdx in COPYLEFT:
        return "copyleft", "no (study only)"
    if "NC" in spdx:
        return "non-commercial", "no"
    return "unknown", "read the license text"


HINTS = [("AGPL", r"\bAGPL"), ("GPL", r"\bGPL(?:-?v?[23])?\b|GNU General Public"), ("LGPL", r"\bLGPL"),
         ("NONCOMMERCIAL", r"non-?commercial|CC[ -]BY-NC"), ("Apache", r"\bApache\b"),
         ("MIT", r"\bMIT\b"), ("BSD", r"\bBSD\b")]


def readme_hint(repo):
    """GitHub's license detector misses some repos; the README often states the real license."""
    import base64
    rc, out = gh(f"repos/{repo}/readme", ".content")
    if rc != 0 or not out.strip():
        return None
    try:
        text = base64.b64decode(out.strip()).decode("utf-8", "replace")
    except Exception:
        return None
    found = [name for name, rx in HINTS if re.search(rx, text, re.I)]
    # keep the strictest-looking mention first
    order = ["AGPL", "GPL", "LGPL", "NONCOMMERCIAL", "Apache", "MIT", "BSD"]
    found.sort(key=order.index)
    return found[:2] or None


def probe(repo):
    row = {"repo": repo, "flags": []}
    rc, out = gh(f"repos/{repo}", '{stars:.stargazers_count,spdx:(.license.spdx_id // "none"),pushed:.pushed_at,'
                 'archived:.archived,desc:.description,topics:.topics,default:.default_branch,size:.size,fork:.fork}')
    if rc != 0:
        row["flags"].append("NOT_FOUND")
        return row
    meta = json.loads(out)
    row.update(stars=meta["stars"], license=meta["spdx"], desc=(meta["desc"] or "")[:80], topics=meta["topics"], fork=meta["fork"])
    cls, verdict = classify(meta["spdx"])
    row.update(license_class=cls, closed_app=verdict, pushed=meta["pushed"][:10])
    rc, out = gh(f"repos/{repo}/languages")
    langs = json.loads(out) if rc == 0 and out.strip() else {}
    row["code_bytes"] = sum(langs.values())
    rc, out = gh(f"repos/{repo}/git/trees/{meta['default']}?recursive=1", ".tree | length")
    row["files"] = int(out.strip()) if rc == 0 and out.strip().isdigit() else None
    if row["code_bytes"] < 5000 and (row["files"] is None or row["files"] < 15):
        row["flags"].append("NO_SOURCE")
    if meta["archived"]:
        row["flags"].append("ARCHIVED")
    age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(meta["pushed"].replace("Z", "+00:00"))).days
    if age > 730:
        row["flags"].append("STALE")
    row["flags"] += {"none": ["NO_LICENSE"], "copyleft": ["COPYLEFT"], "non-commercial": ["NONCOMMERCIAL"], "unknown": ["UNKNOWN_LICENSE"]}.get(cls, [])
    if cls in ("none", "unknown"):
        hint = readme_hint(repo)
        if hint:
            row["readme_license_hint"] = hint
            row["flags"].append("README_SAYS_" + "/".join(hint).upper())
    return row


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    repos = [r for r in (norm(l) for l in open(argv[1], encoding="utf-8")) if r]
    rows = [probe(r) for r in repos]
    if "--json" in argv:
        json.dump(rows, open(argv[argv.index("--json") + 1], "w", encoding="utf-8"), indent=1)
    print("| repo | stars | license | closed-app? | pushed | code KB | files | flags |\n|---|---|---|---|---|---|---|---|")
    for r in rows:
        if "NOT_FOUND" in r["flags"]:
            print(f"| {r['repo']} | - | - | - | - | - | - | NOT_FOUND |")
            continue
        print(f"| {r['repo']} | {r['stars']} | {r['license']} | {r['closed_app']} | {r['pushed']} | {r['code_bytes'] // 1000} | {r['files']} | {' '.join(r['flags']) or '-'} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
