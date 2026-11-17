#!/usr/bin/env python3
"""Lint tokens.json and (optionally) HTML/CSS/Kotlin files for hard-coded values.

Usage: token_lint.py <design-dir> [--code <dir-with-html-css-kt>]
Checks:
  - spacing tokens are on the 4-pt grid
  - type scale has no size < 12 and is monotonic
  - at most 2 font families if 'fonts' is given
  - radius tokens are positive ints
  - with --code: hex colours / dp-px spacing literals that are not defined in tokens.json
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import Report, load_json  # noqa: E402

HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
PX = re.compile(r"(?<![\w.])(\d{1,3})(?:px|dp)\b")
EXT = {".html", ".css", ".kt", ".xml", ".dart", ".tsx", ".jsx"}


def lint_tokens(tokens, rep):
    for s in tokens.get("spacing", []):
        if not isinstance(s, int) or s % 4:
            rep.fail(f"spacing {s} is not on the 4-pt grid")
    scale = tokens.get("type", {})
    for name, size in scale.items():
        if size < 12:
            rep.fail(f"type '{name}' = {size} < 12")
    vals = list(scale.values())
    if vals != sorted(vals, reverse=True):
        rep.warn("type scale is not listed from largest to smallest")
    if len(vals) > 7:
        rep.warn(f"{len(vals)} text sizes defined; keep <= 6-7 for coherence")
    fonts = tokens.get("fonts", {})
    fams = {v for v in fonts.values()} if isinstance(fonts, dict) else set(fonts)
    if len(fams) > 2:
        rep.fail(f"{len(fams)} font families ({', '.join(sorted(fams))}); max 2")
    for k, v in tokens.get("radius", {}).items():
        if not isinstance(v, int) or v <= 0:
            rep.fail(f"radius '{k}' invalid: {v}")
    if tokens.get("touch_target", 48) < 44:
        rep.fail("touch_target token < 44")
    if not rep.rows:
        rep.ok("tokens ok")


def lint_code(code_dir, tokens, rep):
    known_hex = {v.lower() for mode in tokens.get("color", {}).values() for v in mode.values() if isinstance(v, str)}
    known_sp = set(tokens.get("spacing", [])) | set(tokens.get("type", {}).values()) | set(tokens.get("radius", {}).values()) | {0, 1, 2}
    for p in Path(code_dir).rglob("*"):
        if p.suffix.lower() not in EXT or not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "generated" in text[:200].lower() and "tokens" in p.name.lower():
            continue  # token definition files themselves
        for m in HEX.finditer(text):
            if m.group(0).lower() not in known_hex:
                rep.warn(f"{p.name}: colour {m.group(0)} not in tokens")
        for m in PX.finditer(text):
            if int(m.group(1)) not in known_sp:
                rep.warn(f"{p.name}: size {m.group(0)} not a token value")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1])
    tokens = load_json(root / "tokens.json")
    rep = Report("Token lint")
    lint_tokens(tokens, rep)
    if "--code" in argv:
        lint_code(argv[argv.index("--code") + 1], tokens, rep)
    print(rep.markdown())
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
