---
name: app-design-studio
description: Turn an app name or a website / web-app idea into a complete high-fidelity UI design repository - pages or screens, every state (loading, empty, error, offline), dialogs, sheets, components, interactions - with a locked design system and measurable usability gates. Three targets, each with its own profile and wording - mobile app (portrait screens: splash, onboarding, auth, home, settings), website (landscape desktop pages plus a narrow responsive layout), web app / portal / dashboard. Use whenever the user gives an app name or idea and wants screens, pages, UI design, a design repo, mockups, a screen inventory, or a design to hand to developers/designers, even if they never say "skill" or "Figma". Also use to audit or fix an existing set of generated screens for usability (contrast, targets, states) while keeping them beautiful.
---

# app-design-studio

Goal: from one app name, produce a design repository that is **beautiful and usable at the same time**, consistent across every screen, and ready to hand to a designer, to an agent building Compose/Flutter/React Native, or to the Compose-to-Figma bridge.

Why this skill exists: image models draw attractive single screens but drift between screens, forget states, and quietly break usability (tiny text, low contrast, small tap targets). Fix: lock a design system first, generate from it, then check what can be measured with scripts and what cannot (taste) with a rubric plus a human pick.

## Target = profile (decide FIRST, at S0; never default silently when the user said website/portal/dashboard)
| Target | Orientation / sizes | Read these (and ONLY these for target wording) |
|---|---|---|
| `mobile` (app) | portrait 9:19.5 screens, one size | `screen-taxonomy.md`, mobile blocks of `design-bible-template.md` and `prompt-templates/README.md`, floors in dp/sp |
| `web` kind `site` (website, landing, store, blog) | **landscape desktop 16:10 (1440x900)** pages, plus a narrow 390px responsive layout of the same page | `web-design.md`, `prompt-templates/web.md`, web block of `design-bible-template.md`, floors in px |
| `web` kind `app` (portal, dashboard, admin, SaaS) | landscape desktop first; narrow layout second. Only if the user says phones are the main device, set `"mobile_first": true` and make the narrow layout primary | same as `site` |
| `both` | one shared bible and tokens, two profiles | both sets, never mixed inside one prompt |
Set `"platform": "mobile" | "web"` in `inventory.json`. A prompt is written with exactly one profile's vocabulary.

**Keyword hygiene (the reason this section exists):** image models obey the words they are given. A website prompt that says "portrait", "phone", "status bar", "9:19.5", "bottom navigation", "thumb zone", "Android/iOS" or "app screen" comes back as a phone screen. Web prompts say "website page", "landscape desktop 16:10, 1440 wide", "header with links", "sidebar", "browser-less". The narrow layout is called "narrow responsive layout, 390px wide", never "phone screen". `python scripts/prompt_lint.py <design-dir>` fails any prompt in `prompts/` that uses another profile's words; run it before sending a batch.

## Output rules (always)
- The image is the UI itself, edge to edge: **no device frame, no phone/laptop mockup, no browser chrome, no extra background, no canvas around it.** (Presentation frames only if the user asks for boards.) Mobile: portrait screens. Web: landscape desktop pages and, where listed, the narrow layout; long pages as a tall single image or 2-3 section images of the same width.
- High fidelity: real copy, real icons, real imagery. No lorem ipsum, no placeholder brand names.
- One design system across the whole set. Never invent a new style per screen.
- Two prompt modes (`references/design-craft.md`): **brief** (short intent + the few facts that matter + the feel; default for first renders and S2 directions, gives the most distinctive result) and **locked** (exact strings, counts, bible block; for siblings after the pick and for fixes). Render brief first, look, then lock what must agree. Models fail on consistency far more than on beauty, but over-constraining the first render makes it mechanical.
- Edit, don't reroll: fix one wrong string with an edit pass naming only that change; a full reroll throws away everything already approved.
- No real brands, logos or real people's faces; fictional names and generic marks only. Never write API keys into the repo.
- Reply to the user in the language they write in (often Roman Urdu/Hinglish); files and prompts stay English.

## Workflow (S0-S9)
Work in the user's project folder under `design/<app-slug>/` (layout: `references/repo-layout.md`). Track phase status in `design/<app-slug>/STATUS.md`. Ask the user only when the answer changes the result (max 3 questions at S0); otherwise choose a sensible default and say so.

**S0 Intake.** App/site name, one-line purpose, audience, target + kind (table above; ask if the words "website", "portal", "dashboard" or "landing" appear and the target is unclear), platform feel (mobile default: Android + iOS neutral, Material 3 leaning; web: neutral), tone words, light/dark (default: light + dark tokens, screens in light). Write `BRIEF.md` (problem, audience, scope, non-goals); if the user is unavailable, state the reading you took at the top instead of waiting. Read `references/aesthetic-vs-usability.md` once.

**S1 Screen inventory.** Build `inventory.json` from `references/screen-taxonomy.md` (web: `references/web-design.md` section 4): fixed core (splash, language, onboarding, permissions, auth, home, settings) + feature screens specific to this app + details + states + dialogs + sheets + components. Each item has id, group, purpose, states, priority. Show the user a compact list; confirm before spending image credits.

**S2 Design plan + bible + 3 directions (human gate).** First write a 10-line design plan per direction (`references/design-craft.md` section 2) and self-review it against the generic defaults. Then write the bible (`references/design-bible-template.md`) as three short alternatives (different mood, palette logic, type, shape language). Each bible names the text colour on every filled colour (on-primary, on-accent, badge text) and the platform's status bar (Android: time left, icons right; iOS: 9:41 style). Before rendering, put each direction's palette in a small tokens file and run `scripts/contrast_check.py` on it: a direction that only looks good with failing contrast must not reach the human pick. Write each prompt to `prompts/<id>.<direction>.md` first and send exactly that file's text (the saved prompt is the reproducible one). Render one hero screen per direction (web: the same page, desktop and mobile). Batch all three in one Codex call. **Stop and let the user pick** - taste is the one thing scripts cannot judge, so this is where the human decides. Record the choice in `DESIGN.md`.

