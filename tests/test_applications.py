"""Independent identities, application boundaries and immutable report checks."""
import copy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from atlas_math.applications import (
    SOURCE_COMMIT, analyse_integer_system, applications_report,
    construct_primitive_witness, paired_randomisation_tail,
    verify_integer_witness, write_applications_report,
)


ROOT = Path(__file__).resolve().parents[1]


class AllocationTests(unittest.TestCase):
    def test_batch_examples_distinguish_three_domains(self):
        matrix = [[3, 2], [1, 5]]
        whole = analyse_integer_system(matrix, [8, 7])
        fractional = analyse_integer_system(matrix, [9, 7])
        negative = analyse_integer_system(matrix, [1, 9])
        self.assertEqual(whole["integer_witness"], [2, 1])
        self.assertTrue(whole["nonnegative_integer_feasible"])
        self.assertEqual(fractional["rational_candidate"]["solution"], ["31/13", "12/13"])
        self.assertFalse(fractional["integer_feasible"])
        self.assertEqual(negative["integer_witness"], [-1, 2])
        self.assertTrue(negative["integer_feasible"])
        self.assertFalse(negative["nonnegative_integer_feasible"])
        self.assertEqual(negative["nonnegative_certificate"]["negative_coordinates"], [0])

    def test_fractional_singular_particular_does_not_prove_integer_infeasibility(self):
        result = analyse_integer_system([[2, 1], [4, 2]], [5, 10])
        self.assertEqual(result["rational_candidate"]["solution"], ["5/2", "0"])
        self.assertTrue(result["integer_feasible"])
        self.assertTrue(result["nonnegative_integer_feasible"])
        x, y = result["nonnegative_integer_witness"]
        self.assertEqual(2 * x + y, 5)
        self.assertEqual(4 * x + 2 * y, 10)
        self.assertGreaterEqual(min(x, y), 0)
        self.assertTrue(verify_integer_witness([[2, 1], [4, 2]], [5, 10], [2, 1], nonnegative=True))

    def test_conflicting_totals_have_a_direct_row_combination_obstruction(self):
        result = analyse_integer_system([[2, 1], [4, 2]], [5, 11])
        self.assertEqual(result["rational_status"], "inconsistent")
        self.assertFalse(result["integer_feasible"])
        w0, w1 = [Fraction(x) for x in result["integer_certificate"]["row_weights"]]
        self.assertEqual(2 * w0 + 4 * w1, 0)
        self.assertEqual(w0 + 2 * w1, 0)
        self.assertNotEqual(5 * w0 + 11 * w1, 0)

    def test_gcd_obstruction_proves_no_integer_solution_without_search(self):
        result = analyse_integer_system([[2, 4], [4, 8]], [1, 2])
        self.assertEqual(result["rational_status"], "underdetermined")
        self.assertFalse(result["integer_feasible"])
        certificate = result["integer_certificate"]
        self.assertEqual(certificate["kind"], "row_gcd_obstruction")
        self.assertEqual(certificate["divisor"], 2)
        self.assertEqual(certificate["coefficient_remainders"], [0, 0])
        self.assertEqual(certificate["rhs_remainder"], 1)

    def test_zero_rows_zero_matrix_and_negative_totals(self):
        for matrix, rhs, integer, nonnegative in [
            ([[0, 0], [0, 0]], [0, 0], True, True),
            ([[0, 0], [0, 0]], [0, 1], False, False),
            ([[0, 0], [0, 2]], [0, 6], True, True),
            ([[0, 0], [0, 2]], [1, 6], False, False),
            ([[0, 2], [0, 0]], [-6, 0], True, False),
            ([[2, 1], [4, 2]], [-5, -10], True, False),
            ([[-2, 1], [-4, 2]], [5, 10], True, True),
        ]:
            with self.subTest(matrix=matrix, rhs=rhs):
                result = analyse_integer_system(matrix, rhs)
                self.assertIs(result["integer_feasible"], integer)
                self.assertIs(result["nonnegative_integer_feasible"], nonnegative)

    def test_small_rank_one_nonnegative_classifications_match_independent_enumeration(self):
        # This comparison concerns precisely this small finite box, not a proof
        # that the implementation is correct on every permitted integer input.
        for a, b, total in product(range(-3, 4), range(-3, 4), range(-5, 6)):
            if (a, b) == (0, 0):
                continue
            result = analyse_integer_system([[a, b], [-2 * a, -2 * b]], [total, -2 * total])
            found = next(([x, y] for x in range(21) for y in range(21)
                          if a * x + b * y == total), None)
            self.assertEqual(result["nonnegative_integer_feasible"], found is not None, (a, b, total))
            if result["integer_feasible"]:
                x, y = result["integer_witness"]
                self.assertEqual(a * x + b * y, total)
            if result["nonnegative_integer_feasible"]:
                x, y = result["nonnegative_integer_witness"]
                self.assertEqual(a * x + b * y, total)
                self.assertGreaterEqual(min(x, y), 0)

    def test_input_contract_rejects_lossy_boolean_malformed_and_excessive_values(self):
        for value in [True, 2.0, "2", Fraction(2), None, float("nan"), 10**1000]:
            with self.subTest(value=repr(value)[:40]), self.assertRaises(ValueError):
                analyse_integer_system([[value, 0], [0, 1]], [1, 1])
        for matrix, rhs in [([], [1, 2]), ([[1], [0, 1]], [1, 2]), ([[1, 0], [0, 1]], [1]),
                            (((1, 0), (0, 1)), [1, 2]), ([[1, 0], [0, 1]], [True, 2])]:
            with self.subTest(matrix=matrix, rhs=rhs), self.assertRaises(ValueError):
                analyse_integer_system(matrix, rhs)

    def test_solver_output_is_independently_verified_before_use(self):
        lie = {"status": "unique", "solution": ["99", "99"], "certificate": {"determinant": "13"}}
        with patch("atlas_math.engine.solve", return_value=lie), self.assertRaisesRegex(ValueError, "independent rational verifier"):
            analyse_integer_system([[3, 2], [1, 5]], [8, 7])

    def test_witness_verifier_never_calls_the_solver_or_constructor(self):
        with patch("atlas_math.engine.solve", side_effect=AssertionError("solver invoked")), patch("atlas_math.applications.construct_primitive_witness", side_effect=AssertionError("constructor invoked")):
            self.assertTrue(verify_integer_witness([[3, 2], [1, 5]], [8, 7], [2, 1], nonnegative=True))
            self.assertFalse(verify_integer_witness([[3, 2], [1, 5]], [8, 7], [2, 2]))
            self.assertFalse(verify_integer_witness([[3, 2], [1, 5]], [1, 9], [-1, 2], nonnegative=True))
            self.assertFalse(verify_integer_witness([[1, 0], [0, 1]], [1, 2], [True, 2]))

    def test_inputs_are_not_mutated(self):
        matrix, rhs = [[2, 1], [4, 2]], [5, 10]
        before = copy.deepcopy((matrix, rhs))
        analyse_integer_system(matrix, rhs)
        self.assertEqual((matrix, rhs), before)


