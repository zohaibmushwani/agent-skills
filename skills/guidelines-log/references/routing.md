# Routing a rule to the right place

| The lesson is... | Put it in | Why |
|---|---|---|
| a short rule needed in almost every task | `CLAUDE.md` / `AGENTS.md` (keep the file under ~200 lines) | always loaded |
| a rule for one area (UI, network, tests) or file type | `.claude/rules/<topic>.md`, with `paths:` frontmatter if it only applies to some files | loaded only when relevant, keeps the main file short |
| a long checklist or reference | `docs/guidelines/<topic>.md`, linked with `@docs/...` or "read before X" | loaded on demand |
| a personal preference of this user across projects | the agent's memory / `~/.claude/rules/` | not a project rule |
| a repeatable procedure | a skill (`SKILL.md` + scripts) | triggered by the task |
| a rule that **must never be broken** | a hook or a lint/CI script (for example `compose_lint.py`) | instructions are context, not enforcement |
| a one-off instruction for this task | nowhere (do it, do not log it) | not durable |

Decision order: can a script enforce it? -> do that and keep a one-line rule pointing at the script. Otherwise the smallest scope that still loads when needed.

## Log vs guidelines
- **Log** (`GUIDELINES_LOG.md`): history, newest first: what was said, why, when. Not loaded every session.
- **Guidelines / rules files**: the current truth, edited in place. This is what agents follow.
- An entry is "folded" when its rule lives in a rules file; the log line then just points to it.

## Before writing a rule
1. Search the existing rules for the same subject. If one exists, **edit it**; if the new rule contradicts it, replace it and say so in the log entry.
2. Check the size budget of the target file; if the file would pass ~200 lines, split by topic into `.claude/rules/` or `docs/guidelines/` and leave an index line.
3. Make it checkable: "colours only through theme tokens" beats "keep colours consistent".
4. Record the reason (Why), so a later session can judge edge cases instead of following the letter.
