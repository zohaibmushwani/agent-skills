# Research: building an "app name -> full screen repository" design skill (aesthetic vs usability balance)
Date: 2026-11-17. Method: dork + identifier chaining + multilingual (see RESEARCH-TECHNIQUES.md).
Status legend: VERIFIED = page content read directly; LEAD = only seen in search results/aggregators.

## 1. Closest existing work (study first)

| Project | What it gives | Status | License |
|---|---|---|---|
| **Leonxlnx/taste-skill -> `imagegen-frontend-mobile`** (mirror: cdn.jsdelivr.net/npm/@omega3_0/nanoagent@1.1.0/skills/imagegen-frontend-mobile/SKILL.md) | Image-only mobile screen concepts. Dials 1-10 (Design Variance, Density, Art Direction, Clarity, Text Readability, Consistency). **Design bible** locked before generation. **27-point quality check**. Avoid-lists of "AI tells". Regenerate weak screens. | VERIFIED (mirror). GitHub URL guess `leonxlnx/imagegen-frontend-mobile` = 404; real repo is `Leonxlnx/taste-skill` | check |
| **ceorkm/mobile-app-ui-design** (SKILL.md via jsdelivr) | 5-step workflow (context -> UX structure -> visual -> emotion -> polish); concrete numbers: touch >=44pt, thumb-zone CTA, 1-2 fonts, <=4 sizes, 60/30/10 colour, 8-pt grid, 375px base; state list; anti-patterns | VERIFIED | check |
| **awesome-skills/mobile-app-design** | `references/` (ios, android, accessibility-checklist, common-mistakes...), `scripts/check-contrast.py`, `validate-touch-targets.sh` (48x48 strict), `accessibility-audit.sh`; 3-level progressive loading | VERIFIED (README) | MIT |
| **plugin87/ux-ui-agent-skills** | 26 skills + `design-critic` agent, MCP server, 52 gates, tokens/, design-systems/ (2,144 specs), evals/, hooks. Claimed `validate_tokens.py`, `validate_contrast.py` | VERIFIED structure; script behaviour NOT verified | MIT |
| nextlevelbuilder/ui-ux-pro-max-skill | 161 palettes / 67 styles; rule lookup `search.py --domain`; accessibility tier "critical" (4.5:1). Guidance, not a measuring tool. One listing flags runs-shell/credentials -> audit before install | LEAD | check |
| Premium Mobile App Interface Director (agensi.io) | Pipeline: Screen Inventory -> Screen Hierarchy -> Navigation; system states: loading, empty, error, offline, permission-denied | LEAD | ? |
| lcanady/ui-skill, jwynia/agent-skills (frontend-design), Community-Access/accessibility-agents (design-system-auditor), cantagestudio/cosmicatlaspacker (accessibility-contrast-audit w/ tokens.json) | token-first workflow, a11y/contrast/touch audits | LEAD | ? |
| pjt222/agent-almanac `review-ux-ui` | Nielsen heuristics + WCAG 2.1 + flow efficiency review | LEAD | ? |
| Google Stitch + DESIGN.md (KR brunch article), gstack design-consultation (CN article) | DESIGN.md as the style contract | LEAD | ? |

## 2. Academic / evaluation sources (for the rubric)
- **UICrit** (arXiv 2407.08850): LLM prompt chain gives design feedback + bounding boxes + quality ratings; few-shot/visual prompting gave +55%.
- **MLLM as a UI Judge** (arXiv 2510.08783): MLLM ratings vs human on aesthetic appeal, usability, trustworthiness - use to see whether aesthetic scores predict usability scores.
- **UI-Bench** (arXiv 2508.20410): pairwise expert comparison of AI text-to-app tools; absolute ratings are noisy -> prefer **pairwise** compare in our eval.
- **UXBench** (arXiv 2606.16262): scores *actionability* of LLM UX reports by feeding them to a repair agent.
Gap: no paper found that explicitly models the aesthetic-usability effect as an LLM rubric.

