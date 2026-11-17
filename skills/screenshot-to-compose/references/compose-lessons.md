# Compose lessons (each from a real defect)

- **Fixed aspect ratio for sibling cards and tiles.** Cards in a row (stat tiles, action cards) get `Modifier.aspectRatio(...)` taken from the reference, so they keep one shape on every device and language. On a narrow width shrink parts (compact icon, auto-size text with a floor), never switch to a different arrangement. If the ratio cannot hold the content at 360 dp, relax it once and record it, not per language. Defect fixed: tiles stacked on 360 dp and looked different in Arabic.
- **No intrinsic measurement over subcomposition.** `Modifier.height(IntrinsicSize.Min)` crashes at runtime when a child uses `BoxWithConstraints`, a lazy list or another `SubcomposeLayout`. One-line texts with equal widths give equal heights without it.
- **Thresholds are measured where they are read.** A `BoxWithConstraints` inside padding sees the inner width. Write the real values for 360 dp and 390 dp phones in a comment next to the token.
- **Tight text auto-sizes with a floor.** Big numbers and titles in tight cards use `BasicText(autoSize = TextAutoSize.StepBased(min, max))` with the floor as a theme token. User data (names) may take 2 lines, then ellipsize.
- **Tight labels get the concise term** used by apps in that domain in each language, not a dictionary word that can never fit.
- **Prefer weights, aspect ratios and max-width constraints** over fixed widths or `Modifier.offset`. Units are plain `dp`/`sp` 1:1 from the design frame.
- **Do not trade function for pixel match.** A static pixel copy that breaks on a small phone or in RTL is a defect.
