"""Reproduce the retained teaching text and its bounded mathematical checks."""
from pathlib import Path
import subprocess
import sys
import unittest

EDITION = Path(__file__).resolve().parents[1] / 'research' / 'olympiad'


class OlympiadEditionTests(unittest.TestCase):
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
