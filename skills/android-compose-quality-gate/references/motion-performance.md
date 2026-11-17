# Motion and performance

## Motion plan (once per app, per component type)
- Screen transitions: one app-wide spec (fade + slight horizontal slide, mirrored in RTL, ~250 ms); tab switches crossfade.
- Dialogs/sheets: Material defaults. Buttons/cards: press scale; a button shows loading in place without changing size.
- Content states (loading/content/empty/error): `Crossfade` ~200 ms; new list items `animateItem()`. Counters, progress and rings animate to their value once when shown.
- Lottie only where the design asks, paused when not visible.
- Performance: animate `graphicsLayer` properties (alpha, translation, scale), not size/padding (re-runs layout); no infinite animation off-screen; nothing re-animates because of recomposition; durations and easings are theme tokens.
- Respect the system: when animations are off (animator scale 0) jump to the end state; never convey anything by motion alone.

## Production quality
- Feedback within 100 ms (ripple/press scale); work > ~300 ms shows progress; a shown loader stays ~400 ms to avoid flicker.
- Stable Compose: `@Immutable` state with immutable collections; no heavy work/formatting/sorting in composition (ViewModel or keyed `remember`); stable lambdas into lists; read scroll/animation values via `graphicsLayer` or `derivedStateOf`.
- Images: Coil at display size with placeholder and error drawable; no full-size bitmaps.
- Startup: nothing blocking on main in `Application`/splash/`init`; SDK init lazy or background; baseline profile for release.
- Survive everything: rotation, theme switch, locale switch, process death (input and current step restored), backgrounded mid-request. Test with "Don't keep activities".
- Accessibility: touch targets >= 48 dp; `contentDescription` on acting icons (null on decorative); WCAG contrast in both themes; TalkBack order = visual order; usable at font scale 2.0 (may scroll).
- Edge-to-edge: insets handled once by the scaffold; nothing hides under bars or keyboard.
- Input: right keyboard type and IME action; Next moves focus, Done submits; inline validation after the first edit.
- Security/privacy: HTTPS only, no secrets in repo or logs, no personal data in analytics.
- Release QA: the offline scenarios, the device matrix, light/dark, German/Arabic, first vs returning launch, free vs premium.
