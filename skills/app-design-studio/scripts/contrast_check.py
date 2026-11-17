#!/usr/bin/env python3
"""WCAG contrast checker.

Usage:
  contrast_check.py "#14181F" "#FFFFFF"        # two colours
  contrast_check.py tokens.json                # every pair in tokens.json, light+dark
Exit code 1 if any text pair < 4.5 or any icon pair < 3.0.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import Report, contrast, load_json, resolve_color, HEX_RE  # noqa: E402

TEXT_MIN, LARGE_MIN = 4.5, 3.0


def check_tokens(tokens):
    rep = Report("Contrast (tokens.json)")
    modes = tokens.get("color", {})
    if not modes:
        rep.fail("tokens.json has no 'color' section")
        return rep
    for mode, palette in modes.items():
        for fg, bg in tokens.get("pairs", []):
            try:
                ratio = contrast(resolve_color(fg, palette), resolve_color(bg, palette))
            except KeyError as e:
                rep.fail(f"[{mode}] unknown token {e} in pair {fg}/{bg}")
                continue
            if ratio < TEXT_MIN:
                rep.fail(f"[{mode}] text {fg} on {bg} = {ratio:.2f}:1 (need {TEXT_MIN}:1)")
            else:
                rep.ok(f"[{mode}] {fg}/{bg} {ratio:.2f}")
        for fg, bg in tokens.get("icon_pairs", []):
            try:
                ratio = contrast(resolve_color(fg, palette), resolve_color(bg, palette))
            except KeyError as e:
                rep.fail(f"[{mode}] unknown token {e} in icon pair {fg}/{bg}")
                continue
            if ratio < LARGE_MIN:
                rep.fail(f"[{mode}] graphic {fg} on {bg} = {ratio:.2f}:1 (need {LARGE_MIN}:1)")
            else:
                rep.ok(f"[{mode}] icon {fg}/{bg} {ratio:.2f}")
    if not tokens.get("pairs"):
        rep.warn("no 'pairs' defined; nothing text-related was checked")
    return rep


def main(argv):
    if len(argv) == 3 and HEX_RE.match(argv[1]) and HEX_RE.match(argv[2]):
        r = contrast(argv[1], argv[2])
        print(f"{r:.2f}:1  AA text {'pass' if r >= 4.5 else 'FAIL'}  AA large/graphics {'pass' if r >= 3 else 'FAIL'}")
        return 0 if r >= 4.5 else 1
    if len(argv) == 2:
        rep = check_tokens(load_json(argv[1]))
        print(rep.markdown())
        return 1 if rep.failed else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
