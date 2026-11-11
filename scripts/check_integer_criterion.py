#!/usr/bin/env python3
"""Replay the fixed Q0001 module with its original proof-assumption policy.

The source digest identifies the module reviewed and checked on 9 November
2026. A changed mathematical statement needs separate review before updating
this acceptance target. This is not a checker for arbitrary submitted Lean.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_formal import audit_output

SOURCE = "research/agent-attempts/0002/IntegerCriterion.lean"
SOURCE_SHA256 = "8101d90754600546e65b344f2eb41fbc88b66f956e68addc318319f42c2629e9"
THEOREMS = (
    "Atlas.IntegerCriterion.necessary",
    "Atlas.IntegerCriterion.witness",
    "Atlas.IntegerCriterion.solvability_iff",
    "Atlas.IntegerCriterion.unique_solution",
)


def check_module(lean, root=ROOT):
    """Check the recorded source, compiler version, exit status and reports."""
    source_path = root / SOURCE
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if source_hash != SOURCE_SHA256:
        raise ValueError("Q0001 source changed; review the statement before changing the fixed target")
    spec = json.loads((root / "formal/toolchain.json").read_text())
    version = subprocess.run([str(lean), "--version"], check=True, text=True,
                             capture_output=True, timeout=15).stdout.strip()
    if not re.search(rf"\bversion {re.escape(spec['version'])}(?:\s|,)", version):
        raise ValueError(f"Expected Lean {spec['version']}; received {version}")
    result = subprocess.run([str(lean), str(source_path)], text=True,
                            capture_output=True, timeout=120, cwd=root)
    output = result.stdout + result.stderr
    if result.returncode:
        raise ValueError(f"Lean failed ({result.returncode}):\n{output}")
    reports = audit_output(output, THEOREMS, spec["allowed_axioms"])
    return {
        "status": "kernel-checked-known-mathematics",
        "problem_id": "Q0001",
        "scope": "Necessary divisibility, explicit witness, solvability and uniqueness for 2x+3y=p and -x+4y=q over integers",
        "source_path": SOURCE,
        "source_sha256": source_hash,
        "lean_version": version,
        "theorems": reports,
        "output": output,
        "checker": "Pinned Lean kernel and original transitive axiom allowlist; no independent external checker",
        "limitations": "No Python implementation proof, general-matrix theorem, learning outcome, novelty or Millennium claim",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", default="lean", help="Path to the pinned Lean executable")
    args = parser.parse_args()
    print(json.dumps(check_module(args.lean), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
