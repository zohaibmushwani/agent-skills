# Design craft: how to get a distinctive screen, not a template

Why this file exists: in a controlled comparison on one screen, a long locked prompt (every string, count and hex, plus a long negatives list) produced a correct but mechanical result, while a short brief (what it is, who for, its one job, the feel, and "make good design decisions yourself") produced a richer, more believable one. Constraints buy consistency; they also cap quality. Use each where it pays.

**Bias guard (read first):** everything in this skill is an illustration of a pattern, not content to reuse. Never copy example product names, example copy, palettes, typefaces, layouts or "feel" words from this skill into a prompt; derive them from the user's brief each time. If two projects in a row come out looking alike, the prompt has been borrowing from an example.

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

## 8. Learned lessons (generic, from the prompt log)
Write lessons at the level of *model behaviour and prompt technique*. A lesson never names a product, a palette, a typeface or a layout recipe for one kind of product; the project-specific evidence stays in that project's `reports/prompt-log.jsonl`. Add a line only when a tag repeats (>= 2 entries, ideally across different projects); date it, and prune lines that stop being true.

**Content the model invents**
- People: image models draw photo-real faces for owners/avatars. If the product shows people, say how (initials in circles, abstract avatars, or named illustration style), and say "never photos or faces" when that is the rule.
- Dates and "current" facts default to the model's own past; state the month and year when dates are visible.
- Placeholder values (prices, names, counts, versions) need not agree between mock screens; do not spend edit passes on them. Check only counts and labels that must agree structurally on one screen (title count vs filter chips, badge vs list) and names that refer to the same thing.
- Numbered markers (01/02/03) appear on lists that are not sequences; allow numbering only where order matters.

**Layout and framing**
- Dense desktop pages are often returned cropped at the edges; state "the whole layout fits inside the frame with a margin, nothing cropped at any edge" and fix with an edit pass, not a reroll.
- Edit passes can add an outer border/shadow or change unrelated states (a selected control going blank). Add "no outer border" to edit instructions and re-check the whole image after every edit.
- Shared chrome (navigation items, badge counts, header) drifts between screens of a set; put the exact chrome in every prompt of the set and check siblings before accepting. Edits run in parallel (`&` + `wait`) when fixing many screens.
- Small, pale secondary text appears often; give a smallest-size floor in the prompt and check it in the critique.

**Interaction and intent**
- Tool-like pages must be briefed by their interaction, not their fields. A fields-only brief returns a multi-section form. Name the interaction ("click an element and a box opens anchored to it"; "inspector shows the element's properties") and a reference feel in the prompt.
- Annotation/marker screens: the model places numbered markers on the wrong element or detaches them from their list rows. State the mapping in the prompt and verify every marker against its row.
- If the prompt does not name the product's key interaction, the model builds a generic dashboard around it; put the key interaction first.
- Over-constraining a first render flattens it; brief first, lock later.
- Giving each screen one bold idea in the brief ("signature element") lifts distinctiveness; a mood alone ("calm, trustworthy") does not.

**Process**
- Brief skeleton that produced first-attempt accepts on tool-like pages: *who + deliverable, the signature interaction, what each panel holds, the mapping, one primary action (and one secondary), exact chrome + format + constraints, feel*.
- Aspect or orientation words in the wrapper command override the prompt; keep the aspect only in the prompt and run image CLIs with stdin closed (see `prompt-templates/web.md`).
- A generic-looking result is usually a generic brief: the word "dashboard", "app" or "platform" with no named job invites the template kit.
