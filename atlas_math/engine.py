"""An exact 2-by-2 linear-system pilot, without model or network calls.

The deliberately flawed baseline and the corrected solver are predetermined
programs. Their measured difference demonstrates a verification workflow, not
autonomous discovery, language-model training or novel mathematics.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import re
from typing import Any


CASE_BOUND = 10**9
CANDIDATE_BOUND = 10**120
MAX_SCALAR_TEXT = 256
MAX_SEED = 2**63 - 1
KINDS = {"unique", "inconsistent", "underdetermined"}
_INTEGER_OR_FRACTION = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}\Z")


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _object(value: Any, fields: set[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"{label} must contain exactly {sorted(fields)}")
    return value


def _rational(value: Any, bound: int, label: str) -> Fraction:
    # In particular, bool is not an integer input and floats are never rounded.
    if type(value) is int:
        if abs(value) > bound:
            raise ValueError(f"{label} integer exceeds its bound")
        return Fraction(value)
    if type(value) is not str or len(value) > MAX_SCALAR_TEXT:
        raise ValueError(f"{label} must be an integer or bounded canonical rational string")
    if not _INTEGER_OR_FRACTION.fullmatch(value):
        raise ValueError(f"{label} is not a canonical rational string")
    result = Fraction(value)
    if abs(result.numerator) > bound or result.denominator > bound:
        raise ValueError(f"{label} numerator or denominator exceeds its bound")
    if value != _text(result):
        raise ValueError(f"{label} rational string must be reduced and canonical")
    return result


def _vector(value: Any, bound: int, label: str) -> list[Fraction]:
    if type(value) is not list or len(value) != 2:
        raise ValueError(f"{label} must be a list of exactly two scalars")
    return [_rational(x, bound, f"{label}[{i}]") for i, x in enumerate(value)]


def _case(case: Any) -> tuple[list[list[Fraction]], list[Fraction]]:
    _object(case, {"id", "A", "b", "kind"}, "case")
    if type(case["id"]) is not str or not _ID.fullmatch(case["id"]):
        raise ValueError("case id must be a safe identifier of at most 96 characters")
    if type(case["kind"]) is not str or case["kind"] not in KINDS:
        raise ValueError("case kind is invalid")
    if type(case["A"]) is not list or len(case["A"]) != 2:
        raise ValueError("A must contain exactly two rows")
    matrix = [_vector(row, CASE_BOUND, f"A[{i}]") for i, row in enumerate(case["A"])]
    return matrix, _vector(case["b"], CASE_BOUND, "b")


def _seed(seed: Any) -> int:
    if type(seed) is not int or not 0 <= seed <= MAX_SEED:
        raise ValueError(f"seed must be an integer between 0 and {MAX_SEED}")
    return seed


def generate_case(seed: int) -> dict:
    """Generate a deterministic public practice case; no hidden evaluation.

    Residues 0 and 1 modulo 5 produce inconsistent and underdetermined cases.
    Other residues produce coupled, uniquely solvable cases. The kind label is
    metadata; verification derives its judgement from the matrix and certificate.
    """
    rng = random.Random(_seed(seed))
    nonzero = [i for i in range(-9, 10) if i]
    x, y = rng.choice(nonzero), rng.choice(nonzero)
    if seed % 5 in (0, 1):
        a, b, k = rng.choice(nonzero), rng.choice(nonzero), rng.choice(nonzero)
        matrix = [[a, b], [k * a, k * b]]
        rhs = [a * x + b * y, k * (a * x + b * y)]
        kind = "underdetermined"
        if seed % 5 == 0:
            rhs[1] += 1
            kind = "inconsistent"
    else:
        while True:
            a, b, c, d = [rng.choice(nonzero) for _ in range(4)]
            if a * d != b * c:
                break
        matrix = [[a, b], [c, d]]
        rhs = [a * x + b * y, c * x + d * y]
        kind = "unique"
    return {"id": "case-" + _digest({"A": matrix, "b": rhs}),
            "A": matrix, "b": rhs, "kind": kind}


def solve(case: dict) -> dict:
    """Return an exact candidate and a checkable certificate for every 2x2 case."""
    matrix, rhs = _case(case)
    (a, b), (c, d) = matrix
    p, q = rhs
    determinant = a * d - b * c
    if determinant:
        return {"status": "unique",
                "solution": [_text((p * d - b * q) / determinant),
                             _text((a * q - p * c) / determinant)],
                "certificate": {"determinant": _text(determinant)}}

    # A zero row with a nonzero right-hand side is an explicit contradiction.
    for index, row in enumerate(matrix):
        if row == [0, 0] and rhs[index]:
            weights = ["1", "0"] if index == 0 else ["0", "1"]
            return {"status": "inconsistent", "certificate": {"row_weights": weights}}

    if matrix[0] != [0, 0] and matrix[1] != [0, 0]:
        column = 0 if a else 1
        weights = [-matrix[1][column], matrix[0][column]]
        if weights[0] * p + weights[1] * q:
            return {"status": "inconsistent",
                    "certificate": {"row_weights": [_text(v) for v in weights]}}

    index = next((i for i, row in enumerate(matrix) if row != [0, 0]), None)
    if index is None:
        particular, null_vector = [Fraction(0), Fraction(0)], [Fraction(1), Fraction(0)]
    else:
        left, right = matrix[index]
        particular = ([rhs[index] / left, Fraction(0)] if left
                      else [Fraction(0), rhs[index] / right])
        null_vector = [-right, left]
    return {"status": "underdetermined", "solution": [_text(v) for v in particular],
            "certificate": {"null_vector": [_text(v) for v in null_vector]}}


def verify(case: dict, candidate: dict) -> dict:
    """Independently check a candidate; never call the generator or solver.

    Acceptance establishes this exact finite linear-algebra claim under rational
    arithmetic. It is not a Lean/kernel check, a novelty judgement or a statement
    about a language model's capabilities.
    """
    try:
        matrix, rhs = _case(case)
        if not isinstance(candidate, dict) or type(candidate.get("status")) is not str:
            raise ValueError("candidate requires a string status")
        status = candidate["status"]
        if status not in KINDS:
            raise ValueError("candidate status is invalid")
        fields = {"status", "certificate"}
        if status != "inconsistent":
            fields.add("solution")
        _object(candidate, fields, "candidate")
        cert = candidate["certificate"]
        if status == "inconsistent":
            _object(cert, {"row_weights"}, "inconsistency certificate")
            w = _vector(cert["row_weights"], CANDIDATE_BOUND, "row_weights")
            if any(w[0] * matrix[0][j] + w[1] * matrix[1][j] for j in range(2)):
                return {"accepted": False, "reason": "row weights do not eliminate the coefficient matrix"}
            if w[0] * rhs[0] + w[1] * rhs[1] == 0:
                return {"accepted": False, "reason": "row weights do not produce a nonzero contradiction"}
            return {"accepted": True, "reason": "exact row combination proves inconsistency"}

        solution = _vector(candidate["solution"], CANDIDATE_BOUND, "solution")
        if status == "unique":
            _object(cert, {"determinant"}, "uniqueness certificate")
            claimed = _rational(cert["determinant"], CANDIDATE_BOUND, "determinant")
        else:
            _object(cert, {"null_vector"}, "underdetermination certificate")
            null_vector = _vector(cert["null_vector"], CANDIDATE_BOUND, "null_vector")
        if any(sum(matrix[i][j] * solution[j] for j in range(2)) != rhs[i] for i in range(2)):
            return {"accepted": False, "reason": "exact substitution fails at least one original equation"}
        if status == "unique":
            actual = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            if actual == 0 or claimed != actual:
                return {"accepted": False, "reason": "uniqueness requires the correct nonzero determinant"}
            return {"accepted": True, "reason": "exact substitution and nonzero determinant prove a unique solution"}

        if null_vector == [0, 0]:
            return {"accepted": False, "reason": "the null vector must be nonzero"}
        if any(sum(matrix[i][j] * null_vector[j] for j in range(2)) for i in range(2)):
            return {"accepted": False, "reason": "the supplied direction is not in the nullspace"}
        return {"accepted": True, "reason": "exact particular solution and nonzero null vector prove nonuniqueness"}
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        return {"accepted": False, "reason": f"invalid input: {exc}"}


def _flawed_solve(case: dict) -> dict:
    """Frozen illustrative defect: ignore the off-diagonal coefficients."""
    matrix, rhs = _case(case)
    if not matrix[0][0] or not matrix[1][1]:
        return {"status": "unsupported", "reason": "baseline divides by diagonal coefficients"}
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return {"status": "unique",
            "solution": [_text(rhs[0] / matrix[0][0]), _text(rhs[1] / matrix[1][1])],
            "certificate": {"determinant": _text(determinant)}}


def _attempt(case: dict, phase: str, method: str, candidate: dict) -> dict:
    verdict = verify(case, candidate)
    payload = {"schema_version": 1, "case": case, "phase": phase, "method": method,
               "candidate": candidate, "verification": verdict, "synthetic": True,
               "live_model": False,
               "epistemic_status": "exact_certificate_verified" if verdict["accepted"] else "candidate_rejected",
               "novelty": "known_mathematics"}
    return {"id": "attempt-" + _digest(payload), **payload}


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def _check_existing(path: Path, expected: bytes) -> None:
    if path.is_symlink():
        raise ValueError(f"refusing symlink artifact: {path.name}")
    if path.exists() and (not path.is_file() or path.stat().st_size != len(expected)
                          or path.read_bytes() != expected):
        raise FileExistsError(f"immutable artifact differs: {path.name}; use a new output directory")


def _write_new_or_identical(path: Path, expected: bytes) -> None:
    try:
        with path.open("xb") as handle:
            handle.write(expected)
    except FileExistsError:
        _check_existing(path, expected)


def run_demo(output: Path, seed: int = 7) -> dict:
    """Write an immutable, deterministic pilot run, safely replayable in place.

    Every attempt has a full SHA-256 content identifier and its own record file.
    The JSONL event ledger is created once, never rewritten. Identical reruns
    leave all bytes unchanged; a different run needs another output directory.
    """
    _seed(seed)
    if seed > MAX_SEED - 5:
        raise ValueError("demo seed needs room for five subsequent practice seeds")
    output = Path(output)
    cases = [generate_case(seed + offset) for offset in range(6)]
    attempts = []
    for index, case in enumerate(cases):
        phase = "public_practice" if index == 0 else "public_transfer_practice"
        attempts.append(_attempt(case, phase, "frozen_diagonal_baseline", _flawed_solve(case)))
        attempts.append(_attempt(case, phase, "predetermined_exact_solver", solve(case)))
    baseline = [a for a in attempts if a["method"] == "frozen_diagonal_baseline"]
    revised = [a for a in attempts if a["method"] == "predetermined_exact_solver"]
    report = {
        "schema_version": 1,
        "pilot": "exact_2x2_linear_systems",
        "mode": "deterministic_known_mathematics",
        "seed": seed,
        "synthetic": True,
        "live_model": False,
        "language_model_weights_updated": False,
        "agent_learning_measured": False,
        "novel_mathematics_claimed": False,
        "millennium_progress_claimed": False,
        "verification_method": "independent_exact_rational_certificate_check",
        "formal_proof_assistant_used": False,
        "baseline": {"accepted": sum(a["verification"]["accepted"] for a in baseline), "attempted": len(baseline)},
        "revised": {"accepted": sum(a["verification"]["accepted"] for a in revised), "attempted": len(revised)},
        "case_ids": [case["id"] for case in cases],
        "attempt_ids": [attempt["id"] for attempt in attempts],
        "transfer_scope": "public generated practice, not a protected or contamination-free evaluation",
        "lesson": {
            "procedure": "Solve the coupled system, substitute into every original equation, and check the appropriate certificate.",
            "failure": "Dividing each right-hand side by its diagonal coefficient ignores coupled terms.",
            "scope": "Exact rational two-variable linear systems only.",
            "counterexample": "The diagonal shortcut is valid on diagonal systems with nonzero diagonal entries.",
        },
    }
    lesson = f"""# Exact linear systems: a reproducible teaching pilot

