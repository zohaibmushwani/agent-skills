#!/usr/bin/env python3
"""topic_sweep.py - long-tail sweep of GitHub topics (what a human does by paging through a tag).

Why: ranking by stars hides small-but-useful repos that sit on page 2-3 of a topic. This enumerates
MANY repos per topic (several pages, sorted by recent activity), merges them across topics, and ranks by
RELEVANCE to your words, not by stars. A repo that shows up under several relevant tags is a strong signal.

Usage:
  python topic_sweep.py sweep.json [--pages 3] [--out sweep_out.json] [--md sweep.md]
sweep.json:
 {"topics": ["opengl-es", "audio-visualizer", "mikumikudance"],
  "words":  ["audio", "fft", "visualizer", "shader", "beat", "skeletal", "vmd", "pmx", "gltf"],
  "languages": ["Kotlin", "Java", "C++", "GLSL", "Rust"],     # optional boost
  "extra_queries": ["android opengl es visualizer"],          # optional free-text queries (also paged)
  "min_size_kb": 30, "gem_max_stars": 60}
Output: markdown with (1) top by relevance (any stars), (2) HIDDEN GEMS = few stars but relevant, recent, has source.
The user can ALSO feed their own tag list or repo URLs: put tags in "topics", paste repos into repos.txt for repo_probe.py.
Needs `gh auth login` (search API: ~30 requests/min; the script sleeps between calls). Search results already contain
stars/size/license/pushed, so no extra calls per repo.
"""
import collections
import datetime
import json
import subprocess
import sys
import time

PERMISSIVE = {"MIT", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Zlib", "Unlicense", "CC0-1.0", "Apache-2.0", "0BSD", "BSL-1.0"}
JQ = ".items[] | {n:.full_name,s:.stargazers_count,p:.pushed_at,l:(.license.spdx_id // \"none\"),d:.description,sz:.size,lang:.language,t:.topics,a:.archived,f:.fork}"


def gh_search(query, page, sort="updated"):
    cmd = ["gh", "api", "-X", "GET", "search/repositories", "-f", f"q={query}", "-f", f"sort={sort}", "-f", "order=desc",
           "-f", "per_page=100", "-f", f"page={page}", "--jq", JQ]
    for attempt in range(3):
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if p.returncode == 0:
            return [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
        if "rate limit" in (p.stderr + p.stdout).lower() or "403" in p.stderr:
            time.sleep(30)
        else:
            return []
    return []


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cfg = json.load(open(argv[1], encoding="utf-8"))
    pages = int(argv[argv.index("--pages") + 1]) if "--pages" in argv else 3
    words = [w.lower() for w in cfg.get("words", [])]
    langs = set(cfg.get("languages", []))
    min_kb, gem_stars = cfg.get("min_size_kb", 30), cfg.get("gem_max_stars", 60)
    repos = {}
    seen_in = collections.defaultdict(set)
    queries = [(f"topic:{t}", t) for t in cfg.get("topics", [])] + [(q, "q:" + q) for q in cfg.get("extra_queries", [])]
    for q, label in queries:
        got = 0
        for page in range(1, pages + 1):
            items = gh_search(q, page)
            time.sleep(2.2)
            for it in items:
                repos[it["n"]] = it
                seen_in[it["n"]].add(label)
            got += len(items)
            if len(items) < 100:
                break
        print(f"[{label}] {got} repos", file=sys.stderr)
    now = datetime.datetime.now(datetime.timezone.utc)
    rows = []
    for n, it in repos.items():
        text = " ".join([n, it.get("d") or "", " ".join(it.get("t") or [])]).lower()
        hits = sorted({w for w in words if w in text})
        age = (now - datetime.datetime.fromisoformat(it["p"].replace("Z", "+00:00"))).days
        rel = len(hits) + 1.5 * (len(seen_in[n]) - 1) + (1 if it.get("lang") in langs else 0)
        rel -= 2 if it["a"] else 0
        rel -= 1 if it["f"] else 0
        rel -= 1 if it["sz"] < min_kb else 0
        rel -= 1 if age > 1095 else 0
        rows.append({**it, "age_days": age, "hits": hits, "tags_matched": sorted(seen_in[n]), "rel": round(rel, 1)})
    rows.sort(key=lambda r: (-r["rel"], -r["s"]))
    json.dump(rows, open(argv[argv.index("--out") + 1] if "--out" in argv else "sweep_out.json", "w", encoding="utf-8"), indent=1)

    def line(r):
        d = (r.get("d") or "")[:70].replace("|", "/")
        return (f"| {r['n']} | {r['rel']} | {r['s']} | {r['l']} | {r['age_days'] // 30}mo | {r['sz'] // 1000}MB | "
                f"{len(r['tags_matched'])} | {', '.join(r['hits'][:5])} | {d} |")

    head = "| repo | relevance | stars | license | last push | size | tags | word hits | description |\n|---|---|---|---|---|---|---|---|---|"
    top = [r for r in rows if r["rel"] >= 2][:40]
    gems = [r for r in rows if r["s"] <= gem_stars and r["rel"] >= 2 and not r["a"] and r["sz"] >= min_kb and r["age_days"] <= 730][:40]
    md = [f"# Sweep: {len(repos)} unique repos from {len(queries)} tag/queries\n", "## Top by relevance (stars ignored)\n", head] + [line(r) for r in top]
    md += ["\n## Hidden gems (<= %d stars, relevant, recent, has source)\n" % gem_stars, head] + [line(r) for r in gems]
    open(argv[argv.index("--md") + 1] if "--md" in argv else "sweep.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[:2] + md[2:3 + len(top)]))
    print(f"\n{len(gems)} hidden gems; full tables in the md file", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
