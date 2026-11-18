#!/usr/bin/env python3
"""keyword_freq.py - what words competitors use (standard library only).

Usage: python keyword_freq.py competitors.json [--mine draft.json] [--top 25]
competitors.json: [{"title": "...", "summary": "...", "description": "..."}, ...]   (gplay_probe.mjs `app` output works)
Prints, over competitors: top single words and 2-word phrases in titles, and in title+summary+first 100 words of descriptions,
with how many apps use each. With --mine, lists frequent competitor terms that the draft (title/short/description) lacks.
This shows what the market says, not what ranks. Label it MEASURED text frequency, not volume.
"""
import collections
import json
import re
import sys

STOP = set("the a an and or of to in for on with is are be it this that as by at from your you our we app apps free best new all more can get use using make makes will not no one any 's".split())


def toks(text):
    return [w for w in re.findall(r"[a-z0-9][a-z0-9+#']*", text.lower()) if w not in STOP and len(w) > 1]


def grams(words):
    return words + [f"{a} {b}" for a, b in zip(words, words[1:])]


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    top = int(argv[argv.index("--top") + 1]) if "--top" in argv else 25
    mine = None
    if "--mine" in argv:
        mine = argv[argv.index("--mine") + 1]
    args = [a for a in args if a not in (str(top), mine)]
    if not args:
        print(__doc__)
        return 2
    apps = json.load(open(args[0], encoding="utf-8"))
    if isinstance(apps, dict):
        apps = [apps]
    t_title, t_body = collections.Counter(), collections.Counter()
    for a in apps:
        t_title.update(set(grams(toks(a.get("title", "")))))
        body = " ".join([a.get("title", ""), a.get("summary", a.get("short", "")), " ".join(a.get("description", "").split()[:100])])
        t_body.update(set(grams(toks(body))))
    n = len(apps)
    for name, c in (("titles", t_title), ("title + summary + first 100 words", t_body)):
        print(f"\n== {name} ({n} apps; count = apps using the term) ==")
        for term, k in c.most_common(top):
            print(f"{k:3d}/{n}  {term}")
    if mine:
        m = json.load(open(mine, encoding="utf-8"))
        mt = set(grams(toks(" ".join([m.get("title", ""), m.get("short", m.get("summary", "")), m.get("description", "")]))))
        missing = [(t, k) for t, k in t_body.most_common(top * 3) if t not in mt and k >= max(2, n // 3)]
        print(f"\n== frequent competitor terms missing from your draft ==")
        for t, k in missing[:top]:
            print(f"{k:3d}/{n}  {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
