"""Regression checks for evidence drift and failed research executions."""
from pathlib import Path
import tempfile
import unittest

from scripts.replay_research import replay


class ResearchReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "evidence.json").write_text('{"checked": 7}\n')

    def test_changed_evidence_cannot_pass_a_successful_script(self):
        (self.root / "script.py").write_text('print(\'{"checked": 8}\')\n')
        with self.assertRaisesRegex(ValueError, "differs"):
            replay("script.py", "evidence.json", self.root)

    def test_failed_script_cannot_pass_by_printing_expected_evidence(self):
        (self.root / "script.py").write_text(
            'import sys\nprint(\'{"checked": 7}\')\nsys.exit(1)\n'
        )
        with self.assertRaisesRegex(ValueError, "failed"):
            replay("script.py", "evidence.json", self.root)

    def test_missing_evidence_is_not_a_successful_replay(self):
        (self.root / "script.py").write_text('print(\'{"checked": 7}\')\n')
        with self.assertRaises(OSError):
            replay("script.py", "missing.json", self.root)


if __name__ == "__main__":
    unittest.main()
