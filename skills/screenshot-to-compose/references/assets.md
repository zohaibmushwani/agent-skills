# Assets

## Icons: Iconify
1. Decide the icon's meaning and look (outline or filled, stroke weight, rounded or sharp).
2. Search several keywords (Iconify MCP, or `https://api.iconify.design/search?query=<word>&prefix=<set>`) and compare candidates visually.
3. Pick **one family** for the whole app. Safe defaults: Material Symbols Rounded (Apache-2.0), Lucide (ISC), Tabler (MIT). Mix sets only when the family truly lacks an icon.
4. Fetch the SVG (`https://api.iconify.design/<set>/<name>.svg`) and convert it:
   `python scripts/svg_to_vectordrawable.py icon.svg res/drawable/ic_<name>.xml --tint`
   Result: 24 dp, black fill or stroke so it can be tinted at the call site, `autoMirrored` set for directional icons.
5. Record set, name and licence in `ASSET_INVENTORY.md`. Delete fetched icons the finished screen does not use.
Never use Unicode symbols, emoji or icons from mismatched sets. Check the project's `res/drawable` first.

## Artwork (mascots, illustrations, food photos, avatars)
**Never crop from the reference screenshots.** Try, in order: the project's image-generation tool (an image MCP, or the agent's built-in generator), then a cheap batch service as fallback.
- Generate 2-3 candidates at the slot's aspect ratio (for a 112 x 76 dp photo, 1216 x 832).
- Review each: matches the brief and palette, anatomy and artifacts, **no text in the image**, subject centred if it will be cropped to a circle, not blank/black.
- At most 3 attempts per asset; each retry changes the prompt where the last one failed.
- Transparent background for cut-out art; avatars cropped to head and shoulders.
- Export WebP at about 4x the slot's dp size (256 px for a 64 dp avatar) into `drawable-nodpi`.
- Record model, prompt, attempt and cost in `ASSET_INVENTORY.md` so it can be regenerated.
- If a generator is rate-limited or unreachable, say so and use a clearly labelled placeholder; do not silently fall back to cropped screenshots, and do not use a paid key the user has not authorised.

## Other sources
Photos: Unsplash/Pexels (check each licence). Lottie: LottieFiles in `res/raw`. Fonts: Google Fonts in `res/font`. Decorative shapes, gradients, rings and charts are drawn in Compose (`Canvas`, `Brush`).
