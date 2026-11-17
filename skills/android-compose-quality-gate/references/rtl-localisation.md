# RTL and localisation
- Use **start/end**, never left/right (`paddingStart`, `Arrangement.Start`, `Alignment.Start`). Mirror directional icons (`autoMirrored`), arrows, chevrons, progress direction.
- Images composed against text are flipped in RTL (`graphicsLayer { scaleX = -1f }` guarded by `LayoutDirection`). A screen is not RTL-ready until its **cards**, not only its rows, are checked mirrored.
- Support every `res/values-*` locale; Urdu, Arabic, Persian, Hebrew are RTL. Translated text must fit.
- Check each screen in LTR and RTL, and in German (long words) and Arabic/Urdu.

## Translation standards
- **Tone:** native, polite, consistent with the app; Arabic uses Modern Standard Arabic.
- **Length:** concise enough for fixed-height buttons, chips, tabs and cards without clipping or ugly wrapping. Tight labels use the short term apps in that domain use.
- **Placeholders:** preserve specifiers exactly (`%1$s`, `%2$d`, `%s`, `%d`), same indexes, none dropped.
- **Plurals:** full CLDR forms where the language needs them (Arabic: zero, one, two, few, many, other).
- **Punctuation and escaping:** Arabic punctuation (`؟ ، …`); escape XML (`\'`, `&amp;`, `&lt;`, `\"`).
- Run `scripts/strings_audit.py app/src/main/res` after any string change.
