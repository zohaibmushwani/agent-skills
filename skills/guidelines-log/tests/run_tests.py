#!/usr/bin/env python3
"""Self-test: rules_audit.py must flag the known defects in tests/fixtures/repo and exit 1."""
import subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
p = subprocess.run([sys.executable, str(here.parent / "scripts" / "rules_audit.py"), str(here / "fixtures" / "repo"), "--budget", "10"],
                   capture_output=True, text=True, encoding="utf-8")
ok = p.returncode == 1
for need in ("secret", "broken-ref", "over-budget", "duplicate", "conflict", "log-no-why", "log-order"):
    if need not in p.stdout:
        print("MISSING:", need); ok = False
print("PASS" if ok else "FAIL\n" + p.stdout)
sys.exit(0 if ok else 1)
