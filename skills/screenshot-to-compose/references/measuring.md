# Measuring a screenshot

## px to dp
A screenshot has no real density. Pick a **design frame width in dp** (default 390 unless the reference says otherwise) and compute
`scale = imageWidthPx / frameDp`, `dp = px / scale`.
Example: a 941 px wide AI screenshot gives scale 2.41, so a 24 px gap is 10 dp and a 96 px button is 40 dp.
`scripts/measure_image.py shot.png --frame-dp 390` prints the size, aspect ratio and scale; add `--px 96 24` to convert spans.

## Colours
Sample real pixels, never guess a hex from how it looks:
`python scripts/measure_image.py shot.png --sample 120,300 --sample 400,80`
Sample the centre of flat areas (not anti-aliased edges). For gradients sample both ends and the middle. Round to the nearest value that makes a sensible palette and record both.

## Observed vs inferred (keep them in separate columns)
| Token | Observed (measured) | Inferred (guessed) | Notes |
|---|---|---|---|
| primary | #2F6BFF at (120,300) | | |
| dark theme background | | #101418 | only a light screenshot exists |
| font family | | Inter-like | not identifiable from a PNG |

Inferred values are fine, but state them, so a reviewer knows which numbers to trust.

## Typography
Measure cap height or line spacing in px, convert to dp, then choose the nearest Material type role. Record weight by eye as inferred. Exact fonts are rarely recoverable from a screenshot: pick a close Google Font and note it.

## Spacing and shapes
Measure paddings and gaps between sibling elements, corner radii (distance from the corner to where the edge turns straight), borders and shadows. Snap to the spacing scale (4/8 dp multiples) when the measured value is within about 1 dp, otherwise keep the measured one and record it.
