# Prompt templates

Website or web-app target: use `web.md` in this folder for the FORMAT block and page templates; the block order below stays.

Every image prompt has the same 6 blocks in this order. Order matters: the model weights the start most, and the bible must not be diluted.

```
1. FORMAT      Portrait mobile app screen, 9:19.5. Show ONLY the app UI, full-bleed. No phone frame, no device mockup, no outer background, no shadow around the screen.
2. BIBLE       <paste DESIGN BIBLE block>
3. SCREEN      <id> - <title>. Purpose: <one sentence>. State: <default|loading|empty|error|...>.
4. CONTENT     Exact text and structure, top to bottom (see below). Exact counts.
5. CONSISTENCY "Same app as the attached component board / previous screen: identical top bar, bottom navigation, button style, icon family."
6. DO NOT ADD  <extra elements, other tabs, extra cards, ads, fake brand names, lorem ipsum, device frame>
```

## CONTENT block pattern
```
Status bar: 9:41, full battery, signal, wifi.
Top bar: back arrow left, title "Library" centered, search icon right.
Section: "Recent" (heading 20sp semibold). 3 horizontal cards: "Annual Report 2025.pdf" 2.4 MB, "Invoice 0412.pdf" 310 KB, "Lease Agreement.pdf" 1.1 MB.
List: exactly 4 rows (title, subtitle, trailing more-icon).
Bottom navigation: exactly 4 tabs - Home (selected), Library, Tools, Settings.
Primary action: one filled button "Open file" bottom, 56dp tall, 20dp margins.
```
Rules: quote every visible string; give counts ("exactly 4"); name the selected tab; keep strings short; use realistic data. For image moments describe subject, style (from bible) and where the scrim goes.

## Per screen type
- **Splash:** logo mark centered, app name, optional tagline <= 5 words, nothing else. Brand colour background from bible.
- **Language:** title, search field optional, list of 6-8 languages in native script with radio, current preselected, bottom "Continue".
- **Onboarding:** one illustration, headline (<= 6 words), one-sentence body, page dots (exact count), "Skip" top-right, "Next"/"Get started" bottom. Slides share layout, vary illustration and accent usage.
- **Home:** greeting or context line, one hero module, one list/grid, bottom nav. State the single primary action.
- **List/detail:** top bar with back, content hierarchy, sticky primary CTA when action-driven.
- **Settings:** grouped sections with section headers, rows with leading icon, trailing chevron/switch/value, exactly N rows per group.
- **Empty:** illustration in bible style, one-line headline, one-line guidance, ONE button.
- **Error:** distinct from empty (different illustration/icon, error colour accent), reason in plain words, "Try again" + secondary.
- **Loading:** skeleton blocks matching the real layout of the default screen; keep top bar and nav real.
- **Dialog:** dimmed scrim over the real screen behind; centered card; title, one-line body, two buttons (secondary left, primary right, or stacked); destructive uses error colour.
- **Bottom sheet:** screen dimmed behind, sheet with drag handle, title, content, safe-area bottom padding.
- **Component board:** white/bg canvas, grid of components grouped with small labels, all states in a row; this is the one image where a labelled board layout is wanted.

## Editing prompt (regenerate)
"Keep everything identical (same text, layout, colours, icons) except: <specific change>. Reason: <floor/rubric failure>." One change set per retry.

## Tool notes
- gpt-image MCP: no size parameter; state "portrait 9:19.5" in the prompt; ~30-90s per image; use background mode for batches; pass the component board as reference when editing is supported.
- Runware (FLUX etc.): **not for whole screens.** Smoke test (2026-11-17, FLUX dev 768x1600, full template prompt): format rule worked (no frame, portrait) but text garbled ("Eecent files", "Crein.dlp:", "Poplc Nuw"), counts wrong (5 nav tabs instead of 4, 6 list rows instead of 4), search field missing, time 3:40 not 9:41, real-looking faces in avatars, soft/blurry. Use Runware only for illustrations, photos, textures and backgrounds that sit *inside* a screen or store graphic, and `remove_background` for cutouts. Whole screens need a text-capable model (GPT Image via gpt-image MCP/Codex, Nano Banana, Stitch) or the HTML-render route (write the screen as HTML with tokens, screenshot it with Playwright, put generated art inside) which gives exact text and counts.
- Iconify MCP: search by concept within ONE icon set id from the bible; record chosen icon names in `assets/icons.json`.
- Always write the prompt to `prompts/<id>.md` **before** sending and send that exact text; never rebuild it afterwards (rebuilt prompts drift from what was sent).
- Codex/gpt-image has a separate image quota (`imagegen_premium`) that `codex_status` does not show. Before a batch, send ONE image and check it succeeded; on "usage limit reached" stop, record the reset time in STATUS.md, and offer the HTML-render route or waiting. Never switch to a paid API key without the user's consent.
- Every filled button/badge in a prompt names its text colour ("dark text #1A1206 on amber"), otherwise models default to white and fail contrast.
