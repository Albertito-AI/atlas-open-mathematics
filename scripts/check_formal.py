#!/usr/bin/env python3
"""Check the fixed, reviewed Lean pilot and audit its transitive axioms.

This script is deliberately specific to formal/Atlas.lean. It is not an
acceptance service for arbitrary, potentially hostile proof submissions.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit_output(output, theorem_names, allowed_axioms):
    """Fail closed if a theorem's dependency report is absent or unexpected."""
    if re.search(r"\b(?:warning|error):", output, flags=re.IGNORECASE):
        raise ValueError("Lean emitted a warning or error")
    reports = {}
    for name in theorem_names:
        escaped = re.escape(name)
        pattern = rf"'{escaped}' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)"
        matches = list(re.finditer(pattern, output))
        if len(matches) != 1:
            raise ValueError(f"Expected one axiom report for {name}")
        raw = matches[0].group(1)
        axioms = [] if raw is None else [a.strip() for a in raw.split(',') if a.strip()]
        unexpected = set(axioms) - set(allowed_axioms)
        if unexpected:
            raise ValueError(f"Unapproved assumptions for {name}: {sorted(unexpected)}")
        reports[name] = axioms
    return reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", default="lean", help="Path to the pinned Lean executable")
    parser.add_argument("--output", type=Path, help="Optional new JSON evidence file")
    args = parser.parse_args()
    spec = json.loads((ROOT / "formal/toolchain.json").read_text())
    source_path = ROOT / "formal/Atlas.lean"
    source = source_path.read_text()
    # This is an additional review aid, not a general code-security boundary.
    forbidden = r"\b(sorry|admit|axiom|unsafe|native_decide|set_option)\b"
    if re.search(forbidden, source):
        raise ValueError("Unexpected proof escape or additional assumption in pilot source")
    imports = re.findall(r"^import\s+(.+)$", source, flags=re.MULTILINE)
    if imports != ["Lean.Elab.Tactic.Omega"]:
        raise ValueError("Pilot imports changed; a separate review is required")
    version = subprocess.run([args.lean, "--version"], check=True, text=True,
                             capture_output=True, timeout=15).stdout.strip()
    if not re.search(rf"\bversion {re.escape(spec['version'])}(?:\s|,)", version):
        raise ValueError(f"Expected Lean {spec['version']}; received {version}")
    result = subprocess.run([args.lean, str(source_path)], text=True,
                            capture_output=True, timeout=120, cwd=ROOT / "formal")
    output = result.stdout + result.stderr
    if result.returncode:
        raise ValueError(f"Lean failed ({result.returncode}):\n{output}")
    axioms = audit_output(output, spec["theorems"], spec["allowed_axioms"])
    evidence = {
        "status": "kernel-checked-known-supporting-algebra",
        "scope": "Four integer linear-equation statements; no claim about Python correctness or Millennium problems",
        "lean_version": version,
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "theorems": axioms,
        "checker": "Pinned Lean kernel with transitive axiom inspection; no independent external checker",
        "output": output,
    }
    serialised = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        # Do not overwrite evidence produced by a different check.
        if args.output.exists():
            if args.output.read_text() != serialised:
                raise ValueError("Existing formal evidence differs; choose a new output path")
        else:
            with args.output.open("x") as handle:
                handle.write(serialised)
    print(serialised, end="")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
