"""Independent checks of exact certificates, input boundaries and durable records."""

import copy
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from atlas_math.engine import generate_case, run_demo, solve, verify


def case(A, b, kind="unique", identifier="independent-test"):
    return {"id": identifier, "A": A, "b": b, "kind": kind}


def unique(x, determinant):
    return {"status": "unique", "solution": x,
            "certificate": {"determinant": determinant}}


def underdetermined(x, null_vector):
    return {"status": "underdetermined", "solution": x,
            "certificate": {"null_vector": null_vector}}


def inconsistent(weights):
    return {"status": "inconsistent", "certificate": {"row_weights": weights}}


class CertificateTests(unittest.TestCase):
    def assertAccepted(self, problem, candidate):
        result = verify(problem, candidate)
        self.assertIs(result["accepted"], True, result)
        self.assertIsInstance(result["reason"], str)

    def assertRejected(self, problem, candidate):
        result = verify(problem, candidate)
        self.assertIs(result["accepted"], False, result)
        self.assertTrue(result["reason"])

    def test_hand_supplied_unique_certificate_with_fractional_answer(self):
        problem = case([[2, 1], [1, -1]], [1, 0])
        self.assertAccepted(problem, unique(["1/3", "1/3"], -3))
        self.assertRejected(problem, unique(["1/3", "2/3"], -3))
        self.assertRejected(problem, unique(["1/3", "1/3"], 3))

    def test_zero_initial_pivot_is_solved_without_division_by_zero(self):
        problem = case([[0, 2], [3, 4]], [6, 15])
        self.assertAccepted(problem, unique([1, 3], -6))
        result = solve(problem)
        self.assertEqual([Fraction(x) for x in result["solution"]], [1, 3])
        self.assertAccepted(problem, result)

    def test_rational_coefficients_are_not_rounded(self):
        problem = case([["1/2", "1/3"], ["1/4", "-1/6"]], ["5/6", "1/12"])
        self.assertAccepted(problem, unique([1, 1], "-1/6"))
        self.assertAccepted(problem, solve(problem))

    def test_singular_consistent_needs_particular_solution_and_nonzero_null_vector(self):
        problem = case([[1, 2], [2, 4]], [3, 6], "underdetermined")
        self.assertAccepted(problem, underdetermined([3, 0], [-2, 1]))
        self.assertAccepted(problem, underdetermined([1, 1], [-4, 2]))
        self.assertRejected(problem, underdetermined([3, 0], [0, 0]))
        self.assertRejected(problem, underdetermined([0, 0], [-2, 1]))
        self.assertRejected(problem, underdetermined([3, 0], [2, 1]))
        self.assertRejected(problem, unique([3, 0], 0))

    def test_inconsistent_certificate_is_a_contradictory_linear_combination(self):
        problem = case([[1, 2], [2, 4]], [3, 7], "inconsistent")
        self.assertAccepted(problem, inconsistent([-2, 1]))
        self.assertAccepted(problem, inconsistent([4, -2]))
        self.assertRejected(problem, inconsistent([0, 0]))
        self.assertRejected(problem, inconsistent([1, 0]))
        self.assertRejected(problem, underdetermined([3, 0], [-2, 1]))

    def test_zero_matrix_distinguishes_consistency(self):
        consistent = case([[0, 0], [0, 0]], [0, 0], "underdetermined")
        contradiction = case([[0, 0], [0, 0]], [0, 2], "inconsistent")
        self.assertAccepted(consistent, underdetermined([17, -29], [1, 0]))
        self.assertRejected(consistent, inconsistent([1, 1]))
        self.assertAccepted(contradiction, inconsistent([0, 1]))
        for problem, status in [(consistent, "underdetermined"), (contradiction, "inconsistent")]:
            with self.subTest(status=status):
                candidate = solve(problem)
                self.assertEqual(candidate["status"], status)
                self.assertAccepted(problem, candidate)

    def test_single_nonzero_row_and_second_column_dependencies(self):
        problems = [
            case([[0, 0], [0, 2]], [0, 6], "underdetermined"),
            case([[0, 2], [0, 0]], [6, 0], "underdetermined"),
            case([[0, 2], [0, 4]], [6, 13], "inconsistent"),
            case([[0, 0], [1, 1]], [1, 0], "inconsistent"),
        ]
        for problem in problems:
            with self.subTest(problem=problem):
                candidate = solve(problem)
                self.assertEqual(candidate["status"], problem["kind"])
                self.assertAccepted(problem, candidate)

    def test_kind_is_metadata_and_does_not_establish_the_answer(self):
        problem = case([[1, 2], [2, 4]], [3, 7], "unique")
        self.assertRejected(problem, unique([3, 0], 1))
        self.assertAccepted(problem, inconsistent([-2, 1]))
        self.assertEqual(solve(problem)["status"], "inconsistent")

    def test_verify_does_not_call_the_solver(self):
        from unittest.mock import patch
        problem = case([[2, 1], [1, -1]], [1, 0])
        with patch("atlas_math.engine.solve", side_effect=AssertionError("solver invoked")):
            self.assertAccepted(problem, unique(["1/3", "1/3"], -3))
            self.assertRejected(problem, unique([1, 1], -3))

    def test_solver_outputs_independently_satisfy_certificates(self):
        statuses = set()
        for seed in range(90):
            problem = generate_case(seed)
            A = [[Fraction(x) for x in row] for row in problem["A"]]
            b = [Fraction(x) for x in problem["b"]]
            candidate = solve(problem)
            statuses.add(candidate["status"])
            cert = candidate["certificate"]
            if candidate["status"] == "inconsistent":
                w = [Fraction(x) for x in cert["row_weights"]]
                self.assertTrue(all(sum(w[i] * A[i][j] for i in range(2)) == 0 for j in range(2)))
                self.assertNotEqual(sum(w[i] * b[i] for i in range(2)), 0)
            else:
                x = [Fraction(v) for v in candidate["solution"]]
                self.assertEqual([sum(a * v for a, v in zip(row, x)) for row in A], b)
                if candidate["status"] == "underdetermined":
                    v = [Fraction(x) for x in cert["null_vector"]]
                    self.assertTrue(any(v))
                    self.assertEqual([sum(a * q for a, q in zip(row, v)) for row in A], [0, 0])
            self.assertAccepted(problem, candidate)
        self.assertEqual(statuses, {"unique", "inconsistent", "underdetermined"})

    def test_inputs_are_not_mutated(self):
        problem = case([[2, 1], [1, -1]], [1, 0])
        original = copy.deepcopy(problem)
        candidate = solve(problem)
        saved_candidate = copy.deepcopy(candidate)
        verify(problem, candidate)
        self.assertEqual(problem, original)
        self.assertEqual(candidate, saved_candidate)


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.problem = case([[1, 0], [0, 1]], [1, 2])
        self.candidate = unique([1, 2], 1)

    def assertMalformedCase(self, bad):
        with self.assertRaises(ValueError):
            solve(bad)
        self.assertIs(verify(bad, self.candidate)["accepted"], False)

    def test_invalid_scalar_types_and_unbounded_values_are_rejected(self):
        for value in [True, False, 1.0, float("nan"), float("inf"), None, [], {},
                      10**1000, "9" * 1000, "1/0", "0.5", "1e3", " 1", "1 "]:
            with self.subTest(value=repr(value)[:40]):
                bad = copy.deepcopy(self.problem)
                bad["A"][0][0] = value
                self.assertMalformedCase(bad)

    def test_invalid_case_structure_and_unknown_fields_are_rejected(self):
        bad_cases = [None, [], {}, {**self.problem, "extra": 1},
                     {**self.problem, "A": [[1, 0]]},
                     {**self.problem, "A": [[1], [0, 1]]},
                     {**self.problem, "A": [[1, 0, 0], [0, 1, 0]]},
                     {**self.problem, "b": [1]}, {**self.problem, "b": [1, 2, 3]},
                     {**self.problem, "id": ""}, {**self.problem, "id": "../escape"},
                     {**self.problem, "id": "x" * 97}, {**self.problem, "kind": "solved"}]
        for bad in bad_cases:
            with self.subTest(bad=bad):
                self.assertMalformedCase(bad)

    def test_invalid_candidates_are_rejected_without_exceptions(self):
        bad_candidates = [None, [], {}, {**self.candidate, "extra": 1},
                          {**self.candidate, "status": "proved"},
                          {**self.candidate, "solution": [1]},
                          {**self.candidate, "solution": [1, 2, 3]},
                          {**self.candidate, "certificate": {}},
                          {**self.candidate, "certificate": {"determinant": 1, "trust_me": True}}]
        for value in [True, 1.0, 10**1000, "9" * 1000, "1/0"]:
            bad_candidates.append(unique([value, 2], 1))
            bad_candidates.append(unique([1, 2], value))
        for bad in bad_candidates:
            with self.subTest(bad=repr(bad)[:100]):
                self.assertIs(verify(self.problem, bad)["accepted"], False)

    def test_case_bounds_apply_to_numerator_and_denominator(self):
        for value in [10**9 + 1, f"1/{10**9 + 1}"]:
            bad = copy.deepcopy(self.problem)
            bad["b"][0] = value
            self.assertMalformedCase(bad)

    def test_noncanonical_rational_strings_are_rejected(self):
        for value in ["01", "+1", "-0", "2/4", "1/1", "0/2", "1/-2"]:
            with self.subTest(value=value):
                bad = copy.deepcopy(self.problem)
                bad["b"][0] = value
                self.assertMalformedCase(bad)

    def test_generator_rejects_boolean_and_noninteger_seed(self):
        for seed in [True, 1.0, "1", None]:
            with self.subTest(seed=seed), self.assertRaises(ValueError):
                generate_case(seed)


