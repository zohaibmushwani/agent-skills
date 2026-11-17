---
name: app-design-studio
description: Turn an app name or idea into a complete, portrait, high-fidelity mobile UI design repository - every screen (splash, language, onboarding, auth, home, feature screens, details, settings), every state (loading, empty, error, offline, permission), dialogs, bottom sheets, components and interactions - with a locked design system and measurable usability gates. Use whenever the user gives an app name/idea and wants screens, UI design, a design repo, mockups, a screen inventory, or a design to hand to developers/designers, even if they never say "skill" or "Figma". Also use to audit or fix an existing set of generated app screens for usability (contrast, touch targets, states) while keeping them beautiful.
---

# app-design-studio

Goal: from one app name, produce a design repository that is **beautiful and usable at the same time**, consistent across every screen, and ready to hand to a designer, to an agent building Compose/Flutter/React Native, or to the Compose-to-Figma bridge.

Why this skill exists: image models draw attractive single screens but drift between screens, forget states, and quietly break usability (tiny text, low contrast, small tap targets). Fix: lock a design system first, generate from it, then check what can be measured with scripts and what cannot (taste) with a rubric plus a human pick.

## Output rules (always)
- Portrait mobile screens only. **No device frame, no phone mockup, no extra background, no canvas around the screen** - the image is the UI itself, edge to edge. (Frames are added later only if the user asks for presentation boards.)
- High fidelity: real copy, real icons, real imagery. No lorem ipsum, no placeholder brand names.
- One design system across the whole set. Never invent a new style per screen.
- State before layout: in every prompt write the facts first (exact strings, counts, selected tab, numbers that must agree), then the layout, then explicit negatives. Models fail on consistency far more than on beauty.
- Edit, don't reroll: fix one wrong string with an edit pass naming only that change; a full reroll throws away everything already approved.
- No real brands, logos or real people's faces; fictional names and generic marks only. Never write API keys into the repo.
- Reply to the user in the language they write in (often Roman Urdu/Hinglish); files and prompts stay English.

## Workflow (S0-S9)
Work in the user's project folder under `design/<app-slug>/` (layout: `references/repo-layout.md`). Track phase status in `design/<app-slug>/STATUS.md`. Ask the user only when the answer changes the result (max 3 questions at S0); otherwise choose a sensible default and say so.

**S0 Intake.** App name, one-line purpose, audience, platform (default: Android + iOS neutral, Material 3 leaning), tone words, light/dark (default: light + dark tokens, screens in light). Write `BRIEF.md` (problem, audience, scope, non-goals); if the user is unavailable, state the reading you took at the top instead of waiting. Read `references/aesthetic-vs-usability.md` once.

**S1 Screen inventory.** Build `inventory.json` from `references/screen-taxonomy.md`: fixed core (splash, language, onboarding, permissions, auth, home, settings) + feature screens specific to this app + details + states + dialogs + sheets + components. Each item has id, group, purpose, states, priority. Show the user a compact list; confirm before spending image credits.

**S2 Design bible + 3 directions (human gate).** Write the bible (`references/design-bible-template.md`) as three short alternatives (different mood, palette logic, type, shape language). Render one hero screen per direction. **Stop and let the user pick** - taste is the one thing scripts cannot judge, so this is where the human decides. Record the choice in `DESIGN.md`.

**S3 Tokens.** From the chosen direction write `tokens.json` (colors light/dark, type scale, spacing 4/8 grid, radius, elevation, icon size, touch target). Run `scripts/contrast_check.py tokens.json` and fix failing pairs now - cheaper than fixing 40 screens later.

**S4 Component board.** Generate the component sheet (buttons, inputs, chips, cards, list rows, nav, top bar, toasts, dialogs, sheets) from the tokens. This image is the visual reference passed to every later generation, which is what keeps screens consistent.

