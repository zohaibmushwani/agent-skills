#!/usr/bin/env python3
"""metadata_check.py - check a store listing draft against character limits and common mistakes (standard library only).

Usage: python metadata_check.py draft.json [--store play|apple] [--keywords "pdf reader,offline pdf"]
draft.json: {"title": "...", "short": "...", "description": "...", "keyword_field": "..."(apple only)}
Limits (re-verify before release, see references/store-limits.md): Play title 30, short 80, description 4000;
Apple title 30, subtitle(short) 30, description 4000, keyword field 100.
Checks: length per field, ALL-CAPS words, emoji/symbol stuffing, repeated words in the title, claims like "#1"/"best"/"free" in the title,
and for each target keyword whether it appears in title, short and the first 100 words of the description. Exit 1 on any error.
"""
import json
import re
import sys

LIMITS = {"play": {"title": 30, "short": 80, "description": 4000},
          "apple": {"title": 30, "short": 30, "description": 4000, "keyword_field": 100}}
CLAIM = re.compile(r"(#\s?1\b|\bno\.?\s?1\b|\bbest\b|\btop\b|\bfree\b|\bnew\b)", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B06]")


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    store = argv[argv.index("--store") + 1] if "--store" in argv else "play"
    kws = [k.strip().lower() for k in argv[argv.index("--keywords") + 1].split(",")] if "--keywords" in argv else []
    args = [a for a in args if a not in (store, ",".join(kws))]
    if not args:
        print(__doc__)
        return 2
    d = json.load(open(args[0], encoding="utf-8"))
    errs, warns = [], []
    for field, lim in LIMITS[store].items():
        v = d.get(field, "")
        if len(v) > lim:
            errs.append(f"{field}: {len(v)} chars, limit {lim}")
        elif v:
            print(f"ok   {field}: {len(v)}/{lim}")
        elif field in ("title", "short"):
            warns.append(f"{field} is empty")
    t = d.get("title", "")
    if CLAIM.search(t):
        warns.append("title contains a claim word (#1/best/top/free/new): stores flag unverifiable or promotional titles")
    if EMOJI.search(t):
        warns.append("title contains emoji/symbols: Play policy discourages them")
    tw = [w.lower() for w in re.findall(r"[A-Za-z0-9]+", t)]
    dup = {w for w in tw if tw.count(w) > 1 and len(w) > 2}
    if dup:
        warns.append("repeated word(s) in title: " + ", ".join(sorted(dup)))
    for field in ("title", "short", "description"):
        caps = [w for w in re.findall(r"\b[A-Z]{4,}\b", d.get(field, ""))]
        if len(caps) >= 3:
            warns.append(f"{field}: many ALL-CAPS words ({', '.join(caps[:4])})")
    desc_first = " ".join(d.get("description", "").lower().split()[:100])
    for k in kws:
        where = [n for n, txt in (("title", t.lower()), ("short", d.get("short", "").lower()), ("first 100 words", desc_first)) if k in txt]
        print(("ok   " if where else "WARN ") + f"keyword '{k}' in: {', '.join(where) or 'none of title/short/first 100 words'}")
        if not where:
            warns.append(f"keyword '{k}' not in title, short or the first 100 words")
        full = d.get("description", "").lower()
        if full and full.count(k) * len(k.split()) / max(len(full.split()), 1) > 0.05:
            warns.append(f"keyword '{k}' density above 5%: looks stuffed")
    for w in warns:
        print("WARN " + w)
    for e in errs:
        print("ERR  " + e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
