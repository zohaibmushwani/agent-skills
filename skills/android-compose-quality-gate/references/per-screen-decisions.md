# Decide these for every screen before building it
1. **Back and stack:** what back does, what stays in the stack, what is replaced, what a result screen returns to (`back-permissions.md`). Keep a per-screen table.
2. **Network and offline class:** works offline / needs network to view / needs network to submit; what it fetches and caches; which actions block with a dialog (`network-offline.md`).
3. **Permissions:** which, where they are asked (before the screen), denied states (`back-permissions.md`).
4. **Scroll or fit:** a list or long content scrolls; a screen that can fit (splash, intro, premium, a result, a short form) fits the viewport with bounded scaling, scrolling only as a fallback (`text-fit-devices.md`).
5. **Motion:** which animation each element uses, from one app-wide plan (`motion-performance.md`).
Also plan one app-wide motion plan per component type before animating any screen.
