---
name: screenshot-to-compose
description: Turn app design screenshots (JPG/PNG, often AI-generated) or Figma frames into a native Kotlin Jetpack Compose UI that matches them, design-first. Measures pixels and colours (px to dp), writes screen/asset inventories and a design system with observed vs inferred values, builds Iconify icons into VectorDrawables, generates artwork instead of cropping the screenshots, implements MVI screens, then compares emulator or Roborazzi renders against the reference. Use whenever the user supplies screenshots, mockups or a design repository and wants them built as an Android Compose app, says "make this screen in Compose", "match the design", "px to dp", "screenshot to code", or wants a whole app UI built design-first, even if they never say "Compose".
---

# screenshot-to-compose

Reproduce a design faithfully in Compose without eyeballing it. The reference image is the acceptance test, so every number you use is either **observed** (measured on the image) or **inferred** (a guess you state), and the finished screen is compared with the reference at the end.

## When the design is the input
- Screenshots/mockups only: follow all phases below.
- Figma frames available: skip measuring (read values from Figma) and keep the rest.
- No design yet: use the `app-design-studio` skill first, then come back here.

## Workflow
Work in files (`docs/design/`), one screen at a time after the shared foundations exist. Do not implement anything until the whole screen inventory is understood.

1. **Inspect.** Read the repo first (architecture, theme, shared components, existing screens). Preserve what works. Note assumptions.
2. **Inventory.** Copy the references unchanged into `docs/design/reference/` (kebab-case names). Write `SCREEN_INVENTORY.md`: each image -> screen + state, links between screens, missing references (a screen linked but not shown), pixel size and aspect ratio. Include every state: loading, empty, error, offline, permission, premium.
3. **Measure.** Run `scripts/measure_image.py shot.png --frame-dp 390 --sample x,y ...` for the px->dp scale and colour samples (`references/measuring.md`). Pixels are not dp: assume a 390 dp frame unless told otherwise, `dp = px / (imageWidthPx / 390)`. Record **observed** and **inferred** values in separate columns.
4. **Design system.** Map measured colours to Material 3 roles, type scale, shapes, spacing in the theme. Screens use only theme tokens (no hex, sizes or radii in screens). Define light and dark; if only light exists, derive dark without changing layout.
5. **Assets** (`references/assets.md`). Icons: one family, fetched from Iconify, converted with `scripts/svg_to_vectordrawable.py`. Artwork: **generate it, never crop it out of the screenshots**. Text, buttons, cards, rings and charts are always Compose, never images. Log source, licence, model and prompt in `ASSET_INVENTORY.md`.
6. **Plan.** Per screen decide up front: back behaviour, network/offline class, permissions, scroll-or-fit on small phones, motion. Write `SCREEN_IMPLEMENTATION_PLAN.md` with build order. (Quality rules for these live in the `android-compose-quality-gate` skill.)
7. **Implement** shared foundations first, then screens: stateless composables over an immutable UI state, ViewModel with intents, one composable per file, string resources for all text. Parallelise only independent modules with disjoint files. Read `references/compose-lessons.md` before building cards, tiles or tight text.
8. **Compare** (`references/verification.md`). Render the screen (emulator screenshot or Roborazzi), put it beside the reference at equal width with `scripts/compare_side_by_side.py`, list differences in layout, spacing, type, colour, shapes and assets, fix, repeat. Then check small devices (360 x 526 dp), long text/German, RTL, dark, font scale 1.3. Never trade function or responsiveness for pixel match.
9. **Deliver.** Keep references, assets with prompts, icon sources/licences, inventories and comparison notes current. A screen is done only when it works **and** passes the visual comparison. Commit per topic.

## Rules that stop the usual failures
- Never crop images out of reference screenshots (low-res, compressed, UI baked in).
- Never replace native UI with a picture of it.
- Never invent a design when the reference is ambiguous: make the most reasonable inference, write it in the inferred column, stay close to the reference.
- Do not claim a screen is done before it ran and was compared.
- No secrets (API keys) in the repo or docs; image-service keys come from the environment.

## Files
- `references/measuring.md` - px to dp, colour sampling, observed vs inferred tables.
- `references/assets.md` - Iconify to VectorDrawable, image generation order and review, export sizes, other sources.
- `references/compose-lessons.md` - defects that cost real time: sibling card ratios, intrinsic measurement crash, width thresholds, auto-sizing text.
- `references/verification.md` - emulator vs Roborazzi comparison loop and the device matrix.
- `scripts/measure_image.py`, `scripts/svg_to_vectordrawable.py`, `scripts/compare_side_by_side.py` (Python 3 + Pillow).
