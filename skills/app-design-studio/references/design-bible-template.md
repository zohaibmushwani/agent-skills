# Design bible template

The bible is written once (S2), refined into tokens (S3), and then **pasted verbatim at the top of every image prompt**. Short and concrete beats poetic. Keep it under ~25 lines so it fits every prompt.

```
DESIGN BIBLE - <App name>
Product: <one line what it does, for whom>
Platform feel: <Material 3 leaning | iOS-native leaning | neutral>; portrait 9:19.5; UI only, full-bleed, no device frame, no phone mockup, no outer background.
Mood: <3 words, e.g. calm, precise, warm>
Palette: background <hex>, surface <hex>, primary <hex>, accent <hex>, text <hex>, secondary text <hex>, success/warn/error <hex/hex/hex>. Usage ~60% neutral / 30% surface-text / 10% accent.
Typography: headings <font>, body <font>; scale 32/24/20/16/14/12; weights 400/600/700. Sentence case.
Shape: corner radius <8/12/16/28>; buttons <pill|rounded>; cards <flat|soft shadow>.
Spacing: 4/8 grid; screen margin 20; section gap 24-32; list row height 64; touch target >= 48.
Iconography: <outline|filled|duotone> set <Iconify set id, e.g. lucide / solar / phosphor>, 24px, 1.5-2px stroke, one family only.
Imagery: <illustration style | photography style | abstract shapes>; treatment <grain/none>; one image moment per screen at most.
Navigation: <bottom bar with 4 tabs: ...>; top bar <style>.
Components: primary button <style>, input <style>, chip <style>, card <style>.
Status bar: <time 9:41, battery, signal>, light/dark per screen; gesture bar area clear.
Avoid: <from ai-tells-avoid.md + app-specific>.
```

## Direction alternatives (S2)
Write three bibles differing on at least: palette logic (e.g. warm neutral + one accent / deep dark + neon-free accent / pastel duo), type personality (geometric sans / humanist / serif headline + sans body), shape language (soft pill / crisp 8dp / mixed), imagery (illustration / photo / abstract). Name them by feel ("Paper", "Midnight", "Garden"), not "Option A".
Render one hero screen each (usually home) and present side by side. Wait for the pick.

## Locking
After the pick: copy the chosen bible to `DESIGN.md`, derive `tokens.json`, and never edit the bible mid-set. If something must change, change the token, regenerate affected screens, note it in `STATUS.md`.
