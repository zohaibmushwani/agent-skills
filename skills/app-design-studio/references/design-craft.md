# Design craft: how to get a distinctive screen, not a template

Why this file exists: an A/B run on the same screen (internal portal, requirement detail) showed that a **450-word locked prompt** (every string, count, hex and a long "do not add" list) produced a correct but mechanical screen, while a **130-word brief** (what it is, who for, the one job, the feel, and "make good design decisions yourself") produced a richer, more believable one: real hierarchy, a rewritten brief card, owners and statuses it invented sensibly. Constraints buy consistency; they also cap quality. Use each where it pays.

Method distilled from public design-skill research (Anthropic's frontend-design skill, UI UX Pro Max, Impeccable; ideas only, written in our own words).

## 1. Two prompt modes
| Mode | When | What the prompt contains | Length |
|---|---|---|---|
| `brief` (default for S2 directions and first screens) | exploring, first render of a screen, hero screens | product in one line, audience, the screen's one job, the 3-5 facts that must be true (counts that matter), feel in 4-6 words + 1-2 reference qualities, "make good design decisions yourself", format line | 80-150 words |
| `locked` | after the human pick, for siblings that must match, and for fixing one wrong string | bible block + exact strings/counts + short negatives | as long as needed |
Rule: **render `brief` first, look, then lock only what you liked or what must agree.** Never start a set with a 400-word locked prompt. Keep the format line (no frame, no mockup) and the target's vocabulary (keyword hygiene) in both modes.

## 2. Design plan before any render (S2, 10 lines, written to `DESIGN.md`)
- Subject: product, audience, the primary job of this page/screen.
- Colour: 4-6 named hex values (base, surface, text, secondary text, accent, state). Name the text colour on every filled colour.
- Type: families and roles (one or two; if two, clearly different). A clear scale; line length under ~75 characters.
- Layout: a one-sentence concept plus a rough ASCII wireframe; say the alignment (left, centre).
- Principles: 2-3 sentences on what makes this design specific to this product.
- **Self-review:** compare the plan with the default you would produce for any similar product. If a part matches the default, change it and note what and why (in STATUS.md).

## 3. Generic defaults to avoid (calibrate against these; the brief always wins if it asks for one)
1. warm cream background + high-contrast serif + terracotta/clay accent;
2. near-black background + one acid-green or vermilion accent;
3. broadsheet layout: hairlines, zero radius, dense columns;
4. the SaaS card kit: everything in identical rounded cards, one radius everywhere, the same soft grey shadow, gradient washes;
5. template chrome on every page: tracked ALL-CAPS eyebrow above each heading, dot-joined meta strings, "WORD - fragment" labels, arrows on every link, tinted near-black, monospace for all small labels, one word of a headline in a different colour, numbered 01/02/03 markers on content that is not a sequence.
Also avoid (kept from before): purple-blue gradients, glass for no reason, box-in-box nesting, fake chart spam.

## 4. Spend boldness in one place
One memorable element per screen or flow (a typographic treatment, an illustration, a data visualisation that means something); everything around it quiet and disciplined. Cut one decorative accessory before finishing. Motion in design specs: sparing, only to show what changed or to draw attention once.

## 5. Copy is design
- Write from the user's side: name things by what people understand, not how the system is built.
- Active voice; a button says what will happen ("Save changes", not "Submit") and the same action keeps one name through the flow (button "Publish" -> toast "Published").
- Errors say what happened and how to fix it, never apologise, never vague. Empty states invite the next action. Sentence case, plain verbs, no filler.
- Real-sounding data (names, numbers, dates); fictional brands only.

## 6. Structure is information
Outlines, dividers, labels, numbering and chips must encode something about the content (status, type, sequence); if removing one loses nothing, remove it.

## 7. Critique loop (every render)
Open the image. Check: hierarchy in 2 seconds, one primary action, every string readable at its size, same nav/header as siblings. Write one corrective sentence for the single biggest problem and edit with that sentence only.
