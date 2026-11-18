# Screen taxonomy (mobile app)

For websites and web apps use `web-design.md` section 4 instead.

Build the inventory from this list. Drop what the app doesn't need, add app-specific features. Give every item an id like `onb-02`, a group, a purpose, and the states it needs.

## Contents
1. Core groups  2. Per-screen state matrix  3. Dialogs  4. Sheets  5. Components  6. Interactions  7. Inventory sizing

## 1. Core groups
| Group | Screens | Notes |
|---|---|---|
| `entry` | splash, language selection, onboarding (3-4 slides), permission primers (notifications, camera, storage, as needed), consent/terms | Splash is brand only. Language screen lists native names, current device language preselected. Onboarding: one idea per slide, skip + next always reachable. |
| `auth` | welcome/sign-in, sign-up, forgot password, OTP, success | Skip entirely if the app is account-less; say so in the inventory. |
| `home` | main dashboard/feed + bottom navigation tabs | Max 5 tabs. One primary action. Not a widget wall. |
| `feature` | the 4-10 screens that are the app's actual value | Derive from the app's core verbs (e.g. PDF reader: open, read, annotate, search, bookmarks, library). |
| `detail` | item detail, preview, edit, create flows, confirmation/success | Each feature list needs a detail. |
| `search` | search idle (recent + suggestions), results, no-results | Never a blank screen. |
| `profile` | profile/account, subscription/paywall (if any) | Paywall: clear price, clear close, restore. |
| `settings` | settings root, appearance (theme), language, notifications, privacy/permissions, storage/data, about/help/feedback, legal | Settings root is grouped lists, not one long list. |
| `system` | offline, server error, maintenance, force update, permission denied, session expired, 404/not-found | Each is a distinct design, not a recolor of one. |

## 2. Per-screen state matrix
For every data-driven screen decide which apply and generate the ones that matter:
default - loading (skeleton matching real layout) - empty (guidance + one CTA; first-use vs no-results are different) - error (distinct from empty; retry) - offline/cached - partial - success - selected/edit mode - disabled/limit reached - permission denied.
Rule: loading is never shown as empty; error is never shown as empty.

## 3. Dialogs
Confirm destructive (delete, sign out), rename/input, permission rationale, rating (late, never on first run), update available, discard changes, error with retry, progress (blocking only when unavoidable), success.
Anatomy: title (verb-led), one sentence body, primary action right/bottom, secondary clearly weaker, destructive action visually distinct, tap-outside behaviour stated in spec.

## 4. Sheets
Action sheet (share/more), filter/sort, selection list, date/time picker, form sheet, media picker, full-height detail sheet, mini player/persistent sheet. Show drag handle, scrim, safe-area padding.

## 5. Components (board in S4)
Buttons (primary/secondary/tertiary/destructive/icon, each: default, pressed, disabled, loading), text field (default, focus, filled, error, disabled), search bar, chips, tabs/segmented, switches/checkboxes/radios, list rows (1/2/3 line, with avatar, with trailing control), cards, top app bars (standard, search, selection), bottom nav, FAB, snackbars/toasts, badges, progress (linear/circular), skeletons, avatars, empty/error illustrations, tooltips/coach marks.

## 6. Interactions (documented in spec, drawn only when they change layout)
Pull to refresh, swipe actions on rows, long-press selection, drag to reorder, pinch/zoom (content apps), expand/collapse, tab switching, page transitions (shared element notes), keyboard open state (show fields above keyboard), scroll states (collapsed top bar).

## 7. Inventory sizing
Small utility app: 25-35 images. Content/reader app: 40-60. Marketplace/social: 60-90. Prefer fewer, correct, consistent images over exhaustive ones; mark `priority: P0/P1/P2` and generate P0 first.
