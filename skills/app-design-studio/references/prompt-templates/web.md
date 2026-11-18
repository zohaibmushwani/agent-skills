# Web prompt templates

Same 6 blocks as README.md (FORMAT, BIBLE, SCREEN, CONTENT, CONSISTENCY, DO NOT ADD); only FORMAT and CONTENT patterns change.

## FORMAT block
- Desktop: `Website page, desktop 16:10 (1440x900 viewport). Show ONLY the page UI, edge to edge. No browser window, no address bar, no laptop mockup, no outer background, no shadow.`
- Desktop long page: `Full-length landing page, desktop 1440 wide, tall single image, sections top to bottom as listed.` (for >3 sections split into 2-3 images of the same width)
- Mobile: `Website page, mobile 9:19.5 (390x844). Show ONLY the page UI, full-bleed. No phone frame, no browser chrome, no outer background.`
- Web app on a phone: same as mobile; status bar line optional (omit it for a mobile *website*, keep it for an installed/PWA look).

## CONTENT block pattern (site home)
```
Header: logo "[Name]" left, 4 links "Apps", "About", "Careers", "Contact", button "Get the app" right (the only filled button).
Hero: headline "<<=10 words>>", one-sentence subhead, primary button "<<label>>", secondary text link "<<label>>", right: one illustration/app screenshot described exactly.
Section 2 "<<title>>": exactly 3 items, each icon + title + one line.
Section 3 ... Final CTA band: headline + ONE button. Footer: 3 link columns, legal line.
```
## CONTENT block pattern (web-app page)
```
Left sidebar (desktop) / bottom bar (mobile): exactly 4 items - Inbox (selected), Requests, Library, Me.
Page title + status chips (exact strings). Tabs: exactly 4 - ... Main content: cards/rows with exact count and exact strings.
Sticky bottom/right action: ONE primary button "<<label>>".
```
## Per page type
- **Landing/home:** hero, proof (real-sounding numbers with source label or none), 3-5 sections, one CTA repeated, footer.
- **Pricing:** exactly N plans, one highlighted, monthly/yearly toggle, plan features as short list, FAQ (5 items).
- **List/catalog:** filter row or sidebar, exactly N items, sort control, pagination or load more; empty/loading/error variants.
- **Detail:** hero/summary, key facts block, media, related items, sticky CTA.
- **Form/contact:** single column, labels above, exact fields, validation-error variant, success variant.
- **Dashboard/board:** one primary summary, one list/board, at most one chart that means something; filters visible; role in header.
- **Master-detail (desktop):** list left, detail right, selected row marked; on mobile show list and detail as two images.
- **404/offline:** distinct illustration, plain reason, one way back.
- **Cookie/consent dialog:** over dimmed real page, 2-3 clear buttons, equal visual weight for accept/reject.

## Tool notes (web)
- Codex image_gen (gpt-image): returns ~900x1600 for 9:16; for desktop ask 16:10 and expect a near ratio; send one image first, then batch 3-5 per call. All three style directions can render in one batch.
- Show the same hero page for every direction at S2 (home for a site, the most important detail/list for a web app) so the human pick compares like with like.
