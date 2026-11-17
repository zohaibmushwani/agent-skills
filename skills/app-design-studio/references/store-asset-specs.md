# Store asset specs (verified from official help pages and secondary guides, 2026)

Always re-check the official page before submitting — sizes change with new devices.
Official: Google Play preview assets https://support.google.com/googleplay/android-developer/answer/1078870 · Apple https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications

## Google Play

| Asset | Requirement |
|---|---|
| App icon | 512 × 512 px, 32-bit PNG **with alpha**, ≤ 1024 KB. Upload a full-bleed square; Google applies the mask, so do not bake corners or shadows |
| Feature graphic | 1024 × 500 px, JPEG or 24-bit PNG **without alpha** |
| Phone screenshots | JPEG or 24-bit PNG **without alpha**; each side 320–3840 px; longest side ≤ 2× shortest; 2–8 per device type |
| 7" / 10" tablet, Chromebook | same file rules; up to 8 each; optional but improves tablet presence |
| Promo video | YouTube link (optional); plays from the feature graphic, so keep its focal point clear of the play button |

Practical export sizes: phone 1080 × 1920; tablet 1200 × 1920 / 1600 × 2560; feature graphic 1024 × 500.

## Apple App Store

| Asset | Requirement |
|---|---|
| iPhone | 6.9" set is the base: 1320 × 2868, 1290 × 2796 or 1260 × 2736 (portrait; landscape swapped). 6.5" set (1284 × 2778 / 1242 × 2688) is an accepted alternative. Apple scales to smaller devices |
| iPad (if supported) | 13": 2064 × 2752 or 2048 × 2732 (portrait; landscape swapped) |
| Count | 1–10 per device class; JPEG/PNG, no alpha; do not mix orientations inside a family |
| App icon | 1024 × 1024 PNG, no alpha, no pre-rounded corners (taken from the app bundle) |
| Preview video | resolution must match the screenshot resolution for that device |

## Web / PWA / social (if asked)

| Asset | Size |
|---|---|
| favicon | 16, 32, 48 px + ICO; plus SVG |
| PWA icons | 192, 512, maskable 512 |
| Open Graph image | 1200 × 630 |

## Validator rules to implement in `tools/validate-assets`

- exact dimension match per slot (list above in `store/specs.json`)
- alpha present/absent per slot (icon has alpha on Play; screenshots and feature graphic must not)
- file size caps (icon ≤ 1024 KB)
- per-locale folders complete (`store/<platform>/<device>/<locale>/NN.png`)
- every file listed in `store/manifest.json` with `status: concept | final` and `source: generated | captured`

## Content rules to respect

- Store screenshots must represent the real app. Pre-launch graphics are `status: concept`; before publishing, replace UI areas with real captures (`source: captured`).
- No misleading badges, ranks, awards, or price claims in images; keep text in the image short and legible at thumbnail size.
- Keep the first 2–3 screenshots self-sufficient: they carry the listing for most visitors.