class ConstructiveTests(unittest.TestCase):
    def test_supplied_bezout_construction_is_checked_without_the_solver(self):
        with patch("atlas_math.engine.solve", side_effect=AssertionError("solver invoked")):
            result = construct_primitive_witness([[2, 3], [3, 7]], [7, 13])
        self.assertEqual(result["bezout"], {"u": -1, "v": 1, "identity": 1})
        self.assertEqual(result["determinant"], 5)
        self.assertEqual(result["solution"], [2, 1])
        x, y = result["solution"]
        self.assertEqual(2 * x + 3 * y, 7)
        self.assertEqual(3 * x + 7 * y, 13)
        self.assertEqual(result["formal_status"], "Q0004-universal-formalisation-pending")

    def test_negative_determinants_zero_entries_and_signed_bezout_coefficients(self):
        from math import gcd
        count = 0
        for a, b, c, d in product(range(-2, 3), repeat=4):
            if a * d == b * c or gcd(a, c) != 1:
                continue
            p, q = 2 * a - b, 2 * c - d
            result = construct_primitive_witness([[a, b], [c, d]], [p, q])
            self.assertEqual(result["solution"], [2, -1])
            self.assertEqual(result["bezout"]["u"] * a + result["bezout"]["v"] * c, 1)
            count += 1
        self.assertGreater(count, 100)

    def test_nonprimitive_counterexample_does_not_misclassify_callers_rhs(self):
        matrix, rhs = [[2, 1], [4, 3]], [8, 20]
        result = construct_primitive_witness(matrix, rhs)
        self.assertFalse(result["applicable"])
        counter = result["counterexample"]
        self.assertEqual(counter["b"], [1, 2])
        self.assertEqual(counter["y_numerator"], 0)
        self.assertTrue(counter["one_divisibility_test_passes"])
        self.assertEqual(counter["rational_candidate"]["solution"], ["1/2", "0"])
        self.assertTrue(analyse_integer_system(matrix, rhs)["integer_feasible"])

    def test_primitive_column_still_requires_divisibility(self):
        result = construct_primitive_witness([[2, 3], [3, 7]], [1, 0])
        self.assertTrue(result["applicable"])
        self.assertEqual(result["status"], "integer_obstruction")
        self.assertFalse(result["integer_feasible"])
        self.assertEqual(result["rational_candidate"]["solution"], ["7/5", "-3/5"])

    def test_singular_matrix_is_outside_q0004_construction(self):
        for matrix in [[[2, 1], [4, 2]], [[0, 0], [0, 0]]]:
            with self.subTest(matrix=matrix), self.assertRaisesRegex(ValueError, "nonzero determinant"):
                construct_primitive_witness(matrix, [0, 0])


