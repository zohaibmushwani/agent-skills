# agent-skills

Two [Agent Skills](https://docs.claude.com) (`SKILL.md` format) for Claude Code and other skill-aware agents.

| Skill | What it does | Use it when |
|---|---|---|
| [`oss-first-development`](skills/oss-first-development) | Finds, verifies and judges existing open-source code before you write anything: targeted web dorks chained on identifiers, optional long-tail GitHub topic sweep, license gate, source check, reuse/adapt/idea/write decision, clone script, build plan. | "Is there a library for X?", building a complex app/backend, converting A to B, avoiding reinventing the wheel. |
| [`app-design-studio`](skills/app-design-studio) | Turns an app name into a full portrait, high-fidelity mobile screen set (splash to settings, states, dialogs, components) with no device frame, and audits it with measurable usability gates. | You need a complete mobile UI design repository, not one mockup. |

## Install
**Claude Code (plugin marketplace)**
```
/plugin marketplace add zohaibmushwani/agent-skills
/plugin install agent-skills@agent-skills
```
**Manual:** copy a folder from `skills/` into `~/.claude/skills/` (all projects) or `<project>/.claude/skills/`.

## Requirements
- Python 3.9+ (scripts use the standard library only).
- `oss-first-development`: [GitHub CLI](https://cli.github.com) logged in (`gh auth login`) for repo probing and topic sweeps; a web search tool for dorks.
- `app-design-studio`: Node 18+ and Playwright with Chromium for `render_screens.mjs` (HTML-render route); an image model is optional.

## Try it
- `oss-first-development`: ask "I want to build an SVG editor for Android. Research existing projects first." You should get a research doc with verified repos, license verdicts and a decision table, and no code.
- `app-design-studio`: `python skills/app-design-studio/scripts/run_gates.py skills/app-design-studio/assets/example` runs the contrast, token, touch-target and state-coverage gates on the bundled example. Contrast, token and element gates pass; the state-coverage gate reports FAIL on purpose, because the example is a small partial set (2 screens) so you can see what a missing state looks like.

## What these skills will not do
- Bypass bot protection or login walls (Cloudflare, search-engine checkpoints). They ask you to open the page instead.
- Copy GPL/AGPL/unlicensed code into a closed-source plan. Those repos are marked study-only.
- Put your name, email or project details into search queries.
- Start building inside the research skill. It stops at a plan and your decisions.

## Evidence and limits (v0.1.0)
- Each skill ships 3 eval cases (`evals/`). Early runs, one run per case: with the skill the research cases passed more assertions than without it, at roughly +50 s and +6k tokens. That is a small sample; some assertions mirror the skill's own method.
- The topic sweep found small permissive repos that dorks missed on one topic (audio-reactive 3D dance app); it has been measured on that single topic.
- Not yet done: description trigger tuning on a larger query set, repeated runs for variance, RTL/dark-mode/real-font coverage in the design example.

## Layout
```
skills/<name>/SKILL.md      instructions (loaded when the skill triggers)
skills/<name>/references/   detail loaded on demand
skills/<name>/scripts/      deterministic helpers
skills/<name>/evals/        test prompts and checks
skills/<name>/examples/     worked runs (oss-first-development)
```

## Contributing
Issues and PRs welcome. Keep `description` at or below 1024 characters, keep `SKILL.md` under ~500 lines, and add an eval case for any new behaviour.

## License
MIT. Third-party projects mentioned in the examples keep their own licenses.
