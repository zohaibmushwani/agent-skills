# Research-before-build — techniques that worked

Source: shared Claude chat (design-bridge research, Nov 2026). Raw text: `source-chat/design-bridge-research-chat.txt`.
Result of using these: 3 kits (design-bridge, raster-to-figma, app-design-studio) + working Figma MCP/CLI tool.

## Core principle
Complex systems are not written from scratch.
**Search → Shortlist → Verify → License scan → Clone → Study → Note → Implement fresh against our own IR.**
Reuse ideas and permissive-licensed modules; write only the glue and the unique value.

## 1. Dork-style search (not generic web search)
Tell the agent explicitly: "research like an OSINT researcher / hacker, using operators and regex-like dorks, not plain queries."

Operators: `site:` · exact phrase `"..."` · `OR` · exclusion `-word` · `filename:` · `path:` · `extension:` · `topic:` · `language:` · `stars:>N` · `pushed:>date`

Patterns that worked:
```
site:github.com "compose" "figma" export semantics tree plugin -relay
site:github.com "html-to-figma" OR "dom-to-figma" auto layout plugin
site:github.com "figma" "style-dictionary" "compose" tokens kotlin DTCG
site:github.com figma plugin "import json" create nodes "figma.createFrame"
site:github.com python figma plugin bridge websocket "createFrame" MCP
site:github.com google automotive-design-compose DesignCompose
"Paparazzi" OR "Roborazzi" Figma compare screenshot design drift Compose
site:github.com UI element detection screenshot OmniParser OR UIED OR "GUI grouping"
```

### Identifier chaining (the key trick)
After the first round, take **unique identifiers** found inside results (API names, file names, DOM ids) and make them the next dork:
`site:github.com "compose/figma-svg"` · `site:github.com "cmp_a11y_root"`
This finds the source code and anyone else using the same mechanism.

## 2. Multilingual + regional platforms
Tools often never surface in English results. Search by **platform name**, in the local language:

| Region | Platforms | Example query shape |
|---|---|---|
| CN | Juejin, CSDN, Zhihu, V2EX, Gitee | `Figma 转 代码 D2C juejin OR csdn` |
| JP | Zenn, Qiita | `Figma MCP Jetpack Compose 実装 zenn OR qiita` |
| RU | Habr, Ozon/VK talks | `конвертер HTML в Figma плагин код в дизайн habr` |
| KR | Velog, GeekNews, GitHub | `Figma Compose 토큰 자동화 velog` |

Also try 4–5 synonyms of the same idea: design-to-code, d2c, c2d, figma export, UI codegen, image-to-design.

## 3. Verify before trusting
- Every repo URL actually exists (the chat checked all 18 / 34 repos before zipping).
- README claims ("pixel-perfect") are not truth — **read the code**.
- Mark unverified items as `unverified` in the resource list.
- Prefer: recent commits, issue responsiveness, tests, small readable core. Stars are secondary.

## 4. License scan (separate step, always)
Table per repo: license · commercial OK? · reuse as code / ideas only.
Traps seen: YOLO = AGPL, CCimen/imagegen = AGPL, 5 repos with no license (ideas only).
Keep attribution; clone into `references/` (git-ignored), never vendor blindly.

## 5. Finding code cheaply
- Known name → `grep`.
- Unknown name ("how do they map auto-layout to Row?") → local semantic search (EmbeddingGemma 2 + hybrid BM25, e.g. Claude Context Local / semantic-code-mcp, LanceDB). Index **only `references/`**, not our own repo (yet).
- Search finds; **real file read confirms**. Test the index with ~10 real questions (Kotlin coverage unproven).
- Sparse-checkout only needed folders.
- Biggest saving: write `notes/research.md` once per repo; later phases read notes, not repos.
- Use a subagent (Explore) for searching so file dumps stay out of the main context.
- Embeddings only **suggest** (component/token mapping candidates, confidence score). Human approves, saved to file; conversion stays deterministic and fails loudly.

## 6. Kit structure (reusable template)
```
CLAUDE.md                     non-negotiable rules, read-first list, verify commands
.claude/commands/<x>-plan.md      study references -> ask <=4 decisions -> write PLAN.md (no code)
.claude/commands/<x>-execute.md   one phase at a time, tests + gates
docs/ARCHITECTURE.md          spec, IR contract, traps, quality gates
docs/EVALUATION.md            datasets, metrics, targets, baselines
resources/RESOURCES.md        every link grouped by purpose, star = study first
resources/LIBRARIES.md        library per pipeline stage + install lines
resources/LICENSES.md         license scan
resources/clone-references.sh shallow clone (core / all)
```
Rules that mattered in CLAUDE.md:
- One IR; every converter is reader (->IR) or writer (IR->). No direct X->Y.
- Deterministic first, AI second (AI only for naming/grouping/decisions).
- Tokens/components beat raw values; unmapped = fail loudly or visible TODO.
- "Study before writing": read matching reference repo, list reuse (with license) vs fresh.
- Small vertical slices: one adapter, one fixture, one test, green.
- Ambiguous decision -> stop and ask the user.

## 7. App-design-studio lessons (screens pipeline)
- Codex built-in `$imagegen` (no API key), GPT-Image / Gemini MCPs, Google Stitch MCP.
- A PNG is not a handoff: per screen = PNG (look) + HTML with real CSS/tokens (exact values) + spec (behavior). HTML wins on conflict.
- Image models fail on **state/text/counts** more than style: write exact strings and counts first, add "no extra items", QA every image, render store headlines as HTML text.
- Graphics made before the app exists are `concept`; swap in real captures before publishing.
- Human checkpoints: direction pick (S3) and final review (S9).

## 8. Techniques for raster -> design (from the 2nd research)
- Hierarchy + layout are the real bottleneck; text/colour recovery is easy.
- Specialised models for geometry (OCR boxes, masks), VLM only for decisions and names.
- Verify and repair locally per node; never one-shot.
- Componentise repeats and snap to tokens = what makes output flexible.
- Evaluate with resize test (frame width +/-20%), SSIM, token-binding %, auto-layout %.

## Planned skills (next)
- A: `research-before-build` (dorks, multilingual, verify, license scan, clone script, kit generator)
- B: `app-design-system` (screen taxonomy, aesthetic-vs-usability rubric, lint scripts)
- C: `asset-pipeline` (image gen + Iconify, style lock)
- D: compose <-> figma MCP + CLI (already built)

## Still missing
- `app-design-studio-kit.zip` (3rd zip in the chat; not yet downloaded here).

## 9. Method comparison and the funnel (2026-11-18, audio-dance GLES topic) - see RESEARCH-audio-dance-gles.md
Three methods on the same topic, judged R/P/N: web dorks (A) ~95% precision but only what engines index; Sourcegraph code search (B) ~15% - grep-like noise, misses small repos, good only inside a shortlist; GitHub topic + short-phrase repo search (C) ~19% but found the one jackpot nobody else did. Raw "concept coverage" score is a BAD ranking (giant repos win) - rank by judged relevance.
Funnel: concept map (incl. API symbols + file formats) -> repo-level discovery (A + C + awesome lists) -> asset-first search (scarce data + license) -> shortlist/judge (check the repo actually contains source) -> code-level depth ONLY inside shortlist (Sourcegraph/`gh search code` with repo: filters, mine identifiers) -> chain -> verify/license/clone/decide.
Facts: grep.app is behind a bot checkpoint (do not bypass); Sourcegraph stream API works without login; `gh search repos` needs short queries (all words must match) and `--topic`; `gh search code` works with the user's login; check repo trees (README-only repos exist).
