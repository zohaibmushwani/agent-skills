# Per-image QA loop (every generated image)

Why: image models fail on consistency, not beauty - a list with 3 unchecked tasks and a ring saying "1 done"; header says Tuesday, Wednesday selected. Trust the file, not the prompt.

1. **Open the PNG** (Read tool) - do not rely on the prompt.
2. Compare with the prompt's STATE block: every string, every count, selected tab/day, numbers that must agree (progress vs list, total vs items).
3. Check alignment, clipping, overlap, legibility at thumbnail size.
4. Check icons share one stroke/fill style, nav bar identical to siblings; mobile target: status bar text identical (9:41); web target: header/sidebar identical, no OS status bar.
5. Check palette against tokens (eyeball 5 spots; if unsure, sample pixels with Pillow if installed).
6. Write the result to `qa/<round>.md`: id, pass/fail per item, what to fix.
7. **Edit, don't reroll:** if one string is wrong, run an image-edit pass naming only that change ("keep everything identical except the title text, which must read 'Library'"). Rerolling resets everything already approved. Max 2 retries, then flag.
8. Update `<id>.spec.json` to match what is actually on the image, then run `scripts/run_gates.py`.

Never invent: statistics, brands/logos, real people's faces. Use fictional names, generic marks.

## Truth layer (optional, S8)
When developers need exact values, build `<id>.html` from the approved PNG: real CSS using only token values (`token_lint.py <dir> --code <dir>` checks this), rendered at 412x892 with Playwright, then compare screenshot vs PNG. If they disagree, the HTML plus DESIGN.md wins and the PNG is regenerated or annotated. Skip when the user only wants image concepts.

## Copy
Every user-visible string also goes to `copy/strings.json` (key -> text, note for translators). The image must not be the only home of a string; check each string in the image exists in strings.json.
