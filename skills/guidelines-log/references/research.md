# Research behind this skill (2026-11-18)
Method: oss-first-development (dorks, chain, verify, judge). Existing agent "memory / self-improvement" skills and the official Claude Code docs, compared with this skill's first version.

| Source | Evidence | License | Label | What we take |
|---|---|---|---|---|
| Claude Code memory docs (code.claude.com/docs/en/memory) | VERIFIED (read) | docs | R | CLAUDE.md target < 200 lines; instructions are context, not enforcement (use a hook to block); contradicting rules are picked arbitrarily; `.claude/rules/*.md` with `paths:` frontmatter load only for matching files; `@path` imports; AGENTS.md is read directly; auto memory is written by Claude (first 200 lines / 25 KB load); `/doctor prompt-audit` finds stale or conflicting instructions |
| pskoett/self-improving-agent (~790 stars) | VERIFIED (SKILL.md read) | none found -> ideas only | P | capture categories (correction / insight / knowledge gap / best practice), recurrence key to count repeats, promotion from a log to the always-loaded file, revalidate a claim when its source changes (not by age), never log secrets |
| builderio/agent-native `capture-learnings` | VERIFIED (SKILL.md read) | none found -> ideas only | P | memory types user / feedback / project / reference; capture **confirmed approaches** as well as corrections; "don't capture what is obvious from code, standard behaviour, or temporary debugging"; scope by audience; review at a natural stopping point |
| tobihagemann/turbo `self-improve` (~420 stars) | VERIFIED (SKILL.md read) | none found -> ideas only | P | route each lesson to the right layer (instructions, memory, skill); verify before routing; optional sweep of past sessions |
| Registry pages (skills.sh, tessl, skills.cat, playbooks) | LEAD (snippets) | - | N | mirrors of the above; one entry was flagged by a registry scan for telling agents to copy full file contents into shared files, a reason to keep a "no secrets, no raw dumps" rule |

No code was copied: the repos above show no license, so only ideas were used.

## What version 1 of this skill lacked (gap analysis)
1. **Routing:** it only wrote to a log and one guidelines file. Real systems route a lesson to the layer that fits: always-on instructions, path-scoped rules, memory, a skill, a hook or a lint script.
2. **Size budget:** nothing stopped GUIDELINES.md from growing past what is reliably followed (official guidance: under ~200 lines per file).
3. **Contradiction check** before writing a rule (the docs warn that conflicting rules are resolved arbitrarily).
4. **Confirmed approaches** were not captured, only corrections.
5. **Recurrence and staleness:** no way to see a rule that keeps being broken (promote it to a script) or one whose subject no longer exists.
6. **No audit tool** to keep the rule files healthy.

## Not verified
- Auto-memory internals beyond what the docs page states.
- Behaviour of the registry skills in practice (only their SKILL.md text was read).
