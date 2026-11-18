#!/usr/bin/env python3
"""Run every gate and write <design-dir>/reports/gates.md.

Usage: run_gates.py <design-dir> [--strict]
Exit 0 only if no FAIL (and, with --strict, no WARN either).
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def run(script, args):
    p = subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    root = Path(argv[1])
    strict = "--strict" in argv
    steps = [
        ("contrast_check.py", [str(root / "tokens.json")]),
        ("prompt_lint.py", [str(root)]),
        ("token_lint.py", [str(root)]),
        ("spec_audit.py", [str(root)] + (["--strict"] if strict else [])),
        ("state_coverage.py", [str(root)]),
    ]
    out, worst = ["# Gate report", ""], 0
    for script, args in steps:
        code, text = run(script, args)
        worst = max(worst, code)
        out.append(text.rstrip() + f"\n\n_exit {code}_\n")
    (root / "reports").mkdir(exist_ok=True)
    (root / "reports" / "gates.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    print("RESULT:", "PASS" if worst == 0 else "FAIL")
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
