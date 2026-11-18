# Frame recipes and set.json
Codex generates each frame at portrait 9:16 (Play) or 9:19.5 (iPhone); `fit_store.py` centre-crops to the exact size, so keep headlines and key UI away from the outer 5%.

## Frame types (`type` in set.json)
- `poster`: colour field or art fills the frame, huge headline (120-170 px), optional subline, optional proof row (laurels) at the bottom, optional small UI fragment.
- `ui`: headline top 28%, then a UI screenshot (a phone-shaped rounded rect, no device bezel by default) scaled to ~85% width; `crop` selects the part of the screen to show; `pop` lifts one rectangle of the screen out as a floating zoomed card.
- `zoom`: no phone; the cropped UI fragment itself is the hero, scaled up to ~90% width with a shadow.
- `notify`: a notification/lock-screen style card with app icon, title, text over the colour field.
- `panorama`: any of the above, plus a strip image that spans all frames (`panorama.image`, sliced by frame index).

## set.json
{
 "app": "P## set.json
{
 "app": "Plotline", "aspect": "9:16",
 "style": {"look": "cinematic dark colour field, one coral accent", "headFont": "very bold condensed sans-serif",
           "art": "painterly characters seen from behind, no faces"},
 "colors": {"bg": "#121214", "head": "#FFFFFF", "accent": "#FF5A4E", "accentText": "#121214"},
 "panorama": "a red ribbon of film",            // optional motif that crosses frame edges
 "styleFrame": "final/01.png",                   // approved frame 1, attached to frames 2+
 "frames": [
  {"type": "poster", "head": "Drama in 90 seconds", "emph": "90 seconds", "sub": "New episodes every day",
   "scene": "a woman in a red coat on a rainy neon street, seen from behind", "proof": ["1M+ viewers"]},
  {"type": "ui", "head": "Unlock the next twist", "screen": "screens/play-03.png", "pop": "the 'Unlock with 30 coins' button"}
 ]
}
"emph" must be a substring of "head"; "proof" items must be real; "screen" is a real app screen attached as reference.
