"""Replay the arcade's published calculations and independent game checkers."""
from pathlib import Path
import shutil
import subprocess
import unittest

from tools.verify_arcade_whitepapers import verify_boardroom, verify_sudoku


class ArcadeWhitePaperTests(unittest.TestCase):
    def test_sudoku_positions_and_counterexamples(self):
        verify_sudoku()

    def test_boardroom_thresholds_and_transfer_case(self):
        verify_boardroom()

    @unittest.skipUnless(shutil.which("node"), "Node.js is required for the browser game models")
    def test_published_javascript_models(self):
        repo = Path(__file__).resolve().parents[1]
        tests = sorted((repo / "research" / "arcade").glob("*.test.mjs"))
        self.assertTrue(tests, "No arcade model tests found")
        result = subprocess.run(["node", "--test", *tests], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
