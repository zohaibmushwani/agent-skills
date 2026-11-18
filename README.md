# agent-skills

Seven [Agent Skills](https://docs.claude.com) (`SKILL.md` format) for Claude Code and other skill-aware agents.

| Skill | What it does | Use it when |
|---|---|---|
| [`oss-first-development`](skills/oss-first-development) | Finds, verifies and judges existing open-source code before you write anything: targeted web dorks chained on identifiers, optional long-tail GitHub topic sweep, license gate, source check, reuse/adapt/idea/write decision, clone script, build plan. | "Is there a library for X?", building a complex app/backend, converting A to B, avoiding reinventing the wheel. |
| [`screenshot-to-compose`](skills/screenshot-to-compose) | Builds screenshots/mockups into a native Jetpack Compose UI: px to dp, sampled colours, observed vs inferred values, Iconify icons to VectorDrawable, generated (never cropped) artwork, side-by-side comparison with the reference. | You have screenshots or a design repo and want the Compose app. |
| [`android-compose-quality-gate`](skills/android-compose-quality-gate) | Acceptance checklist and rules for Compose apps (MVI, RTL, text fit, device matrix, back, permissions, network/offline, motion) plus `compose_lint.py` and `strings_audit.py`. | Before calling an Android UI task done, or when reviewing a screen. |
| [`guidelines-log`](skills/guidelines-log) | Records durable user rules the same turn and routes each to the right layer (always-on file, path-scoped rule, doc, skill, or a hook/lint script), checks contradictions and size first, and audits rule files (`rules_audit.py`). | You keep telling the agent the same rules every session, or CLAUDE.md has grown unwieldy. |
| [`aso-research`](skills/aso-research) | ASO and market research for Google Play / App Store with free open data: autocomplete keyword ideas, competitor listings, metadata limit checks, keyword frequency, and honest MEASURED / ESTIMATE / UNKNOWN labels where paid tools (Sensor Tower, AppFigures) would be needed. | You want store-listing and competitor research without paid ASO tools. |
| [`store-screenshots`](skills/store-screenshots) | Headline-led App Store / Google Play screenshot sets like top-chart apps: message map, set style, Codex prompts with the real screens attached, text-and-truth check, exact store sizes. | You need store listing screenshots that convert. |
| [`app-design-studio`](skills/app-design-studio) | Turns an app name into a full portrait, high-fidelity mobile screen set (splash to settings, states, dialogs, components) with no device frame, and audits it with measurable usability gates. | You need a complete mobile UI design repository, not one mockup. |

## Install
**Claude Code (plugin marketplace)**
```
/plugin marketplace add zohaibmushwani/agent-skills
/plugin install agent-skills@agent-skills
```
**Manual:** copy a folder from `skills/` into `~/.claude/skills/` (all projects) or `<project>/.claude/skills/`.

## Requirements
- Python 3.9+ (scripts use the standard library only, except the Node probe in `aso-research`; `screenshot-to-compose` scripts need Pillow: `pip install pillow`).
- `oss-first-development`: [GitHub CLI](https://cli.github.com) logged in (`gh auth login`) for repo probing and topic sweeps; a web search tool for dorks.
- `app-design-studio`: Node 18+ and Playwright with Chromium for `render_screens.mjs` (HTML-render route); an image model is optional.

## Try it
- `oss-first-development`: ask "I want to build an SVG editor for Android. Research existing projects first." You should get a research doc with verified repos, license verdicts and a decision table, and no code.
- `app-design-studio`: `python skills/app-design-studio/scripts/run_gates.py skills/app-design-studio/assets/example` runs the contrast, token, touch-target and state-coverage gates on the bundled example. Contrast, token and element gates pass; the state-coverage gate reports FAIL on purpose, because the example is a small partial set (2 screens) so you can see what a missing state looks like.

- `android-compose-quality-gate`: `python skills/android-compose-quality-gate/tests/run_tests.py` checks that both audit scripts flag the known defects in the fixtures; then run `compose_lint.py` on your `src` folder.
- `aso-research`: `python skills/aso-research/tests/run_tests.py`; for live Google Play data `npm i google-play-scraper` then `node skills/aso-research/scripts/gplay_probe.mjs suggest "pdf read"` (smoke-tested: search, autocomplete and app details returned real data).
- `guidelines-log`: `python skills/guidelines-log/tests/run_tests.py`, then `python skills/guidelines-log/scripts/rules_audit.py .` on your repo.

## What these skills will not do
- Bypass bot protection or login walls (Cloudflare, search-engine checkpoints). They ask you to open the page instead.
- Copy GPL/AGPL/unlicensed code into a closed-source plan. Those repos are marked study-only.
- Put your name, email or project details into search queries.
- Start building inside the research skill. It stops at a plan and your decisions.
- Crop artwork out of your design screenshots, or claim a screen matches before it was rendered and compared.

## Evidence and limits (v0.1.0)
- Each skill ships 2-3 eval cases (`evals/`). Early runs, one run per case: with the skill the research cases passed more assertions than without it, at roughly +50 s and +6k tokens. That is a small sample; some assertions mirror the skill's own method.
- The topic sweep found small permissive repos that dorks missed on one topic (audio-reactive 3D dance app); it has been measured on that single topic.
- The three Android skills were distilled from real app builds; their eval cases are written but not yet run against a baseline. `compose_lint.py` and `strings_audit.py` were run on a real project and tuned for false positives (they are heuristics; read each hit).
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
