#!/usr/bin/env python3
"""Validate Play/App Store asset files against exact sizes and alpha rules (stdlib only; PNG + JPEG).

Usage: validate_assets.py <store-dir> [--slots slots.json]
Default slots map a path-glob to rules, see DEFAULT_SLOTS. Paths are relative to <store-dir>.
Rules: w,h exact | min_side,max_side | max_ratio | alpha True/False/None | max_kb
"""
import fnmatch
import json
import struct
import sys
from pathlib import Path

DEFAULT_SLOTS = {
    "icon/play-512.png": {"w": 512, "h": 512, "alpha": True, "max_kb": 1024},
    "icon/appstore-1024.png": {"w": 1024, "h": 1024, "alpha": False},
    "feature-graphic/*.png": {"w": 1024, "h": 500, "alpha": False},
    "feature-graphic/*.jpg": {"w": 1024, "h": 500, "alpha": False},
    "screenshots/play/phone/*/*.png": {"min_side": 320, "max_side": 3840, "max_ratio": 2.0, "alpha": False},
    "screenshots/appstore/iphone-6.9/*/*.png": {"w_in": [1320, 1290, 1260], "alpha": False},
}


def png_info(b):
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", b[16:24])
    ctype = b[25]
    alpha = ctype in (4, 6)
    if not alpha:  # palette PNG may have tRNS
        alpha = b"tRNS" in b[:4096]
    return w, h, alpha


def jpg_info(b):
    if b[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(b):
        if b[i] != 0xFF:
            i += 1
            continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", b[i + 5:i + 9])
            return w, h, False
        i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return None


def info(path):
    b = path.read_bytes()
    return png_info(b) or jpg_info(b)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1])
    slots = DEFAULT_SLOTS
    if "--slots" in argv:
        slots = json.loads(Path(argv[argv.index("--slots") + 1]).read_text(encoding="utf-8"))
    bad = checked = 0
    for f in sorted(p for p in root.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg")):
        rel = f.relative_to(root).as_posix()
        for pat, r in slots.items():
            if not fnmatch.fnmatch(rel, pat):
                continue
            checked += 1
            inf = info(f)
            if inf is None:
                print(f"FAIL {rel}: unreadable image"); bad += 1; continue
            w, h, a = inf
            errs = []
            if "w" in r and (w, h) != (r["w"], r["h"]):
                errs.append(f"size {w}x{h} != {r['w']}x{r['h']}")
            if "w_in" in r and w not in r["w_in"]:
                errs.append(f"width {w} not in {r['w_in']}")
            if "min_side" in r and min(w, h) < r["min_side"]:
                errs.append(f"short side {min(w, h)} < {r['min_side']}")
            if "max_side" in r and max(w, h) > r["max_side"]:
                errs.append(f"long side {max(w, h)} > {r['max_side']}")
            if "max_ratio" in r and max(w, h) / min(w, h) > r["max_ratio"]:
                errs.append("aspect ratio > 2:1")
            if r.get("alpha") is False and a:
                errs.append("has alpha (forbidden)")
            if r.get("alpha") is True and not a:
                errs.append("needs alpha")
            if "max_kb" in r and f.stat().st_size > r["max_kb"] * 1024:
                errs.append(f"{f.stat().st_size // 1024} KB > {r['max_kb']} KB")
            print(("FAIL " if errs else "PASS ") + rel + (": " + "; ".join(errs) if errs else ""))
            bad += bool(errs)
    manifest = root / "manifest.json"
    if not manifest.exists():
        print("WARN store/manifest.json missing (mark each asset status: concept|final, source: generated|captured)")
    print(f"checked {checked}, failed {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
