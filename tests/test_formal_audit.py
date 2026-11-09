"""Test fail-closed axiom-report handling; these tests do not run Lean."""

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_formal.py"
SPEC = importlib.util.spec_from_file_location("atlas_formal_audit", MODULE_PATH)
FORMAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FORMAL)


class FormalAuditTests(unittest.TestCase):
    names = ["Atlas.first", "Atlas.second"]
    allowed = ["propext", "Classical.choice", "Quot.sound"]

    def test_standard_axioms_and_axiom_free_report_are_accepted(self):
        output = ("'Atlas.first' depends on axioms: [propext, Quot.sound]\n"
                  "'Atlas.second' does not depend on any axioms\n")
        reports = FORMAL.audit_output(output, self.names, self.allowed)
        self.assertEqual(reports, {"Atlas.first": ["propext", "Quot.sound"], "Atlas.second": []})

    def test_missing_report_is_rejected(self):
        with self.assertRaises(ValueError):
            FORMAL.audit_output("'Atlas.first' depends on axioms: []", self.names, self.allowed)

    def test_duplicate_report_is_rejected(self):
        output = ("'Atlas.first' depends on axioms: []\n" * 2
                  + "'Atlas.second' does not depend on any axioms\n")
        with self.assertRaises(ValueError):
            FORMAL.audit_output(output, self.names, self.allowed)

    def test_incomplete_custom_and_compiler_trusting_assumptions_are_rejected(self):
        for axiom in ["sorryAx", "FalseAssumption", "Lean.trustCompiler", "Lean.ofReduceBool", "test_native"]:
            output = (f"'Atlas.first' depends on axioms: [propext, {axiom}]\n"
                      "'Atlas.second' does not depend on any axioms\n")
            with self.subTest(axiom=axiom), self.assertRaises(ValueError):
                FORMAL.audit_output(output, self.names, self.allowed)

    def test_warnings_and_errors_reject_otherwise_complete_output(self):
        valid = ("'Atlas.first' depends on axioms: []\n"
                 "'Atlas.second' does not depend on any axioms\n")
        for diagnostic in ["warning: declaration uses unfinished proof", "error: unknown identifier", "WARNING: diagnostic"]:
            with self.subTest(diagnostic=diagnostic), self.assertRaises(ValueError):
                FORMAL.audit_output(valid + diagnostic, self.names, self.allowed)

    def test_similar_theorem_name_cannot_replace_expected_declaration(self):
        output = ("'Atlas.first_extra' depends on axioms: []\n"
                  "'Atlas.second' does not depend on any axioms\n")
        with self.assertRaises(ValueError):
            FORMAL.audit_output(output, self.names, self.allowed)


if __name__ == "__main__":
    unittest.main()
