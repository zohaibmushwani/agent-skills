# Research: SVG editor / previewer for Android (Compose), learning from Flutter, React Native, Kotlin, Java, Rust, web
Date 2026-11-17. Same method as before (dorks + identifier chaining + EN/ZH/JA/RU/KR searches + direct reading).
VERIFIED = page read directly. LEAD = search result / third-party summary only.

## 0. Answer in one paragraph
There is **no maintained, complete runtime SVG renderer written for Compose on Android**; the market is split into (a) build-time converters (SVG -> ImageVector), (b) Coil's SVG decoder, (c) a Rust renderer (resvg) already bridged to Kotlin, and (d) editors that exist mostly on web/Flutter/Godot. So the strong plan is: **keep the SVG source text/DOM as the single source of truth (GodSVG idea), render previews with resvg through Rust+NDK (coil-resvg proves the bridge), model editing node-centrically (Flutter `path_editor` idea), export via svg-to-compose**. Everything we need as *ideas* exists; as *code* we can reuse MIT/Apache parts and must only study the AGPL one.

## 1. Rendering engines (previewer)

| Option | Status | License | Strengths | Weaknesses |
|---|---|---|---|---|
| **resvg** (linebender; crates resvg + usvg, renders with tiny-skia) | VERIFIED | **MIT or Apache-2.0** (dual) | static SVG 1.1 + SVG2 in progress; ~1,600-test suite; pixel-identical across platforms; no system libs; parse (usvg) and render separable; has C API; ~4.2k stars | no animation/scripting; SVG Tiny 1.2 unsupported; font loading on mobile "rough edges" (bundle fonts); MSRV Rust 1.85 |
| **coil-resvg** (hash-sequence) | VERIFIED | Apache-2.0 | resvg + tiny-skia via **UniFFI + Gobley** into Kotlin; Android/iOS/JVM; `ResvgDecoder.Factory()` for Coil 3; v1.1.2. Best proof that Rust-on-Android SVG works | decoder only (bitmap), no tree access for editing; ABIs not listed |
| **AndroidSVG** (BigBadaboom) | VERIFIED (README) | Apache-2.0 | "almost complete" static SVG 1.1 / 1.2 Tiny; Java, tiny, used by Coil's old svg module; renders to Canvas/Picture | **no filters**; repo shows no release/activity date; text/CSS/clip/mask support not stated; Habr notes older SVG-Android parsed XML twice |
| Coil `coil-svg` (Coil 3) | LEAD | Apache-2.0 | easiest for display from URL/bytes | engine = AndroidSVG-class limits; display only |
| Skia `SVGDOM` (Skiko) | LEAD (Kotlin Slack) | BSD | works on Desktop/iOS | **not available on Android** per community threads |
| Android `VectorDrawable` / Compose `ImageVector` | LEAD (official docs) | - | native, fast | **subset of SVG** only |
| WebView (Chromium) | known | - | full browser fidelity, animation, CSS, filters | heavy, harder to script/measure; best as a **comparison oracle** |
| flutter_svg + `vector_graphics_compiler` | LEAD | (Flutter, BSD-3 expected, unverified) | compiles SVG to binary at build time; optimizations (opacity peephole, group collapse, clip/mask elimination) | no filters, limited text, no CSS - good *design reference* for a "compile" step |
| react-native-svg | VERIFIED (partial) | MIT | most elements; 8k stars; Fabric | mechanism not documented on page; Android RadialGradient focus point unsupported |
| Qt QtSvg (2GIS case on Habr) | LEAD | LGPL/GPL | used on Android by 2GIS because no cross-platform choice | heavy |

Test oracle: **resvg-test-suite** (linebender/resvg-test-suite, MIT, ~1,600 SVG->PNG tests, support table at linebender.org/resvg-test-suite) and the **W3C SVG 1.1 test suite** (static subset). Use them to score our previewer.

## 2. Editor building blocks

| Piece | Status | License | Take |
|---|---|---|---|
| **GodSVG** (Godot, desktop + web + **Android builds**) | VERIFIED | **MIT** | **Source markup is the canonical data; UI is a live view; no editor metadata in output;** hybrid code + viewport editing; path-command editor with shortcuts; optimization. Proof an SVG editor can ship on Android |
| **Flutter `path_editor`** v1.1.1 | VERIFIED | **Apache-2.0** | data model: path = subpaths = nodes (`position`, in/out handles, type corner/mirrored/aligned/disconnected); `NodeRef/SegmentRef/HandleRef`; normalise to absolute M/L/C; pen + select tools; transactional undo (one gesture = one step); **handles stay constant screen size while path scales**; snapping with guides; separate observable path/selection/tool state |
| **Yqnn/svg-path-editor** (Angular/TS, lib `svg-path-editor-lib`) | VERIFIED | **AGPL-3.0** | feature spec only: add/delete/insert/retype commands, abs<->rel toggle, reverse subpath, transform, optimize, undo/redo, Esc cancels drag. **Do not copy code** unless the app is AGPL |
| react-native-svg-editor | LEAD | ? | RN editor reference |
| ktakiman/svgeditor, eetu/nib, d3-svg-path-editor, WeSP-Editor | LEAD | ? | web path/node editing patterns (smooth vs corner nodes) |
| SVG-Edit (web) | not checked | MIT (expected) | possible WebView-embedded fallback editor - verify |

