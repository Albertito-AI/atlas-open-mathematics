"""Exercise complete cycle publication and replay in disposable repository copies."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CycleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="atlas-cycle-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for directory in ("atlas_math", "scripts", "vendor"):
            shutil.copytree(ROOT / directory, self.root / directory,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    def run_script(self, name, *arguments):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / name), *arguments],
            cwd=self.root, capture_output=True, text=True, timeout=20, check=False,
        )

    def make_cycle(self):
        result = self.run_script("research_cycle.py", "--date", "2026-11-09")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        cycles = [p for p in (self.root / "research/cycles").iterdir() if not p.name.startswith(".")]
        self.assertEqual(len(cycles), 1)
        self.assertTrue((cycles[0] / "manifest.json").is_file())
        return cycles[0]

    def assertInvalid(self):
        result = self.run_script("validate_repository.py")
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_same_date_and_source_replay_preserve_every_byte(self):
        cycle = self.make_cycle()
        before = {str(p.relative_to(cycle)): p.read_bytes() for p in cycle.rglob("*") if p.is_file()}
        manifest = json.loads(before["manifest.json"])
        self.assertIs(manifest["live_model"], False)
        self.assertIs(manifest["new_mathematical_discovery"], False)
        self.assertEqual(set(manifest["files"]), set(before) - {"manifest.json"})
        for name, digest in manifest["files"].items():
            self.assertEqual(hashlib.sha256(before[name]).hexdigest(), digest)
        result = self.run_script("research_cycle.py", "--date", "2026-11-09")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        after = {str(p.relative_to(cycle)): p.read_bytes() for p in cycle.rglob("*") if p.is_file()}
        self.assertEqual(after, before)

    def test_valid_markdown_byte_change_is_detected_by_manifest(self):
        cycle = self.make_cycle()
        manual = cycle / "opsbook/MANUAL.md"
        changed = manual.read_bytes() + b"\n"
        manual.write_bytes(changed)
        self.assertInvalid()
        replay = self.run_script("research_cycle.py", "--date", "2026-11-09")
        self.assertNotEqual(replay.returncode, 0)
        self.assertEqual(manual.read_bytes(), changed)

    def test_missing_manifest_is_not_a_completed_cycle(self):
        cycle = self.make_cycle()
        (cycle / "manifest.json").unlink()
        self.assertInvalid()
        replay = self.run_script("research_cycle.py", "--date", "2026-11-09")
        self.assertNotEqual(replay.returncode, 0)
        self.assertFalse((cycle / "manifest.json").exists())

    def test_empty_existing_target_is_not_treated_as_success_or_overwritten(self):
        cycle = self.make_cycle()
        for child in cycle.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
        replay = self.run_script("research_cycle.py", "--date", "2026-11-09")
        self.assertNotEqual(replay.returncode, 0, replay.stdout)
        self.assertEqual(list(cycle.iterdir()), [])

    def test_unlisted_evidence_file_is_rejected(self):
        cycle = self.make_cycle()
        (cycle / "unrecorded-claim.txt").write_text("Unmanifested evidence must not be accepted.\n")
        self.assertInvalid()

    def test_empty_manifest_cannot_make_missing_evidence_acceptable(self):
        cycle = self.make_cycle()
        manifest_path = cycle / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"] = {}
        manifest_path.write_text(json.dumps(manifest))
        self.assertInvalid()

    def test_manifest_cannot_refer_outside_its_cycle(self):
        cycle = self.make_cycle()
        outside = cycle.parent / "outside.txt"
        outside.write_text("outside cycle\n")
        manifest_path = cycle / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"]["../outside.txt"] = hashlib.sha256(outside.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        self.assertInvalid()

    def test_failed_bridge_leaves_no_complete_or_temporary_cycle(self):
        bridge = self.root / "scripts/opsbook_bridge.py"
        bridge.write_text("import sys\nsys.exit(7)\n")
        result = self.run_script("research_cycle.py", "--date", "2026-11-09")
        self.assertNotEqual(result.returncode, 0)
        parent = self.root / "research/cycles"
        self.assertEqual(list(parent.iterdir()) if parent.exists() else [], [])

    def test_modified_vendored_source_fails_provenance_check(self):
        source = self.root / "vendor/atlas-opsbook/opsbook.py"
        source.write_bytes(source.read_bytes() + b"\n# Changed copy\n")
        self.assertInvalid()


if __name__ == "__main__":
    unittest.main()