class RecordTests(unittest.TestCase):
    def test_generator_is_deterministic_and_json_serialisable(self):
        for seed in [0, 1, 2, 17, 123456]:
            first = generate_case(seed)
            self.assertEqual(first, generate_case(seed))
            self.assertEqual(first, json.loads(json.dumps(first)))

    def test_demo_is_byte_reproducible_and_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            run_demo(output, seed=17)
            before = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
            self.assertTrue(before)
            self.assertTrue(any(str(p).startswith("records/attempt-") for p in before))
            run_demo(output, seed=17)
            after = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_existing_attempt_record_is_never_silently_rewritten(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            run_demo(output, seed=17)
            record = next((output / "records").glob("attempt-*.json"))
            corrupt = record.read_bytes() + b"\ncorruption-marker\n"
            record.write_bytes(corrupt)
            with self.assertRaises((ValueError, FileExistsError, RuntimeError)):
                run_demo(output, seed=17)
            self.assertEqual(record.read_bytes(), corrupt)


class CommandLineTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "-m", "atlas_math", *map(str, arguments)],
            cwd=Path(__file__).resolve().parents[1], capture_output=True,
            text=True, timeout=10, check=False,
        )

    def write_inputs(self, folder, candidate):
        problem_path, candidate_path = Path(folder) / "case.json", Path(folder) / "candidate.json"
        problem_path.write_text(json.dumps(case([[2, 1], [1, -1]], [1, 0])), encoding="utf-8")
        candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
        return problem_path, candidate_path

    def test_external_candidate_exit_codes_distinguish_proof_rejection_and_bad_input(self):
        samples = [(unique(["1/3", "1/3"], -3), 0),
                   (unique([1, 1], -3), 1),
                   (unique([True, 1], -3), 2),
                   ({"status": "unique", "solution": [1, 1], "certificate": {}}, 2)]
        with tempfile.TemporaryDirectory() as folder:
            for candidate, expected in samples:
                with self.subTest(candidate=candidate):
                    problem_path, candidate_path = self.write_inputs(folder, candidate)
                    result = self.run_cli("verify", "--case", problem_path, "--candidate", candidate_path)
                    self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
                    verdict = json.loads(result.stdout)
                    self.assertIs(verdict["accepted"], expected == 0)

    def test_nonstandard_or_ambiguous_json_is_rejected(self):
        bad_json = [
            '{"status":"unique","status":"inconsistent","certificate":{"row_weights":[1,0]}}',
            '{"status":"unique","solution":[NaN,1],"certificate":{"determinant":-3}}',
            '{"status":"unique","solution":[Infinity,1],"certificate":{"determinant":-3}}',
            '{"status":',
        ]
        with tempfile.TemporaryDirectory() as folder:
            problem_path, candidate_path = self.write_inputs(folder, unique(["1/3", "1/3"], -3))
            for content in bad_json:
                with self.subTest(content=content):
                    candidate_path.write_text(content, encoding="utf-8")
                    result = self.run_cli("verify", "--case", problem_path, "--candidate", candidate_path)
                    self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
                    self.assertIs(json.loads(result.stderr)["ok"], False)

    def test_oversized_external_json_is_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as folder:
            problem_path, candidate_path = self.write_inputs(folder, unique(["1/3", "1/3"], -3))
            candidate_path.write_text(" " * 20_000 + "{}", encoding="utf-8")
            result = self.run_cli("verify", "--case", problem_path, "--candidate", candidate_path)
            self.assertEqual(result.returncode, 2)
            self.assertIn("exceeds", json.loads(result.stderr)["error"])

    def test_generate_refuses_to_overwrite_even_an_identical_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "case.json"
            first = self.run_cli("generate", "--seed", 17, "--output", target)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = target.read_bytes()
            self.assertEqual(json.loads(before), generate_case(17))
            second = self.run_cli("generate", "--seed", 17, "--output", target)
            self.assertEqual(second.returncode, 2)
            self.assertEqual(target.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