## 3. Import/export and conversion
- **svg-to-compose** (rafaeltonholo; KMP parser, CLI + Gradle plugin, SVGO/Avocado optimize): VERIFIED, **MIT**, ~223 stars, ~450 commits. Parser is the author's own because Google's `sdk-common` Svg2Vector is incomplete; IR/API not documented on page - read `modules/`.
- DevSrSouza/svg-to-compose (uses Android Svg2Vector), irgaly/compose-vector-plugin, amarland/svg2iv, jzbrooks/**vgo** (converts SVG / AVD / ImageVector), Valkyrie (IDE plugin): LEAD.
- Export targets for our tool: SVG (clean, metadata-free), PNG (resvg), Android VectorDrawable XML, Compose `ImageVector` Kotlin.
- Optimization: SVGO is Node (not on device). On-device options unverified: usvg normalisation, `svgcleaner`/`oxvg` (not researched).

## 4. Findings that shape the design
1. **No runtime renderer for Compose-Android is a gap, not a mistake in the search**: Slack threads, CN/JA/RU searches all converge on "convert at build time or use Coil".
2. **Use resvg as the accurate renderer and keep AndroidSVG only as a light fallback**; resvg is dual MIT/Apache (clean for closed apps) and has the conformance suite.
3. **`usvg::Tree` is a simplified render tree** (resolves CSS, `use`, units), so it loses original structure. For an *editor*, keep our **own source-preserving DOM** (text-first, like GodSVG) and feed the serialised SVG to resvg on every change; do not try to round-trip from usvg.
4. **Editing model = node-centric absolute paths** (path_editor) with operation list from svg-path-editor as spec; elements (rect/circle/etc.) convert to paths only on demand.
5. **Fidelity is measured, not claimed**: run resvg-test-suite through our previewer and compare against resvg CLI output; compare WebView screenshots as a second oracle.
6. **Android specifics:** bundle fonts (resvg mobile font loading is rough), 16 KB page size alignment (NDK r28+), per-ABI size of Rust lib (not measured), `Bitmap` conversion cost for large canvases (tile / limit size).
7. **Compose Canvas editor interactions** to copy: screen-space handles, hit radii by touch (>= 48dp for handles via larger invisible hit area), pinch-zoom/pan viewport transform, long-press = break handle (no modifier keys on touch), snap guides, one-gesture-one-undo-step.

## 5. Recommended architecture (to validate by prototype)
```
Compose UI (Material 3): canvas viewport, toolbar, node inspector, XML/code pane, layers list
  state holders: Document (source text + DOM), Selection, Tool, Viewport, History(transactions)
Kotlin domain: SvgDocument (source-preserving DOM) <-> PathModel (nodes/handles) ; export (VectorDrawable, ImageVector)
Rust core (cdylib via cargo-ndk, UniFFI):  render(svgBytes, size, fonts) -> RGBA   [usvg + resvg + tiny-skia]
                                           optional: geometry ops (kurbo - unverified), path simplify/boolean (to research)
Test: resvg-test-suite + W3C subset (host JVM/desktop), golden images, WebView oracle (instrumented)
```
Previewer-only MVP is just: Compose + coil-resvg-style bridge; editor is phase 2.

## 6. Decisions for the user
1. Previewer only, or full editor (nodes, shapes, layers)? 2. Closed or open source app (AGPL/GPL code reuse)? 3. Accuracy vs APK size (resvg per-ABI size unknown; WebView = zero size but heavy runtime). 4. KMP target (Desktop/iOS later) or Android-only? 5. Need animation (SMIL/CSS)? resvg does not do it.

## 7. Not verified / gaps
AndroidSVG text/CSS/clip/mask support and min API; resvg support table content (filters/text/CSS details); kurbo/lyon/boolean-ops libs; tiny-skia and flutter_svg licenses; on-device SVG optimizer; SVG-Edit status; coil-resvg ABIs and size; no Zenn/Qiita/Juejin comparison articles found (JP/CN searches returned only generic hits); Korean search not run.

## 8. Next steps (prototype order)
P0 Compose app that loads an `.svg` from storage and shows it with AndroidSVG (baseline). P1 Rust `render()` via UniFFI for 4 ABIs; compare with P0 on 30 files. P2 run resvg-test-suite subset, produce a score table. P3 viewport (pinch/pan/zoom) + source pane. P4 path node editor (pen/select, handles, undo). P5 exporters (ImageVector, VectorDrawable). P6 fonts, large-file limits, 16 KB alignment, Play-ready.

## Sources
AndroidSVG https://github.com/BigBadaboom/androidsvg · resvg https://github.com/linebender/resvg · resvg test suite https://linebender.org/resvg-test-suite/svg-support-table.html · coil-resvg https://klibs.io/project/hash-sequence/coil-resvg · svg-to-compose https://github.com/rafaeltonholo/svg-to-compose · GodSVG https://github.com/FlooferLand/GodSVG · svg-path-editor https://github.com/Yqnn/svg-path-editor · Flutter path_editor https://pub.dev/packages/path_editor · react-native-svg https://github.com/software-mansion/react-native-svg · flutter vector_graphics_compiler https://pub.dev/packages/vector_graphics_compiler · Skiko/Compose SVG threads https://slack-chats.kotlinlang.org/t/16670045/ · ComposeSVGExample https://github.com/makzimi/ComposeSVGExample · W3C SVG test suite https://www.w3.org/Graphics/SVG/Test/ · Android ImageBitmap vs ImageVector https://developer.android.com/jetpack/compose/graphics/images/compare
