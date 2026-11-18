#!/usr/bin/env python3
"""fit_store.py - fit generated frames to exact store sizes and remove alpha (Python 3 + Pillow).

Usage: python fit_store.py in_dir out_dir [--size play|ios69|WxH]
Scales each NN.png to cover the target size (centre crop, never stretch) and saves RGB PNG without alpha + contact.png.
"""
import sys
from pathlib import Path

from PIL import Image

SIZES = {"play": (1080, 1920), "ios69": (1290, 2796)}


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    sz = argv[argv.index("--size") + 1] if "--size" in argv else "play"
    W, H = SIZES.get(sz) or tuple(map(int, sz.split("x")))
    src, dst = Path(args[0]), Path(args[1])
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(src.glob("[0-9][0-9]*.png"))
    thumbs = []
    for p in files:
        im = Image.open(p).convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        k = max(W / bg.width, H / bg.height)
        r = bg.resize((round(bg.width * k), round(bg.height * k)), Image.LANCZOS)
        x, y = (r.width - W) // 2, (r.height - H) // 2
        r = r.crop((x, y, x + W, y + H))
        name = p.name[:2] + ".png"
        r.save(dst / name)
        thumbs.append(r.resize((216, round(216 * H / W))))
        print(f"{p.name} -> {name} {W}x{H}" + ("  (cropped)" if abs(bg.width / bg.height - W / H) > 0.01 else ""))
    if thumbs:
        sheet = Image.new("RGB", (len(thumbs) * 228 + 12, thumbs[0].height + 24), (233, 233, 236))
        for i, t in enumerate(thumbs):
            sheet.paste(t, (12 + i * 228, 12))
        sheet.save(dst / "contact.png")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
