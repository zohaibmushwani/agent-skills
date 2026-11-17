---
name: android-compose-quality-gate
description: Production-quality rules and an acceptance checklist for Android Jetpack Compose apps, plus two audit scripts. Covers MVI structure, RTL and localisation (translations, placeholders, plurals), text fit and the device matrix (360 x 526 dp, German, font scale), back press, runtime permissions, network requests (no accidental repeats, cache first, offline dialogs vs toasts), motion and performance, accessibility, previews and code cleanliness. Use whenever you build, review or finish a Compose screen or feature, before calling an Android UI task done, when asked to "review this screen", "check RTL", "audit strings/translations", "production ready", "why does it crash on small phones", or when planning a new app's per-screen behaviour, even if the user does not name these rules.
---

# android-compose-quality-gate

A screen that looks right but breaks offline, in Arabic, on a 360 dp phone or after rotation is not finished. This skill is the checklist and the scripts that catch those defects before the user does.

## Use it in three moments
1. **Planning a screen:** decide the five things in `references/per-screen-decisions.md` (back, network class, permissions, scroll-or-fit, motion) *before* building it.
2. **Building:** follow the rules in `references/` for the area you touch (read only that file).
3. **Finishing:** run the scripts, then walk the acceptance checklist below and report each item as pass / fail / not checked. Do not say "done" on a build that was not run.

## Scripts (Python 3, standard library)
- `scripts/compose_lint.py <src-dir>` - heuristic scan of Kotlin sources: hex colours/`Color(0x..)` outside the theme, `Modifier.offset`, `IntrinsicSize.Min`, `Alignment/Arrangement` left/right words and `paddingLeft/Right`, `android.util.Log`, `Text(` without `maxLines` in a bounded component, UI files without `@Preview`, `GlobalScope`, `!!`, swallowed `CancellationException`. Prints `file:line rule message`; exit 1 on errors. It is a smell detector, not a compiler: read each hit.
- `scripts/strings_audit.py <res-dir>` - compares every `values-<locale>/strings.xml` with the default: missing and extra keys, changed placeholders (`%1$s`, `%d`), missing plural quantities for Arabic (zero, one, two, few, many, other), unescaped apostrophes, untranslated copies, and RTL locales that still contain Latin-only values. Exit 1 on errors.

## Acceptance checklist (report each item)
1. Compared with the design/reference: spacing, alignment, type, colour.
2. Navigation: back behaviour (`references/back-permissions.md`), recreation, no duplicate destinations.
3. LTR **and** RTL checked on rows *and* cards (`references/rtl-localisation.md`); `strings_audit.py` clean.
4. Small and standard devices, font scale 1.3, German text; no clipped or word-broken text (`references/text-fit-devices.md`).
5. Sibling cards keep their aspect ratio; no `IntrinsicSize.Min` over subcomposing children.
6. State handled: loading, empty, error, offline, content; input survives rotation and process death.
7. Network: no repeated request on rotation/recomposition/double tap; every outcome handled; technical cause logged, general message shown (`references/network-offline.md`).
8. Permissions asked before the screen opens; denied and permanently-denied states exist.
9. Motion minimal, tokens not literals, respects "animations off" (`references/motion-performance.md`).
10. Accessibility: 48 dp targets, content descriptions, contrast in both themes.
11. Code: stateless composables over an immutable state, one composable per file, previews with key states, no dead code or stray files (`references/architecture-mvi.md`).
12. `compose_lint.py` reviewed; build and unit tests run and their result stated.

## Rules for using the rules
- A rule is a default. If the design or the user requires the opposite, follow them and record the deviation.
- Verify by running, not by reading: say which items you checked on a device/emulator/Roborazzi render and which only by reading code.
- When the user gives a new standing rule, record it (see the `guidelines-log` skill).

## Files
`references/`: `per-screen-decisions.md`, `architecture-mvi.md`, `rtl-localisation.md`, `text-fit-devices.md`, `back-permissions.md`, `network-offline.md`, `motion-performance.md`.
