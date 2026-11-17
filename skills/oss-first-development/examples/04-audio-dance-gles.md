# Research: OpenGL ES Android app - 3D character dancing + audio-reactive effects (music / mic)
Date 2026-11-18. This run compares THREE discovery methods on the same topic. Labels (R/P/N) are my judgement from verified facts, not automatic.

## 0. Answer in one paragraph
Nothing ready-made does "3D female character dances to the music with effects on Android", so the app is an **assembly of 3 pillars**: (1) audio -> features (FFT/beat) -> shader uniforms, (2) skinned character + dance motion playback, (3) post-FX chain driven by audio. Each pillar has good open-source donors (below). The scarce resource is **dance motion data + model/music licenses**, not code. Biggest design decision: **raw OpenGL ES vs Filament** (Filament gives glTF skinning + bloom/DoF/vignette out of the box, Apache-2.0, GLES backend exists).

## 1. Pillar donors (judged)  R = usable base/template, P = learn-from/partial, N = noise
### Pillar 1 - audio -> GL (uniforms/texture)
| Repo | Label | Notes | License |
|---|---|---|---|
| **nekocode/MusicVisualization** | R | Shadertoy shaders ported to Android GLES; FFT + waveform from system `Visualizer` -> **texture** the shader samples (iChannel-style). Cleanest template. ~494 stars | Apache-2.0 |
| markusfisch/ShaderEditor | R | on-device GLSL editor + live wallpaper (user's "shader editor" idea). Not audio by default | MIT |
| minthubk/waveinapp (+forks Cleveroad, icss91) | P | GLES2 audio wave view on `Visualizer` | ? |
| Yalantis/Horizon | P | equalizer shader with amplitude uniform | ? |
| projectM (projectM-visualizer/projectm) | P | MilkDrop engine, GLES3, F-Droid app exists | LGPL-2.1 (verify) |
| lostjared/shaders, sandner-art/Audio-Shader-Studio, TornaxO7/vibe | P | audio feature -> uniform mapping ideas (vibe is desktop Rust, AGPL) | mixed |
| Ipsedo/Spectrix | P | Android visualizer app (found only by topic search) | GPL-3.0 |
| JorenSix/TarsosDSP | P | onset/beat detection algorithms in Java (ideas; GPL-3.0 -> reimplement) | GPL-3.0 |
### Pillar 2 - skinned character + dance motion
| Repo | Label | Notes | License |
|---|---|---|---|
| **google/filament** | R (engine choice) | glTF 2.0 via gltfio incl. skinning/morph, PBR, post-FX; Android Kotlin helpers; ~20.7k stars | Apache-2.0 |
| the3deer / andresoviedo **android-3D-model-viewer** | R | GLES skeletal animation, DAE/glTF/OBJ; FBX static only | LGPL-3.0 (WenlinMao fork) - verify upstream |
| the3deer/android-3D-engine | P | Android OpenGL 3D engine | MIT |
| TheThinMatrix/OpenGL-Animation | R (learning) | classic skeletal-animation reference | ? |
| benikabocha/**saba** | R (format) | C++ PMD/PMX/VMD load+play (desktop OpenGL/DX/Vulkan samples) -> port render to GLES | (verify) |
| ReaNAiveD/**mdanceio** | R (format) | Rust PMX+VMD; Android demo mentioned | (verify) |
| hujyjjkkth/**MMD-Studio** | P (feature spec) | Android MMD viewer/editor; **README only, no source**; Babylon.js render; features: VMD play/blend/mirror/loop, audio folder, bloom/DoF/chromatic/vignette, GLB export | MIT label, binary release |
| kool-engine/kool, GearVRf, libgdx (+mgsx-dev/gdx-gltf), Rajawali, re-ovo/k3d, mikikg/AndroidJgltfViewer, lwjglbook | P | engines/loaders with skinning or glTF | mostly Apache/MIT |
| kibotu/glTF-Renderer | N | hello-world only, archived, CC BY-NC | NC |
### Pillar 3 - dance data and generation
- **Assets are the bottleneck:** VMD motions / PMX models carry per-asset licenses (many non-commercial); Mixamo FBX/glTF has Adobe terms; verify before shipping.
- Mixamo pitfall (verified via issues/forums): animation attached to parent armature, needs retarget/re-export (Blender) before glTF skinning works.
- AI generation: **EDGE** (Stanford, MIT code, research-grade) and **Bailando** (AIST++) generate dance from music - offline/server-side, not real-time on phone.
- Sync approach (hypothesis, unverified): drive motion time from the **audio clock**, not the frame clock; tempo-match playback speed to detected BPM; blend loops on beat.

## 2. Pipeline sketch (to validate)
```
Audio: MediaPlayer/ExoPlayer or file decode  |  mic: AudioRecord(RECORD_AUDIO)
   -> FFT (own/KissFFT) -> bands (bass/mid/treble) + spectral-flux onset + BPM -> AudioFeatures (smoothed)
Renderer: GLES 3.0 (or Filament) : skinned mesh (glTF/VMD->internal) + AnimationPlayer(audio clock)
   uniforms: uBass,uBeat,uTime ; audio texture (nekocode pattern) ; post-FX: bloom, chromatic aberration, glitch, vignette, camera shake on beat
UI: Compose (song picker, effect presets, camera) ; recorder (MediaCodec) optional
```

## 3. Method comparison (same topic, same judging)
Counts are approximate and judged by me; "relevant" = R or P.

| Method | What I did | Candidates | Relevant | Precision | Unique valuable finds |
|---|---|---|---|---|---|
| **A. Web dorks + multilingual** (EN/ZH/JA/RU) | 8 searches, `site:` + exact terms + format names + CN/JP/RU wording | 27 repos | ~26 | **~95%** | nekocode, ShaderEditor, saba, mdanceio, OpenGL-Animation, EDGE/Bailando, babylon-mmd, DanceXR (closed). CN/JA/RU searches mostly **repeated** the EN hits (no new repos), they added tutorials (LearnOpenGL-Android CSDN) |
| **B. Code search (Sourcegraph stream API, my `code_chain.py`)** | 2 rounds of concept queries (file-level AND), co-occurrence ranking, identifier mining | ~62 unique | ~9 | **~15%** | kool-engine, TarsosDSP, GearVRf, lwjglbook, haxademic, kde-shader-wallpaper: **"implementation donors"** (big repos containing the pattern). Missed all small named projects; top ranks were JDK/Android-framework noise (tokens like `VMD`, `beat`, `bones` match everywhere) |
| **C. GitHub repo search by topic + short query (human-style)** | 7 queries with `--topic`, short phrases via `gh search repos` | ~70 listed | ~13 | **~19%** (but best-ranked hits are strong) | **MMD-Studio** (found by no other method), Spectrix, android-3D-engine, rsahlin/graphics-by-opengl, ouyangpeng/OpenGLESDemo, TaoShaderToy, skia-labs |
| D. Sourcegraph with repo filter `repo:has.topic(...)` | 3 queries | 10 repos, 2 queries empty | ~1 | low | finds `google/filament`; topics too sparse |

Failure modes observed
- **A**: great precision, but dependent on whatever the search engine indexes; ignores code that is not described in text.
- **B**: grep-like precision problem with common tokens; **public index misses/ranks small repos** (nekocode appeared only when scoring by repo, not in top results); good only AFTER you have a shortlist.
- **C**: long multi-word queries return **nothing** (all words must match); needs short phrase + topic; depends on authors tagging topics.
- **My "shared concept-coverage score" was a bad yardstick**: it ranked `Mac.apk`, `androidx`, `LineageOS frameworks` highest (7/9, 4/9) because giant repos contain every token, and scored relevant small repos 0 (unindexed or no match). Do not rank by raw coverage; rank by **judged relevance** or normalise by repo size/IDF.
- grep.app is behind a Vercel bot checkpoint (not bypassed). GitHub code search via `gh` works for logged-in users (rate-limited).

## 4. Best method = a funnel (hybrid), not a single tool
1. **Concept map**: pillars + synonyms + *API symbols* + *file formats/extensions* (`.vmd .pmx .glb`, `getFft`, `glUniform1f`).
2. **Repo-level discovery (precision)**: web dorks (A) + `gh search repos --topic <t> "<2-3 words>"` (C) + awesome lists. Multilingual only for ecosystems that are regional (MMD = JA/CN); otherwise skip.
3. **Asset-first search**: look for the scarce data (VMD/BVH/glTF dance clips, free models) and their licenses *before* code.
4. **Shortlist -> judge** R/P/N by reading READMEs/trees (check for source! MMD-Studio had none) + license.
5. **Code-level depth only inside the shortlist**: Sourcegraph/`gh search code` with `repo:` filters to locate the exact files (skinning shader, FFT->uniform) + mine identifiers.
6. **Chain**: new identifiers/format names from step 5 -> repeat step 2 until no new R/P repos appear (usually 2-3 rounds).
7. **Verify -> clone -> notes -> reuse/adapt/idea/write decision**.

## 5. Feasibility notes (what is possible)
- Audio-reactive shader effects on Android GLES: **proven** (nekocode, ProjectM, ShaderEditor).
- Skeletal character on GLES: **proven** (several viewers); dance playback via glTF clips: straightforward; via VMD: needs PMX/VMD parser (saba/mdanceio as donors) + IK/physics (non-trivial).
- Real-time AI dance generation on phone: **not realistic**; pre-generate or use clip library with beat-synced blending.
- Mic-driven visuals need `RECORD_AUDIO`; playback visualisation via `Visualizer` also needs it (verify current API behaviour/policy for target SDK).
- Licensing/legal: model + motion + music rights per asset; ship your own/CC0 assets for the first release; check Play policies for audio permissions and user-generated content.

## 6. Not verified / gaps
Licenses of saba, mdanceio, projectm (version), OpenGL-Animation, waveinapp, Horizon; whether `Visualizer` still works well on recent Android; MMD-Studio internals (closed); Babylon-in-WebView vs native GLES performance; whether Filament's GLES backend is acceptable for the "OpenGL ES" requirement; no Qiita/Zenn/Juejin tutorials found for Android+VMD; Korean search not run; Sourcegraph public index coverage unknown.

## 7. Next steps (prototype order)
P0 GLSurfaceView + nekocode-style audio texture + one shader (proof of audio->GL). P1 load one glTF skinned model and play one clip (Filament vs raw GLES spike, pick one). P2 audio clock sync + beat/BPM -> playback speed + camera shake. P3 post-FX chain (bloom/chromatic/vignette) with audio uniforms. P4 VMD/PMX import (optional). P5 Compose UI, recorder, presets. P6 licenses + Play policy.

## Tools produced in this run
`research/tools/code_chain.py` (concept co-occurrence mining + identifier chaining on Sourcegraph stream API, `--meta` adds stars/license via `gh`), `research/tools/coverage.py` (shared yardstick - see warning above), examples in `research/tools/examples/`.

## Sources
nekocode/MusicVisualization https://github.com/nekocode/MusicVisualization · ShaderEditor https://github.com/markusfisch/ShaderEditor · saba https://github.com/benikabocha/Saba · mdanceio https://github.com/ReaNAiveD/mdanceio · MMD-Studio https://github.com/hujyjjkkth/MMD-Studio · filament https://github.com/google/filament · android-3D-model-viewer https://github.com/the3deer/android-3D-model-viewer · android-3D-engine https://github.com/the3deer/android-3D-engine · OpenGL-Animation https://github.com/TheThinMatrix/OpenGL-Animation · projectM https://github.com/projectM-visualizer/projectm · EDGE https://github.com/Stanford-TML/EDGE · Bailando https://github.com/lisiyao21/Bailando · TarsosDSP https://github.com/JorenSix/TarsosDSP · babylon-mmd https://www.npmjs.com/package/babylon-mmd · Sourcegraph stream API https://sourcegraph.com/.api/search/stream
