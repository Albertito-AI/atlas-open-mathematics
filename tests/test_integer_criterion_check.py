"""Exercise the Q0001 checker boundary with a compiler stub, not a Lean proof."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from scripts import check_integer_criterion as checker


class IntegerCriterionCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in (checker.SOURCE, "formal/toolchain.json"):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(checker.ROOT / relative, destination)
        self.reports = "".join(
            f"'{name}' depends on axioms: [propext, Quot.sound]\n"
            for name in checker.THEOREMS
        )

    def compiler(self, output=None, version="4.24.0", exit_code=0):
        executable = self.root / "compiler-stub"
        body = (
            f"#!{sys.executable}\nimport sys\n"
            f"if '--version' in sys.argv: print('Lean (version {version}, test stub)')\n"
            f"else:\n print({json.dumps(self.reports if output is None else output)})\n"
            f" sys.exit({exit_code})\n"
        )
        executable.write_text(body)
        executable.chmod(0o700)
        return executable

    def test_complete_reports_cover_the_exact_reviewed_module(self):
        result = checker.check_module(self.compiler(), self.root)
        self.assertEqual(set(result["theorems"]), set(checker.THEOREMS))
        self.assertEqual(result["source_sha256"], checker.SOURCE_SHA256)

    def test_missing_report_rejects_a_zero_exit_status(self):
        with self.assertRaises(ValueError):
            checker.check_module(self.compiler(output=""), self.root)

    def test_wrong_compiler_version_is_rejected(self):
        with self.assertRaises(ValueError):
            checker.check_module(self.compiler(version="4.25.0"), self.root)

    def test_changed_statement_is_rejected_before_compiler_execution(self):
        source = self.root / checker.SOURCE
        source.write_text(source.read_text().replace("11 ∣ p", "1 ∣ p"))
        with self.assertRaisesRegex(ValueError, "source changed"):
            checker.check_module(self.root / "must-not-be-executed", self.root)

    def test_compiler_failure_cannot_pass_with_valid_reports(self):
        with self.assertRaisesRegex(ValueError, "Lean failed"):
            checker.check_module(self.compiler(exit_code=1), self.root)


if __name__ == "__main__":
    unittest.main()
