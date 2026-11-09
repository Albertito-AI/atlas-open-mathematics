#!/usr/bin/env python3
"""Record one bounded, deterministic practice cycle. No model calls or new claims."""
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from atlas_math.engine import run_demo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=datetime.now(ZoneInfo('Asia/Singapore')).date().isoformat())
    args = parser.parse_args()
    day = datetime.strptime(args.date, '%Y-%m-%d').date().isoformat()
    source_files = sorted(list((ROOT / 'atlas_math').glob('*.py')) +
                          list((ROOT / 'scripts').glob('*.py')) +
                          [ROOT / 'vendor/atlas-opsbook/opsbook.py'])
    h = hashlib.sha256()
    for path in source_files:
        h.update(str(path.relative_to(ROOT)).encode() + b'\0' + path.read_bytes())
    fingerprint = h.hexdigest()
    target = ROOT / 'research/cycles' / f'{day}-{fingerprint[:12]}'
    if target.exists():
        if not (target / 'manifest.json').is_file():
            raise ValueError('An incomplete cycle exists; preserve it and investigate before resuming.')
        subprocess.run([sys.executable, str(ROOT / 'scripts/validate_repository.py')], check=True)
        print(f'Existing immutable cycle: {target.relative_to(ROOT)}')
        return 0
    target.parent.mkdir(parents=True, exist_ok=True)
    # A failed cycle leaves no apparently complete target directory.
    with tempfile.TemporaryDirectory(dir=target.parent, prefix='.cycle-') as tmp:
        temp = Path(tmp)
        report = run_demo(temp / 'mathematics', int(day.replace('-', '')))
        subprocess.run([sys.executable, str(ROOT / 'scripts/opsbook_bridge.py'),
                        '--output', str(temp / 'opsbook')], check=True, cwd=ROOT)
        for db in (temp / 'opsbook').glob('*.db*'):
            db.unlink()
        files = {str(p.relative_to(temp)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted(temp.rglob('*')) if p.is_file()}
        manifest = {'schema_version': 1, 'date_singapore': day,
                    'source_fingerprint_sha256': fingerprint,
                    'activity': 'generated public practice; known mathematics',
                    'live_model': False, 'new_mathematical_discovery': False,
                    'files': files}
        (temp / 'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
        temp.rename(target)
    print(f'Recorded immutable cycle: {target.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
