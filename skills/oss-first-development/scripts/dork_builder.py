#!/usr/bin/env python3
"""dork_builder.py - turn a concept map into ready-to-run web dork queries (stdlib only).

Usage: python dork_builder.py concepts.json [--max-per-pillar 6]
concepts.json:
{
 "topic": "audio-reactive 3D dance app",
 "platform": "android",                 # words that anchor every query
 "languages": ["Kotlin", "Java"],       # optional
 "pillars": {
   "audio_to_gl": {"words": ["audio visualizer", "music reactive shader"],
                   "symbols": ["Visualizer getFft", "AudioRecord", "glUniform1f"],
                   "formats": [],
                   "noise": ["tutorial"]},
   "dance_motion": {"words": ["skeletal animation viewer"], "symbols": [], "formats": ["PMX VMD", "glTF skin"]}
 },
 "regional": ["ja", "zh"],               # ONLY if the ecosystem is regional (MMD, Shadowsocks...)
 "registries": ["klibs.io", "crates.io"]  # optional
}
Prints one query per line, grouped by pillar and family. Copy them into your web search tool in parallel.
Why: specific, quoted, operator-rich queries are what gave ~95% precision in measured runs.
"""
import json
import sys

REGION = {
    "zh": ("{t} 开源 {p}", ["juejin", "csdn", "zhihu", "gitee"]),
    "ja": ("{t} 実装 {p}", ["zenn", "qiita"]),
    "ko": ("{t} 구현 {p}", ["velog", "geeknews"]),
    "ru": ("{t} {p} исходники", ["habr"]),
}


def q(*parts):
    return " ".join(x for x in parts if x)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cfg = json.load(open(argv[1], encoding="utf-8"))
    cap = int(argv[argv.index("--max-per-pillar") + 1]) if "--max-per-pillar" in argv else 6
    plat = cfg.get("platform", "")
    langs = cfg.get("languages", [])
    lang = " OR ".join(langs) if langs else ""
    lang_q = f"({lang})" if len(langs) > 1 else lang
    out = []
    for name, p in cfg["pillars"].items():
        noise = " ".join(f"-{n}" for n in p.get("noise", []))
        rows = []
        for w in p.get("words", []):
            rows.append(("product", q("site:github.com", f'"{w}"', plat, lang_q, noise)))
            rows.append(("awesome", q("awesome", w, plat, "open source")))
        for s in p.get("symbols", []):
            rows.append(("symbol", q("site:github.com", f'"{s}"', plat, lang_q, noise)))
        for f in p.get("formats", []):
            rows.append(("format", q(f, plat, "viewer OR loader OR parser OR library", "site:github.com")))
            rows.append(("asset", q(f, '"free" OR "CC0" OR "MIT"', "sample OR dataset OR assets")))
        for w in p.get("words", [])[:2]:
            rows.append(("limits", q(f'"{w}"', plat, '"limitations" OR "does not support" OR "not supported"')))
            rows.append(("compare", q(f'"{w}"', plat, "vs OR alternative OR comparison")))
        for reg in cfg.get("regional", []):
            if reg in REGION and p.get("words"):
                tmpl, sites = REGION[reg]
                rows.append((f"regional-{reg}", q(tmpl.format(t=p["words"][0], p=plat), " OR ".join(sites))))
        for reg in cfg.get("registries", []):
            if p.get("words"):
                rows.append(("registry", q(reg, p["words"][0], plat)))
        out.append((name, rows[:cap if cap > 0 else None]))
    print(f"# topic: {cfg.get('topic', '')}\n# run in parallel, then CHAIN: take unique identifiers from the best 3-5 hits as the next queries\n")
    for name, rows in out:
        print(f"## {name}")
        for fam, line in rows:
            print(f"[{fam}] {line}")
        print()
    print("## chain (fill after round 1)\n[chain] site:github.com \"<identifier from a good hit>\" <platform>")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
