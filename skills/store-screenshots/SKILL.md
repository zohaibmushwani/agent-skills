---
name: store-screenshots
description: Create App Store and Google Play marketing screenshot sets that look like top-chart apps - a headline-led story of 5-8 frames with a poster-style first frame, zoomed real UI fragments, a dominant brand colour, panoramic links between frames, social proof and human touches - generated frame by frame with Codex (GPT Image) using the app's real screens as reference images, text-checked and edit-passed, then fitted to the exact store sizes. Use whenever the user wants store screenshots, "App Store screenshots", "Play Store images", listing graphics, a screenshot redesign or "before/after" for a store page, or wants their app's store page to convert better, even if they only say "screenshots" for an app. Takes real app screens (for example from app-design-studio) as input.
---

# store-screenshots

Store screenshots are an ad, not a gallery of screens. Visitors decide in one or two seconds, mostly from the first 2-3 frames, so each frame sells **one benefit** with a big headline and only the slice of UI that proves it. The patterns here come from studying high-performing sets (see `references/patterns.md`); use them as principles, never copy another app's layout, brand or art.

## Inputs (gather first)
- Real UI screens of the app (PNG). From the `app-design-studio` skill or captures. Without them, stop: invented UI in store screenshots misrepresents the app.
- `tokens.json` or brand colours, logo/wordmark, app name, the one-line promise.
- Keywords and competitor claims (the `aso-research` skill, if available) so headlines use the words people search.
- Platform(s) and languages. Default: Google Play phone 1080 x 1920 and iPhone 6.9" 1290 x 2796.

## Workflow (Codex is the renderer; this skill writes its instructions)
1. **Message map.** List 5-8 benefits, ordered by what makes someone install. Frame 1 = the promise (poster); frames 2-3 = the core loop; then differentiators, proof, retention. Write `story.md`: per frame a headline (2-4 words), optional 3-6 word subline, and the real screen that proves it. Rules in `references/copy.md`.
2. **set.json.** Fill the set style once (look, colours with text-on-accent, headline font description, art direction, panorama motif) and the frames (schema in `references/frame-recipes.md`). The style block is repeated verbatim in every prompt; that is what keeps the set consistent.
3. **Prompts.** `python scripts/build_prompts.py set.json prompts/` writes `NN.md` (exact text to send) and `NN.refs.txt` (real UI screens to attach, plus the approved frame 1 as style reference for frames 2+). Never retype a prompt; send the file.
4. **Three directions (human gate).** Generate frame 1 in three set styles (e.g. Poster, Panorama, Character) with Codex - send ONE image first to confirm the image quota (`codex_status` does not show it). The user picks one; save it as `final/01.png` (it becomes the style reference).
5. **Generate the rest** with `generate_image` (prompt = file text, `reference_images` = refs file, background mode for batches). Save as `raw/NN.png`.
6. **Text and truth check (every frame).** Open each image and read it: headline spelled exactly, no extra words, UI not redesigned, no invented logos/ratings. Fix with an edit pass (the frame as reference image + "keep everything identical except: <one change>"), max 2 edits per frame; if text still breaks, shorten the headline.
7. **Fit and check.** `python scripts/fit_store.py raw/ final/play --size play` (and `--size ios69`), then `python scripts/check_set.py final/play --set set.json`; score the contact sheet with `references/rubric.md` at thumbnail size. Regenerate the weakest frame first.
8. **Deliver** `final/<platform>/NN.png`, `story.md`, `set.json`, `prompts/`, contact sheet. Label anything made before the app is real as `concept`.

## Non-negotiables
- UI shown must be the app's real UI (or the approved design marked concept). No fake features, fake ratings, fake awards or "No. 1" claims you cannot prove; social proof only with real numbers the user supplies.
- No other companies' logos or trademarks unless the user has the right and the store allows it; no real people's likeness from the internet.
- Every visible word is quoted in the prompt and verified in the output; a frame with a misspelled or extra word is not shipped. Headline must contrast clearly with its background.
- Keep the first 2 frames understandable on their own, at thumbnail size.
- Follow store rules: Play screenshots no alpha, 320-3840 px per side, aspect <= 2:1; Apple sizes per device class (re-check official pages).

## Files
- `references/patterns.md` - what top sets do (8 patterns) and the before/after lessons.
- `references/frame-recipes.md` - frame types, layout grid, `set.json` schema, panorama slicing.
- `references/copy.md` - headline formulas, length, tone, localisation.
- `references/rubric.md` - 1-second test and scoring.
- `scripts/build_prompts.py` (set.json -> Codex prompts + reference lists), `scripts/fit_store.py` (exact store size, no alpha, contact sheet), `scripts/check_set.py`; `assets/example/` (set.json, prompts, real screens).
