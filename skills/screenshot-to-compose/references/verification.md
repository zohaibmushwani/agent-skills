# Visual verification

The original screenshot is the acceptance reference. For each screen: implement, render, compare, list differences, fix, repeat.

## Render
- Emulator: screenshot via an adb tool or `adb exec-out screencap -p > shot.png`. Use the same tools for rotation, offline, slow-network and permission scenarios.
- No emulator: **Roborazzi**. One `<Screen>ScreenshotTest` per screen renders the stateless `<Screen>Content` from preview data at: 390 x 844 light (the reference frame), dark (`w390dp-h844dp-night-xxhdpi`), 360 x 640, a long-text locale (German) at 360 x 800, and RTL (Arabic) at 390 x 844. Record with `./gradlew :app:recordRoborazziDebug --tests "*<Screen>ScreenshotTest*"`. It also catches layout crashes.

## Compare
`python scripts/compare_side_by_side.py reference.png render.png out.png` scales the reference to the render's width and places both at equal height (add `--overlay` for a 50% blend). List the differences in layout, spacing, type, colour, shapes and assets; fix; render again; then check the small-device and translation images.

Record deviations you accept (font family, icon fill) in `SCREEN_INVENTORY.md`.

## Device matrix
360 x 526, 360 x 640, 360 x 800, 393 x 852, 402 x 874, 411 x 891 dp; font scale 1.0 and 1.3; long text; German and RTL; light and dark; scrolling, keyboard, system bars, insets. Add 600 dp+ for tablets/foldables.
