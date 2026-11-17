#!/usr/bin/env python3
"""Self-test: the audit scripts must flag the known defects in tests/fixtures and exit 1."""
import subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
s = here.parent / "scripts"
def run(*a):
    p = subprocess.run([sys.executable, *map(str, a)], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout
ok = True
rc, out = run(s / "strings_audit.py", here / "fixtures" / "res")
for need in ("missing-key", "placeholder", "extra-key", "plural-quantity", "untranslated"):
    if need not in out:
        print("MISSING in strings_audit output:", need); ok = False
if rc != 1: print("strings_audit should exit 1"); ok = False
rc, out = run(s / "compose_lint.py", here / "fixtures" / "src")
for need in ("hex-color", "intrinsic-min", "android-log", "offset", "left-right", "hardcoded-string", "no-preview", "text-no-maxlines"):
    if need not in out:
        print("MISSING in compose_lint output:", need); ok = False
if rc != 1: print("compose_lint should exit 1"); ok = False
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
