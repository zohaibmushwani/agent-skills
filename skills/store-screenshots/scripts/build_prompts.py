#!/usr/bin/env python3
"""build_prompts.py - write one complete GPT Image (Codex) prompt per store screenshot frame from set.json (stdlib only).

Usage: python build_prompts.py set.json prompts_dir
Writes prompts_dir/NN.md (the exact text to send) and prompts_dir/NN.refs.txt (reference images to attach: the real UI
screens plus the approved style frame). Send each file's text unchanged with reference_images from the .refs.txt.
"""
import json
import sys
from pathlib import Path

FORMAT = ("FORMAT: One App Store / Google Play marketing screenshot, portrait {ar}. The whole image is the screenshot itself, "
          "full-bleed. No device mockup around the whole image, no outer background, no border, no watermark.")


def frame_prompt(s, f, i, n):
    c = s.get("colors", {})
    st = s.get("style", {})
    L = [FORMAT.format(ar=s.get("aspect", "9:16")), "",
         f"SET STYLE (identical in every frame of this {n}-frame set): {st.get('look', '')}",
         f"Colours: dominant field {c.get('bg')}, headline text {c.get('head')}, accent {c.get('accent')} (text on accent {c.get('accentText')}).",
         f"Headline typography: {st.get('headFont', 'very bold condensed sans-serif')}, huge, tight leading, top third of the frame, centred, max 2 lines.",
         f"Art direction: {st.get('art', '')}", ""]
    L.append(f"FRAME {i}/{n} - type: {f['type']}.")
    head = f.get("head", "")
    L.append(f'HEADLINE, exact text, spelled exactly, nothing else in the headline: "{head}"'
             + (f' - the words "{f["emph"]}" sit on an accent highlight box' if f.get("emph") else ""))
    if f.get("sub"):
        L.append(f'SUBLINE under it, smaller, exact text: "{f["sub"]}"')
    if f["type"] == "poster":
        L.append(f"Composition: poster. {f.get('scene', 'A bold visual of the app promise fills the lower two thirds.')} Little or no UI.")
    elif f["type"] in ("ui", "zoom"):
        L.append("Composition: show the attached app screen exactly as it is (same layout, text, icons, colours) - do not redesign or invent UI. "
                 + ("Show it inside a modern phone, slightly tilted, lower 70% of the frame. " if f["type"] == "ui" else "No phone: crop to the important part and enlarge it as a floating card with a soft shadow. ")
                 + (f"Pop-out: enlarge this element and let it break out past the phone edge as a floating card: {f['pop']}. " if f.get("pop") else "")
                 + f.get("scene", ""))
    elif f["type"] == "notify":
        L.append(f'Composition: a large notification card in the middle (app icon, title "{f.get("noteTitle", s.get("app", ""))}", text "{f.get("noteText", "")}"), {f.get("scene", "over the colour field")}.')
    if f.get("sticker"):
        L.append(f'One small tilted sticker with exact text "{f["sticker"]}".')
    if f.get("proof"):
        L.append("Proof row at the bottom with laurels, exact texts: " + ", ".join(f'"{p}"' for p in f["proof"]) + ".")
    if s.get("panorama"):
        L.append(f"Panorama: this frame is part {i} of {n} of one continuous scene; {s['panorama']} must continue across the left and right edges.")
    L += ["", "TEXT RULES: render only the quoted texts above, each exactly once, correctly spelled; no other words, no fake logos, no lorem ipsum.",
          "DO NOT ADD: real brand logos, real celebrities, star ratings or awards not listed above, extra phones, watermarks, borders."]
    return "\n".join(L) + "\n"


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    sp = Path(argv[1])
    s = json.loads(sp.read_text(encoding="utf-8"))
    out = Path(argv[2])
    out.mkdir(parents=True, exist_ok=True)
    n = len(s["frames"])
    for i, f in enumerate(s["frames"], 1):
        if f.get("emph") and f["emph"] not in f.get("head", ""):
            print(f"frame {i}: emph not in head", file=sys.stderr)
            return 1
        (out / f"{i:02d}.md").write_text(frame_prompt(s, f, i, n), encoding="utf-8")
        refs = [str((sp.parent / f["screen"]).resolve())] if f.get("screen") else []
        if s.get("styleFrame") and i > 1:
            refs.append(str((sp.parent / s["styleFrame"]).resolve()))
        (out / f"{i:02d}.refs.txt").write_text("\n".join(refs) + "\n", encoding="utf-8")
    print(f"wrote {n} prompts to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
