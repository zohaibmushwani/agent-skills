#!/usr/bin/env python3
"""scaffold_kit.py - create research/<topic-slug>/ with the standard files.

Usage: python scaffold_kit.py "<topic>" [--root research]
Creates: RESEARCH.md (8-section template), RESOURCES.md, LICENSES.md, DECISIONS.md, concepts.json, repos.txt, shortlist.json, notes/
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent / "templates"


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    topic = argv[1]
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else Path("research")
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-") or "topic"
    d = root / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "notes").mkdir(exist_ok=True)
    for name in ("research-doc.md", "RESOURCES.md", "LICENSES.md", "DECISIONS.md"):
        src = HERE / name
        target = d / ("RESEARCH.md" if name == "research-doc.md" else name)
        if not target.exists():
            target.write_text(src.read_text(encoding="utf-8").replace("<TOPIC>", topic), encoding="utf-8")
    skeleton = {"topic": topic, "platform": "", "languages": [], "pillars": {"pillar_1": {"words": [], "symbols": [], "formats": [], "noise": []}},
                "regional": [], "registries": []}
    if not (d / "concepts.json").exists():
        (d / "concepts.json").write_text(json.dumps(skeleton, indent=1), encoding="utf-8")
    for f, content in (("repos.txt", "# one owner/name per line, then: python repo_probe.py repos.txt\n"), ("shortlist.json", "[]\n")):
        if not (d / f).exists():
            (d / f).write_text(content, encoding="utf-8")
    print(f"created {d}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
