# Search techniques (the one method: dork + chain)

Why dorks win: a specific, quoted, operator-rich query reads like what the target page itself says, so the engine returns pages that are *about* the thing rather than pages that mention one of your words. Measured precision ~95% vs ~15-19% for topic search and code search.

## Contents
1. Operators  2. Query families  3. Identifier chaining  4. Asset-first  5. Awesome lists and registries  6. Regional rules  7. Stop rules  8. Mistakes seen

## 1. Operators (web search)
`site:github.com` - restrict. `"exact phrase"` - literal. `OR` - alternatives. `-word` - exclude noise (`-relay`, `-tutorial`). `intitle:`, `inurl:` - when the engine supports them. Some engines drop `site:`/`OR`; if results look unrestricted, add "github" as a plain word and re-check the URLs. Keep each query to 1 purpose.

## 2. Query families (run several in parallel)
| Family | Shape | Example |
|---|---|---|
| Product + platform | `site:github.com <thing> <platform> <language>` | `site:github.com android svg renderer compose "ImageVector"` |
| API symbol | `"<symbol>" <platform>` | `"Visualizer" "getFft" GLSurfaceView` |
| File format | `<format> <platform> viewer OR loader` | `PMX VMD android OpenGL ES` |
| Architecture | `<product> architecture <tech>` | `mullvadvpn-app android architecture rust daemon kotlin gRPC` |
| Policy/spec | official site + exact policy words | `Google Play VpnService declaration requirements` |
| Comparison | `<A> vs <B> <aspect>` | `flutter_svg vector_graphics compiler vs react-native-svg` |
| Awesome/list | `awesome <topic> <platform>` | `awesome audio visualizer android shaders` |
| Registry | `crates.io / npm / pub.dev / klibs.io <topic>` | `klibs.io svg compose` |
| Failure/limits | `<tool> limitations OR "does not support"` | `AndroidSVG filters not supported` |

## 3. Identifier chaining (what makes it deep)
After each round, mine the top results for **unique identifiers** and turn them into the next queries:
- file/class names (`compose/figma-svg`, `proxydroid-tun2socks`), DOM ids (`cmp_a11y_root`), flags (`daemon_auto_start`), crate/package names, JNI function names, shader uniform names (`iChannel0`, `u_jointMatrix`).
- the *dependencies* of a good project (its Cargo.toml/Gradle/package.json) - the project's choices are free research.
- the *credits/acknowledgements* section - authors list the projects they built on.
Round limit 3; each round must add at least one new R/P repo or you stop.

## 4. Asset-first (when data is scarce)
Some products are limited by data, not code (dance motions, fonts, models, datasets, server images, test suites). Search for the asset and its **license** before code: `"free" "CC0" motion capture dance .bvh`, `test suite svg conformance MIT`. A perfect codebase with unusable assets is a dead end.

## 5. Awesome lists and registries
Awesome lists and `awesome.ecosyste.ms`, klibs.io (Kotlin multiplatform), crates.io, pub.dev, npm, Maven Central, PyPI pages summarise ecosystems cheaply and list licenses. Use them to **expand** an already good seed, not to start blind.

## 6. Regional rules (when to add CN/JA/KO/RU)
Add them only if the ecosystem is regional: MMD/VMD (JA, CN), Shadowsocks/Xray/sing-box (CN, RU), Figma-to-code agents (CN), design-token automation (KR). Search by **platform name + local words**, not by translating the whole query:
| Region | Platforms | Shape |
|---|---|---|
| CN | Juejin, CSDN, Zhihu, V2EX, Gitee | `<topic 中文> juejin OR csdn` |
| JA | Zenn, Qiita | `<topic 日本語> zenn OR qiita` |
| RU | Habr | `<тема> habr` |
| KR | Velog, GeekNews, Brunch | `<주제> velog OR geeknews` |
For non-regional topics (SVG rendering, Compose, OpenGL basics) regional searches mostly repeated the English hits - skip them.

## 7. Stop rules
Stop a chain when two consecutive queries add no new R/P repo, or you have 2-3 verified R candidates per pillar. Do not keep searching to feel safe; write the gap list instead.

## 8. Mistakes seen in practice
- Long multi-word natural-language queries - the engine drifts; use quoted phrases + one operator.
- Trusting a mirror/aggregator page for license or activity - open the repo.
- Counting keyword hits as relevance (giant repos match every token).
- Missing that a repo is README-only/binary-release.
- Searching for code when the bottleneck was assets or a policy.
