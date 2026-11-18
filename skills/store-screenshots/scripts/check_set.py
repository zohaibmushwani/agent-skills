#!/usr/bin/env python3
"""check_set.py - store checks for a rendered screenshot set (Python 3 + Pillow).

Usage: python check_set.py out_dir [--store play|ios] [--set set.json]
Checks: frame count (Play 2-8, iOS 1-10), every PNG same size, no alpha channel, side 320-3840 and aspect <= 2:1 (Play),
exact iOS 6.9" sizes (ios), headline length <= 26 chars per frame and <= 4 words in frame 1 (with --set),
proof items flagged for the user to confirm are real. Exit 1 on errors.
"""
import json
import sys
from pathlib import Path

from PIL import Image

IOS = {(1320, 2868), (1290, 2796), (1260, 2736), (1284, 2778), (1242, 2688)}


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    store = argv[argv.index("--store") + 1] if "--store" in argv else "play"
    d = Path(args[0])
    pngs = sorted(p for p in d.glob("[0-9][0-9].png"))
    err, warn = [], []
    lo, hi = (2, 8) if store == "play" else (1, 10)
    if not lo <= len(pngs) <= hi:
        err.append(f"{len(pngs)} frames; {store} needs {lo}-{hi}")
    sizes = set()
    for p in pngs:
        im = Image.open(p)
        sizes.add(im.size)
        if im.mode in ("RGBA", "LA") or "transparency" in im.info:
            err.append(f"{p.name}: has alpha (stores require none) - flatten")
        w, h = im.size
        if store == "play" and (min(w, h) < 320 or max(w, h) > 3840 or max(w, h) > 2 * min(w, h)):
            err.append(f"{p.name}: {w}x{h} outside Play limits")
        if store == "ios" and (w, h) not in IOS:
            err.append(f"{p.name}: {w}x{h} is not an accepted iPhone 6.9/6.5 size")
    if len(sizes) > 1:
        err.append(f"mixed sizes {sizes}")
    if "--set" in argv:
        s = json.loads(Path(argv[argv.index("--set") + 1]).read_text(encoding="utf-8"))
        for i, f in enumerate(s["frames"], 1):
            h = f.get("head", "")
            if len(h) > 26:
                warn.append(f"frame {i}: headline {len(h)} chars (aim <= 26)")
            if i == 1 and len(h.split()) > 4:
                warn.append("frame 1: headline over 4 words")
            for p in f.get("proof", []):
                warn.append(f"frame {i}: confirm proof '{p}' is real before publishing")
    for w in warn:
        print("WARN " + w)
    for e in err:
        print("ERR  " + e)
    print(f"{len(pngs)} frames checked ({store}); {len(err)} errors")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
