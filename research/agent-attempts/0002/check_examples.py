#!/usr/bin/env python3
"""Finite teaching checks for Q0001. The universal proof is in Lean."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from atlas_math.engine import verify


def checked_case(identifier, matrix, rhs, solution, determinant):
    case = {"id": identifier, "A": matrix, "b": rhs, "kind": "unique"}
    candidate = {"status": "unique", "solution": [str(v) for v in solution],
                 "certificate": {"determinant": str(determinant)}}
    result = verify(case, candidate)
    if not result["accepted"]:
        raise ValueError((case, candidate, result))
    return {"case": case, "candidate": candidate, "rational_verification": result,
            "integer_solution": all(Fraction(v).denominator == 1 for v in solution)}


def main():
    integral = 0
    for p in range(-11, 12):
        for q in range(-11, 12):
            x, y = Fraction(4*p-3*q, 11), Fraction(p+2*q, 11)
            result = checked_case(f"grid-{p}-{q}", [[2, 3], [-1, 4]], [p, q], [x, y], 11)
            criterion = (p + 2*q) % 11 == 0
            if criterion != result["integer_solution"]:
                raise ValueError((p, q, "criterion mismatch"))
            if criterion:
                k = (p + 2*q) // 11
                if [x, y] != [4*k-q, k]:
                    raise ValueError((p, q, "witness mismatch"))
                integral += 1
    modular_image = {((2*x+3*y) % 11, (-x+4*y) % 11)
                     for x in range(11) for y in range(11)}
    for p in range(11):
        for q in range(11):
            if ((p, q) in modular_image) != ((p+2*q) % 11 == 0):
                raise ValueError((p, q, "modular image mismatch"))
    counter = checked_case("one-numerator-counterexample", [[2, 2], [2, 4]],
                           [1, 2], [Fraction(0), Fraction(1, 2)], 4)
    counter.update({"x_numerator": 0, "y_numerator": 2,
                    "first_numerator_divisible": True, "second_numerator_divisible": False,
                    "refutation": "2x+2y=1 has no integer solution; rational uniqueness gives (0,1/2)."})
    practice = checked_case("batching-public-practice", [[3, 2], [1, 5]],
                            [8, 7], [Fraction(2), Fraction(1)], 13)
    output = {
        "problem_id": "Q0001", "scope": "Finite supporting checks, not a universal proof or a held-out agent evaluation",
        "command": "python research/agent-attempts/0002/check_examples.py",
        "source_base_commit": "0fcb42f3e52853a46116ce835338c3d9f84e8c1b",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "verifier_sha256": hashlib.sha256((ROOT / "atlas_math/engine.py").read_bytes()).hexdigest(),
        "grid": {"p_bounds_inclusive": [-11, 11], "q_bounds_inclusive": [-11, 11],
                 "checked": 529, "integer_solutions": integral, "criterion_mismatches": 0},
        "modulo_11": {"input_pairs_checked": 121, "image_size": len(modular_image), "criterion_mismatches": 0},
        "rejected_generalisation": counter, "public_practice": practice,
        "novelty": "Known elementary mathematics", "human_or_agent_transfer_measured": False}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
