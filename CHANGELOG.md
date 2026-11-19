# Changelog
## 0.8.1
- app-design-studio: generic lessons on zoomed-in desktop renders (proportional SCALE paragraph, no oversized style reference), layout edits that re-crop (regenerate instead), critique template gains an "Avoid next time" line fed into the next prompt, new `zoomed-in` log tag.

## 0.8.0
- app-design-studio: `references/interaction-and-density.md` (word/density budget, one idea per panel, progressive disclosure, visible interaction state, review questions; distilled from public UX rule lists incl. MIT-licensed UI UX Pro Max, with a warning not to take keyword-matched style/pattern picks from such databases). Critique template now fails text-heavy or crowded screens. New generic lessons: density target in the brief, explicit state words, vendor logos.

## 0.7.0
- app-design-studio: lessons generalised. design-craft "Learned lessons" rewritten at the level of model behaviour and prompt technique (no product names, palettes, layouts or project evidence); bias guard added (examples are illustrations, never content); web prompt examples turned into placeholders; project-specific evidence stays in each project's prompt log.

## 0.6.3
- app-design-studio: design-craft adds the brief skeleton that produced a first-attempt accept (signature interaction + marker mapping + exact chrome + single primary).

## 0.6.2
- app-design-studio: critique no longer fails on placeholder values (user correction); new lessons (shared chrome drift, edit side effects, pin mapping); prompt_lint false positives fixed ("phone 1080x2400" as content, "thumbnails").

## 0.6.1
- app-design-studio: self-critique loop (`references/critique-template.md`): every render is critiqued for usability (pass/fail with evidence) and aesthetics (rubric), then fixed by edit pass or rejected and regenerated automatically, with reasons logged. Lessons added from the portal run: wrong interaction model (form instead of canvas), pin/number mapping, edit side effects, distinctiveness.

## 0.6.0
- app-design-studio: prompt-log system. `scripts/prompt_log.py add|summary` records every accept/fix/reject with prompt, mode, tags and reason, and summarises accept rate per prompt mode and recurring failure tags (a tag rejected twice is promoted into `references/design-craft.md` "Learned lessons", seeded with 9 lessons from a real portal run). SKILL.md S7 now requires a verdict + log entry for every generated image.

## 0.5.2
- app-design-studio: new `references/design-craft.md` (brief vs locked prompt modes, 10-line design plan with self-review, calibrated generic-defaults list, boldness in one place, copy rules, critique loop; ideas from Anthropic's frontend-design skill, written in our own words). Verified by an A/B run: a 130-word brief gave a richer screen than a 450-word locked prompt; landscape desktop web prompts now come out landscape.
- prompt_lint no longer flags a product domain like "Android app studio"; Codex notes: always `codex exec ... < /dev/null`, no aspect in the wrapper, put `-i` after the prompt.

## 0.5.1
- app-design-studio: target = profile. Mobile wording (portrait, phone, status bar, 9:19.5, bottom nav, dp/sp) moved out of shared rules into mobile-only blocks; website default is landscape desktop 16:10 with a narrow 390px responsive layout (`mobile_first` flag for mobile-first work tools). New keyword-hygiene rule and `scripts/prompt_lint.py` (wired into run_gates) fail prompts that use another target's vocabulary.

## 0.5.0
- app-design-studio: website and web-app target (desktop 1440 + mobile 390 pages, px floors, web page taxonomy, web prompt templates, Codex PNG route by default); spec_audit/state_coverage understand `platform: web` and per-view files; render_screens.mjs gains optional `--viewports` and `--full-page`.

## 0.4.0
- Added store-screenshots (Codex-rendered, real UI as reference, build_prompts.py, fit_store.py, check_set.py).
- app-design-studio: contrast check and on-colour text before S2, platform status bar, save-then-send prompts, Codex image-quota preflight.

## 0.3.0
- Added aso-research: free-data ASO workflow (google-play-scraper probe, metadata checker, keyword frequency), tools review, store limits, honest data labels.

## 0.2.3
- guidelines-log: Setup also adds the two instruction lines when the log exists but CLAUDE.md/AGENTS.md lacks them.

## 0.2.2
- guidelines-log: restored the original log + fold-into-GUIDELINES flow as the default; routing, size and audit are optional extras.

## 0.2.1
- guidelines-log rewritten after researching existing self-improvement/memory skills and the Claude Code memory docs: routing to the right layer, size and contradiction checks, confirmed approaches, `rules_audit.py` (+ self-test), `references/research.md`.

## 0.2.0
- Added screenshot-to-compose (measure/convert/compare scripts), android-compose-quality-gate (compose_lint.py, strings_audit.py + self-test) and guidelines-log.

## 0.1.0
- oss-first-development: dork + identifier-chain research workflow, long-tail topic sweep, user-seed intake, license gate, repo verification scripts, 3 eval cases.
- app-design-studio: screen taxonomy, design-bible template, HTML-render route, measurable gates (contrast, token lint, 48dp touch targets, state coverage), 3 eval cases.
