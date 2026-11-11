"""Independent finite and adversarial review of integer-work certificates.

The finite oracle enumerates original integer boxes without using the producer,
dual-bound calculation, modular checker or proof walker. These tests are bounded
implementation evidence, not a universal proof of the verifier.
"""
from fractions import Fraction
from itertools import product
import random
import unittest

from atlas_math.challenges import make_case, verify_certificate


def feasible_points(case):
    return [
        point
        for point in product(*(range(lo, hi + 1) for lo, hi in
                               zip(case["lower"], case["upper"])))
        if all(sum(coefficient * value for coefficient, value in zip(row, point)) == rhs
               for row, rhs in zip(case["A"], case["b"]))
    ]


def finite_cases():
    rng = random.Random(20261111)
    for index in range(90):
        columns, rows = 1 + index % 3, 1 + (index // 3) % 3
        lower = [rng.randint(-2, 1) for _ in range(columns)]
        upper = [value + rng.randint(0, 3) for value in lower]
        matrix = [[rng.randint(-3, 3) for _ in range(columns)] for _ in range(rows)]
        if index % 3:
            witness = [rng.randint(lo, hi) for lo, hi in zip(lower, upper)]
            rhs = [sum(a * x for a, x in zip(row, witness)) for row in matrix]
        else:
            rhs = [rng.randint(-9, 9) for _ in range(rows)]
        cost = [rng.randint(-4, 4) for _ in range(columns)]
        yield make_case(matrix, rhs, lower, upper, cost)


def candidate(case, claim, **fields):
    return {"case_id": case["case_id"], "claim": claim, **fields}


def bound_leaf():
    return {"type": "bound", "row_weights": [0]}


class IndependentChallengeReview(unittest.TestCase):
    def test_signed_rectangular_bounds_against_finite_oracle(self):
        accepted_optima = checked = 0
        for case in finite_cases():
            points = feasible_points(case)
            if not points:
                continue
            objective = lambda point: sum(c * x for c, x in zip(case["cost"], point))
            optimum = min(map(objective, points))
            rows = len(case["A"])
            weights_to_try = [[0] * rows, [1] * rows, [-1] * rows,
                              ["1/2"] * rows,
                              ["-2/3" if i % 2 else "3/2" for i in range(rows)]]
            for point in {points[0], points[-1], min(points, key=objective)}:
                for weights in weights_to_try:
                    with self.subTest(case=case["case_id"], point=point, weights=weights):
                        result = verify_certificate(case, candidate(
                            case, "bound", solution=list(point), row_weights=weights))
                        self.assertTrue(result["accepted"], result)
                        self.assertLessEqual(Fraction(result["lower_bound"]), optimum)
                        self.assertLessEqual(result["integer_lower_bound"], optimum)
                        self.assertGreaterEqual(result["integer_gap"], 0)
                        if result["optimality_proved"]:
                            self.assertEqual(result["objective"], optimum)
                            accepted_optima += 1
                        proof_result = verify_certificate(case, candidate(
                            case, "optimal", solution=list(point),
                            proof={"type": "bound", "row_weights": weights}))
                        if proof_result["accepted"]:
                            self.assertEqual(objective(point), optimum)
                        checked += 1
        self.assertGreater(checked, 300)
        self.assertGreater(accepted_optima, 0)

    def test_infeasibility_leaves_against_finite_oracle(self):
        accepted_obstructions = 0
        for case in finite_cases():
            points = feasible_points(case)
            rows = len(case["A"])
            weights_to_try = [[0] * rows, [1] * rows, [-1] * rows,
                              [(-1) ** i * (i + 1) for i in range(rows)]]
            weights_to_try += [[int(i == j) for i in range(rows)] for j in range(rows)]
            for weights in weights_to_try:
                proofs = [{"type": "contradiction", "row_weights": weights}]
                proofs += [{"type": "modular", "row_weights": weights, "modulus": modulus}
                           for modulus in (2, 3, 5)]
                for proof in proofs:
                    result = verify_certificate(case, candidate(case, "infeasible", proof=proof))
                    if result["accepted"]:
                        self.assertEqual(points, [], (case, proof, points))
                        accepted_obstructions += 1
        self.assertGreater(accepted_obstructions, 0)

    def test_both_children_must_cover_and_prove_the_claim(self):
        # The left half supports cost >= 0; the right half contains a better plan.
        case = make_case([[0]], [0], [-3], [4], [-1])
        proof = {"type": "split", "variable": 0, "at": 0,
                 "left": bound_leaf(), "right": bound_leaf()}
        result = verify_certificate(case, candidate(case, "optimal", solution=[0], proof=proof))
        self.assertFalse(result["accepted"])
        self.assertEqual(result["error"], "unproved")

        # The left half is infeasible, but the right half contains x = 2.
        case = make_case([[1]], [2], [0], [3], [0])
        proof = {"type": "split", "variable": 0, "at": 1,
                 "left": {"type": "contradiction", "row_weights": [1]},
                 "right": {"type": "contradiction", "row_weights": [1]}}
        self.assertFalse(verify_certificate(case, candidate(case, "infeasible", proof=proof))["accepted"])

    def test_fixed_variable_substitution_does_not_leak_between_siblings(self):
        case = make_case([[2, 3]], [7], [0, 0], [5, 2], [0, 0])
        self.assertIn((2, 1), feasible_points(case))
        # y = 0 is obstructed modulo two, but the sibling interval has y = 1.
        proof = {"type": "split", "variable": 1, "at": 0,
                 "left": {"type": "modular", "row_weights": [1], "modulus": 2},
                 "right": {"type": "modular", "row_weights": [1], "modulus": 2}}
        result = verify_certificate(case, candidate(case, "infeasible", proof=proof))
        self.assertFalse(result["accepted"])

    def test_integer_ceiling_is_correct_for_negative_fractional_bound(self):
        case = make_case([[2, -1]], [-1], [-2, 0], [1, 3], [1, 0])
        result = verify_certificate(case, candidate(case, "bound", solution=[0, 1], row_weights=["1/2"]))
        self.assertTrue(result["accepted"])
        self.assertEqual(result["lower_bound"], "-1/2")
        self.assertEqual(result["integer_lower_bound"], 0)
        self.assertTrue(result["optimality_proved"])
        self.assertEqual(min(point[0] for point in feasible_points(case)), 0)

    def test_node_limit_counts_both_subtrees_at_the_exact_boundary(self):
        def tree(lo, hi):
            if lo == hi:
                return bound_leaf()
            middle = (lo + hi) // 2
            return {"type": "split", "variable": 0, "at": middle,
                    "left": tree(lo, middle), "right": tree(middle + 1, hi)}
        for upper, expected in ((128, True), (129, False)):
            case = make_case([[0]], [0], [0], [upper], [0])
            result = verify_certificate(case, candidate(case, "optimal", solution=[0], proof=tree(0, upper)))
            self.assertEqual(result["accepted"], expected, result)
            if expected:
                self.assertEqual(result["checked_nodes"], 257)
            else:
                self.assertEqual(result["error"], "invalid_input")

    def test_depth_limit_applies_even_within_node_budget(self):
        def chain(lo, hi):
            if lo == hi:
                return bound_leaf()
            return {"type": "split", "variable": 0, "at": lo,
                    "left": bound_leaf(), "right": chain(lo + 1, hi)}
        for upper, expected in ((64, True), (65, False)):
            case = make_case([[0]], [0], [0], [upper], [0])
            result = verify_certificate(case, candidate(case, "optimal", solution=[0], proof=chain(0, upper)))
            self.assertEqual(result["accepted"], expected, result)
            if not expected:
                self.assertEqual(result["error"], "invalid_input")


if __name__ == "__main__":
    unittest.main()
