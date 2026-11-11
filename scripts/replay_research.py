#!/usr/bin/env python3
"""Reproduce the fixed finite investigations and compare their recorded JSON.

These are known, reviewed repository scripts, not untrusted submissions. A
matching replay establishes reproducibility within each recorded finite scope.
It does not turn finite checks into a universal proof or collect learner data.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPLAYS = (
    ("Q0001", "research/agent-attempts/0002/check_examples.py",
     "research/agent-attempts/0002/finite-evidence.json"),
    ("Q0004", "research/agent-attempts/0003/check.py",
     "research/agent-attempts/0003/evidence.json"),
    ("Q0002-calibration", "research/agent-attempts/0004/calibrate.py",
     "research/agent-attempts/0004/calibration.json"),
)


def replay(script, evidence, root=ROOT):
    result = subprocess.run([sys.executable, str(root / script)], cwd=root,
                            text=True, capture_output=True, timeout=120)
    if result.returncode or result.stderr.strip():
        raise ValueError(f"Research replay failed for {script}: {result.stderr}")
    actual = json.loads(result.stdout)
    expected = json.loads((root / evidence).read_text())
    # Python equality equates booleans/integers and 7/7.0; evidence types matter.
    if json.dumps(actual, sort_keys=True, allow_nan=False) != json.dumps(
        expected, sort_keys=True, allow_nan=False
    ):
        raise ValueError(f"Research output differs from retained evidence: {script}")


def main():
    for problem_id, script, evidence in REPLAYS:
        replay(script, evidence)
        print(f"{problem_id}: replay exactly matches {evidence}")
    print("Finite evidence and calibration only; no new theorem or learner outcome.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
