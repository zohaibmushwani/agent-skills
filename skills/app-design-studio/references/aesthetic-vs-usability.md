# Aesthetic vs usability: how to keep both

Principle: **usability is the floor, aesthetics is the ceiling.** The floor is measurable, so scripts enforce it. The ceiling is taste, so we use dials, a rubric, pairwise comparison and a human pick. (Research basis: UI-Bench found absolute aesthetic ratings noisy, pairwise comparison reliable; AI-generated UI is good at drafts and checks, weak at final taste.)

## 1. Dials (set at S0, written into the design bible)
Scale 1-10. Defaults for a general consumer app; adjust by category.

| Dial | Default | Meaning |
|---|---|---|
| Clarity | 9 | one obvious primary action, scannable hierarchy |
| Text readability | 9 | body >= 16sp, high contrast, short copy |
| Consistency | 10 | every screen is clearly the same app |
| Art direction | 7 | distinctive type, accent, imagery |
| Variance | 5 | how different screens are from each other in layout |
| Density | 4 | information per screen (reader/finance may go 6; kids/wellness 3) |

Category nudges: fintech/health -> raise trust and calm (Variance down, Clarity 10). Creative/social -> Art direction 8-9. Utility/tools -> Density 5-6, Art 5-6. Kids -> larger targets (56dp), Variance up.

## 2. The floor (hard gates, scripts check these)
| Rule | Value | Why |
|---|---|---|
| Touch target | >= 48dp (44pt on iOS); 8dp between adjacent targets | thumbs; WCAG 2.5.8 24px is only the legal minimum |
| Body text | >= 16sp; secondary >= 14sp; nothing < 12sp | readability |
| Contrast | text 4.5:1; large text (>=18sp or 14sp bold) and meaningful icons 3:1 | WCAG AA |
| Spacing | values from the 4/8 scale: 4, 8, 12, 16, 24, 32, 48, 64 | rhythm, buildable |
| One primary action per screen | 1 | decision clarity |
| Primary actions in lower 40% (thumb zone) when frequent | - | reachability |
| Max 2 font families, <= 6 text styles used | - | coherence |
| Every data screen has loading/empty/error covered | - | real apps |
| Safe areas respected (status bar, gesture bar) | - | native feel |

## 3. The ceiling (rubric, scored by looking at the actual image)
Score 1-5, then average per screen. Describe the evidence in one line each; "looks fine" is not evidence.
1. **Hierarchy** - can you tell in 2 seconds what matters most?
2. **Rhythm** - consistent spacing, aligned edges, grouped by proximity.
3. **Typography** - clear scale, intentional weights, comfortable line length.
4. **Colour** - controlled palette (about 60/30/10), accent used with purpose.
5. **Imagery and icons** - one family, purposeful, not decorative filler.
6. **Distinctiveness** - could this only be this app? Not generic template.
7. **Consistency** - matches the bible and sibling screens.
8. **Delight** - one considered moment (illustration, motion cue, empty state charm).
Pass: average >= 4.0 and no single criterion below 3. Otherwise regenerate with a *specific* fix instruction ("increase heading size contrast, reduce card nesting"), not "make it better".

## 4. Resolving conflicts
- Pale elegant secondary text fails 4.5:1 -> darken, then keep elegance through lighter weight, smaller caps/letterspacing, or spacing. Never lower the floor.
- Dense dashboard looks impressive but fails clarity -> split into 2 screens or progressive disclosure.
- Small decorative labels -> delete them; decoration that can't be read is noise.
- Full-bleed photo behind text -> add a scrim/gradient fade, then re-check contrast on the worst region.
- Beautiful icon too small to tap -> keep the glyph size, enlarge the hit area (spec the hit area; image shows glyph).

## 5. Regenerate protocol
1. Run gates -> list failures (numbers, not feelings).
2. Rubric -> list lowest two criteria.
3. Write one corrective prompt addressing only those items; keep everything else identical (same bible block, same strings).
4. Max 2 retries per screen; then flag to user with the best version.
5. After any fix to shared elements (nav bar, top bar), re-check siblings so one screen does not diverge.

## 6. Human gates
S2 (pick direction) and S9 (final review). Do not skip S2: it is the cheapest place to apply taste.
