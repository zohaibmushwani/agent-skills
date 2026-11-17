# License matrix (practical, not legal advice - confirm with counsel for a commercial launch)

| License (SPDX) | Copy code into a **closed** app? | Depend on as library? | Must you open your code? | Notes |
|---|---|---|---|---|
| MIT, BSD-2/3, ISC, Zlib, Unlicense/CC0 | yes | yes | no | keep copyright notice (CC0/Unlicense: none) |
| Apache-2.0 | yes | yes | no | keep NOTICE + license, patent grant, state changes |
| MPL-2.0 | yes (file-level) | yes | only changes to MPL files | weak copyleft per file |
| LGPL-2.1/3.0 | conditional | yes if dynamically linked/replaceable | changes to the LGPL lib | static linking on Android is risky; verify |
| GPL-2.0/3.0 | **no** | **no** (whole app becomes GPL) | yes, whole work | study only |
| AGPL-3.0 | **no** | **no** (also network use triggers) | yes, incl. server use | study only; common for panels/servers |
| CC BY-NC / non-commercial | **no** for commercial | no | - | blocks monetised apps |
| No license file | **no** (all rights reserved) | no | - | ideas only; ask author |
| "NOASSERTION"/custom | unknown | unknown | - | read the text |
Dual licenses ("MIT OR Apache-2.0") - you choose. "MIT in README but no code/LICENSE" - treat as no usable code.

Mixed binaries: a library that links a GPL component makes the *built artifact* GPL (e.g. an AAR bundling sing-box). Check the build output, not only the repo license.

Assets (models, motions, fonts, music, images, datasets) have **their own licenses**, often non-commercial; verify per asset. Store/policy rules (Google Play VpnService declaration, audio permissions, user content) are separate from code licenses.

Attribution checklist: LICENSE/NOTICE text in repo + in-app "open source licenses" screen; keep copyright headers in copied files; record each reused project in `LICENSES.md` with version and what was taken.
