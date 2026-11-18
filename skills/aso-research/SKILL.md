---
name: aso-research
description: App store optimization (ASO) and market research for Google Play and the App Store using free, open data instead of paid tools like Sensor Tower or AppFigures. Finds keyword ideas from store autocomplete, studies competitor titles/descriptions/ratings/reviews, checks metadata against store character limits, counts keyword frequency in competitor text, and states clearly which numbers are measured and which cannot be known without paid panels (search volume, downloads, revenue). Use when the user asks for ASO, keyword research, competitor analysis, "app store listing", "Play Store title/description", market trends for an app idea, or wants to avoid paid ASO tools, even if they never say "ASO".
---

# aso-research

Do the ASO job with open data and be explicit about its limits. Paid tools sell *estimates* built from private panels; an agent can still do the useful 80%: find the words people type, see what competitors rank for, and write a listing that fits the store rules.

## What is measurable for free, and what is not
| Question | Free answer | Not available free |
|---|---|---|
| What do people type? | Store autocomplete suggestions (`scripts/gplay_probe.mjs suggest`) | real search volume / popularity (Play) |
| Who ranks for a keyword? | position in search results, first page only (`search`) | deep ranks, historical rank |
| What do competitors say? | title, short + long description, ratings, install bucket, updated date, reviews (`app`, `reviews`) | downloads and revenue (only buckets such as "1M+") |
| Is my listing valid? | `scripts/metadata_check.py` against store limits | store-side policy review |
| Which words recur? | `scripts/keyword_freq.py` over competitor text | keyword difficulty scores (a vendor's estimate) |
| Your own app's numbers | Play Console / App Store Connect reports (needs your account) | - |
iOS keyword popularity exists only through Apple Search Ads (a free account is enough); the open-source `semihcihan/App-Store-Optimization-CLI` and `KenanAtmaca/aso-mcp` use it or their own scoring. Treat any score as an estimate and label it so.

## Workflow
1. **Frame.** Platform(s), countries and languages, app category, 3-6 seed phrases (what the user would type), 5-10 known competitors if any.
2. **Expand keywords.** `node scripts/gplay_probe.mjs suggest "<seed>"` for each seed and for seed + each letter a-z (long-tail). Keep a list with the source (autocomplete) and country/language.
3. **Find competitors.** `search "<keyword>"` for the top keywords; the apps that appear for several keywords are the real competitors. Collect appId, title, score, ratings, install bucket, last update.
4. **Read their listings.** `app <appId>` for the top 5-10; save title, short description and description to a JSON file. Optionally `reviews` for complaints (a source of features and keywords).
5. **Analyse.** `python scripts/keyword_freq.py competitors.json` -> frequent words and phrases in titles and first 100 words of descriptions, and which keywords are *missing* from the user's draft. Treat frequency as "what the market says", not as proof of ranking.
6. **Draft and check.** Write title / short description / long description with the target keyword naturally, then `python scripts/metadata_check.py draft.json`. Never keyword-stuff; stores penalise it and users notice.
7. **Report** with three labels on every claim: **MEASURED** (from store data, with date and country), **ESTIMATE** (any score or trend, say how it was derived), **UNKNOWN** (volume, downloads, revenue). Put the method and limits at the end.

## Rules
- Use the stores' public pages and open libraries only. Respect rate limits (a few requests per second at most, cache results), never use proxies or tricks to evade blocks, and do not scrape logged-in areas.
- Do not invent numbers. If a paid tool would be needed, say so and say what free proxy you used instead.
- Store limits change; the values in `references/store-limits.md` were written from public documentation and must be re-checked against the store's current help page before a release.
- Keep the user's private details (name, project, email) out of queries.

## Files
- `scripts/gplay_probe.mjs` (Node 18+, needs `npm i google-play-scraper`): `suggest`, `search`, `app`, `reviews` -> JSON. Built on the MIT-licensed `google-play-scraper`.
- `scripts/keyword_freq.py` and `scripts/metadata_check.py` (Python 3, standard library).
- `references/tools.md` (open-source ASO tools judged, with licenses and what each can and cannot do), `references/store-limits.md`.
