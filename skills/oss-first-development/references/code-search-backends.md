# Code search backends (helper only - not for discovery)

Measured: code search returned ~15% relevant results when used for discovery (tokens like `bones`, `VMD`, `beat` match JDK/framework code). Use it **inside a shortlist** to find the exact file.

| Backend | Works? | Use |
|---|---|---|
| **Sourcegraph stream API** `https://sourcegraph.com/.api/search/stream?v=V3&q=<query>` (header `Accept: text/event-stream`) | yes, no login (at time of testing) | regex/literal, `lang:`, `AND/OR`, `repo:^github\.com/o/r$`, `select:repo`, `count:`, `fork:`/`archived:` |
| `gh search code "<q>" --repo o/r --language kotlin` | yes if the user is `gh auth login`ed | file-content search, rate-limited (~10/min) |
| `gh search repos "<2-3 words>" --topic <t> --sort stars` | yes | repo-level; **long queries return nothing** (all words must match) |
| `gh api repos/o/r`, `/languages`, `/git/trees/HEAD`, `/readme` | yes | metadata, language bytes, tree (source present?), README |
| grep.app | **blocked** by Vercel bot checkpoint | do not bypass |
| Cloudflare-protected pages (claude.ai shares, etc.) | blocked for headless | ask the user to open/paste, or use their own logged-in browser extension |

Sourcegraph query tips: `context:global fork:no archived:no lang:Kotlin getFft AND glUniform`. Scope to a repo list: `repo:^(github\.com/a/b|github\.com/c/d)$`. Public index covers popular repos best; small repos may be missing (absence is not evidence).

`scripts/code_chain.py` runs concept queries, ranks repos by how many different concepts they cover, and mines identifiers from matched lines. **Raw coverage ranking is biased toward giant repos** - treat its output as leads for the Judge step, never as the answer.

Never send private project details in queries to external services.
