#!/usr/bin/env python3
"""Validate public evidence and vendored provenance without network access."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from atlas_math.engine import verify


def main():
    errors = []
    checked = 0
    for path in ROOT.rglob('*.json'):
        if any(x in path.parts for x in ('.git', 'runs', '__pycache__')):
            continue
        try:
            json.loads(path.read_text())
        except (ValueError, OSError) as exc:
            errors.append(f'{path.relative_to(ROOT)}: {exc}')
        checked += 1
    lock = json.loads((ROOT / 'vendor/atlas-opsbook/PROVENANCE.json').read_text())
    for name, expected in lock['sha256'].items():
        actual = hashlib.sha256((ROOT / 'vendor/atlas-opsbook' / name).read_bytes()).hexdigest()
        if actual != expected:
            errors.append(f'Vendored Opsbook changed: {name}')
    for path in (ROOT / 'research').rglob('attempt-*.json'):
        record = json.loads(path.read_text())
        payload = {k: v for k, v in record.items() if k != 'id'}
        serial = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)
        expected_id = 'attempt-' + hashlib.sha256(serial.encode()).hexdigest()
        if record.get('id') != expected_id or path.stem != expected_id:
            errors.append(f'Attempt identity mismatch: {path.relative_to(ROOT)}')
        verdict = verify(record['case'], record['candidate'])
        if verdict != record['verification']:
            errors.append(f'Attempt verdict mismatch: {path.relative_to(ROOT)}')
    for path in (ROOT / 'research/agent-attempts').glob('*/verification.json'):
        case = json.loads((path.parent / 'problem.json').read_text())
        candidate = json.loads((path.parent / 'candidate.json').read_text())
        if json.loads(path.read_text()) != verify(case, candidate):
            errors.append(f'Agent verification mismatch: {path.relative_to(ROOT)}')
    for cycle in (ROOT / 'research/cycles').glob('*'):
        if not cycle.is_dir() or cycle.name.startswith('.'):
            continue
        manifest = cycle / 'manifest.json'
        if not manifest.is_file():
            errors.append(f'Incomplete cycle has no manifest: {cycle.relative_to(ROOT)}')
            continue
        data = json.loads(manifest.read_text())
        files = data.get('files')
        if not isinstance(files, dict) or not files:
            errors.append(f'Cycle manifest has no evidence: {cycle.relative_to(ROOT)}')
            continue
        actual_files = {str(p.relative_to(cycle)) for p in cycle.rglob('*')
                        if p.is_file() and p != manifest}
        required = {'mathematics/report.json', 'mathematics/lesson.md',
                    'mathematics/attempts.jsonl', 'opsbook/report.json',
                    'opsbook/MANUAL.md', 'opsbook/fixtures.json'}
        if set(files) != actual_files or not required <= set(files):
            errors.append(f'Cycle manifest does not cover the complete evidence: {cycle.relative_to(ROOT)}')
        for name, digest in files.items():
            target = (manifest.parent / name).resolve()
            if not target.is_relative_to(manifest.parent.resolve()) or not target.is_file():
                errors.append(f'Invalid cycle manifest path: {name}')
            elif not isinstance(digest, str) or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                errors.append(f'Cycle evidence changed: {target.relative_to(ROOT)}')
    for path in ROOT.rglob('*.md'):
        if any(x in path.parts for x in ('.git', 'runs')):
            continue
        for target in re.findall(r'\]\(([^\s)]+)\)', path.read_text()):
            if target.startswith(('http:', 'https:', 'mailto:', '#')) or '{' in target:
                continue
            target = target.split('#')[0]
            if target and not (path.parent / target).exists():
                errors.append(f'Broken local link: {path.relative_to(ROOT)} -> {target}')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Validated {checked} JSON files, vendored provenance, recorded certificates, manifests and local documentation links.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
