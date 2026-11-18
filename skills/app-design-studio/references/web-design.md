# Web target: websites and web apps

Use when the S0 target is `web` or `both`. Everything in SKILL.md still applies (locked bible, tokens, gates, edit-don't-reroll); this file replaces the mobile-only assumptions.

## Contents
1. Which kind of web  2. Viewports and output  3. Floors in px  4. Page taxonomy  5. Layout rules  6. Responsive rules  7. Web AI tells  8. Verification

## 1. Which kind of web (ask at S0 if unclear)
| Kind | Examples | Design emphasis |
|---|---|---|
| `site` (marketing/content) | company, portfolio, landing, store, blog | story order, one CTA per section, imagery, SEO copy, trust |
| `web-app` (work tool) | internal portal, dashboard, admin, SaaS app | density, tables/boards, filters, states, roles, fast scanning |
Never apply landing-page tricks (giant hero, scroll storytelling) to a work tool, and never apply dense tool chrome to a marketing site.
Mobile-first work tool (phone is the main device): design 390 first, desktop second.

## 2. Viewports and output
- Set `"platform": "web"` and `"viewports"` in `inventory.json`; each item lists `views`.
- Default pair: **landscape desktop 1440x900 (16:10) is the primary view**, plus a narrow responsive layout 390 wide (file suffix `@mobile`, but in prompts call it "narrow responsive layout, 390px wide", not "phone screen"). Add tablet 834x1112 only if needed. Only when the user says phones are the main device (`"mobile_first": true` in inventory.json) is the narrow layout primary.
- Image = the page itself: **no browser chrome, no laptop/phone mockup, no outer background**. Long pages: render the full scroll height as one tall image (HTML route `--full-page`), not a cropped first screen.
- File names: `<id>@desktop.png`, `<id>@mobile.png`, states `<id>.empty@mobile.png`, plus matching `.spec.json`.
- **Default route = PNG designs from an image model (Codex image_gen), no HTML.** Write the prompt file, generate, look at the image, fix with edit prompts. Ask for 16:10 (desktop, above the fold) or 9:19.5 (mobile); real size is only close (measure it). Long pages: generate section-by-section (hero / middle / footer images) or one tall page per 3-4 sections, keeping the same bible. The HTML-render route is optional: use it only if the user asks for real HTML or for measured specs.

## Words to use / avoid in web prompts
Use: website page, landscape desktop 16:10, 1440 wide, header with N links, sidebar, hero, section, footer, narrow responsive layout. Avoid (lint fails): portrait, phone, status bar, 9:19.5, 9:16, Android, iOS, iPhone, bottom navigation, thumb zone, app screen, mobile app.

## 3. Floors in px (measured by `spec_audit.py` with `platform: web`)
| Rule | Value |
|---|---|
| Interactive hit area | >= 44x44 (touch viewports), pointer-only controls >= 32; 8px gap between targets |
| Body text | >= 16px; secondary >= 14px; nothing < 12px; dense table text >= 14px |
| Line length | 45-75 characters for paragraphs (max-width ~ 65ch) |
| Contrast | text 4.5:1, large text/icons 3:1, focus ring visible 3:1 |
| Layout | no horizontal scroll at 390; content width <= 1200 (site) / fluid with max 1440 (app) |
| One primary action per view/section | 1 (nav "Sign in" is secondary) |
| Spacing | 4/8 scale; section padding 64-96 desktop, 40-56 mobile |
| Thumb-zone rule | mobile viewport only |

## 4. Page taxonomy (build `inventory.json` from this)
Site: home (hero, proof, 3-5 value sections, CTA, footer), product/feature, pricing, about, contact (+error/success), blog list + post, case study, careers + job, legal (privacy/terms), 404, nav (header, mobile drawer), cookie/consent dialog, newsletter dialog.
Web app: sign in, role dashboard, list/board (filters, saved views), detail (tabs, timeline, comments), create/edit form (+validation errors), library/gallery, review/approve, notifications, settings/integrations, empty/loading/error/no-access, filter sheet (mobile), confirm dialogs.
Data pages need loading (skeleton), empty (first-use vs no-results), error (retry), and for sync tools: sync-failed and stale.

## 5. Layout rules
- 12-col grid desktop (max 1200, gutter 24), 4-col mobile (margin 16-20). Name the grid in the bible.
- Header: logo left, <= 5 links, one CTA right; sticky only if it earns the space. Mobile: logo + menu button, drawer lists the same links.
- Hero (site): headline <= 10 words, one sentence, ONE primary CTA + one secondary, one real image/illustration. No stock-photo grids, no carousel.
- Sections alternate rhythm (text/media, cards/list); each has a heading and one job. Footer: links, legal, contact.
- Cards: only for repeated items; do not nest cards. Prefer dividers and spacing.
- Work tools: left sidebar (desktop) -> bottom bar/drawer (mobile); list + detail as master-detail on desktop, separate pages on mobile; sticky action bar for the one primary action.
- Forms: labels above fields, errors beside the field in text (not colour alone), single column.

## 6. Responsive rules
Define at each breakpoint (390 / 834 / 1440): column count, nav pattern, which sections stack, which are hidden (never hide the primary CTA or core content). Tables -> stacked rows or cards on mobile. Images keep subject centred when cropped.

## 7. Web AI tells (avoid, on top of ai-tells-avoid.md)
Gradient-blob hero, 3 identical icon cards "Fast / Secure / Scalable", fake dashboard screenshot hero, logo wall of invented brands, testimonial with stock face, "Trusted by 10,000+" with no source, floating glass nav, emoji as icons, every section centred, wall of CTAs, footer with 40 links, dashboard of 8 equal KPI tiles.

## 8. Verification
- Default (image route): write specs by hand from the prompt (`<id>@<view>.spec.json`, sizes in px), correct them after looking at the image, then run `run_gates.py`. Optional HTML-render (only when asked): `node scripts/render_screens.mjs <design-dir> --viewports desktop=1440x900,mobile=390x844 --full-page --scale 1` writes PNG + measured spec per viewport; then `python scripts/run_gates.py <design-dir>`.
- Image route checks: write each prompt to `prompts/<id>@<view>.md` first, send that file, then open the image and check every string, count and the one-primary-action rule. Text smaller than 12px inside a *thumbnail of another design* is acceptable; in real UI it is a fail.
- Rubric in aesthetic-vs-usability.md applies unchanged; add "responsive consistency" (desktop and mobile clearly the same site).