**S5 Screens.** Generate screens in inventory order using `references/prompt-templates/`. Every prompt starts with the locked bible block, then exact strings and counts, then an explicit "do not add" list. Pick the engine by job: a text-capable model (gpt-image/Codex, Nano Banana, Stitch) for whole screens, or the HTML-render route (exact text and counts, then screenshot; tested end to end on a 21-screen PDF reader set: write `html/<group>/<id>.html` from `tokens.json` CSS variables and Iconify icons, then `node scripts/render_screens.mjs <design-dir>` writes the PNG plus a *measured* `<id>.spec.json` from the real DOM, and `run_gates.py` audits it; needs Node + playwright, env `PLAYWRIGHT_MODULE`/`CHROME_PATH` if not installed locally) - FLUX/Runware garbles UI text and counts, so use it only for art that sits inside a screen. Use Iconify MCP for icons so the icon style stays one family. Pass the component board as the style reference when the tool supports it. Save as `screens/<group>/<id>.png` plus `<id>.spec.json` (elements with size, font size, colors, interactive flag - schema in `references/repo-layout.md`).

**S6 States, dialogs, sheets.** Same prompts, same bible. Empty states guide the next action; error is visually different from empty; loading uses skeletons that match the real layout.

**S7 Gates and regenerate.** Run `python scripts/run_gates.py design/<app-slug>`. It runs contrast, token lint, element audit (touch targets, min text size), and state coverage, and writes `reports/gates.md`. Then score each screen with the rubric in `references/aesthetic-vs-usability.md` (open the PNG and look - do not score from memory). Regenerate failing screens, max 2 attempts each; if still failing, flag it for the user rather than looping.

**S8 Export.** Assemble the repo (`references/repo-layout.md`): PNGs, specs, tokens, DESIGN.md, inventory, flow map, `copy/strings.json`, reports. Optional extras, only when the user wants them: (a) HTML truth layer for exact CSS values (`references/image-qa-loop.md`), (b) store assets - icon, feature graphic, store screenshots with headlines rendered as HTML text, validated by `scripts/validate_assets.py` against `references/store-asset-specs.md`. Optional handoff: tokens/specs feed the Compose code + Figma bridge; say so in `HANDOFF.md`.

**S9 Human review.** Present the contact sheet and the gate report. Anything generated before the real app exists is labelled `concept` (never present concept store graphics as real captures).

## Judgement guide (aesthetic vs usability)
Treat usability as a floor and aesthetics as the ceiling. Floor numbers are non-negotiable because they are measurable: touch targets >= 48dp (44pt iOS), body text >= 16sp and nothing under 12sp, contrast 4.5:1 (3:1 large text and icons), one primary action per screen, key actions in the lower thumb zone, 4/8 spacing grid. Above the floor, spend personality: a distinctive type pairing, a controlled accent, one memorable illustration or image moment per flow, generous spacing. When they conflict (e.g. a pale-grey elegant label), usability wins and you recover the elegance elsewhere (weight, spacing, size contrast), not by lowering the floor.

## Avoid ("AI tells")
Read `references/ai-tells-avoid.md` before writing the first prompt. The short version: purple-blue gradients, glass cards for no reason, box-in-box nesting, fake chart spam, twelve-widget homes, generic icon-pack mixes, tiny decorative labels, lorem ipsum, cloned screens with small edits.

## Reference map
- `references/screen-taxonomy.md` - what screens/states/dialogs/sheets exist and when.
- `references/aesthetic-vs-usability.md` - dials, floors, rubric, regenerate rules.
- `references/design-bible-template.md` - the block repeated in every prompt.
- `references/prompt-templates/` - per screen type prompts.
- `references/ai-tells-avoid.md` - anti-patterns.
- `references/repo-layout.md` - folder layout and JSON schemas.
- `references/image-qa-loop.md` - the per-image verify/edit loop, optional HTML truth layer, strings.json.
- `references/store-asset-specs.md` - Play/App Store sizes and rules (re-check official pages before submitting).
- `assets/` - example `tokens.json`, `inventory.json`, `spec.json`, `DESIGN.md` skeleton.
- `scripts/` - deterministic gates (Python 3 stdlib only): contrast_check, token_lint, spec_audit, state_coverage, validate_assets, run_gates.
