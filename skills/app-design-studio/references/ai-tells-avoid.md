# AI tells and anti-patterns (avoid)

Why: image models fall to the statistical average. Naming the defaults is how you steer away from them. Banning one default can summon the next, so also state what to prefer.

## Visual
- Purple-blue or generic startup gradients; muddy or rainbow palettes -> prefer a controlled palette with one accent.
- Glass/blur cards with no purpose, ambient blobs, fake neon, glossy over-rendering -> prefer flat or softly shadowed surfaces.
- Oversized corner radii on everything -> prefer radius logic (e.g. 12 cards, pill buttons only).
- Pure grey/black shadows on coloured surfaces -> tint shadows to the surface.
- Mixed icon weights/sets, generic default icon-pack look -> one Iconify set, one stroke width.

## Layout
- Box-in-box nesting, five levels of framing, cards inside cards -> flatten; use spacing and dividers.
- Homepage as 12 widgets, repeated stat cards, fake chart spam -> one hero + one list + at most one chart that means something.
- Cloned screens with minor edits -> each screen needs a distinct purpose and composition.
- Phone-shaped website (hero banners, footers, wide paddings) -> real mobile patterns: bottom nav, sheets, sticky CTA.
- Empty giant cards, tiny packed widgets, excessive pills/badges.
- CTAs outside the thumb zone, hidden primary actions, sliders for precise input.

## Text
- Lorem ipsum, "Welcome to the future of...", filler motivation, invented brand names.
- Long paragraphs on mobile; labels that outweigh values; tiny decorative micro-labels.
- Text over busy imagery without a scrim.
- Shrinking text to fit instead of cutting copy.

## Device/framing
- Any device frame, bezel, notch mockup, drop shadow around the screen, or coloured outer background (we want the UI only).
- Edge crops, inconsistent aspect ratios between screens.

## Image-model failure modes to pre-empt in prompts
- Wrong counts (tabs, list items, onboarding dots) -> state exact numbers.
- Garbled or invented text -> give exact strings; keep strings short; re-check every label.
- Inconsistent nav bar between screens -> reuse the exact nav description; verify siblings.
- Extra unrequested elements -> end every prompt with "Do not add: ...".
- Fake OS chrome that differs per image -> same status bar text/time (9:41) everywhere.

## Prefer
Distinct type pairing, one accent used sparingly, generous whitespace, one considered image/illustration moment per flow, real-sounding data (names, prices, dates), empty states with personality, consistent iconography.

## Web
See `web-design.md` section 7 (gradient-blob hero, identical 3-icon cards, fake logo walls, glass nav, KPI tile walls). Phone-shaped layouts on desktop (one narrow column floating in a wide canvas) are also a tell.
