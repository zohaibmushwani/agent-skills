#!/usr/bin/env python3
"""compare_side_by_side.py - put a reference screenshot and a render next to each other (Python 3 + Pillow).

Usage: python compare_side_by_side.py reference.png render.png out.png [--overlay]
The reference is scaled to the render's width (same dp frame), then both are shown at equal height side by side.
--overlay also writes out_overlay.png with a 50% blend, which shows offsets at a glance.
"""
import sys

from PIL import Image


def main(argv):
    args = [x for x in argv[1:] if not x.startswith("--")]
    if len(args) != 3:
        print(__doc__)
        return 2
    ref, ren, out = args
    r = Image.open(ref).convert("RGB")
    c = Image.open(ren).convert("RGB")
    r = r.resize((c.width, round(r.height * c.width / r.width)), Image.LANCZOS)
    h = max(r.height, c.height)
    sheet = Image.new("RGB", (r.width + c.width + 24, h), (128, 128, 128))
    sheet.paste(r, (0, 0))
    sheet.paste(c, (r.width + 24, 0))
    sheet.save(out)
    print(f"wrote {out} ({sheet.width}x{sheet.height}); left = reference, right = render")
    if "--overlay" in argv:
        top = min(r.height, c.height)
        blend = Image.blend(r.crop((0, 0, c.width, top)), c.crop((0, 0, c.width, top)), 0.5)
        o = out.rsplit(".", 1)[0] + "_overlay.png"
        blend.save(o)
        print(f"wrote {o}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
