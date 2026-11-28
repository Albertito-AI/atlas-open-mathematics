"""Reproduce all four Atlas Math Olympiad application cases, using standard Python 3."""
from collections import deque
from fractions import Fraction as F
from itertools import combinations


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def reach_tickets(start):
    seen = {start}
    queue = deque([start])
    while queue:
        counts = queue.popleft()
        for source, stock in enumerate(counts):
            if stock < 2:
                continue
            updated = list(counts)
            updated[source] -= 2
            updated[(source + 1) % 3] += 1
            state = tuple(updated)
            if state not in seen:
                seen.add(state)
                queue.append(state)
    return seen


def check_tickets():
    targets = [(2, 1, 1), (2, 2, 0)]
    from_eight = reach_tickets((8, 0, 0))
    from_nine = reach_tickets((9, 0, 0))
    check([target in from_eight for target in targets] == [True, False], 'Eight-ticket bundles')
    check(not any(target in from_nine for target in targets), 'Nine-ticket follow-up')
    print('Club tickets: from eight red, (2 red, 1 blue, 1 gold) is reachable; '
          '(2 red, 2 blue, 0 gold) is unreachable. From nine red, neither is reachable.')


def triangle_pass(vertices, setting):
    result = []
    for i in range(3):
        x, y = vertices[(i + 1) % 3]
        u, v = vertices[(i + 2) % 3]
        result.append(((x + u) / F(2) - setting * (v - y),
                       (y + v) / F(2) + setting * (u - x)))
    return result


def check_triangle():
    start = [(0, 0), (120, 0), (0, 90)]
    vertices = start
    for setting in [F(1, 2), F(1, 6), F(-1, 3)]:
        vertices = triangle_pass(vertices, setting)
    (ax, ay), (bx, by), (cx, cy) = vertices
    check((bx - ax, by - ay) == (10, 0), 'Horizontal edge')
    check((cx - ax, cy - ay) == (0, F(15, 2)), 'Vertical edge')
    check((cx - bx) ** 2 + (cy - by) ** 2 == F(25, 2) ** 2, 'Sloping edge')
    check(tuple(map(sum, zip(*vertices))) == tuple(map(sum, zip(*start))), 'Centroid')
    print('Printed icon: exact-coordinate passes 1/2, 1/6, -1/3 give a 10 by 7.5 mm box, '
          'a 12.5 mm sloping edge and zero centroid displacement.')


def check_logger():
    def width(n):
        return n * n - 1

    for n in range(2, 101):
        old = width(n)
        check(width(n * n) == old * (n * n + 1), 'Unshifted bin factor')
        check(width(n * n - 2) == old * (n * n - 3), 'Minus-two bin factor')
    check((width(9) // width(3), width(7) // width(3)) == (10, 6), 'Mode 3 outputs')
    old, new = width(4), width(4 * 4 + 2)
    preceding_boundary = new // old * old
    check((old, new, preceding_boundary, preceding_boundary + old) == (15, 323, 315, 330), 'Boundary cut')
    print('Sensor logger: mode 3 produces whole-bin ratios 10 and 6. Both identities check '
          'for modes 2 through 100. At mode 4, the +2 update cuts the old 315-to-330 bin at tick 323.')


def check_switches():
    # Integers encode ABCDE as five bits, A most significant and E least.
    all_cubes = set()
    for a, b, c in combinations(range(1, 32), 3):
        direction_space = {0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c}
        if len(direction_space) == 8:
            for origin in range(32):
                all_cubes.add(frozenset(origin ^ v for v in direction_space))
    schedules = [set(range(0, 32, 2)) - {0b00000, 0b11110}]
    schedules.append((schedules[0] - {0b00110}) | {0b00111})
    check(len(all_cubes) == 620, 'Distinct affine three-dimensional cubes')
    observations = []
    for selection in schedules:
        check(len(selection) == 14, 'Schedule budget')
        complete = sum(cube <= selection for cube in all_cubes)
        warnings = sum(1 for row in selection if (row & 1) and not (row & 16))
        observations.append((complete, warnings))
    check(observations == [(7, 0), (3, 1)], 'Experimental coverage and warning counts')
    print('Five-switch lab: 32 switch settings form 620 distinct eight-setting experiments. '
          'The two 14-run schedules cover 7 and 3 complete experiments and trigger 0 and 1 warnings.')


if __name__ == '__main__':
    check_tickets()
    check_triangle()
    check_logger()
    check_switches()
    print('All four application checks passed.')
