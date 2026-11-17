---
name: guidelines-log
description: Keep a project's standing rules alive across sessions. When the user gives a new instruction, preference, best practice or correction that should apply from now on ("always do X", "never Y", "from now on", "remember this", "this is a rule"), record it in the same turn as a dated entry in docs/guidelines/GUIDELINES_LOG.md and, if it is a lasting rule, fold it into the project's main guidelines file; also read the newest entries before starting a UI or feature task. Use at the start of work in any repo that has such a log, and whenever the user states a rule, convention or lesson learned, even in passing.
---

# guidelines-log

Agents forget between sessions; a repository does not. Rules the user states once should be written where the next session will read them, in the same turn they were given, or they are lost.

## Setup (once per repo)
If the repo has no log, create `docs/guidelines/GUIDELINES_LOG.md` and `docs/guidelines/GUIDELINES.md` from `templates/`, and add two lines to the repo's agent instructions file (`CLAUDE.md` / `AGENTS.md`): read the guidelines and the newest log entries before any UI or feature task; record new rules in the same turn.

## When the user states a rule
1. Decide if it is **durable** (applies to all future work: "colours only through theme tokens") or **one-off** (this task only: "make this button blue"). One-off instructions are not logged.
2. Append an entry at the **top** of the log (newest first): `YYYY-MM-DD - <short title>`, the rule in one or two sentences, **Why** (the defect or preference behind it), **How to apply** (where it bites).
3. If durable, also fold it into the matching section of `GUIDELINES.md` (edit the section; do not append a duplicate). If it contradicts an existing rule, replace the old rule and say so in the log entry.
4. Tell the user in one line what you recorded and where.

## Before work
Read `GUIDELINES.md` and the newest ~10 log entries. Apply them without being asked; if a task needs to break one, ask first and log the exception.

## Do not
- Put secrets, tokens, personal data or private business details in the log.
- Log your own guesses as user rules: record only what the user said or confirmed.
- Let the log grow into history: when an entry is folded into `GUIDELINES.md`, keep the log line short and point to the section.
- Rewrite old entries; add a new one that supersedes them.
