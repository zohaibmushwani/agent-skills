#!/usr/bin/env python3
"""Check that every item and state in inventory.json has an image (and spec) on disk.

Usage: state_coverage.py <design-dir>
Lookup for item id 'home-01' state 'default':  screens/**/home-01.png
Web items declare "views": ["desktop","mobile"] -> every view must exist as home-01@desktop.png, home-01.empty@mobile.png ...
A data screen can be flagged with "data": true (web lists/dashboards); inventory "platform": "web" skips the mobile-only
entry/home/settings group warning.
For other states:                              states/home-01.<state>.png (also searched under dialogs/, sheets/)
Dialog/sheet groups are looked up under dialogs/ and sheets/.
Also warns on data screens that define no loading/empty/error state, unless the item has "states_na": "<reason>".
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import Report, load_json  # noqa: E402

DATA_GROUPS = {"home", "feature", "detail", "search", "apps", "requests", "dashboard", "catalog"}
EXPECT = {"loading", "empty", "error"}


def find(root, stem):
    hits = [p for p in root.rglob(f"{stem}.png")]
    return hits[0] if hits else None


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1])
    inv = load_json(root / "inventory.json")
    rep = Report("State coverage")
    items = inv.get("items", [])
    if not items:
        rep.fail("inventory.json has no items")
    for it in items:
        iid, group = it["id"], it.get("group", "")
        states = it.get("states", ["default"])
        views = it.get("views") if inv.get("platform") == "web" else None
        for st in states:
            for view in (views or [None]):
                stem = iid if st == "default" else f"{iid}.{st}"
                if view:
                    stem = f"{stem}@{view}"
                png = find(root, stem)
                if png is None:
                    rep.fail(f"missing image for {stem} (group {group})")
                    continue
                spec = png.parent / f"{stem}.spec.json"
                if not spec.exists():
                    rep.warn(f"no spec for {stem}")
        if (group in DATA_GROUPS or it.get("data")) and not it.get("states_na"):
            missing = EXPECT - set(states)
            if missing:
                rep.warn(f"{iid}: data screen without states {sorted(missing)} (add them or mark why not needed)")
    groups = {i.get("group") for i in items}
    for need in (("home",) if inv.get("platform") == "web" else ("entry", "home", "settings")):
        if need not in groups:
            rep.warn(f"inventory has no '{need}' group")
    print(rep.markdown())
    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
