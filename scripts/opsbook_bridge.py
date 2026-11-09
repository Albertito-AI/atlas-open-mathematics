#!/usr/bin/env python3
"""Exercise the pinned Atlas Opsbook with an actual mathematical verifier.

All teaching and exam-labelled fixtures are public synthetic cases. This is a
deterministic procedural-memory integration, not a live-model learning study.
"""

from __future__ import annotations

import argparse
from contextlib import closing
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from atlas_math import generate_case, solve, verify  # noqa: E402

UPSTREAM_COMMIT = "94b84261d0d2ae23f783522a3c2e4cb697aecde3"
OPSBOOK_PATH = ROOT / "vendor" / "atlas-opsbook" / "opsbook.py"
CHECK = "exact-substitution"
INSTRUCTION = (
    "Before submitting a linear-system certificate, independently substitute any proposed solution "
    "into every original equation and verify its uniqueness, nullspace or inconsistency certificate."
)


def _opsbook():
    spec = importlib.util.spec_from_file_location("atlas_math_vendored_opsbook", OPSBOOK_PATH)
    if spec is None or spec.loader is None:
        raise ValueError("pinned Opsbook module is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def _state(path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 5_000_000:
        raise ValueError("manual must be a bounded regular SQLite file")
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as connection:
        row = connection.execute("SELECT data FROM book WHERE id=1").fetchone()
    if row is None or len(row[0]) > 1_000_000:
        raise ValueError("manual state missing or oversized")
    return json.loads(row[0])


def _immutable(path, data):
    if path.is_symlink():
        raise ValueError(f"refusing symlink artifact: {path.name}")
    if path.exists():
        if not path.is_file() or path.stat().st_size != len(data) or path.read_bytes() != data:
            raise FileExistsError(f"immutable artifact differs: {path.name}")
        return
    with path.open("xb") as handle:
        handle.write(data)


def _fresh_brief(db):
    context = {"task": "submit-certificate", "domain": "linear-system", "case": "fresh-session"}
    result = subprocess.run(
        [sys.executable, str(OPSBOOK_PATH), "--db", str(db), "brief", json.dumps(context)],
        capture_output=True, text=True, timeout=15, check=False,
    )
    if result.returncode != 0:
        raise ValueError("fresh-process manual reload failed: " + result.stderr[:500])
    brief = json.loads(result.stdout)
    checks = sorted({rule["check"] for rule in brief["instructions"]})
    if checks != [CHECK]:
        raise ValueError("fresh manual must explicitly select the required exact-substitution check")
    return brief


def _fixtures():
    maths = [generate_case(7), generate_case(8)]
    records = []
    for split, case in zip(("practice", "exam"), maths):
        for task in ("submit-certificate", "read-note"):
            records.append({
                "id": f"{split}-{'submit' if task == 'submit-certificate' else 'read'}",
                "set": split,
                "context": {"task": task, "domain": "linear-system", "case": case["id"]},
                "expected": [CHECK] if task == "submit-certificate" else [],
                "evidence": (
                    "Public synthetic fixture for " + case["id"] + ". " +
                    ("Submission requires the independently executed certificate check; reading a note does not."
                     if task == "submit-certificate" else "Read-only teaching-note control; no certificate is being submitted.")
                ),
            })
    return maths, records


def run_bridge(output: Path) -> dict:
    output = Path(output)
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        raise ValueError("output must be a real directory")
    opsbook = _opsbook()
    maths, fixtures = _fixtures()
    correct = solve(maths[0])
    incorrect = json.loads(json.dumps(correct))
    incorrect["solution"][0] = str(Fraction(incorrect["solution"][0]) + 1)
    correct_result, incorrect_result = verify(maths[0], correct), verify(maths[0], incorrect)
    if not correct_result["accepted"] or incorrect_result["accepted"]:
        raise ValueError("mathematical fixture failed its independently checked premise")

    with tempfile.TemporaryDirectory(prefix="atlas-opsbook-bridge-") as temporary:
        temporary = Path(temporary)
        teaching_db = temporary / "teaching.db"
        fixture_file = temporary / "fixtures.json"
        fixture_file.write_bytes(_encoded(fixtures))

        def run(db, *arguments):
            return opsbook.transact(db, opsbook.parser().parse_args(list(arguments)))

        run(teaching_db, "init")
        run(teaching_db, "record", str(fixture_file))
        broad_file = temporary / "overbroad.json"
        broad_file.write_bytes(_encoded({
            "id": "overbroad-math-check", "when": {"domain": "linear-system"},
            "check": CHECK, "instruction": INSTRUCTION, "basis": "practice-submit",
        }))
        broad = run(teaching_db, "propose", str(broad_file))["proposal"]
        broad_report = run(teaching_db, "evaluate", broad)
        if broad_report["eligible"]:
            raise ValueError("overbroad rule unexpectedly passed its read-only controls")
        promotion_refused = False
        try:
            run(teaching_db, "promote", broad)
        except ValueError:
            promotion_refused = True
        if not promotion_refused:
            raise ValueError("overbroad promotion was not refused")

        learned = run(teaching_db, "learn", "practice-submit", CHECK, INSTRUCTION)
        narrowed_report = run(teaching_db, "evaluate", learned["proposal"])
        if not narrowed_report["eligible"] or learned["rule"]["when"] != {"task": "submit-certificate"}:
            raise ValueError("learning did not produce the intended scoped procedure")
        promoted = run(teaching_db, "promote", learned["proposal"])
        expected_state = _state(teaching_db)
        manual_text = run(teaching_db, "manual") + "\n"

        output.mkdir(parents=True, exist_ok=True)
        persistent_db = output / "manual.db"
        if persistent_db.exists() or persistent_db.is_symlink():
            if _state(persistent_db) != expected_state:
                raise ValueError("existing persistent manual differs; use a new output directory")
        else:
            with persistent_db.open("xb") as handle:
                handle.write(teaching_db.read_bytes())
        # Read the retained database in a genuinely new Python process.
        reloaded = _fresh_brief(persistent_db)
        case_file, bad_file, good_file = (temporary / name for name in ("case.json", "incorrect.json", "correct.json"))
        case_file.write_bytes(_encoded(maths[0]))
        bad_file.write_bytes(_encoded(incorrect))
        good_file.write_bytes(_encoded(correct))
        results = {}
        for name, candidate_file in (("incorrect_candidate", bad_file), ("correct_candidate", good_file)):
            commands = temporary / f"{name}-commands.json"
            # This trusted argument vector is constructed by the maintainer's
            # script. Learned instruction text is never interpreted as code.
            commands.write_bytes(_encoded({CHECK: [sys.executable, str(Path(__file__).resolve()),
                                                   "--execute-check", str(case_file), str(candidate_file)]}))
            selected = reloaded["instructions"]
            if sorted({rule["check"] for rule in selected}) != [CHECK]:
                raise ValueError("empty or unexpected check selection cannot count as success")
            results[name] = opsbook.run_checks(selected, str(commands))
        if results["incorrect_candidate"]["pass"] or not results["correct_candidate"]["pass"]:
            raise ValueError("trusted executable checks did not reject/accept the expected certificates")

        recovery_db = temporary / "rollback-copy.db"
        shutil.copyfile(persistent_db, recovery_db)
        recovered = run(recovery_db, "rollback", "0", "Recovery rehearsal on an isolated copy")
        recovered_brief = run(recovery_db, "brief", json.dumps({"task": "submit-certificate"}))
        if recovered_brief["instructions"] or _state(persistent_db) != expected_state:
            raise ValueError("rollback rehearsal altered the retained manual or failed to restore revision zero")

        report = {
            "schema_version": 1,
            "integration": "atlas_opsbook_exact_linear_systems",
            "upstream_commit": UPSTREAM_COMMIT,
            "synthetic": True, "live_model": False, "model_weights_updated": False,
            "assessment_scope": "public practice and exam-labelled software fixtures; no protected learner evaluation",
            "overbroad": {"promotion_refused": promotion_refused, "report": broad_report},
            "learned": {"guard": learned["rule"]["when"], "check": CHECK,
                        "revision": promoted["number"], "report": narrowed_report},
            "fresh_process": {"revision": reloaded["revision"], "selected_checks": [CHECK]},
            "execution": results,
            "mathematical_fixture": {"case_id": maths[0]["id"], "incorrect": incorrect_result, "correct": correct_result},
            "rollback": {"isolated_copy": True, "copy_revision": recovered["number"],
                         "restored_revision": recovered["restored"], "copy_instructions": recovered_brief["instructions"],
                         "retained_revision": promoted["number"]},
            "empty_check_selection_counts_as_success": False,
            "novel_mathematics_claimed": False,
        }
        artifacts = {
            "report.json": _encoded(report),
            "MANUAL.md": manual_text.encode("utf-8"),
            "fixtures.json": _encoded({"public_synthetic": True, "math_cases": maths, "opsbook_cases": fixtures,
                                      "correct_candidate": correct, "incorrect_candidate": incorrect}),
        }
        for name, data in artifacts.items():
            path = output / name
            if path.exists() or path.is_symlink():
                if path.is_symlink() or not path.is_file() or path.stat().st_size != len(data) or path.read_bytes() != data:
                    raise FileExistsError(f"immutable artifact differs: {name}")
        for name, data in artifacts.items():
            _immutable(output / name, data)
        return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--execute-check", nargs=2, metavar=("CASE", "CANDIDATE"), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.execute_check:
        from atlas_math.cli import _load_json
        result = verify(*[_load_json(Path(path)) for path in args.execute_check])
        print(json.dumps(result, sort_keys=True))
        return 0 if result["accepted"] else 1
    if args.output is None:
        parser.error("--output is required")
    try:
        report = run_bridge(args.output)
    except (ValueError, OSError, sqlite3.Error, subprocess.SubprocessError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, "report": report}, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