class PairedDesignTests(unittest.TestCase):
    def test_exact_requested_tails_and_threshold(self):
        nine = paired_randomisation_tail(9, 3)
        ten = paired_randomisation_tail(10, 2)
        self.assertEqual(nine["one_sided_p"], "299/4096")
        self.assertEqual(ten["one_sided_p"], "79/4096")
        self.assertFalse(nine["crosses_predeclared_threshold"])
        self.assertTrue(ten["crosses_predeclared_threshold"])
        self.assertEqual(nine["assignments_enumerated"], 4096)
        self.assertEqual(nine["observed_agent_sessions"], 0)

    def test_ties_do_not_supply_fair_discordance_bits(self):
        tied = paired_randomisation_tail(0, 0, 12)
        mixed = paired_randomisation_tail(3, 0, 9)
        self.assertEqual(tied["one_sided_p"], "1")
        self.assertEqual(tied["discordant_pairs"], 0)
        self.assertEqual(mixed["one_sided_p"], "1/8")
        self.assertEqual(mixed["pairs"], 12)
        self.assertEqual(mixed["assignments_enumerated"], 8)

    def test_independent_assignment_count_detects_a_broken_formula_path(self):
        with patch("atlas_math.applications.comb", return_value=0), self.assertRaisesRegex(ValueError, "disagrees"):
            paired_randomisation_tail(9, 3)

    def test_tail_boundaries_and_monotonicity(self):
        previous = Fraction(1)
        for wins in range(9):
            result = paired_randomisation_tail(wins, 8 - wins)
            current = Fraction(result["one_sided_p"])
            self.assertLessEqual(current, previous)
            previous = current
        self.assertEqual(paired_randomisation_tail(20, 0)["one_sided_p"], "1/1048576")
        self.assertEqual(paired_randomisation_tail(0, 0)["one_sided_p"], "1")

    def test_invalid_counts_are_rejected_before_enumeration(self):
        for counts in [(True, 1, 0), (1.0, 1, 0), (-1, 1, 0), (1, 1, -1), (10**1000, 0, 0), (10, 10, 1), ("9", 3, 0)]:
            with self.subTest(counts=repr(counts)[:50]), self.assertRaises(ValueError):
                paired_randomisation_tail(*counts)


class ReportTests(unittest.TestCase):
    def test_report_is_deterministic_and_source_pinned_without_learning_claims(self):
        first, second = applications_report(), applications_report()
        self.assertEqual(first, second)
        self.assertEqual(first["difficulty"], "warm_up_only")
        self.assertTrue(first["synthetic"])
        for key in ["live_model", "agent_learning_measured", "novel_mathematics_claimed", "frontier_challenge_solved", "millennium_progress_claimed"]:
            self.assertFalse(first[key])
        self.assertEqual(first["observed_agent_sessions"], 0)
        for source in first["sources"]:
            self.assertIn("/blob/" + SOURCE_COMMIT + "/", source["url"])
        self.assertEqual([len(a["cases"]) for a in first["applications"]], [6, 2, 3])
        self.assertEqual(json.loads(json.dumps(first, allow_nan=False)), first)

    def test_new_or_identical_write_preserves_existing_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "report.json"
            write_applications_report(path)
            original = path.read_bytes()
            write_applications_report(path)
            self.assertEqual(path.read_bytes(), original)
            path.write_text("retained earlier evidence\n")
            with self.assertRaises(FileExistsError):
                write_applications_report(path)
            self.assertEqual(path.read_text(), "retained earlier evidence\n")

    def test_symlink_destination_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / "report.json"
            destination.write_text("original\n")
            link = Path(folder) / "link.json"
            try:
                link.symlink_to(destination)
            except OSError:
                self.skipTest("symlink creation unavailable")
            with self.assertRaises(ValueError):
                write_applications_report(link)
            self.assertEqual(destination.read_text(), "original\n")

    def test_cli_reports_same_result_and_refuses_conflicting_output(self):
        result = subprocess.run([sys.executable, "-m", "atlas_math", "applications"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), applications_report())
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "old.json"
            path.write_text("old evidence\n")
            result = subprocess.run([sys.executable, "-m", "atlas_math", "applications", "--output", str(path)], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stderr)["ok"])
            self.assertEqual(path.read_text(), "old evidence\n")


if __name__ == "__main__":
    unittest.main()
