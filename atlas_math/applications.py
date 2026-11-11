"""Exact, reproducible applications of established mathematics.

These public synthetic examples are warm-ups for inspecting certificates and
assumptions. They are neither frontier challenge results nor agent learning
measurements. Input systems use bounded integer coefficients; the existing
rational verifier checks candidates independently of their producer.
"""
from __future__ import annotations

from fractions import Fraction
import json
from math import ceil, comb, floor, gcd
from pathlib import Path

from . import engine


SOURCE_COMMIT = "45e4042884119a0496755c48083846ed85634b79"
SOURCE_ROOT = "https://github.com/Albertito-AI/atlas-open-mathematics/blob/" + SOURCE_COMMIT
MAX_PAIRS = 20


def _integer_system(matrix, rhs):
    if type(matrix) is not list or len(matrix) != 2 or any(type(row) is not list or len(row) != 2 for row in matrix):
        raise ValueError("A must be a list of two integer rows, each of length two")
    if type(rhs) is not list or len(rhs) != 2:
        raise ValueError("b must be a list of two integers")
    if any(type(value) is not int or abs(value) > engine.CASE_BOUND for row in matrix for value in row):
        raise ValueError("A entries must be integers, excluding booleans, of absolute value at most 10^9")
    if any(type(value) is not int or abs(value) > engine.CASE_BOUND for value in rhs):
        raise ValueError("b entries must be integers, excluding booleans, of absolute value at most 10^9")
    return [row[:] for row in matrix], rhs[:]


def _bezout(a, b):
    """Return g,u,v with g>=0 and ua+vb=g, using extended Euclid."""
    r0, r1, u0, u1, v0, v1 = abs(a), abs(b), 1, 0, 0, 1
    while r1:
        quotient = r0 // r1
        r0, r1 = r1, r0 - quotient * r1
        u0, u1 = u1, u0 - quotient * u1
        v0, v1 = v1, v0 - quotient * v1
    return r0, u0 * (-1 if a < 0 else 1), v0 * (-1 if b < 0 else 1)


def verify_integer_witness(matrix, rhs, witness, *, nonnegative=False):
    """Check an independently supplied integer witness by direct substitution."""
    matrix, rhs = _integer_system(matrix, rhs)
    if type(nonnegative) is not bool:
        raise ValueError("nonnegative must be a boolean")
    if type(witness) is not list or len(witness) != 2 or any(type(x) is not int or abs(x) > engine.CANDIDATE_BOUND for x in witness):
        return False
    return ((not nonnegative or all(x >= 0 for x in witness)) and
            all(sum(row[j] * witness[j] for j in range(2)) == rhs[i] for i, row in enumerate(matrix)))


def _nonnegative_family(particular, direction):
    """Intersect the exact integer bounds on the rank-one family parameter."""
    lower, upper, impossible = None, None, False
    for base, step in zip(particular, direction):
        if step == 0:
            impossible = impossible or base < 0
        elif step > 0:
            bound = ceil(Fraction(-base, step))
            lower = bound if lower is None else max(lower, bound)
        else:
            bound = floor(Fraction(-base, step))
            upper = bound if upper is None else min(upper, bound)
    feasible = not impossible and (lower is None or upper is None or lower <= upper)
    bounds = {"integer_parameter_lower": lower, "integer_parameter_upper": upper,
              "fixed_coordinate_negative": impossible}
    if not feasible:
        return None, bounds
    parameter = 0
    if lower is not None:
        parameter = max(parameter, lower)
    if upper is not None:
        parameter = min(parameter, upper)
    bounds["chosen_parameter"] = parameter
    return [base + parameter * step for base, step in zip(particular, direction)], bounds


