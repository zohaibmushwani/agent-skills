#!/usr/bin/env python3
"""compose_lint.py - heuristic smell scan for Kotlin/Compose sources (standard library only).

Usage: python compose_lint.py <src-dir> [--theme-dirs ui/theme,theme] [--json]
Rules (E = error, W = warning). It reads text, it does not compile: review every hit.
  E hex-color      Color(0x..)/Color(0xFF..) outside the theme directories
  E intrinsic-min  IntrinsicSize.Min/Max (crashes over BoxWithConstraints / lazy lists)
  E android-log    android.util.Log / Log.d( (use the app logger)
  E global-scope   GlobalScope
  W offset         Modifier.offset( (absolute positioning)
  W left-right     paddingLeft/Right, Alignment.Left/Right, Arrangement.Left/Right, TextAlign.Left/Right (use start/end)
  W text-no-maxlines  Text( call without maxLines/softWrap in a file under components/ (single-line labels need it)
  W no-preview     UI file (has @Composable, not a theme/preview file) with no @Preview
  W bang-bang      '!!' non-null assertion
  W swallow-cancel catch (e: Exception/Throwable) without rethrowing CancellationException nearby
  W hardcoded-string  Text("literal") instead of stringResource
Exit code 1 if any error. Output: path:line rule message.
"""
import json
import re
import sys
from pathlib import Path

RULES = [
    ("E", "hex-color", re.compile(r"Color\(\s*0x[0-9A-Fa-f]{6,8}\s*\)"), "hex colour in a screen: use MaterialTheme.colorScheme tokens", True),
    ("E", "intrinsic-min", re.compile(r"IntrinsicSize\.(Min|Max)"), "intrinsic measurement crashes over subcomposition", False),
    ("E", "android-log", re.compile(r"\bandroid\.util\.Log\b|\bLog\.[dviwe]\("), "use the app logger, not android.util.Log", False),
    ("E", "global-scope", re.compile(r"\bGlobalScope\b"), "GlobalScope leaks work; use viewModelScope/lifecycle scope", False),
    ("W", "offset", re.compile(r"Modifier\.offset\(|\.offset\("), "absolute offset: prefer weights/constraints", False),
    ("W", "left-right", re.compile(r"paddingLeft|paddingRight|Alignment\.(Left|Right)\b|Arrangement\.(Left|Right)\b|TextAlign\.(Left|Right)\b"), "use start/end for RTL", False),
    ("W", "bang-bang", re.compile(r"[A-Za-z0-9_\)\]]!!"), "non-null assertion can crash", False),
    ("W", "hardcoded-string", re.compile(r"\bText\(\s*(text\s*=\s*)?\"[^\"$]{2,}\""), "hard-coded UI string: use stringResource", False),
]


def is_theme(path, theme_dirs):
    p = path.as_posix()
    return any(f"/{d.strip('/')}/" in p or p.endswith(f"/{d.strip('/')}") for d in theme_dirs)


def scan_file(path, theme_dirs):
    out = []
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    theme = is_theme(path, theme_dirs)
    is_test = "/test/" in path.as_posix() or "/androidTest/" in path.as_posix()
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("//") or s.startswith("*") or s.startswith("/*"):
            continue
        for sev, rid, rx, msg, skip_theme in RULES:
            if skip_theme and theme:
                continue
            if rid in ("hardcoded-string", "bang-bang") and is_test:
                continue
            if rid == "android-log" and re.search(r"Log(ger|ging)?\.kt$", path.name):
                continue  # the logging wrapper itself may call android.util.Log
            if rx.search(line):
                out.append((sev, rid, i, msg))
        if re.search(r"catch\s*\(\s*\w+\s*:\s*(Exception|Throwable)\s*\)", line):
            window = "\n".join(lines[i - 1:i + 6])
            if "CancellationException" not in window and "throw" not in window:
                out.append(("W", "swallow-cancel", i, "catching Exception/Throwable can swallow CancellationException: rethrow it"))
    if "/components/" in path.as_posix() and not is_test:
        for m in re.finditer(r"\bText\(", text):
            seg = text[m.start():m.start() + 400]
            depth, end = 0, len(seg)
            for j, ch in enumerate(seg):
                depth += ch == "("
                depth -= ch == ")"
                if depth == 0:
                    end = j
                    break
            call = seg[:end]
            if "maxLines" not in call and "softWrap" not in call:
                out.append(("W", "text-no-maxlines", text[:m.start()].count("\n") + 1, "Text without maxLines/overflow: decide deliberately"))
    if "@Composable" in text and not theme and not is_test and "@Preview" not in text and "MultiPreview" not in text:
        if re.search(r"fun\s+[A-Z]\w+\(", text) and not re.search(r"(Navigation|NavHost|Destination|Module|Route)", path.name):
            out.append(("W", "no-preview", 1, "UI composable file has no @Preview"))
    return out


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    theme_dirs = ["ui/theme", "theme"]
    if "--theme-dirs" in argv:
        theme_dirs = argv[argv.index("--theme-dirs") + 1].split(",")
        args = [a for a in args if a != argv[argv.index("--theme-dirs") + 1]]
    root = Path(args[0])
    results = []
    for p in sorted(root.rglob("*.kt")):
        if "/build/" in p.as_posix():
            continue
        for sev, rid, ln, msg in scan_file(p, theme_dirs):
            results.append({"file": p.as_posix(), "line": ln, "severity": sev, "rule": rid, "message": msg})
    if "--json" in argv:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            print(f"{r['file']}:{r['line']} {r['severity']} {r['rule']} {r['message']}")
        e = sum(r["severity"] == "E" for r in results)
        print(f"\n{len(results)} findings ({e} errors, {len(results) - e} warnings) in {root}")
    return 1 if any(r["severity"] == "E" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
