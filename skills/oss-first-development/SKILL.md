---
name: oss-first-development
description: Before writing a complex system from scratch, find, evaluate, reuse and adapt existing open-source code, libraries, tools and MCP servers, then build only the glue or the improvement. Uses targeted web dorks (site:, exact phrases, file formats, API symbols) chained on identifiers from each result, optionally a long-tail GitHub topic sweep and user-supplied seed repos; verifies repos contain source, checks licenses (MIT/Apache vs GPL/AGPL/none/non-commercial), labels each project base / learn-from / noise, and writes a reuse-adapt-idea-or-write decision, clone script and build plan. Use when the user wants to build a complex app, tool or backend, asks "is there a library/repo for X", "kya koi project hai", wants to avoid reinventing the wheel, compare existing implementations, convert A to B (SVG to Compose), clone an existing product, or says "research first" or "don't write from scratch".
---

# oss-first-development

Principle: **look at what exists before you write anything; write only what does not exist or what you can do better.** A complex system assembled from proven parts is faster, less buggy and easier to defend than a rewrite - and "better than existing" becomes a concrete, checkable claim.

## The one method: dork, then chain
Five real research runs (see `examples/`) tested three discovery methods on the same topic and judged every result. Web dorks won: **~95% of what they returned was relevant** and they surfaced the projects that were actually usable as bases. Repo search by GitHub topic (~19%) and public code search (~15%) returned mostly noise or repos with no source. So this skill uses **one** discovery method and keeps the others only as helpers:

- **Discovery = targeted web dorks + identifier chaining** (this skill's core, below).
- Code search (`scripts/code_chain.py`, `gh search code`) is **not** for discovery; use it only *inside an already shortlisted repo* to find the exact file.
- Regional-language queries are added **only** when the ecosystem itself is regional (MMD -> JA/CN, Shadowsocks/Xray -> CN/RU); otherwise they just repeat English hits.

## Workflow
Work in `research/<topic-slug>/` (`scripts/scaffold_kit.py <topic>` creates it). Keep notes in files; later phases read notes instead of re-reading repos.

1. **Map.** Split the goal into 3-6 *pillars*. For each write: plain words, synonyms, **API symbols** (`getFft`, `glUniform1f`), **file formats** (`.vmd`, `.glb`), and the **scarce resource** (assets, data, licenses, servers). `scripts/dork_builder.py concepts.json` turns this into ready queries.
2. **Dork.** Run 6-12 queries in parallel: `site:github.com "exact phrase" -noise`, API symbol + platform, format name + platform, "awesome ..." lists, package registries. Prefer specific, quoted, mixed queries; avoid generic words. Add the regional variants only if the ecosystem is regional. Also search for **finished end-user apps** (Play Store, F-Droid, product pages) that do what you want: they are the feature spec and the "better than existing" baseline, and a past eval showed this step gets skipped.
3. **Chain.** Open the best 3-5 hits, take the **unique identifiers** inside them (class names, flags, file names, DOM ids, crate names) and make those the next dork (`site:github.com "compose/figma-svg"`). Repeat 2-3 rounds; stop when a round adds no new useful repo.
3b. **Sweep the long tail (optional, adds recall).** Stars hide small useful repos that sit on page 2-3 of a topic. Take the topics you saw on good hits, run `scripts/topic_sweep.py sweep.json` (pages through each topic, ranks by relevance not stars, prints a "hidden gems" table), then judge the gems like any other lead. Treat it as a supplement to dorks, not a replacement; Measured on the audio-dance topic (2757 repos from 15 tags/queries): it surfaced permissive, source-containing, recently updated repos that the dork rounds had missed, e.g. an Android audio-reactive GLES app with a hand-written FFT (Apache-2.0, 1 star), an Android real-time visualizer (MIT, 0 stars) and a Mixamo-to-MMD motion retargeter (MIT, 3 stars); all verified with `repo_probe.py`. Cost: ~4 minutes, no extra tokens. Log how many finds became R/P (see `examples/audio-dance.sweep.md`).
3c. **User seeds come first.** If the user hands over tags, repo links or "this one was useful because X", treat them as the highest-priority leads: probe the repos, extract identifiers from them for new dorks, sweep their tags. A human who browses a whole tag list finds things no query does. Record the seed list in `research/<slug>/repos.txt` and say which finds came from the user.
4. **Verify.** `scripts/repo_probe.py repos.txt` - exists, stars, license class, last push, archived, and **does the tree contain source** (README-only and binary-release repos exist). Mark every claim VERIFIED (read it) or LEAD (snippet only).
5. **Judge.** Label each repo **R** (usable base), **P** (learn-from), **N** (noise) with one line of evidence. Never rank by keyword counts. (`references/judging-and-decisions.md`)
6. **Locate.** For each R/P repo, read the real files that matter (use code search only here, restricted to that repo). READMEs overstate.
7. **Decide.** One row per R/P project: **reuse as-is / adapt / idea only / write fresh**, the license reason (`references/license-matrix.md`) and the *gap* it leaves. Unfilled gaps are the real design work.
8. **Plan.** Recommended architecture, decisions the user must make, what is NOT verified, prototype order, clone script (`scripts/make_clone_script.py`). Template: `templates/research-doc.md`. Present and stop for the user's decisions; do not start building inside this skill.

## Rules that keep it honest
- **Every reference is a clickable link.** In notes and in the final reply, write each repo as `[owner/name](https://github.com/owner/name)`, each key file as a permalink `[Timeline.kt](https://github.com/owner/name/blob/<branch>/path/File.kt)`, and each docs page or app as `[title](url)`. Never a bare name, a bare path or a backticked URL. Put the link in the first table column and again in a closing "Sources" list. `repo_probe.py` already prints linked repo names; keep them.
- **Study before writing:** read the matching file in a reference repo and list what you reuse (with license) vs write fresh.
- **License is a hard gate.** GPL/AGPL code can be studied but not copied into a closed app; no license = ideas only; non-commercial blocks commercial use.
- **Check that source exists.** A README claiming MIT with no code is a feature spec, not a donor.
- **Do not bypass bot protection** (grep.app's checkpoint, Cloudflare). If a page needs the user's browser, ask them to open or paste it.
- **Privacy:** never put the user's name, email, project or private details into queries.
- Report what was **not** verified and what failed.
- Reply in the language the user writes in; queries and file names stay English plus the target language where useful.

## Reference map
- `references/search-techniques.md` - dork patterns, identifier chaining, format/symbol/asset-first queries, awesome lists, registries, when to go regional.
- `references/judging-and-decisions.md` - R/P/N rubric, VERIFIED/LEAD, decision matrix, gap analysis, "better than existing".
- `references/license-matrix.md` - what each license allows.
- `references/code-search-backends.md` - helper only: Sourcegraph stream API, `gh search`, limits, what is blocked.
- `templates/` - `research-doc.md` (the 8-section document), RESOURCES / LICENSES / DECISIONS skeletons.
- `scripts/` - `dork_builder.py`, `repo_probe.py`, `scaffold_kit.py`, `make_clone_script.py`, `code_chain.py`, `topic_sweep.py` (Python 3 stdlib; `gh` CLI optional but recommended).
- `examples/` - five real runs (app-design skill, VPN app with Rust/NDK, SVG editor for Android, audio-reactive dancing 3D character in OpenGL ES) and the technique log with the measurements.
