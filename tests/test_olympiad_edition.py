"""Reproduce the retained teaching text and its bounded mathematical checks."""
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

EDITION = Path(__file__).resolve().parents[1] / 'research' / 'olympiad'


class OlympiadEditionTests(unittest.TestCase):
    def test_odd_parcel_lab(self):
        subprocess.run([sys.executable, str(EDITION / 'labs' / 'check_odd_parcel.py')], check=True, timeout=30)

    def test_frozen_zip_rebuild(self):
        released = EDITION / 'releases' / 'Maths_Olympiad_Proof_Edition_v1.0.0.zip'
        digest = '43da7a8520b7f4d9202b81d5e9c5cbc67de8f5b0d5d15dab919c2e4b69ef2c27'
        self.assertEqual(sha256(released.read_bytes()).hexdigest(), digest)
        with TemporaryDirectory() as tmp:
            rebuilt = Path(tmp) / 'edition.zip'
            subprocess.run([sys.executable, 'build.py', '--zip', str(rebuilt)], cwd=EDITION, check=True, timeout=30)
            self.assertEqual(rebuilt.read_bytes(), released.read_bytes())

    def test_proof_text_and_checks(self):
        commands = [('node', 'compile-edition.mjs'), (sys.executable, 'build.py')]
        for checker in sorted((EDITION / 'source' / 'checks').iterdir()):
            if checker.suffix in {'.mjs', '.py'}:
                commands.append(('node' if checker.suffix == '.mjs' else sys.executable, str(checker)))
        for command in commands:
            with self.subTest(command=command):
                subprocess.run(command, cwd=EDITION, check=True, timeout=120)


if __name__ == '__main__':
    unittest.main()
