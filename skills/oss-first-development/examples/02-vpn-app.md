# Research: VPN app (Shadowsocks + VPN/VPS backend, Compose UI, NDK + Rust)
Date 2026-11-17. Method: dorks + identifier chaining + EN/ZH/JA/RU searches (see RESEARCH-TECHNIQUES.md).
Legend: VERIFIED = page content read directly. LEAD = only seen in search results / third-party summaries.

## 0. Answer in one paragraph
Do not write a tunnel engine from scratch. The proven shape is: **Compose UI + Kotlin `VpnService` -> TUN fd -> Rust core via JNI** (ProxyDroid, shadowsocks-android, Mullvad all follow this), with the **core made from permissively licensed crates** (shadowsocks-rust MIT, tun-rs Apache-2.0, hev-socks5-tunnel MIT). Backend = a **control plane you write** (auth, plans, node registry, key issuance, usage) + a **node agent** on every VPS that wraps an existing server (shadowsocks-rust `ssmanager` or Outline's shadowbox API, plus WireGuard). The big traps are **GPL code you can study but not copy**, **Google Play's VPN policy**, and **a local unauthenticated SOCKS port**.

## 1. Client building blocks

| Piece | Candidate | Status | License | Use |
|---|---|---|---|---|
| Closest full template | **madeye/proxydroid** | VERIFIED | **GPL-3.0** | Compose UI + VpnService + Rust tun2socks (`app/src/main/rust/proxydroid-tun2socks`, netstack-smoltcp) via JNI, built with `org.mozilla.rust-android-gradle`. Study only unless app is GPL. Needs JDK17, NDK 25, AGP 8.1.2 pinned. 2.6k stars |
| Reference client | **shadowsocks/shadowsocks-android** | VERIFIED (README) | **GPL-3.0** | modules core/mobile/tv/plugin; builds shadowsocks-rust + tun2socks natively; plugin model (SIP003). Integration style (subprocess vs JNI) NOT stated on page; read `core/` source |
| Shadowsocks engine | **shadowsocks/shadowsocks-rust** | VERIFIED | **MIT** | crates `shadowsocks`, `shadowsocks-service`, `shadowsocks-rust`; features `local-tun`, `aead-cipher-2022`, `local-dns`; Android listed under TUN-supported platforms; `ssmanager` add/remove/list/ping for multi-user server |
| Userspace TCP/IP | netstack-smoltcp | LEAD | unknown | used by ProxyDroid |
| TUN wrapper | **tun-rs** | LEAD (docs.rs) | Apache-2.0 | `SyncDevice::from_fd` wraps the fd from `VpnService.Builder().establish()` |
| tun2socks (C) | **heiher/hev-socks5-tunnel** (+ Rust crate `tun2socks` bindings) | LEAD | **MIT** | takes tun fd, proven in v2rayNG-class apps; JNI example in sudoku-android |
| Universal core | sing-box `libbox` (gomobile) | LEAD | **GPL-3.0** (per teapod-core note) | what NekoBox / official SFA use; host implements `PlatformInterface`, `OpenTun` returns fd |
| Xray route | v2rayNG (libv2ray.aar), teapod-core | VERIFIED (teapod) | MIT own code; AAR with sing-box = GPL; xray-rust MPL-2.0 | gomobile fat AAR pattern; minSdk 29 in that lib |
| Best architecture reference | **mullvad/mullvadvpn-app** | VERIFIED (architecture.md) | GPL-3.0 (known; page didn't show) | Rust daemon with actor model; **tunnel state machine** Disconnected/Connecting/Connected/Disconnecting/Error; Error state blocks leaks; frontends talk to daemon over gRPC (desktop) / **JNI (Android)**; **API reachable through a shadowsocks bridge** when blocked; relay selector; Compose screens in `android/app/.../compose/` |
| WireGuard on Android | wireguard-go (+ Rust bindings in Mullvad), gotatun | LEAD | wireguard-go MIT; gotatun unknown | for the "VPN/VPS" (WireGuard) mode |
| Compose VPN clients | SlipNet, sing-box-for-android (SFA), Hiddify | LEAD | mixed | UI reference only |

Rust-on-Android build: ProxyDroid uses `rust-android-gradle` (0.9.6); alternative `cargo-ndk` (+ `uniffi-rs` for Kotlin bindings, pattern seen in mobench-sdk). No authoritative comparison found -> decide by prototype. **16 KB page size** (Play requirement): use NDK r28+ (cargo-ndk aligns by default per a PR; otherwise `-Wl,-z,max-page-size=16384`); official page: developer.android.com/guide/practices/page-sizes.

## 2. Server / backend building blocks

| Piece | Candidate | Status | License | Notes |
|---|---|---|---|---|
| SS server + multi-user | shadowsocks-rust `ssserver` + `ssmanager` | VERIFIED | MIT | add/remove/list/ping server instances; `stat` not supported in manager mode (all in one process) |
| Managed SS server with REST | **Jigsaw/Outline `outline-server` (shadowbox + outline-ss-server)** | VERIFIED | **Apache-2.0** | `GET/POST /access-keys`, `PUT /access-keys/{id}/name`, `DELETE /access-keys/{id}`, `PUT/DELETE /server/access-key-data-limit` (**global** limit per README), `GET /server`. Auth = secret URL prefix, self-signed TLS. Openapi in `src/shadowbox/server/api.yml`. Install via `install_server.sh` (random ports unless set). AEAD only, probe + replay resistance. Per-key limits/usage metrics NOT documented in README -> read api.yml |
| Xray panels | 3x-ui (MHSanaei), Marzban, Hiddify-manager | LEAD | unverified | traffic quota, expiry, subscription URL, REST API (3x-ui: login then `/panel/api/inbounds`); panels poll traffic rather than push |
| Protocols/obfuscation | SS-2022 (`aead-cipher-2022`), SIP003 plugins (v2ray-plugin), shadow-tls, Reality (Xray >= 1.8.0) | LEAD (vendor blogs, opinion) | - | no measured censorship data found; AEAD-2022 keys are base64 (`ssservice genkey`); shadowsocks-rust removed Bloom filter replay defence (Xray issue 625) -> verify |
| Control plane (you write) | auth, plans/billing, node registry, key issuance, usage, health | - | - | no off-the-shelf fit for your own app; keep small. Rust `axum` + Postgres or Go; node agent per VPS |
| Node provisioning | `install_server.sh`, cloud-init, Terraform/Ansible | LEAD | - | not researched deeply |

## 3. Policy / security findings
- **Google Play (VERIFIED, support.google.com/.../12564964):** VPN must be core functionality; submit the **VpnService declaration form**; **encrypt device -> tunnel endpoint**; **prominent in-app disclosure with affirmative consent** if any personal/sensitive data is collected (not only in privacy policy); declaration video <= 90 s plus a second video of disclosure/consent/non-consent flows; no ad-traffic manipulation; resubmit on changes. A "Verified" VPN badge exists (MASA Level 2) - LEAD.
- **Local SOCKS without auth (Habr PoC, LEAD):** many xray/sing-box clients open an unauthenticated local SOCKS5 that any app can use. Prefer **fd -> in-process core with no listening port**, or loopback + random port + auth.
- Android allows **one active VpnService** (LEAD); handle `onRevoke`, `protect()` outbound sockets, `addDisallowedApplication` for per-app bypass (VERIFIED in ProxyDroid).
- **Licenses:** ProxyDroid, shadowsocks-android, Mullvad, sing-box = GPL-3.0 -> read and learn, do not copy into a closed app. Safe to depend on: shadowsocks-rust (MIT), hev-socks5-tunnel (MIT), tun-rs (Apache-2.0), outline-server (Apache-2.0).
- Check local regulation/ISP rules for running VPN services in your jurisdiction (not researched).

## 4. Recommended architecture (to validate by prototype)
```
Android app (Kotlin)
  Compose UI  <-  TunnelState (Disconnected|Connecting|Connected|Disconnecting|Error)  [Mullvad pattern]
  VpnService  -> establish() -> tun fd
        | JNI (UniFFI or hand-written)
  Rust core (cdylib, cargo-ndk / rust-android-gradle, NDK r28+)
     tun-rs(fd) -> userspace stack or hev-socks5-tunnel -> shadowsocks (crate) AEAD-2022 [+ SIP003/shadow-tls later]
     WireGuard mode: wireguard-go (or gotatun) with same fd
     relay selector, latency probe, kill-switch (Error state blocks), API client that can use an SS bridge
Control plane (Rust axum or Go) : auth, plans, nodes, keys, usage, config/subscription endpoint
Node agent on each VPS : wraps ssmanager OR outline shadowbox API (+ wg), reports health/usage
```
Why: every shipped open-source client converges on VpnService + native core; Mullvad shows the clean state machine + JNI split; Outline gives a ready multi-user key API so you only write the control plane.

## 5. Decisions the user must make
1. Closed or open-source app? (decides whether GPL code can be reused at all)
2. Core: **Rust-only** (shadowsocks-rust + tun-rs/hev) vs Go core (sing-box, GPL). User asked Rust+NDK -> Rust-only.
3. Server base: shadowsocks-rust `ssmanager` (full control, you write agent) vs Outline shadowbox (faster, global-limit only) vs Xray panel (more protocols, more moving parts).
4. Protocols for v1: Shadowsocks-2022 only, or + WireGuard, + Reality/shadow-tls?
5. Billing/accounts model and jurisdiction.

## 6. Not verified / gaps
netstack-smoltcp, Marzban, Hiddify, wireguard-android, gotatun licenses; whether shadowsocks-rust `local-tun` accepts an Android fd directly (check `shadowsocks-service` tun config); Outline per-key limits and metrics (read `api.yml`); shadowsocks-android integration style; no Zenn/Qiita or Juejin tutorials found (searched; thin); one Habr article (habr.com/ru/articles/1022422) on Xray+tun2socks not read.

## 7. Next steps (prototype order, each small and testable)
P0 empty Compose app + VpnService that establishes a tun and logs packets. P1 Rust cdylib "hello JNI" built for 4 ABIs with 16 KB alignment. P2 pass tun fd to Rust; connect to a local `ssserver`. P3 state machine + Compose screens. P4 control-plane MVP + node agent. P5 WireGuard mode. P6 Play declaration prep.

## Sources
ProxyDroid https://github.com/madeye/proxydroid · shadowsocks-android https://github.com/shadowsocks/shadowsocks-android · shadowsocks-rust https://github.com/shadowsocks/shadowsocks-rust · Mullvad architecture https://github.com/mullvad/mullvadvpn-app/blob/main/docs/architecture.md · Outline server https://github.com/OutlineFoundation/outline-server and shadowbox README https://github.com/Jigsaw-Code/outline-server/blob/master/src/shadowbox/README.md · teapod-core https://github.com/Wendor/teapod-core · hev-socks5-tunnel https://github.com/heiher/hev-socks5-tunnel · 3x-ui https://github.com/MHSanaei/3x-ui · Google Play VPN policy https://support.google.com/googleplay/android-developer/answer/12564964 · Android 16 KB https://developer.android.com/guide/practices/page-sizes · sing-box internals (platform) https://singbox-internals.hidandelion.com/advanced/platform.html · Habr https://habr.com/ru/articles/1022422
