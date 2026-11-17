#!/usr/bin/env python3
"""Audit *.spec.json files: touch targets, text size, contrast, primary actions, thumb zone.

Usage: spec_audit.py <design-dir> [--strict]
  design-dir contains tokens.json and screens/, states/, dialogs/, sheets/ with *.spec.json
Thresholds: touch >= tokens.touch_target (default 48), body text >= 12 (WARN < 14 for non-caption text types
marked 'body'), contrast 4.5 (3.0 if font >= 18 or element type is icon).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import Report, contrast, load_json, resolve_color  # noqa: E402

MIN_FONT = 12
BODY_FONT = 14


def audit_spec(path, tokens, strict):
    rep_rows = []
    spec = load_json(path)
    sid = spec.get("id", Path(path).stem)
    mode = spec.get("mode", "light")
    palette = tokens.get("color", {}).get(mode, {})
    touch_min = tokens.get("touch_target", 48)
    height = (spec.get("size") or [0, 0])[1]
    primaries = 0

    for el in spec.get("elements", []):
        eid = el.get("id", "?")
        tag = f"{sid}:{eid}"
        w, h = el.get("w"), el.get("h")
        if el.get("interactive"):
            if w is None or h is None:
                rep_rows.append(("WARN", f"{tag} interactive but no w/h (hit area unknown)"))
            elif w < touch_min or h < touch_min:
                rep_rows.append(("FAIL", f"{tag} touch target {w}x{h} < {touch_min}"))
            if el.get("primary"):
                primaries += 1
                y = el.get("y")
                if height and y is not None and y < height * 0.55 and el.get("frequent", True):
                    rep_rows.append(("WARN", f"{tag} primary action at y={y} is above the lower thumb zone"))
        font = el.get("font", 0) or 0
        if font and font < MIN_FONT:
            rep_rows.append(("FAIL", f"{tag} font {font}sp < {MIN_FONT}sp"))
        elif font and el.get("type") == "body" and font < BODY_FONT:
            rep_rows.append(("WARN", f"{tag} body font {font}sp < {BODY_FONT}sp"))
        fg, bg = el.get("fg"), el.get("bg")
        if fg and bg:
            try:
                ratio = contrast(resolve_color(fg, palette), resolve_color(bg, palette))
                need = 3.0 if (font >= 18 or el.get("type") == "icon") else 4.5
                if ratio < need:
                    rep_rows.append(("FAIL", f"{tag} contrast {ratio:.2f}:1 < {need}:1 ({fg} on {bg})"))
            except KeyError as e:
                rep_rows.append(("WARN", f"{tag} unknown colour token {e}"))
    declared = spec.get("primary_actions")
    if declared is not None and declared > 1:
        rep_rows.append(("WARN", f"{sid} has {declared} primary actions (expect at most 1)"))
    elif primaries > 1:
        rep_rows.append(("WARN", f"{sid} has {primaries} elements flagged primary"))
    if spec.get("overflowX"):
        rep_rows.append(("FAIL", f"{sid} has horizontal overflow at {spec.get('size', ['?'])[0]}px width"))
    return rep_rows


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1])
    strict = "--strict" in argv
    tokens = load_json(root / "tokens.json") if (root / "tokens.json").exists() else {}
    rep = Report("Element audit (spec.json)")
    specs = sorted(p for p in root.rglob("*.spec.json"))
    if not specs:
        rep.fail(f"no *.spec.json found under {root}")
    for p in specs:
        rows = audit_spec(p, tokens, strict)
        for lvl, msg in rows:
            (rep.fail if lvl == "FAIL" else rep.warn)(msg)
        if not rows:
            rep.ok(str(p.name))
    print(rep.markdown())
    return 1 if rep.failed or (strict and rep.counts()["WARN"]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
