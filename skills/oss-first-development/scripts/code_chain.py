#!/usr/bin/env python3
"""code_chain.py - HELPER (not for discovery): concept co-occurrence mining over public code search (stdlib only).
Warning: raw coverage ranking favours giant repos; use output as leads for the Judge step only.

Idea: a human chains by hand (keyword -> project -> new keywords in it -> repeat). This automates it:
  1. each CONCEPT is one or more Sourcegraph queries (regex/literal, lang filters)
  2. repos are ranked by how many different concepts they cover (co-occurrence = relevance)
  3. identifiers are mined from the matched lines of the best repos -> suggested next-round keywords
  4. optional: stars / license / pushed date via `gh api` (uses the user's own gh login)

Usage:
  python code_chain.py concepts.json [--out report.json] [--per-concept 400] [--top 25] [--meta]
concepts.json: {"concepts": {"name": ["query fragment", ...]}, "common": "lang:Kotlin OR lang:Java fork:no"}
  every query fragment is sent as:  context:global <common> <fragment> count:<N>
Backends: Sourcegraph stream API (no login). grep.app is behind a bot checkpoint and is NOT used.
"""
import collections, json, re, subprocess, sys, time, urllib.parse, urllib.request

SG = "https://sourcegraph.com/.api/search/stream?v=V3&display=%d&q=%s"
STOP = set("""the and for return val var int float void new null true false this that with from import package class
public private static final string override fun let if else when while try catch throw object data size length index
value values result list map set get put add remove size name type id key res ctx context view views""".split())
IDENT = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]{3,40}\b")


def sg_search(query, count, display=500, retries=2):
    url = SG % (display, urllib.parse.quote(f"context:global {query} count:{count}"))
    last = None
    for _ in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"Accept": "text/event-stream", "User-Agent": "code-chain/0.1"})
            out, ev = [], None
            with urllib.request.urlopen(req, timeout=60) as r:
                for raw in r:
                    line = raw.decode("utf-8", "replace").rstrip("\n")
                    if line.startswith("event:"):
                        ev = line[6:].strip()
                    elif line.startswith("data:") and ev == "matches":
                        out.extend(json.loads(line[5:]))
            return out
        except Exception as e:  # network hiccup, rate limit
            last = e
            time.sleep(2)
    print(f"  ! query failed: {query[:60]} ({last})", file=sys.stderr)
    return []


def repo_of(m):
    return m.get("repository", "")


def mine(matches, repos):
    """identifier frequency from matched lines, only for the given repos"""
    c = collections.Counter()
    for m in matches:
        if repo_of(m) not in repos:
            continue
        for lm in m.get("lineMatches", []) or []:
            for tok in set(IDENT.findall(lm.get("line", ""))):
                if tok.lower() not in STOP:
                    c[tok] += 1
    return c


def gh_meta(repo):
    name = repo.replace("github.com/", "")
    if not repo.startswith("github.com/"):
        return {}
    try:
        p = subprocess.run(["gh", "api", f"repos/{name}", "--jq",
                            "{stars:.stargazers_count,license:(.license.spdx_id // \"none\"),pushed:.pushed_at,"
                            "archived:.archived,desc:.description}"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        return json.loads(p.stdout) if p.returncode == 0 else {}
    except Exception:
        return {}


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    cfg = json.load(open(argv[1], encoding="utf-8"))
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d
    per, top = int(opt("--per-concept", 400)), int(opt("--top", 25))
    common = cfg.get("common", "")
    cover = collections.defaultdict(set)       # repo -> concepts
    files = collections.defaultdict(lambda: collections.defaultdict(set))  # repo -> concept -> paths
    allm = []
    for concept, frags in cfg["concepts"].items():
        n = 0
        for f in frags:
            res = sg_search(f"{common} {f}", per)
            allm.extend(res)
            for m in res:
                r = repo_of(m)
                if r:
                    cover[r].add(concept); files[r][concept].add(m.get("path", "")); n += 1
        print(f"[{concept}] {n} file matches", file=sys.stderr)
    ranked = sorted(cover, key=lambda r: (-len(cover[r]), -sum(len(v) for v in files[r].values())))[:top]
    ids = mine(allm, set(ranked))
    report = {"concepts": list(cfg["concepts"]), "repos": [], "next_keywords": [k for k, _ in ids.most_common(40)]}
    for r in ranked:
        row = {"repo": r, "covers": sorted(cover[r]), "score": len(cover[r]),
               "files": {c: sorted(p)[:3] for c, p in files[r].items()}}
        if "--meta" in argv:
            row.update(gh_meta(r))
        report["repos"].append(row)
    json.dump(report, open(opt("--out", "code_chain_report.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for row in report["repos"]:
        extra = f"  *{row.get('stars','?')} {row.get('license','?')}" if "--meta" in argv else ""
        print(f"{row['score']}/{len(cfg['concepts'])}  {row['repo']}{extra}  [{', '.join(row['covers'])}]")
    print("\nnext-round keywords:", ", ".join(report["next_keywords"][:30]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