def analyse_integer_system(matrix, rhs):
    """Classify one 2x2 integer system over Q, Z and nonnegative Z.

    Nonnegativity is a separate application condition. A fractional particular
    solution of a singular system never by itself excludes integer solutions.
    The rank-one branch uses a row gcd and a complete integer parameter family.
    Python arithmetic and this code remain trusted; this is no formal proof of
    the implementation and no new theorem is claimed.
    """
    matrix, rhs = _integer_system(matrix, rhs)
    case = {"id": "applied-integer-system", "A": matrix, "b": rhs, "kind": "unique"}
    candidate = engine.solve(case)
    verification = engine.verify(case, candidate)
    if not verification["accepted"]:
        raise ValueError("Candidate rejected by independent rational verifier: " + verification["reason"])
    result = {"A": matrix, "b": rhs, "rational_status": candidate["status"],
              "rational_candidate": candidate, "rational_verification": verification,
              "integer_feasible": False, "integer_witness": None,
              "nonnegative_integer_feasible": False, "nonnegative_integer_witness": None,
              "verification_status": "exact-instance-checked", "formal_implementation_proof": False}
    if candidate["status"] == "inconsistent":
        result["integer_certificate"] = {"kind": "rational_inconsistency", **candidate["certificate"]}
        result["nonnegative_certificate"] = {"kind": "no_rational_solution"}
        return result
    if candidate["status"] == "unique":
        values = [Fraction(x) for x in candidate["solution"]]
        a, b = matrix[0]
        c, d = matrix[1]
        determinant = a * d - b * c
        numerators = [d * rhs[0] - b * rhs[1], a * rhs[1] - c * rhs[0]]
        result["integer_certificate"] = {
            "kind": "unique_solution_divisibility", "determinant": determinant,
            "cramer_numerators": numerators,
            "remainders_mod_abs_determinant": [n % abs(determinant) for n in numerators],
        }
        if any(x.denominator != 1 for x in values):
            result["nonnegative_certificate"] = {"kind": "unique_rational_solution_is_not_integral"}
            return result
        witness = [x.numerator for x in values]
        result.update(integer_feasible=True, integer_witness=witness)
        if all(x >= 0 for x in witness):
            result.update(nonnegative_integer_feasible=True, nonnegative_integer_witness=witness[:])
            result["nonnegative_certificate"] = {"kind": "direct_nonnegative_witness"}
        else:
            result["nonnegative_certificate"] = {"kind": "unique_solution_has_negative_coordinate",
                                                   "negative_coordinates": [i for i, x in enumerate(witness) if x < 0]}
        return result

    row_index = next((i for i, row in enumerate(matrix) if row != [0, 0]), None)
    if row_index is None:
        result.update(integer_feasible=True, integer_witness=[0, 0],
                      nonnegative_integer_feasible=True, nonnegative_integer_witness=[0, 0])
        result["integer_certificate"] = {"kind": "zero_system", "all_integer_pairs_solve": True}
        result["nonnegative_certificate"] = {"kind": "direct_nonnegative_witness"}
        return result
    left, right = matrix[row_index]
    divisor, u, v = _bezout(left, right)
    if divisor != gcd(left, right) or u * left + v * right != divisor:
        raise ValueError("Extended-Euclid certificate failed its integer identity")
    total = rhs[row_index]
    if total % divisor:
        result["integer_certificate"] = {
            "kind": "row_gcd_obstruction", "row_index": row_index, "divisor": divisor,
            "coefficient_remainders": [left % divisor, right % divisor],
            "rhs_remainder": total % divisor,
        }
        result["nonnegative_certificate"] = {"kind": "no_integer_solution"}
        return result
    particular = [u * (total // divisor), v * (total // divisor)]
    direction = [right // divisor, -left // divisor]
    if not verify_integer_witness(matrix, rhs, particular):
        raise ValueError("Constructed integer particular solution failed direct substitution")
    witness, bounds = _nonnegative_family(particular, direction)
    if witness is not None and not verify_integer_witness(matrix, rhs, witness, nonnegative=True):
        raise ValueError("Constructed nonnegative solution failed direct substitution")
    result.update(integer_feasible=True, integer_witness=particular,
                  nonnegative_integer_feasible=witness is not None,
                  nonnegative_integer_witness=witness)
    result["integer_certificate"] = {
        "kind": "rank_one_integer_family", "row_index": row_index, "row_gcd": divisor,
        "bezout": {"u": u, "v": v, "identity": u * left + v * right},
        "particular": particular, "direction": direction, "parameter_domain": "integers",
    }
    result["nonnegative_certificate"] = {"kind": "integer_parameter_bounds", **bounds}
    return result


def construct_primitive_witness(matrix, rhs):
    """Apply Q0004's elementary construction or display a failed precondition.

    This producer uses extended Euclid and is checked by substitution through
    the existing verifier. It never calls the rational solver. A nonprimitive
    column returns an explicit counterexample to the universal shortcut, not a
    claim that the caller's particular right-hand side is infeasible.
    """
    matrix, rhs = _integer_system(matrix, rhs)
    a, b = matrix[0]
    c, d = matrix[1]
    p, q = rhs
    determinant = a * d - b * c
    if determinant == 0:
        raise ValueError("Q0004's construction requires a nonzero determinant; use the singular-system analysis")
    divisor, u, v = _bezout(a, c)
    if u * a + v * c != divisor or divisor != gcd(a, c):
        raise ValueError("Bézout identity failed")
    result = {"A": matrix, "b": rhs, "determinant": determinant,
              "first_column_gcd": divisor, "bezout": {"u": u, "v": v, "identity": divisor},
              "formal_status": "Q0004-universal-formalisation-pending",
              "verification_status": "exact-instance-checked"}
    if divisor != 1:
        counter_rhs = [a // divisor, c // divisor]
        candidate = {"status": "unique", "solution": [str(Fraction(1, divisor)), "0"],
                     "certificate": {"determinant": str(determinant)}}
        checked = engine.verify({"id": "q0004-obstruction", "A": matrix, "b": counter_rhs, "kind": "unique"}, candidate)
        if not checked["accepted"]:
            raise ValueError("Nonprimitive obstruction failed substitution")
        result.update(applicable=False, status="primitive_column_precondition_fails",
                      counterexample={"b": counter_rhs, "y_numerator": a * counter_rhs[1] - c * counter_rhs[0],
                                      "one_divisibility_test_passes": True, "integer_feasible": False,
                                      "rational_candidate": candidate, "verification": checked},
                      limitation="The counterexample concerns the displayed obstruction right-hand side, not every right-hand side")
        return result
    numerator = a * q - c * p
    if numerator % determinant:
        candidate = {"status": "unique", "solution": [str(Fraction(d * p - b * q, determinant)), str(Fraction(numerator, determinant))],
                     "certificate": {"determinant": str(determinant)}}
        checked = engine.verify({"id": "q0004-divisibility-obstruction", "A": matrix, "b": rhs, "kind": "unique"}, candidate)
        if not checked["accepted"]:
            raise ValueError("Divisibility obstruction failed substitution")
        result.update(applicable=True, status="integer_obstruction", integer_feasible=False,
                      y_numerator=numerator, remainder_mod_abs_determinant=numerator % abs(determinant),
                      rational_candidate=candidate, verification=checked)
        return result
    k = numerator // determinant
    r, s = p - b * k, q - d * k
    witness = [u * r + v * s, k]
    candidate = {"status": "unique", "solution": [str(x) for x in witness],
                 "certificate": {"determinant": str(determinant)}}
    checked = engine.verify({"id": "q0004-construction", "A": matrix, "b": rhs, "kind": "unique"}, candidate)
    if not checked["accepted"]:
        raise ValueError("Bézout construction failed independent substitution")
    result.update(applicable=True, status="integer_witness_constructed", integer_feasible=True,
                  y_numerator=numerator, k=k, residual=[r, s], solution=witness, verification=checked)
    return result


def paired_randomisation_tail(wins, losses, ties=0):
    """Exact one-sided paired tail under the stated fair-assignment sharp null.

    Combinatorial calculation and exhaustive fair-bit counting use different
    paths and must agree. Counts are illustrative inputs, not observed learners.
    Ties do not supply discordance directions and do not enlarge the tail's n.
    """
    if any(type(value) is not int or value < 0 for value in (wins, losses, ties)):
        raise ValueError("wins, losses and ties must be nonnegative integers, excluding booleans")
    if wins + losses + ties > MAX_PAIRS:
        raise ValueError(f"This enumerated warm-up supports at most {MAX_PAIRS} total pairs")
    discordant = wins + losses
    denominator = 1 << discordant
    numerator = sum(comb(discordant, k) for k in range(wins, discordant + 1))
    enumerated = sum(mask.bit_count() >= wins for mask in range(denominator))
    if numerator != enumerated:
        raise ValueError("Combinatorial tail disagrees with exhaustive assignment counting")
    tail = Fraction(numerator, denominator)
    return {"wins": wins, "losses": losses, "ties": ties, "pairs": wins + losses + ties,
            "discordant_pairs": discordant, "one_sided_p": str(tail), "alpha": "1/20",
            "crosses_predeclared_threshold": tail <= Fraction(1, 20),
            "assignments_enumerated": denominator, "favourable_tail_assignments": enumerated,
            "formula_matches_enumeration": True, "observed_agent_sessions": 0,
            "assumptions": ["Independent fair assignment within each matched pair",
                            "Sharp null: assignment changes neither session's binary outcome",
                            "Frozen one-sided alternative, scoring rule, sample and missingness policy",
                            "No optional stopping or substitution of favourable outcomes"]}


def applications_report():
    """Return a deterministic machine-readable warm-up report, with no I/O."""
    batch_matrix = [[3, 2], [1, 5]]
    batch_cases = []
    for identifier, title, matrix, rhs in [
        ("whole-batches", "Two of batch A and one of batch B meet both totals", batch_matrix, [8, 7]),
        ("fractional-only", "Rational totals can fail whole-batch feasibility", batch_matrix, [9, 7]),
        ("negative-integral", "Integral quantities can fail nonnegativity", batch_matrix, [1, 9]),
        ("dependent-totals", "A fractional particular solution does not decide integer existence", [[2, 1], [4, 2]], [5, 10]),
        ("contradictory-totals", "Dependent rows with conflicting totals are inconsistent", [[2, 1], [4, 2]], [5, 11]),
        ("rank-one-lattice-obstruction", "A row gcd can exclude whole batches in a consistent rational system", [[2, 4], [4, 8]], [1, 2]),
    ]:
        entry = {"id": identifier, "title": title, **analyse_integer_system(matrix, rhs)}
        if identifier == "dependent-totals":
            entry["additional_integer_witness"] = [2, 1]
            entry["additional_witness_checked"] = verify_integer_witness(matrix, rhs, [2, 1], nonnegative=True)
        batch_cases.append(entry)
    construction = construct_primitive_witness([[2, 3], [3, 7]], [7, 13])
    obstruction = construct_primitive_witness([[2, 1], [4, 3]], [1, 2])
    return {
        "schema_version": 1, "report_kind": "applied_mathematics_warmup",
        "difficulty": "warm_up_only", "synthetic": True, "live_model": False,
        "agent_learning_measured": False, "observed_agent_sessions": 0,
        "established_mathematics": True, "novel_mathematics_claimed": False,
        "frontier_challenge_solved": False, "millennium_progress_claimed": False,
        "source_commit": SOURCE_COMMIT,
        "source_commit_role": "pinned research background; the applications module is a subsequent implementation",
        "implementation_version": "applications-0.1",
        "command": "python -m atlas_math applications",
        "sources": [
            {"problem_id": "Q0001", "url": SOURCE_ROOT + "/research/agent-attempts/0002/record.md"},
            {"problem_id": "Q0004", "url": SOURCE_ROOT + "/research/agent-attempts/0003/record.md"},
            {"problem_id": "Q0002", "url": SOURCE_ROOT + "/research/agent-attempts/0004/record.md"},
            {"problem_id": "verification-policy", "url": SOURCE_ROOT + "/docs/VERIFICATION.md"},
        ],
        "applications": [
            {"id": "whole-batch-allocation", "title": "Whole-batch resource allocation and consistent totals",
             "problem_ids": ["Q0001", "Q0005-boundary"],
             "scope": "Exact synthetic two-recipe totals with integer and nonnegativity constraints",
             "cases": batch_cases, "verification_status": "exact-instance-checked",
             "limitations": ["No real inventory, capacity, cost, legal or operational data are supplied",
                             "Feasibility is not optimisation or authority to execute a plan",
                             "Singular boundary handling uses established Diophantine arithmetic; no new Q0005 theorem is claimed"]},
            {"id": "constructive-integer-certificates", "title": "Construct and check an integer allocation certificate",
             "problem_ids": ["Q0004"], "scope": "Nonsingular integer matrices with an explicit primitive-column condition",
             "cases": [{"id": "primitive-construction", **construction}, {"id": "nonprimitive-counterexample", **obstruction}],
             "verification_status": "exact-instance-checked", "universal_formalisation": "pending",
             "limitations": ["The construction illustrates established mathematics and the retained Q0004 argument",
                             "These finite substitutions do not close Q0004's universal formalisation gate"]},
            {"id": "paired-evaluation-design", "title": "Check what a proposed learning comparison could establish",
             "problem_ids": ["Q0002"], "scope": "Exact randomisation tails for illustrative matched binary outcomes",
             "cases": [{"id": "nine-to-three", **paired_randomisation_tail(9, 3)},
                       {"id": "ten-to-two", **paired_randomisation_tail(10, 2)},
                       {"id": "all-tied", **paired_randomisation_tail(0, 0, 12)}],
             "verification_status": "exact-finite-calculation", "learner_study_status": "not_executed",
             "limitations": ["No learner responses or human learning outcomes were collected",
                             "The 12-pair proposal requires 12 complete frozen pairs and independent blinded scoring",
                             "A small p-value under the assumptions does not measure effect size or generalisation",
                             "Ties require raw group totals: both groups could be right or both wrong"]},
        ],
        "purpose": "Inspect domain, feasibility, counterexamples and study assumptions before attempting the separate advanced challenge programme",
        "verification_limits": ["Python and its arithmetic/verifiers remain trusted dependencies",
                                "Public worked examples cannot serve as protected examinations",
                                "This report does not retrain an agent, award competence or authorise external action"],
    }


def write_applications_report(path):
    """Write a new or byte-identical report; never replace differing evidence."""
    path = Path(path)
    report = applications_report()
    payload = (json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    if path.is_symlink():
        raise ValueError("Refusing a symlink report destination")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError:
        if path.is_symlink() or not path.is_file() or path.stat().st_size != len(payload) or path.read_bytes() != payload:
            raise FileExistsError("Existing application report differs; use a new output path")
    return report