## 3. Findings that shape our skill
1. **Skill = short, opinionated, "right altitude"** (Anthropic frontend-design blog): name the model's default (AI slop), ban specific defaults, give concrete rules, load just-in-time, bundle scripts, iterate with skill-creator. ~400 tokens for the core.
2. **Design bible first, then screens** (taste-skill). Lock platform, device scale, palette, type scale, spacing, radius, icon style, nav model, shadows; reuse in every prompt. This fixes cross-screen drift.
3. **Dials are a cheap way to express the aesthetic/usability balance** (Clarity=10, Readability=10, Variance/Art direction tunable per app category: fintech/health up trust+calm, down variance).
4. **Image models are checked by a checklist, not trust.** taste-skill's own tessl review notes it lacks a validate-then-fix loop -> our skill must add: measurable checks + regenerate loop with cap.
5. **Usability rules are measurable; aesthetics mostly isn't.** So: encode usability as scripts (contrast, touch target, font-size min, spacing grid, token-lint, state coverage) and aesthetics as a rubric + pairwise comparison + human pick at the style gate.
6. **Thresholds disagree** - choose and document: touch 44pt iOS / 48dp Android (WCAG 2.5.8 24px is only the legal floor); text 4.5:1, large 3:1; body >=16sp (or 14sp min secondary); grid 4/8.
7. **State coverage is the usual gap:** default, loading (skeleton), empty (guidance + CTA), error (distinct from empty), offline, permission-denied, success.
8. **AI can't replace aesthetic judgement** (CSDN, Habr, Korean columns agree): good for first drafts, contrast checks, boilerplate, checklist audits. Keep a human taste gate.
9. **Three layers** (CN article): System Prompt = global rules, Skill = constrains actions, Design System (DESIGN.md/tokens) = what makes it look good.
10. **Generation vs validation separated, possibly different tools** (KR comparison: ui-ux-pro-max as balanced start, Impeccable for polishing existing, Hallmark for removing "AI-site feel").

## 4. Skill vs MCP vs prompt - recommendation
- **Skill (primary):** workflow + references + scripts. Triggers on "design app X / screens repo".
- **Scripts inside the skill (not MCP):** `contrast_check.py`, `touch_target_audit` (on HTML/Compose/JSON), `token_lint`, `state_coverage`, `grid_audit`. Deterministic, no server.
- **MCP only where state/API needed:** image generation (gpt-image / Runware), Iconify, Figma bridge (already built). These stay separate tools the skill calls.
- **Prompt (thin):** one reusable "mission prompt" that invokes the skill; do not put the knowledge in the prompt.

## 5. Proposed skill layout (to build next)
```
app-design-studio/
  SKILL.md                      workflow S0..S9 + gates, <=500 lines
  references/
    screen-taxonomy.md          splash, language, onboarding, auth, home, features, details, settings,
                                states, dialogs, sheets, components, interactions
    states-checklist.md
    aesthetic-vs-usability.md   dials, rubric (hierarchy, rhythm, consistency / tap, contrast, thumb-zone, size)
    design-bible-template.md
    ai-tells-avoid.md           from taste-skill + ceorkm anti-patterns
    prompt-templates/           per screen type, exact strings + counts first, "no extra items"
    platform-ios.md platform-android.md
  scripts/                      contrast, touch-target, token-lint, state-coverage, grid, qa-report
  assets/templates/             DESIGN.md, tokens.json, screen-spec.md, repo skeleton
  evals/                        3 app briefs (fitness, PDF reader, finance), with/without-skill, pairwise compare
```
Pipeline: brief -> screen inventory -> design bible + 3 style directions (HUMAN PICK) -> tokens -> screens (portrait, no device frame, high fidelity) -> state variants -> auto checks + rubric -> regenerate (max N) -> repo export (PNG + HTML/tokens + spec) -> optional Compose/Figma bridge.

## 6. Open items / not verified
- taste-skill real GitHub path + license; 27-check list read from a mirror, not repo.
- plugin87 script behaviour and licence of scripts; ceorkm and awesome-skills licences (README only).
- Hindi/Urdu/Arabic sources not searched; JP/KR/CN/RU searches returned thin results for "usability+aesthetics" - mostly skill catalogs.
- `app-design-studio-kit.zip` from the earlier chat still not downloaded.

## Sources
- https://github.com/awesome-skills/mobile-app-design
- https://cdn.jsdelivr.net/gh/ceorkm/mobile-app-ui-design@main/SKILL.md
- https://cdn.jsdelivr.net/npm/@omega3_0/nanoagent@1.1.0/skills/imagegen-frontend-mobile/SKILL.md
- https://github.com/plugin87/ux-ui-agent-skills
- https://claude.com/blog/improving-frontend-design-through-skills
- https://tessl.io/registry/skills/github/Leonxlnx/taste-skill/imagegen-frontend-mobile/review
- https://arxiv.org/html/2407.08850v3 (UICrit) · https://arxiv.org/html/2510.08783v1 · https://arxiv.org/pdf/2508.20410 · https://www.alphaxiv.org/abs/2606.16262.md
- https://skills.sh/bitjaru/styleseed/ux-feedback · https://productbuilder.net/skills/empty-states
- https://www.woshipm.com/ai/6379844.html · https://zenn.dev/tmasuyama1114/articles/apple_design_skills · https://habr.com/ru/articles/881358 · https://brunch.co.kr/@ghidesigner/473
