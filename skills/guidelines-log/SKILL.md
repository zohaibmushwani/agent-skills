---
name: guidelines-log
description: Keep a project's standing rules alive across sessions and healthy. When the user states a durable instruction, preference, convention, correction or confirmed approach ("always X", "never Y", "from now on", "remember this", "yes, exactly like that"), record it the same turn in a dated log and route it to the right place - always-on CLAUDE.md/AGENTS.md, path-scoped .claude/rules, a docs guideline, a skill, or a hook/lint script if it must be enforced. Checks for contradictions and size before writing, skips one-off or obvious things, and audits rule files for bloat, duplicates and stale references. Use at the start of work in any repo with rules or a log, whenever the user gives a rule or says the agent keeps forgetting something, or when asked to clean up or audit CLAUDE.md, AGENTS.md or guidelines.
---

# guidelines-log

Agents forget between sessions; a repository does not. A rule the user says once must be written where the next session will read it, in the same turn, without bloating the files agents load every time. Instructions are context, not enforcement, so the rules that matter most should become scripts.

## When the user states something
1. **Durable?** A rule, preference, convention, correction, or a *confirmed non-obvious approach* ("yes, that's the way") that should apply from now on. One-off instructions ("make this button blue"), things obvious from the code, standard framework behaviour and temporary debugging notes are **not** recorded.
2. **Route it** (`references/routing.md`): can a script or hook enforce it? Do that and keep a one-line pointer. Otherwise the smallest scope that still loads when needed: always-on file, path-scoped rule, on-demand doc, memory, or skill.
3. **Before writing:** search the existing rules for the same subject (edit, do not duplicate); if the new rule contradicts one, replace the old rule and say so; if the target file would pass ~200 lines, split by topic. `scripts/rules_audit.py` does these checks.
4. **Write the rule** as a checkable sentence with its **Why**, and append a dated entry at the top of `GUIDELINES_LOG.md` (rule, why, how to apply, where it went).
5. **Tell the user** in one line what was recorded and where.

## Before work
Read the always-on files and the newest ~10 log entries; apply them without being asked. If a task needs to break a rule, ask first and log the exception. When the same rule is broken twice in a session, treat it as a candidate for a lint script.

## Setup and upkeep
- New repo: create `docs/guidelines/GUIDELINES_LOG.md` and `GUIDELINES.md` from `templates/`, and add to `CLAUDE.md`/`AGENTS.md` two lines: read the guidelines and newest log entries before UI/feature work; record new rules in the same turn. (Claude Code reads `AGENTS.md` directly; for other setups import it from `CLAUDE.md` with `@AGENTS.md`.)
- Audit now and then, and when a rules file feels long: `python scripts/rules_audit.py <repo-root>`. It reports files over the line budget, duplicate and contradicting rules, references to files that no longer exist, secret-like strings, and log entries with no Why. Claude Code also has `/doctor prompt-audit`.
- Revalidate a rule when its subject changes (library replaced, folder renamed), not because it is old.

## Do not
- Log secrets, tokens, personal data or private business details, and never paste raw command output or whole files into entries.
- Record your own guesses as user rules: only what the user said or confirmed.
- Rewrite old log entries; add a new one that supersedes them.
- Let `CLAUDE.md`/`AGENTS.md` become a dump: long reference material belongs in docs loaded on demand.

## Files
`references/routing.md` (where each kind of lesson goes), `references/research.md` (existing tools compared, sources, gaps this version closes), `scripts/rules_audit.py`, `templates/`.
