from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from atlas_math.challenges import (DATA_BOUND, _generated, generate_challenge,
                                   make_case, verify_certificate)


class ChallengeTests(unittest.TestCase):
    def candidate(self, case, claim, **kwargs):
        return {"case_id": case["case_id"], "claim": claim, **kwargs}

    def test_coupled_optimum_is_not_just_feasibility(self):
        case = make_case([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]],
                         [7, 6, 5], [0] * 4, [10] * 4, [3, 1, 4, 2])
        proof = {"type": "bound", "row_weights": [3, -2, 2]}
        good = self.candidate(case, "optimal", solution=[1, 6, 0, 5], proof=proof)
        self.assertEqual(verify_certificate(case, good)["objective"], 19)
        bad = self.candidate(case, "optimal", solution=[2, 5, 1, 4], proof=proof)
        self.assertFalse(verify_certificate(case, bad)["accepted"])
        del bad["proof"]
        bad["claim"] = "feasible"
        result = verify_certificate(case, bad)
        self.assertTrue(result["accepted"])
        self.assertFalse(result["optimality_proved"])
        self.assertEqual(result["objective"], 23)

    def test_mixed_modular_obstruction_with_row_gcds_one(self):
        case = make_case([[1, 1, 1, 0], [1, -1, 1, 0], [0, 0, 1, 2]],
                         [2, 1, 4], [0] * 4, [10] * 4, [1] * 4)
        rational = [Fraction(3, 2), Fraction(1, 2), Fraction(0), Fraction(2)]
        self.assertEqual([sum(a*x for a, x in zip(row, rational)) for row in case["A"]], case["b"])
        candidate = self.candidate(case, "infeasible", proof={
            "type": "modular", "row_weights": [1, 1, 0], "modulus": 2})
        self.assertTrue(verify_certificate(case, candidate)["accepted"])
        candidate["proof"]["row_weights"] = [1, 0, 0]
        self.assertFalse(verify_certificate(case, candidate)["accepted"])

    def test_singular_fractional_particular_does_not_imply_integer_infeasibility(self):
        case = make_case([[2, 1], [4, 2]], [5, 10], [0, 0], [5, 5], [1, 1])
        self.assertTrue(verify_certificate(case, self.candidate(case, "feasible", solution=[2, 1]))["accepted"])
        forged = self.candidate(case, "infeasible", proof={
            "type": "modular", "row_weights": [1, 0], "modulus": 2})
        self.assertFalse(verify_certificate(case, forged)["accepted"])

    def test_integer_rounding_closes_a_fractional_gap(self):
        case = make_case([[2, -1]], [1], [0, 0], [2, 2], [1, 0])
        candidate = self.candidate(case, "bound", solution=[1, 1], row_weights=["1/2"])
        result = verify_certificate(case, candidate)
        self.assertEqual(result["lower_bound"], "1/2")
        self.assertEqual(result["integer_lower_bound"], 1)
        self.assertTrue(result["optimality_proved"])

    def test_branching_can_close_a_gap_that_rounding_does_not(self):
        case = make_case([[1, 5]], [9], [0, 0], [9, 2], [1, 1])
        bounded = self.candidate(case, "bound", solution=[4, 1], row_weights=["1/5"])
        result = verify_certificate(case, bounded)
        self.assertTrue(result["accepted"])
        self.assertFalse(result["optimality_proved"])
        self.assertEqual(result["integer_gap"], 3)
        loose = self.candidate(case, "optimal", solution=[4, 1],
                               proof={"type": "bound", "row_weights": ["1/5"]})
        self.assertFalse(verify_certificate(case, loose)["accepted"])
        proof = {"type": "split", "variable": 1, "at": 1,
                 "left": {"type": "bound", "row_weights": [1]},
                 "right": {"type": "contradiction", "row_weights": [1]}}
        checked = verify_certificate(case, self.candidate(case, "optimal", solution=[4, 1], proof=proof))
        self.assertTrue(checked["optimality_proved"])
        self.assertEqual(checked["checked_nodes"], 3)
        del proof["right"]
        self.assertFalse(verify_certificate(case, self.candidate(case, "optimal", solution=[4, 1], proof=proof))["accepted"])

    def test_modular_certificate_substitutes_fixed_variables(self):
        case = make_case([[2, 3]], [7], [0, 2], [5, 2], [1, 1])
        proof = {"type": "modular", "row_weights": [1], "modulus": 2}
        self.assertTrue(verify_certificate(case, self.candidate(case, "infeasible", proof=proof))["accepted"])
        unfixed = make_case([[2, 3]], [7], [0, 0], [5, 2], [1, 1])
        self.assertFalse(verify_certificate(unfixed, self.candidate(unfixed, "infeasible", proof=proof))["accepted"])

    def test_empty_bounds_and_false_infeasibility_are_distinct(self):
        case = make_case([[0]], [0], [2], [1], [0])
        self.assertTrue(verify_certificate(case, self.candidate(case, "infeasible", proof={"type": "empty"}))["accepted"])
        case = make_case([[0]], [0], [0], [1], [0])
        for proof in ({"type": "empty"}, {"type": "bound", "row_weights": [1]},
                      {"type": "contradiction", "row_weights": [1]},
                      {"type": "modular", "row_weights": [1], "modulus": 2}):
            self.assertFalse(verify_certificate(case, self.candidate(case, "infeasible", proof=proof))["accepted"])

    def test_generated_constructions_and_large_boundaries(self):
        for family, size, seed in product(("allocation", "obstruction", "branching"), (4, 16, 64), (0, 7, 31)):
            with self.subTest(family=family, size=size, seed=seed):
                case, candidate = _generated(family, size, seed)
                self.assertTrue(verify_certificate(case, candidate)["accepted"])
                self.assertEqual(case, generate_challenge(family, size, seed))
                self.assertNotIn("solution", case)
                self.assertNotIn("proof", case)

    def test_small_branching_optimum_against_exhaustive_enumeration(self):
        case, candidate = _generated("branching", 4, 7)
        feasible = []
        for x in product(*(range(l, u + 1) for l, u in zip(case["lower"], case["upper"]))):
            if all(sum(a*v for a, v in zip(row, x)) == b for row, b in zip(case["A"], case["b"])):
                feasible.append(sum(c*v for c, v in zip(case["cost"], x)))
        self.assertEqual(verify_certificate(case, candidate)["objective"], min(feasible))

    def test_signed_dual_certificates_against_independent_small_enumeration(self):
        for a, b, c, d in product((-1, 1), repeat=4):
            case = make_case([[a, b]], [a + b], [-1, -1], [2, 2], [c, d])
            feasible = [(x, y) for x, y in product(range(-1, 3), repeat=2) if a*x + b*y == a+b]
            optimum = min(c*x + d*y for x, y in feasible)
            for x, y in feasible:
                for w in (-2, -1, 0, 1, 2):
                    candidate = self.candidate(case, "optimal", solution=[x, y],
                                               proof={"type": "bound", "row_weights": [w]})
                    result = verify_certificate(case, candidate)
                    if result["accepted"]:
                        self.assertEqual(result["objective"], optimum)

    def test_verifier_does_not_call_candidate_construction(self):
        case, candidate = _generated("allocation", 4, 7)
        with patch("atlas_math.challenges._generated", side_effect=AssertionError("Generator called")):
            self.assertTrue(verify_certificate(case, candidate)["accepted"])

    def test_changed_target_rejects_stale_identity(self):
        case, candidate = _generated("allocation", 4, 7)
        changed = deepcopy(case)
        changed["cost"][0] += 1
        self.assertFalse(verify_certificate(changed, candidate)["accepted"])
        changed = make_case(changed["A"], changed["b"], changed["lower"], changed["upper"], changed["cost"])
        self.assertFalse(verify_certificate(changed, candidate)["accepted"])

    def test_input_types_and_unsupported_claims_fail_closed(self):
        case, candidate = _generated("allocation", 4, 7)
        for value in (True, 1.0, "2/2", "__import__('os')", "1/0", "1" * 257, DATA_BOUND * 10**100):
            item = deepcopy(candidate)
            item["proof"]["row_weights"][0] = value
            self.assertFalse(verify_certificate(case, item)["accepted"])
        for value in (True, 1.0, "1"):
            item = deepcopy(candidate)
            item["solution"][0] = value
            self.assertFalse(verify_certificate(case, item)["accepted"])
        item = deepcopy(candidate)
        item["claim"] = "probably_optimal"
        self.assertFalse(verify_certificate(case, item)["accepted"])

    def test_cli_accepts_only_bounded_unambiguous_json_and_preserves_files(self):
        with tempfile.TemporaryDirectory() as directory:
            case_path, candidate_path = Path(directory) / "case.json", Path(directory) / "candidate.json"
            command = [sys.executable, "-m", "atlas_math.challenges"]
            generated = subprocess.run(command + ["generate", "--seed", "7", "--output", str(case_path)], capture_output=True)
            self.assertEqual(generated.returncode, 0, generated.stderr)
            original = case_path.read_bytes()
            duplicate = subprocess.run(command + ["generate", "--seed", "8", "--output", str(case_path)], capture_output=True)
            self.assertEqual(duplicate.returncode, 2)
            self.assertEqual(case_path.read_bytes(), original)
            for raw in ('{"claim":"feasible","claim":"optimal"}', '{"x":NaN}', 'x' * 2_000_001):
                candidate_path.write_text(raw)
                result = subprocess.run(command + ["verify", "--case", str(case_path), "--candidate", str(candidate_path)], capture_output=True)
                self.assertEqual(result.returncode, 2, result.stderr)


if __name__ == "__main__":
    unittest.main()
