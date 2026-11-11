"""Exact certificates for public bounded integer-planning challenges.

This is a data checker and development generator, not an agent runner. Generated
cases, constructions and reference certificates are public and uncalibrated.
The checker never invokes a solver or executes a contributor's code.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import re
import sys


SCHEMA = "atlas-integer-work-v1"
MAX_DIMENSION = 64
DATA_BOUND = 10**30
CERTIFICATE_BOUND = 10**120
MAX_NODES = 257
MAX_DEPTH = 64
MAX_INPUT_BYTES = 2_000_000
FAMILIES = ("allocation", "obstruction", "branching")
_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


class Rejected(Exception):
    """A well-formed certificate does not establish the submitted claim."""


def _fields(value, expected, label):
    if type(value) is not dict or set(value) != set(expected):
        raise ValueError(f"{label} must contain exactly {sorted(expected)}")


def _integer(value, bound=DATA_BOUND):
    if type(value) is not int or abs(value) > bound:
        raise ValueError("Expected a bounded integer, excluding booleans")
    return value


def _rational(value):
    if type(value) is int:
        return Fraction(_integer(value, CERTIFICATE_BOUND))
    if type(value) is not str or len(value) > 256 or not _RATIONAL.fullmatch(value):
        raise ValueError("Expected an integer or a bounded canonical rational string")
    result = Fraction(value)
    if abs(result.numerator) > CERTIFICATE_BOUND or result.denominator > CERTIFICATE_BOUND:
        raise ValueError("Certificate rational exceeds its bound")
    if str(result) != value:
        raise ValueError("Rational strings must be reduced and canonical")
    return result


def _vector(value, length, parse=_integer):
    if type(value) is not list or len(value) != length:
        raise ValueError(f"Expected a vector with {length} entries")
    return [parse(v) for v in value]


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _identity(payload):
    return "integer-" + hashlib.sha256(_canonical(payload).encode()).hexdigest()


def make_case(A, b, lower, upper, cost):
    """Bind an exact mathematical target to its content digest."""
    payload = {"schema_version": SCHEMA, "A": A, "b": b,
               "lower": lower, "upper": upper, "cost": cost}
    case = {"case_id": _identity(payload), **payload}
    _case(case)
    return case


def _case(case):
    _fields(case, {"schema_version", "case_id", "A", "b", "lower", "upper", "cost"}, "case")
    if case["schema_version"] != SCHEMA:
        raise ValueError("Unknown case schema")
    A = case["A"]
    if type(A) is not list or not 1 <= len(A) <= MAX_DIMENSION:
        raise ValueError("Matrix row count is outside the supported bound")
    if type(A[0]) is not list or not 1 <= len(A[0]) <= MAX_DIMENSION:
        raise ValueError("Matrix column count is outside the supported bound")
    n = len(A[0])
    A = [_vector(row, n) for row in A]
    b = _vector(case["b"], len(A))
    lower, upper, cost = [_vector(case[name], n) for name in ("lower", "upper", "cost")]
    payload = {key: value for key, value in case.items() if key != "case_id"}
    if case["case_id"] != _identity(payload):
        raise ValueError("Case identity does not match its exact target")
    return A, b, lower, upper, cost


def _dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def _combination(A, weights):
    return [_dot(weights, column) for column in zip(*A)]


def _interval(coefficients, lower, upper):
    low = sum(min(a * l, a * u) for a, l, u in zip(coefficients, lower, upper))
    high = sum(max(a * l, a * u) for a, l, u in zip(coefficients, lower, upper))
    return low, high


def _lower_bound(A, b, lower, upper, cost, weights):
    reduced = [c - a for c, a in zip(cost, _combination(A, weights))]
    return _dot(weights, b) + _interval(reduced, lower, upper)[0]


def _ceil(value):
    return -(-value.numerator // value.denominator)


def _witness(A, b, lower, upper, cost, solution):
    x = _vector(solution, len(cost))
    if any(not l <= value <= u for value, l, u in zip(x, lower, upper)):
        raise Rejected("The integer witness violates a bound")
    if any(_dot(row, x) != rhs for row, rhs in zip(A, b)):
        raise Rejected("The integer witness does not satisfy every original equality")
    return _dot(cost, x)


def _proof(node, A, b, lower, upper, cost, target, counter, depth=0):
    counter[0] += 1
    if counter[0] > MAX_NODES or depth > MAX_DEPTH:
        raise ValueError("Proof exceeds the node or depth verification bound")
    if type(node) is not dict or type(node.get("type")) is not str:
        raise ValueError("Every proof node needs a type")
    kind = node["type"]
    if kind == "split":
        _fields(node, {"type", "variable", "at", "left", "right"}, "split")
        index = _integer(node["variable"])
        at = _integer(node["at"])
        if not 0 <= index < len(cost) or not lower[index] <= at < upper[index]:
            raise ValueError("A split must strictly divide one current integer interval")
        left_upper, right_lower = list(upper), list(lower)
        left_upper[index], right_lower[index] = at, at + 1
        _proof(node["left"], A, b, lower, left_upper, cost, target, counter, depth + 1)
        _proof(node["right"], A, b, right_lower, upper, cost, target, counter, depth + 1)
        return
    if kind == "empty":
        _fields(node, {"type"}, "empty leaf")
        if not any(l > u for l, u in zip(lower, upper)):
            raise Rejected("The alleged empty integer box is nonempty")
        return
    if kind not in {"bound", "contradiction", "modular"}:
        raise ValueError("Unknown proof-node type")
    fields = {"type", "row_weights", "modulus"} if kind == "modular" else {"type", "row_weights"}
    _fields(node, fields, kind + " leaf")
    if kind == "modular":
        weights = _vector(node["row_weights"], len(A))
        modulus = _integer(node["modulus"], 10**12)
        if modulus < 2:
            raise ValueError("A modular obstruction needs an integer modulus at least two")
        coefficients = _combination(A, weights)
        residual = _dot(weights, b)
        for a, l, u in zip(coefficients, lower, upper):
            if l == u:
                residual -= a * l
            elif a % modulus:
                raise Rejected("A free variable has a nonzero coefficient modulo the modulus")
        if residual % modulus == 0:
            raise Rejected("The proposed modular obstruction has zero residual")
        return
    weights = _vector(node["row_weights"], len(A), _rational)
    if kind == "contradiction":
        low, high = _interval(_combination(A, weights), lower, upper)
        rhs = _dot(weights, b)
        if low <= rhs <= high:
            raise Rejected("The row combination does not contradict the current bounds")
        return
    if target is None:
        raise ValueError("An objective bound alone cannot establish infeasibility")
    value = _lower_bound(A, b, lower, upper, cost, weights)
    if _ceil(value) < target:
        raise Rejected("The integer lower bound leaves an unclosed optimality gap")


def verify_certificate(case, candidate):
    """Verify one data certificate, with exact arithmetic and no candidate solver.

    Acceptance establishes the stated bounded claim, not novelty, model fitness,
    learner improvement, hidden assessment, or correctness of this checker for
    all inputs. An unsupported proof can be reviewed through a separate route.
    """
    try:
        A, b, lower, upper, cost = _case(case)
        if type(candidate) is not dict or type(candidate.get("claim")) is not str:
            raise ValueError("Candidate requires a claim")
        claim = candidate["claim"]
        fields = {"case_id", "claim"}
        if claim in {"feasible", "optimal", "bound"}:
            fields.add("solution")
        if claim in {"optimal", "infeasible"}:
            fields.add("proof")
        if claim == "bound":
            fields.add("row_weights")
        if claim not in {"feasible", "optimal", "infeasible", "bound"}:
            raise ValueError("Unsupported certificate claim")
        _fields(candidate, fields, "candidate")
        if candidate["case_id"] != case["case_id"]:
            raise ValueError("Candidate belongs to a different frozen case")
        result = {"accepted": True, "case_id": case["case_id"], "claim": claim,
                  "optimality_proved": False, "checked_nodes": 0,
                  "scope": "Exact submitted bounded integer model; public development material"}
        if claim != "infeasible":
            result["objective"] = _witness(A, b, lower, upper, cost, candidate["solution"])
        if claim == "bound":
            weights = _vector(candidate["row_weights"], len(A), _rational)
            bound = _lower_bound(A, b, lower, upper, cost, weights)
            result.update(lower_bound=str(bound), integer_lower_bound=_ceil(bound),
                          rational_gap=str(Fraction(result["objective"]) - bound),
                          integer_gap=result["objective"] - _ceil(bound),
                          optimality_proved=_ceil(bound) == result["objective"])
        if claim in {"optimal", "infeasible"}:
            counter = [0]
            _proof(candidate["proof"], A, b, lower, upper, cost,
                   result.get("objective"), counter)
            result.update(checked_nodes=counter[0], optimality_proved=claim == "optimal")
        return result
    except (ValueError, TypeError, KeyError, RecursionError) as exc:
        return {"accepted": False, "error": "invalid_input", "reason": str(exc)}
    except Rejected as exc:
        return {"accepted": False, "error": "unproved", "reason": str(exc)}


def _generated(family, size, seed):
    if type(family) is not str or family not in FAMILIES:
        raise ValueError("Unknown public challenge family")
    if type(size) is not int or not 4 <= size <= MAX_DIMENSION:
        raise ValueError("Public generator size must be between 4 and 64 variables")
    if type(seed) is not int or not 0 <= seed < 2**63:
        raise ValueError("Seed must be an integer between 0 and 2**63-1")
    rng = random.Random(seed)
    m, n = max(2, size // 2), size
    if family == "allocation":
        A = [[rng.randint(1, 9) for _ in range(n)] for _ in range(m)]
        weights = [rng.randint(1, 7) for _ in range(m)]
        lower, upper = [0] * n, [rng.randint(5, 20) for _ in range(n)]
        reduced = [rng.randint(-4, 4) if j % 3 else 0 for j in range(n)]
        x = [l if r > 0 else u if r < 0 else rng.randint(l, u)
             for l, u, r in zip(lower, upper, reduced)]
        cost = [v + r for v, r in zip(_combination(A, weights), reduced)]
        b = [_dot(row, x) for row in A]
        proof = {"type": "bound", "row_weights": weights}
        claim = "optimal"
    elif family == "obstruction":
        modulus = rng.choice([2, 3, 5, 7, 11])
        weights = [rng.randint(1, 3) for _ in range(m - 1)] + [1]
        A = [[rng.randint(-7, 7) for _ in range(n)] for _ in range(m - 1)]
        A.append([modulus * rng.randint(-3, 3) - sum(weights[i] * A[i][j] for i in range(m - 1))
                  for j in range(n)])
        x = [rng.randint(0, 10) for _ in range(n)]
        b = [_dot(row, x) for row in A]
        b[-1] += 1
        lower, upper, cost = [0] * n, [10] * n, [1] * n
        proof = {"type": "modular", "row_weights": weights, "modulus": modulus}
        claim = "infeasible"
    else:
        if n % 2:
            raise ValueError("The branching family requires an even variable count")
        ks = [rng.randint(3, 9) for _ in range(m)]
        A = [[(1 if j == 2 * i else k if j == 2 * i + 1 else 0) for j in range(n)]
             for i, k in enumerate(ks)]
        b = [2 * k - 1 for k in ks]
        lower = [0] * n
        upper = [value for k in ks for value in (2 * k - 1, 2)]
        x = [value for k in ks for value in (k - 1, 1)]
        cost = [1] * n
        proof = {"type": "bound", "row_weights": [1] * m}
        for i in reversed(range(m)):
            weights = [int(j == i) for j in range(m)]
            proof = {"type": "split", "variable": 2 * i + 1, "at": 1,
                     "left": proof, "right": {"type": "contradiction", "row_weights": weights}}
        claim = "optimal"
    case = make_case(A, b, lower, upper, cost)
    candidate = {"case_id": case["case_id"], "claim": claim, "proof": proof}
    if claim == "optimal":
        candidate["solution"] = x
    return case, candidate


def generate_challenge(family="branching", size=8, seed=7):
    """Return only the problem. The public generator is not a hidden exam."""
    return _generated(family, size, seed)[0]


def describe():
    return {
        "schema_version": SCHEMA, "domain": "integers", "objective": "minimise cost dot x",
        "constraints": "A x = b and lower <= x <= upper",
        "case_fields": ["schema_version", "case_id", "A", "b", "lower", "upper", "cost"],
        "claims": {
            "feasible": ["case_id", "claim", "solution"],
            "bound": ["case_id", "claim", "solution", "row_weights"],
            "optimal": ["case_id", "claim", "solution", "proof"],
            "infeasible": ["case_id", "claim", "proof"],
        },
        "proof_nodes": {
            "bound": ["type", "row_weights"], "contradiction": ["type", "row_weights"],
            "modular": ["type", "row_weights", "modulus"], "empty": ["type"],
            "split": ["type", "variable", "at", "left", "right"],
        },
        "limits": {"rows": MAX_DIMENSION, "columns": MAX_DIMENSION,
                   "absolute_input_integer": DATA_BOUND, "proof_nodes": MAX_NODES,
                   "proof_depth": MAX_DEPTH, "input_bytes": MAX_INPUT_BYTES},
        "public_development_only": True, "difficulty_calibrated": False,
        "agent_runner": False, "unknown_claim_route": "Independent mathematical review; automatic rejection is not disproof",
    }


def run_challenge_demo():
    records = []
    for family in FAMILIES:
        case, candidate = _generated(family, 8, 7)
        verdict = verify_certificate(case, candidate)
        if not verdict["accepted"]:
            raise RuntimeError("A reference construction failed its independent certificate check")
        records.append({"family": family, "case": case, "reference_candidate": candidate, "verification": verdict})
    return {"schema_version": "atlas-challenge-demo-v1", "synthetic": True,
            "learning_measured": False, "difficulty_calibrated": False,
            "novelty_status": "established_mathematics", "records": records,
            "limitations": ["Public generators and reference answers are exposed development material.",
                            "Dimensions alone do not establish difficulty for a capable AI agent.",
                            "Certificates address the submitted model, not its fit to a real deployment.",
                            "No live model, weight update, held-out study or autonomous task execution occurs."]}


def _read(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    def bad_constant(value):
        raise ValueError("Non-finite JSON constant: " + value)
    with path.open("rb") as stream:
        raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError("Input exceeds the 2 MB development limit")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=bad_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("describe")
    commands.add_parser("demo")
    generate = commands.add_parser("generate")
    generate.add_argument("--family", choices=FAMILIES, default="branching")
    generate.add_argument("--size", type=int, default=8)
    generate.add_argument("--seed", type=int, required=True)
    generate.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("--case", type=Path, required=True)
    verify.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "generate":
            case = generate_challenge(args.family, args.size, args.seed)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(json.dumps(case, sort_keys=True, indent=2) + "\n")
            result = {"ok": True, "case_id": case["case_id"], "output": str(args.output),
                      "public_development_only": True, "difficulty_calibrated": False}
        elif args.command == "verify":
            result = verify_certificate(_read(args.case), _read(args.candidate))
        else:
            result = describe() if args.command == "describe" else run_challenge_demo()
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0 if result.get("accepted", True) else 2 if result.get("error") == "invalid_input" else 1
    except (ValueError, OSError, UnicodeError, RecursionError) as exc:
        print(json.dumps({"accepted": False, "error": "invalid_input", "reason": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
