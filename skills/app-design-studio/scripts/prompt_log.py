#!/usr/bin/env python3
"""Log every accept/reject of a generated design so the skill learns which prompts work.

Usage:
  prompt_log.py add <design-dir> --id 03-list --image screens/03.png --prompt prompts/03.md \
      --verdict accept|reject|fix --mode brief|locked|edit --tags faces,cropped --reason "..." [--fix "..."] [--engine codex]
  prompt_log.py summary <design-dir>      # writes reports/prompt-learnings.md, prints it

Storage: <design-dir>/reports/prompt-log.jsonl (one JSON per line, append-only).
Tags (free text allowed, prefer these): faces, cropped, wrong-orientation, generic-tell, missing-core, stale-date,
count-mismatch, small-text, numbering, outer-frame, label-wrong, inconsistent-nav, over-constrained, other.
Rule: when the same tag is rejected >= 2 times, promote it to references/design-craft.md "Learned lessons".
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


def log_path(root):
    return Path(root) / "reports" / "prompt-log.jsonl"


def load(root):
    p = log_path(root)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def add(a):
    p = log_path(a.dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    prompt_text = ""
    pp = Path(a.dir) / a.prompt if a.prompt else None
    if pp and pp.exists():
        prompt_text = pp.read_text(encoding="utf-8")
    rec = {"date": a.date or str(date.today()), "id": a.id, "image": a.image, "prompt_file": a.prompt,
           "prompt_words": len(prompt_text.split()) if prompt_text else None, "mode": a.mode, "engine": a.engine,
           "verdict": a.verdict, "tags": [t for t in (a.tags or "").split(",") if t], "reason": a.reason, "fix": a.fix}
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"logged {a.verdict}: {a.id}")


def summary(root):
    rows = load(root)
    out = ["# Prompt learnings (generated from reports/prompt-log.jsonl)", ""]
    if not rows:
        out.append("No entries yet.")
    else:
        v = Counter(r["verdict"] for r in rows)
        out.append(f"Entries: {len(rows)}  |  accept {v['accept']}  fix {v['fix']}  reject {v['reject']}")
        out += ["", "## Accept rate by prompt mode", "", "| mode | n | accept | fix | reject | avg words |", "|---|---|---|---|---|---|"]
        by = defaultdict(list)
        for r in rows:
            by[r.get("mode") or "?"].append(r)
        for m, rs in sorted(by.items()):
            c = Counter(r["verdict"] for r in rs)
            w = [r["prompt_words"] for r in rs if r.get("prompt_words")]
            out.append(f"| {m} | {len(rs)} | {c['accept']} | {c['fix']} | {c['reject']} | {round(sum(w)/len(w)) if w else '-'} |")
        tags = Counter(t for r in rows if r["verdict"] in ("reject", "fix") for t in r["tags"])
        out += ["", "## Failure tags (reject + fix)", ""]
        for t, n in tags.most_common():
            out.append(f"- **{t}**: {n}" + ("  -> PROMOTE to design-craft.md Learned lessons" if n >= 2 else ""))
        out += ["", "## Log", "", "| date | id | mode | verdict | tags | reason |", "|---|---|---|---|---|---|"]
        for r in rows:
            out.append(f"| {r['date']} | {r['id']} | {r.get('mode') or ''} | {r['verdict']} | {','.join(r['tags'])} | {r.get('reason') or ''} |")
    text = "\n".join(out) + "\n"
    (Path(root) / "reports").mkdir(exist_ok=True)
    (Path(root) / "reports" / "prompt-learnings.md").write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("add")
    a.add_argument("dir"); a.add_argument("--id", required=True); a.add_argument("--image", default="")
    a.add_argument("--prompt", default=""); a.add_argument("--verdict", required=True, choices=["accept", "reject", "fix"])
    a.add_argument("--mode", default="", choices=["", "brief", "locked", "edit"]); a.add_argument("--tags", default="")
    a.add_argument("--reason", default=""); a.add_argument("--fix", default=""); a.add_argument("--engine", default="codex")
    a.add_argument("--date", default="")
    s = sp.add_parser("summary"); s.add_argument("dir")
    args = ap.parse_args()
    add(args) if args.cmd == "add" else summary(args.dir)


if __name__ == "__main__":
    sys.exit(main())