**S3 Tokens.** From the chosen direction write `tokens.json` (colors light/dark, type scale, spacing 4/8 grid, radius, elevation, icon size, touch target). Run `scripts/contrast_check.py tokens.json` and fix failing pairs now - cheaper than fixing 40 screens later.

**S4 Component board.** Generate the component sheet (buttons, inputs, chips, cards, list rows, nav, top bar, toasts, dialogs, sheets) from the tokens. This image is the visual reference passed to every later generation, which is what keeps screens consistent.

**S5 Screens.** Generate screens in inventory order using `references/prompt-templates/`. Every prompt starts with the locked bible block, then exact strings and counts, then an explicit "do not add" list. Pick the engine by job: a text-capable model (gpt-image/Codex, Nano Banana, Stitch) for whole screens, or the HTML-render route (exact text and counts, then screenshot; tested end to end on a 21-screen PDF reader set: write `html/<group>/<id>.html` from `tokens.json` CSS variables and Iconify icons, then `node scripts/render_screens.mjs <design-dir>` writes the PNG plus a *measured* `<id>.spec.json` from the real DOM, and `run_gates.py` audits it; needs Node + playwright, env `PLAYWRIGHT_MODULE`/`CHROME_PATH` if not installed locally) - FLUX/Runware garbles UI text and counts, so use it only for art that sits inside a screen. Use Iconify MCP for icons so the icon style stays one family. Pass the component board as the style reference when the tool supports it. Save as `screens/<group>/<id>.png` plus `<id>.spec.json` (elements with size, font size, colors, interactive flag - schema in `references/repo-layout.md`).

**S6 States, dialogs, sheets.** Same prompts, same bible. Empty states guide the next action; error is visually different from empty; loading uses skeletons that match the real layout.

**S7 Gates and regenerate.** Run `python scripts/run_gates.py design/<app-slug>`. It runs contrast, token lint, element audit (touch targets, min text size), and state coverage, and writes `reports/gates.md`. Then score each screen with the rubric in `references/aesthetic-vs-usability.md` (open the PNG and look - do not score from memory). Regenerate failing screens, max 2 attempts each; if still failing, flag it for the user rather than looping.

**S8 Export.** Assemble the repo (`references/repo-layout.md`): PNGs, specs, tokens, DESIGN.md, inventory, flow map, `copy/strings.json`, reports. Optional extras, only when the user wants them: (a) HTML truth layer for exact CSS values (`references/image-qa-loop.md`), (b) store assets - icon, feature graphic, store screenshots with headlines rendered as HTML text, validated by `scripts/validate_assets.py` against `references/store-asset-specs.md`. For marketing store screenshots (headline-led sets like top-chart apps) use the `store-screenshots` skill with these screens as input. Optional handoff: tokens/specs feed the Compose code + Figma bridge; say so in `HANDOFF.md`.

**S9 Human review.** Present the contact sheet and the gate report. Anything generated before the real app exists is labelled `concept` (never present concept store graphics as real captures).

## Judgement guide (aesthetic vs usability)
Floors depend on target: mobile = dp/sp numbers below; web = px floors in `references/web-design.md` section 3 (44px hit area, body >= 16px, 65ch lines, no horizontal scroll at 390). Treat usability as a floor and aesthetics as the ceiling. Floor numbers are non-negotiable because they are measurable: touch targets >= 48dp (44pt iOS), body text >= 16sp and nothing under 12sp, contrast 4.5:1 (3:1 large text and icons), one primary action per screen, key actions in the lower thumb zone, 4/8 spacing grid. Above the floor, spend personality: a distinctive type pairing, a controlled accent, one memorable illustration or image moment per flow, generous spacing. When they conflict (e.g. a pale-grey elegant label), usability wins and you recover the elegance elsewhere (weight, spacing, size contrast), not by lowering the floor.

## Avoid ("AI tells")
Read `references/design-craft.md` and `references/ai-tells-avoid.md` before writing the first prompt. The short version: purple-blue gradients, glass cards for no reason, box-in-box nesting, fake chart spam, twelve-widget homes, generic icon-pack mixes, tiny decorative labels, lorem ipsum, cloned screens with small edits.

## Reference map
- `references/screen-taxonomy.md` - what screens/states/dialogs/sheets exist and when (MOBILE target only).
- `references/web-design.md` - website / web-app target: viewports, px floors, page taxonomy, layout, web AI tells.
- `references/prompt-templates/web.md` - web FORMAT/CONTENT blocks and per page-type prompts.
- `references/aesthetic-vs-usability.md` - dials, floors, rubric, regenerate rules.
- `references/design-bible-template.md` - the block repeated in every prompt.
- `references/prompt-templates/` - per screen type prompts.
- `references/design-craft.md` - brief vs locked prompts, design plan, generic defaults, boldness in one place, copy rules, critique loop.
- `references/ai-tells-avoid.md` - anti-patterns.
- `references/repo-layout.md` - folder layout and JSON schemas.
- `references/image-qa-loop.md` - the per-image verify/edit loop, optional HTML truth layer, strings.json.
- `references/store-asset-specs.md` - Play/App Store sizes and rules (re-check official pages before submitting).
- `assets/` - example `tokens.json`, `inventory.json`, `spec.json`, `DESIGN.md` skeleton.
- `scripts/` - deterministic gates (Python 3 stdlib only): contrast_check, token_lint, spec_audit, state_coverage, validate_assets, run_gates.
