# Interaction and density: calm screens that work

Added after a user review: generated screens were text-heavy and crowded, and some interactions were unclear. Rules below are distilled from public UX guideline sets (notably the MIT-licensed UI UX Pro Max rule list: one primary action, progressive disclosure, whitespace, hierarchy by size/spacing/contrast, feedback states, confirm destructive actions) plus our own critique runs. They are heuristics; judge by looking at the image.

## 1. Density budget (check before accepting any screen)
- **Words:** a desktop page shows roughly 120-180 words of interface copy outside data rows; a narrow layout 60-90. Count what is visible. Over budget -> cut or move to a drawer/tab.
- **One idea per panel.** If a panel needs two headings, it is two panels or one is hidden behind a click.
- **Lists:** at most 6-7 visible rows; sentences in rows <= 1 line (truncate, reveal on click).
- **Sentences:** no paragraph over 2 lines in a work tool; prefer a label + value, a chip, or an icon with a word.
- **Repetition:** the same sentence, status or warning appears once per screen. Duplicate panels (a summary that restates the list) are deleted, not restyled.
- **Whitespace is structure:** >= 24px between groups, >= 16px inside panels, consistent; group by proximity before boxes or lines. If everything is in a card, nothing is grouped.
- **Squint test:** blur the image; you should still see 3-4 regions and one clear primary action. If it looks like uniform texture, it is crowded.

## 2. Progressive disclosure
Show the decision first, the evidence second, the detail on demand: summary row -> click -> drawer / expanded row / side panel. Logs, long reasoning, full diffs, history live behind a click, not on the main canvas.

## 3. Interaction must be visible in the image
- Show the **current state of the key interaction**: what is selected, what is open, what is focused (a box open next to its target, a selected row, a hovered control), and **what the next step is** (one primary action).
- Only one primary action per screen; secondary actions visually quiet; destructive actions separated and in a danger colour; confirm irreversible ones.
- Feedback states exist for the interaction: loading (skeleton, not spinner walls), success (brief confirmation), error (what happened + how to fix, near the cause), empty (what to do next).
- Gates and approvals say what approving allows and what exists right now, once, in plain words.
- Clickable things look clickable (not text only); no hover-only controls; icon-only buttons have a label or tooltip noted in the spec.
- If the interaction needs an explanation paragraph to be understood, the design is wrong.

## 4. Review questions (add to the critique)
1. In 3 seconds, what is this screen asking me to do? 2. Can I do it in <= 3 clicks with no reading? 3. What can I delete without losing meaning? 4. Is anything said twice? 5. Is there room to breathe between groups?

## 5. Using external design databases
Rule lists (accessibility, touch, forms, feedback) transfer well. Their keyword-matched "pattern / style / palette" picks do not: a search for an internal approval tool returned a documentation-site landing pattern and a default dark style. Use such databases to check rules and borrow vocabulary, never to pick the product's pattern or look, and verify any pick against the user's brief.
