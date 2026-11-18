# Self-critique template (write one per generated image, `reports/critique/<id>.md`)

Do this after EVERY render, before showing the user. Open the image; do not score from memory.

```
# Critique <id> (<mode>, attempt N of 3)
Job of this screen: <one sentence>   Key interaction: <what the user does>
Usability (pass/fail + evidence):
- Key interaction obvious in 3 seconds?  - One primary action?  - Numbered pins/badges/counts map to the right items?
- Nothing cropped, nothing covered that must stay visible?  - Text >= 13px, no pale grey?  - Same nav/header as siblings?
- No faces, plausible dates, labels and structure match the earlier screens?
- NOT a defect: invented placeholder VALUES (prices, names, numbers, dates, versions) that differ between screens of a mock. Only check counts that must agree structurally on one screen (title count vs chips, badge vs list) and labels/roles that name the same thing.
Aesthetics (1-5, one line of evidence each): hierarchy, rhythm, typography, colour, imagery/icons, distinctiveness, consistency, delight -> average
Verdict: ACCEPT | FIX (edit pass, name the exact change) | REJECT (regenerate; say what the new prompt changes)
Lesson for next project: <one line, or "none">
```
Rules: average < 4.0, or any usability FAIL -> not accepted. Prefer FIX (one edit pass naming only the defect) over regenerate; max 2 edit passes + 1 regenerate per screen, then flag to the user. Log with `scripts/prompt_log.py add ...`; reject/fix reasons use the standard tags so repeats surface in `summary`.
After any edit, re-check the whole image: edits can change things you did not ask about (a selected radio, an outer border).
Distinctiveness below 4 cannot be fixed by an edit pass; it needs a changed brief (a bolder single idea).
