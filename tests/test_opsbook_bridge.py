"""Real pinned-Opsbook integration checks, not mocked acceptance labels."""

import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("opsbook_bridge", ROOT / "scripts" / "opsbook_bridge.py")
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)


class OpsbookBridgeTests(unittest.TestCase):
    def test_real_teaching_reload_execution_and_rollback(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            report = bridge.run_bridge(output)
            self.assertTrue(report["overbroad"]["promotion_refused"])
            self.assertFalse(report["overbroad"]["report"]["eligible"])
            self.assertEqual(report["learned"]["guard"], {"task": "submit-certificate"})
            self.assertTrue(report["learned"]["report"]["eligible"])
            self.assertEqual(report["fresh_process"], {"revision": 1, "selected_checks": ["exact-substitution"]})
            bad = report["execution"]["incorrect_candidate"]
            good = report["execution"]["correct_candidate"]
            self.assertFalse(bad["pass"])
            self.assertEqual(bad["checks"], [{"check": "exact-substitution", "exit": 1}])
            self.assertTrue(good["pass"])
            self.assertEqual(good["checks"], [{"check": "exact-substitution", "exit": 0}])
            self.assertFalse(report["empty_check_selection_counts_as_success"])
            self.assertEqual(report["rollback"]["copy_instructions"], [])
            self.assertEqual(bridge._state(output / "manual.db")["versions"][-1]["number"], 1)
            self.assertFalse(report["live_model"])
            self.assertEqual(json.loads((output / "report.json").read_text()), report)

    def test_identical_replay_preserves_every_artifact_including_database(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            first = bridge.run_bridge(output)
            before = {path.name: path.read_bytes() for path in output.iterdir()}
            self.assertEqual(bridge.run_bridge(output), first)
            self.assertEqual({path.name: path.read_bytes() for path in output.iterdir()}, before)

    def test_tampered_manual_or_report_is_not_silently_replaced(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "run"
            bridge.run_bridge(output)
            report_path = output / "report.json"
            report_path.write_text("tampered\n")
            with self.assertRaises(FileExistsError):
                bridge.run_bridge(output)
            self.assertEqual(report_path.read_text(), "tampered\n")
            (output / "manual.db").write_bytes(b"not a database")
            with self.assertRaises(sqlite3.DatabaseError):
                bridge.run_bridge(output)
            self.assertEqual((output / "manual.db").read_bytes(), b"not a database")


if __name__ == "__main__":
    unittest.main()
