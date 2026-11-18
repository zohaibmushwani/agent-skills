#!/usr/bin/env python3
"""Self-test for the offline scripts (the Node probe needs network and is not tested here)."""
import subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
s = here.parent / "scripts"
def run(*a):
    p = subprocess.run([sys.executable, *map(str, a)], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout
ok = True
rc, out = run(s / "metadata_check.py", here / "fixtures" / "draft_bad.json", "--keywords", "pdf reader,dark mode")
for need in ("ERR  short" if False else "WARN title contains a claim", "emoji", "repeated word", "ALL-CAPS" if False else "density", "not in title"):
    if need not in out:
        print("MISSING in bad draft output:", need); ok = False
rc, out = run(s / "metadata_check.py", here / "fixtures" / "draft_ok.json", "--keywords", "pdf reader,offline")
if rc != 0 or "ERR" in out:
    print("good draft should pass:\n" + out); ok = False
rc, out = run(s / "keyword_freq.py", here / "fixtures" / "competitors.json", "--mine", here / "fixtures" / "draft_ok.json")
for need in ("pdf viewer", "missing from your draft"):
    if need not in out:
        print("MISSING in keyword_freq output:", need); ok = False
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
