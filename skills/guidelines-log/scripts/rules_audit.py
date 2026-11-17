#!/usr/bin/env python3
"""rules_audit.py - health check for agent rule files (standard library only).

Usage: python rules_audit.py <repo-root> [--budget 200] [--json]
Scans CLAUDE.md, AGENTS.md, .claude/rules/*.md, docs/guidelines/*.md (and GUIDELINES_LOG.md) for:
  E secret          token/key-like strings (sk-..., ghp_..., AKIA..., 'password = ...', private key headers)
  E broken-ref      a backticked repo path or @import that does not exist
  W over-budget     an always-loaded file (CLAUDE.md/AGENTS.md/.claude/rules) longer than --budget lines (default 200);
                    other guideline files are only noted when over 3x the budget
  W duplicate       two rule lines that are nearly identical (same words) in different places
  W conflict        the same subject with opposite polarity (always/never, must/must not) in different lines
  W log-no-why      a log entry without a Why: line
  W log-order       log entry dates not newest-first
Exit code 1 on any error. It is a heuristic: read each hit before changing anything.
"""
import json
import re
import sys
from pathlib import Path

SECRET = [re.compile(p) for p in (r"\bsk-[A-Za-z0-9_-]{20,}", r"\bghp_[A-Za-z0-9]{30,}", r"\bgho_[A-Za-z0-9]{30,}", r"\bAKIA[0-9A-Z]{16}\b",
                                  r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"(?i)\b(password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_-]{12,}")]
STOP = set("the a an and or of to in for on with is are be it this that as by at from when use used using not no never always must should do does only any all each every your you we".split())
ALWAYS = ("CLAUDE.md", "AGENTS.md")


def words(line):
    return {w for w in re.findall(r"[a-z][a-z0-9_]{2,}", line.lower()) if w not in STOP}


def polarity(line):
    l = line.lower()
    neg = bool(re.search(r"\b(never|must not|do not|don't|no |avoid|forbid)", l))
    pos = bool(re.search(r"\b(always|must|should|use |prefer)", l)) and not neg
    return "neg" if neg else ("pos" if pos else None)


def rule_lines(text):
    out = []
    in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        s = line.strip()
        if in_code or not s.startswith(("-", "*", "1", "2", "3", "4", "5", "6", "7", "8", "9")) or len(s) < 25:
            continue
        out.append((i, s))
    return out


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    budget = 200
    if "--budget" in argv:
        budget = int(argv[argv.index("--budget") + 1])
        args = [a for a in args if a != argv[argv.index("--budget") + 1]]
    if not args:
        print(__doc__)
        return 2
    root = Path(args[0])
    files = []
    for pat in ("CLAUDE.md", "AGENTS.md", ".claude/CLAUDE.md", ".claude/rules/**/*.md", "docs/guidelines/*.md", "docs/**/GUIDELINES*.md"):
        files += [p for p in root.glob(pat) if p.is_file()]
    files = sorted(set(files))
    res = []
    all_rules = []
    for f in files:
        rel = f.relative_to(root).as_posix()
        text = f.read_text(encoding="utf-8", errors="replace")
        n = len(text.splitlines())
        is_log = "LOG" in f.name.upper()
        always = f.name in ALWAYS or rel.startswith(".claude/rules/")
        if not is_log and ((always and n > budget) or n > 3 * budget):
            res.append(("W", "over-budget", rel, 1, f"{n} lines (budget {budget}): split by topic or move detail to on-demand docs"))
        elif is_log is False and not always and n > budget:
            res.append(("I", "long-file", rel, 1, f"{n} lines: fine if loaded on demand, but not if it is always loaded"))
        for i, line in enumerate(text.splitlines(), 1):
            for rx in SECRET:
                if rx.search(line):
                    res.append(("E", "secret", rel, i, "secret-like string"))
                    break
        for m in re.finditer(r"`((?:[\w.-]+/)+[\w.-]+\.\w{1,5})`|(?<![\w`])@((?:[\w.-]+/)*[\w.-]+\.\w{1,5})", text):
            ref = m.group(1) or m.group(2)
            if re.search(r"[<>*{}$]|^https?:|^~|^\.\.|^/|\.(com|org|io|dev|net|app)\b", ref) or ref.startswith(("res/", "app/", "src/")):
                continue
            cands = [root / ref, f.parent / ref]
            if not any(c.exists() for c in cands) and not list(root.rglob(Path(ref).name))[:1]:
                res.append(("E", "broken-ref", rel, text[:m.start()].count("\n") + 1, f"`{ref}` not found"))
        if not is_log:
            for i, s in rule_lines(text):
                all_rules.append((rel, i, s))
        else:
            entries = re.split(r"(?m)^## ", text)[1:]
            dates = []
            nowhy = 0
            for e in entries:
                head = e.splitlines()[0]
                d = re.match(r"(\d{4}-\d{2}-\d{2})", head)
                if d:
                    dates.append(d.group(1))
                    if not re.search(r"(?im)^\**\s*why\b", e) and "why:" not in e.lower():
                        nowhy += 1
            if nowhy:
                res.append(("W", "log-no-why", rel, 1, f"{nowhy} of {len(dates)} dated entries have no Why line (a Why lets a later session judge edge cases)"))
            if dates and dates != sorted(dates, reverse=True):
                res.append(("W", "log-order", rel, 1, "entries are not newest-first"))
    seen = []
    for a in range(len(all_rules)):
        fa, la, sa = all_rules[a]
        wa = words(sa)
        if len(wa) < 4:
            continue
        for b in range(a + 1, len(all_rules)):
            fb, lb, sb = all_rules[b]
            wb = words(sb)
            if len(wb) < 4 or (fa == fb and abs(la - lb) < 2):
                continue
            j = len(wa & wb) / len(wa | wb)
            if j >= 0.45 and polarity(sa) and polarity(sb) and polarity(sa) != polarity(sb):
                key = (fa, la, fb, lb)
                if key not in seen:
                    seen.append(key)
                    res.append(("W", "conflict", fa, la, f"opposite polarity on a similar subject as {fb}:{lb}"))
            elif j >= 0.7:
                res.append(("W", "duplicate", fa, la, f"nearly the same as {fb}:{lb}"))
    if "--json" in argv:
        print(json.dumps([dict(zip(("severity", "rule", "file", "line", "message"), r)) for r in res], indent=1))
    else:
        for sev, rule, rel, ln, msg in res:
            print(f"{rel}:{ln} {sev} {rule} {msg}")
        print(f"\n{len(files)} files scanned; {sum(r[0]=='E' for r in res)} errors, {sum(r[0]=='W' for r in res)} warnings")
    return 1 if any(r[0] == "E" for r in res) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
