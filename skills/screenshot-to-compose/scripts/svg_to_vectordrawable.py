#!/usr/bin/env python3
"""svg_to_vectordrawable.py - convert a simple icon SVG (Iconify/Lucide/Tabler/Material style) to an Android VectorDrawable.

Usage: python svg_to_vectordrawable.py icon.svg res/drawable/ic_name.xml [--size 24] [--mirror] [--tint]
Supports path, circle, ellipse, rect (with rx), line, polyline, polygon, and group-level stroke/fill attributes
inherited from <svg>/<g>. Colours become black (tint at the call site) with --tint, otherwise the SVG colours are kept.
Not supported (the script says so and exits 1): transforms, gradients, masks, clipPaths, <use>, text, images.
"""
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
UNSUPPORTED = {"linearGradient", "radialGradient", "mask", "clipPath", "use", "text", "image", "filter"}


def f(v):
    s = ("%.4f" % float(v)).rstrip("0").rstrip(".")
    return s or "0"


def shape_path(tag, at):
    g = lambda k, d="0": float(at.get(k, d))
    if tag == "path":
        return at.get("d")
    if tag == "circle":
        cx, cy, r = g("cx"), g("cy"), g("r")
        return f"M{f(cx - r)},{f(cy)}a{f(r)},{f(r)} 0 1,0 {f(2 * r)},0a{f(r)},{f(r)} 0 1,0 {f(-2 * r)},0"
    if tag == "ellipse":
        cx, cy, rx, ry = g("cx"), g("cy"), g("rx"), g("ry")
        return f"M{f(cx - rx)},{f(cy)}a{f(rx)},{f(ry)} 0 1,0 {f(2 * rx)},0a{f(rx)},{f(ry)} 0 1,0 {f(-2 * rx)},0"
    if tag == "rect":
        x, y, w, h = g("x"), g("y"), g("width"), g("height")
        rx = g("rx", at.get("ry", "0"))
        if rx <= 0:
            return f"M{f(x)},{f(y)}h{f(w)}v{f(h)}h{f(-w)}z"
        rx = min(rx, w / 2, h / 2)
        return (f"M{f(x + rx)},{f(y)}h{f(w - 2 * rx)}a{f(rx)},{f(rx)} 0 0,1 {f(rx)},{f(rx)}v{f(h - 2 * rx)}"
                f"a{f(rx)},{f(rx)} 0 0,1 {f(-rx)},{f(rx)}h{f(-(w - 2 * rx))}a{f(rx)},{f(rx)} 0 0,1 {f(-rx)},{f(-rx)}"
                f"v{f(-(h - 2 * rx))}a{f(rx)},{f(rx)} 0 0,1 {f(rx)},{f(-rx)}z")
    if tag == "line":
        return f"M{f(g('x1'))},{f(g('y1'))}L{f(g('x2'))},{f(g('y2'))}"
    if tag in ("polyline", "polygon"):
        nums = re.findall(r"-?\d*\.?\d+(?:e-?\d+)?", at.get("points", ""))
        pts = [(nums[i], nums[i + 1]) for i in range(0, len(nums) - 1, 2)]
        if not pts:
            return None
        d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts)
        return d + ("z" if tag == "polygon" else "")
    return None


def inherit(parent, el):
    st = dict(parent)
    for k in ("fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin", "fill-rule", "opacity", "fill-opacity", "stroke-opacity"):
        if el.get(k) is not None:
            st[k] = el.get(k)
    style = el.get("style")
    if style:
        for part in style.split(";"):
            if ":" in part:
                k, v = (x.strip() for x in part.split(":", 1))
                st[k] = v
    return st


def color(v, tint, default):
    if v is None:
        return default
    if v in ("none",):
        return None
    if tint or v == "currentColor":
        return "#FF000000"
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", v)
    if m:
        h = m.group(1)
        h = "".join(c * 2 for c in h) if len(h) == 3 else h
        return "#FF" + h.upper()
    return "#FF000000"


def walk(el, st, tint, out, bad):
    for ch in el:
        tag = ch.tag.replace(NS, "")
        if tag in UNSUPPORTED:
            bad.add(tag)
            continue
        if ch.get("transform"):
            bad.add("transform")
        cs = inherit(st, ch)
        if tag == "g":
            walk(ch, cs, tint, out, bad)
            continue
        d = shape_path(tag, ch.attrib)
        if not d:
            continue
        fill = color(cs.get("fill"), tint, "#FF000000")
        stroke = color(cs.get("stroke"), tint, None)
        out.append((d, fill, stroke, cs))


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    size = float(argv[argv.index("--size") + 1]) if "--size" in argv else 24.0
    if "--size" in argv:
        args = [a for a in args if a != argv[argv.index("--size") + 1]]
    src, dst = args[0], args[1]
    tint = "--tint" in argv
    root = ET.parse(src).getroot()
    vb = [float(x) for x in re.split(r"[ ,]+", root.get("viewBox", "0 0 24 24").strip())]
    st = inherit({}, root)
    out, bad = [], set()
    walk(root, st, tint, out, bad)
    if bad:
        print("unsupported SVG features: " + ", ".join(sorted(bad)) + " - simplify the SVG first", file=sys.stderr)
        return 1
    mirror = ' android:autoMirrored="true"' if "--mirror" in argv else ""
    L = ['<vector xmlns:android="http://schemas.android.com/apk/res/android"',
         f'    android:width="{f(size)}dp" android:height="{f(size)}dp"',
         f'    android:viewportWidth="{f(vb[2])}" android:viewportHeight="{f(vb[3])}"{mirror}>']
    for d, fill, stroke, cs in out:
        a = [f'        android:pathData="{d}"']
        if fill:
            a.append(f'        android:fillColor="{fill}"')
        if stroke:
            a.append(f'        android:strokeColor="{stroke}"')
            a.append(f'        android:strokeWidth="{f(cs.get("stroke-width", "1"))}"')
            a.append(f'        android:strokeLineCap="{cs.get("stroke-linecap", "butt")}"')
            a.append(f'        android:strokeLineJoin="{cs.get("stroke-linejoin", "miter")}"')
        if cs.get("fill-rule") == "evenodd":
            a.append('        android:fillType="evenOdd"')
        L.append("    <path\n" + "\n".join(a) + "/>")
    L.append("</vector>")
    open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"wrote {dst} ({len(out)} paths)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
