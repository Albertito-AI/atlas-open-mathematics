"""Exhaustive Q0005 audit of unchanged applications; MIT, AI-assisted."""
from collections import Counter
import hashlib
from itertools import product
import json
from math import gcd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from atlas_math.applications import analyse_integer_system


def run():
    counts = Counter()
    digest = hashlib.sha256()
    for a, b, c, d in product(range(-3, 4), repeat=4):
        if a*d != b*c:
            continue
        counts['matrices'] += 1
        A = [[a, b], [c, d]]
        # Independent finite oracle: enumerate points, never call the solver.
        images = {}
        for x, y in product(range(-12, 13), repeat=2):
            rhs = (a*x+b*y, c*x+d*y)
            images.setdefault(rhs, []).append((x, y))
        for p, q in product(range(-3, 4), repeat=2):
            counts['systems'] += 1
            r = analyse_integer_system(A, [p, q])
            points = images.get((p, q), [])
            assert r['integer_feasible'] == bool(points)
            assert r['nonnegative_integer_feasible'] == any(x >= 0 and y >= 0 for x, y in points)
            counts['rational_' + r['rational_status']] += 1
            counts['integer_feasible'] += r['integer_feasible']
            counts['nonnegative_feasible'] += r['nonnegative_integer_feasible']
            cert = r['integer_certificate']
            counts[cert['kind']] += 1
            if cert['kind'] == 'rank_one_integer_family':
                z, v = cert['particular'], cert['direction']
                assert gcd(*v) == 1
                assert all(row[0]*v[0]+row[1]*v[1] == 0 for row in A)
                assert all(row[0]*z[0]+row[1]*z[1] == rhs for row, rhs in zip(A, [p, q]))
                j = 0 if v[0] else 1
                for point in points:
                    delta = point[j]-z[j]
                    assert delta % v[j] == 0
                    k = delta // v[j]
                    assert point == tuple(z[i]+k*v[i] for i in range(2))
                    counts['enumerated_points_in_family'] += 1
            elif cert['kind'] == 'row_gcd_obstruction':
                row = A[cert['row_index']]
                g = gcd(*row)
                assert g > 0 and g == cert['divisor']
                assert [p, q][cert['row_index']] % g != 0
            digest.update((json.dumps(r, sort_keys=True, separators=(',', ':'))+'\n').encode())
    return {'question': 'Q0005', 'bounds': {'coefficients_rhs': [-3, 3], 'oracle_coordinates': [-12, 12]},
            'counts': dict(sorted(counts.items())), 'ordered_results_sha256': digest.hexdigest(),
            'source_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
                ['research/agent-attempts/0005/audit.py', 'atlas_math/applications.py', 'atlas_math/engine.py']},
            'scope': 'Finite audit; mathematical completeness argument is separate; no novelty or learner outcomes'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
