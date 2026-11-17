"""Shared helpers for app-design-studio gate scripts (stdlib only)."""
import json
import re
import sys
from pathlib import Path

HEX_RE = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def load_json(path):
    p = Path(path)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: file not found: {p}")
    except json.JSONDecodeError as e:
        sys.exit(f"error: invalid JSON in {p}: {e}")


def hex_to_rgb(h):
    m = HEX_RE.match(h.strip())
    if not m:
        raise ValueError(f"not a hex colour: {h!r}")
    s = m.group(1)
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_lin(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg_hex, bg_hex):
    l1, l2 = luminance(hex_to_rgb(fg_hex)), luminance(hex_to_rgb(bg_hex))
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def resolve_color(value, palette):
    """value is a token name in palette or a hex string."""
    if value in palette:
        return palette[value]
    if isinstance(value, str) and HEX_RE.match(value):
        return value if value.startswith("#") else "#" + value
    raise KeyError(value)


class Report:
    def __init__(self, title):
        self.title = title
        self.rows = []  # (level, message)

    def fail(self, msg):
        self.rows.append(("FAIL", msg))

    def warn(self, msg):
        self.rows.append(("WARN", msg))

    def ok(self, msg):
        self.rows.append(("PASS", msg))

    @property
    def failed(self):
        return any(l == "FAIL" for l, _ in self.rows)

    def counts(self):
        return {k: sum(1 for l, _ in self.rows if l == k) for k in ("PASS", "WARN", "FAIL")}

    def markdown(self):
        c = self.counts()
        out = [f"## {self.title}", f"PASS {c['PASS']} / WARN {c['WARN']} / FAIL {c['FAIL']}", ""]
        for lvl, msg in self.rows:
            if lvl != "PASS":
                out.append(f"- **{lvl}** {msg}")
        if c["WARN"] == 0 and c["FAIL"] == 0:
            out.append("- all checks passed")
        return "\n".join(out) + "\n"
