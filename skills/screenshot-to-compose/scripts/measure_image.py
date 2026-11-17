#!/usr/bin/env python3
"""measure_image.py - px to dp scale and colour sampling for a design screenshot (Python 3 + Pillow).

Usage:
  python measure_image.py shot.png [--frame-dp 390] [--px 96 24 ...] [--sample x,y ...] [--json]
Prints image size, aspect ratio, scale (px per dp), px->dp conversions, and the hex colour at each sample point
(averaged over a 3x3 block so anti-aliasing does not skew it). Values are OBSERVED; anything you guess is INFERRED.
"""
import argparse
import json
import sys

from PIL import Image


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--frame-dp", type=float, default=390.0, help="design frame width in dp (default 390)")
    ap.add_argument("--px", type=float, nargs="*", default=[], help="pixel spans to convert to dp")
    ap.add_argument("--sample", action="append", default=[], help="x,y pixel to sample (repeatable)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    im = Image.open(a.image).convert("RGB")
    w, h = im.size
    scale = w / a.frame_dp
    out = {"width_px": w, "height_px": h, "aspect": round(w / h, 4), "frame_dp": a.frame_dp,
           "height_dp": round(h / scale, 1), "px_per_dp": round(scale, 4),
           "px_to_dp": {str(p): round(p / scale, 2) for p in a.px}, "samples": {}}
    for s in a.sample:
        x, y = (int(v) for v in s.split(","))
        if not (0 <= x < w and 0 <= y < h):
            out["samples"][s] = "out of bounds"
            continue
        px = [im.getpixel((min(max(x + dx, 0), w - 1), min(max(y + dy, 0), h - 1))) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        r, g, b = (round(sum(c[i] for c in px) / len(px)) for i in range(3))
        out["samples"][s] = "#%02X%02X%02X" % (r, g, b)
    if a.json:
        print(json.dumps(out, indent=1))
    else:
        print(f"{w} x {h} px, aspect {out['aspect']}, frame {a.frame_dp:g} dp -> {out['px_per_dp']} px/dp, height {out['height_dp']} dp")
        for k, v in out["px_to_dp"].items():
            print(f"  {k} px = {v} dp")
        for k, v in out["samples"].items():
            print(f"  ({k}) {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
