# Changelog
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
