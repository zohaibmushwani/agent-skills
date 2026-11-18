#!/usr/bin/env python3
"""Fail prompts that use another target's vocabulary (e.g. 'portrait' / 'phone' in a website prompt).

Usage: prompt_lint.py <design-dir>
Reads inventory.json: "platform": "web" | "mobile" (default mobile), "mobile_first": true relaxes web checks.
Scans <design-dir>/prompts/*.md. Negations such as 'No phone frame' are allowed (the word after no/not/without).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import Report, load_json  # noqa: E402

WEB_BAD = [r"portrait", r"\bphone\b", r"status bar", r"9:19", r"9:16", r"android (status|nav|ui|screen|app screen)", r"\bios (status|nav|ui|screen)", r"iphone (frame|screen|status)",
           r"bottom nav", r"thumb", r"app screen", r"mobile app"]
MOBILE_BAD = [r"browser (window|chrome)", r"landscape desktop", r"1440", r"\bhero section\b", r"address bar"]
NEG = re.compile(r"\b(no|not|without|never|don't|do not add|avoid)\b[^.\n]{0,60}$", re.I)


def hits(text, patterns):
    found = set()
    for line in text.splitlines():
        for pat in patterns:
            for m in re.finditer(pat, line, re.I):
                if NEG.search(line[: m.start()]):
                    continue  # negated mention ("no phone frame") is fine
                found.add(m.group(0).lower())
    return sorted(found)


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1])
    inv = load_json(root / "inventory.json") if (root / "inventory.json").exists() else {}
    web = inv.get("platform") == "web"
    relaxed = bool(inv.get("mobile_first"))
    rep = Report("Prompt vocabulary lint")
    files = sorted((root / "prompts").glob("*.md")) if (root / "prompts").exists() else []
    if not files:
        rep.ok("no prompts/ files to lint")
    for p in files:
        text = p.read_text(encoding="utf-8")
        bad = hits(text, WEB_BAD) if (web and not relaxed) else hits(text, MOBILE_BAD) if not web else []
        if bad:
            rep.fail(f"{p.name}: wrong-target words {bad} (target {'web' if web else 'mobile'})")
        else:
            rep.ok(p.name)
    print(rep.markdown())
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
