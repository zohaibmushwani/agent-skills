# Back press and permissions

## Back
Write a per-screen table. Typical defaults: splash back disabled; the home root and first-launch steps use a double press to exit; other tab roots go to home; system back equals the top-bar arrow; a dirty form or unsaved result shows a Discard sheet; running work asks before cancelling; closing at a result returns to the flow's entry (replace, not push). Avoid loops and duplicate destinations.

## Runtime permissions
1. Ask **before** the screen that needs the permission opens: a rationale sheet first, then the system dialog. If denied, stay on the previous screen and explain there; do not open a screen that cannot do its job. The feature screen re-checks where it is used (the user can revoke in Settings).
2. Four states, never a dead end: granted, not asked, denied (can ask again: "Try again"), permanently denied (send to the app's Settings with an "Open App Settings" action). Offer a no-permission alternative where one exists.
3. Wrap permission APIs in one helper per permission; screens do not call the APIs directly. "Permanently denied" = persisted "asked once" flag + rationale flag, because Android reports the same state before the first ask and after "don't ask again".