This run uses synthetic public cases and predetermined programs. No live AI
model was called, no language-model weights were updated, and no novel theorem
or Millennium Prize progress is claimed.

The deliberately flawed baseline treats each equation separately by dividing
its right-hand side by the corresponding diagonal coefficient. Coupled equations
also contain the other variable, so this shortcut can fail. It remains valid for
diagonal systems with nonzero diagonal entries; the lesson therefore has a scope.

The corrected solver handles unique solutions, inconsistency and infinitely many
solutions. A separate checker substitutes a proposed solution into every original
equation. Uniqueness additionally requires the correct nonzero determinant;
nonuniqueness requires a nonzero null vector; inconsistency requires a linear
combination of rows with zero coefficients and a nonzero right-hand side.

For seed {seed}, the baseline passed {report['baseline']['accepted']} of {len(baseline)}
exact checks and the predetermined corrected solver passed
{report['revised']['accepted']} of {len(revised)}. These are results on six generated
public practice cases, not an estimate of general intelligence or learning.
Fresh generated variants exercise transfer of the procedure, but they are public
practice and are not a protected evaluation.

Inspect `attempts.jsonl` and each content-addressed record in `records/` to see
the actual matrices, candidate answers, certificates and rejection reasons.
To teach this result, ask a learner to explain the failure, solve a new coupled
case, handle singular cases, and justify why each certificate proves its claim.
Independent learner performance has not been measured by this demonstration.

All mathematical methods used here are standard elementary linear algebra.
An exact arithmetic certificate check is different from formalisation in a
general proof assistant. The implementation and its tests remain inspectable.
"""
    files = {
        output / "report.json": _json_bytes(report),
        output / "lesson.md": lesson.encode("utf-8"),
        output / "attempts.jsonl": ("".join(_canonical(a) + "\n" for a in attempts)).encode("utf-8"),
    }
    for attempt in attempts:
        files[output / "records" / f"{attempt['id']}.json"] = _json_bytes(attempt)
    if output.is_symlink() or (output.exists() and not output.is_dir()):
        raise ValueError("output must be a real directory, not a symlink or file")
    records = output / "records"
    if records.is_symlink() or (records.exists() and not records.is_dir()):
        raise ValueError("records must be a real directory")
    # Detect every existing conflict before writing any new artifact.
    for path, content in files.items():
        _check_existing(path, content)
    output.mkdir(parents=True, exist_ok=True)
    records.mkdir(exist_ok=True)
    for path, content in files.items():
        _write_new_or_identical(path, content)
    return report
