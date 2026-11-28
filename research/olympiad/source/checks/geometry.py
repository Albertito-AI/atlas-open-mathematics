"""Verify the construction against exact coordinates using Python's standard library."""
from fractions import Fraction as F
from itertools import product


def one_pass(triangle, setting):
    result = []
    for i in range(3):
        x, y = triangle[(i + 1) % 3]
        u, v = triangle[(i + 2) % 3]
        result.append(((x + u) * F(1, 2) - setting * (v - y),
                       (y + v) * F(1, 2) + setting * (u - x)))
    return result


def centroid(triangle):
    return tuple(sum(coords) * F(1, 3) for coords in zip(*triangle))


def scaled(triangle, factor):
    gx, gy = centroid(triangle)
    return [(gx + factor * (x - gx), gy + factor * (y - gy)) for x, y in triangle]


example = [(0, 0), (8, 0), (0, 4)]
assert one_pass(example, F(1, 2))[0] == (2, -2)
assert one_pass(example, F(-1, 2))[0] == (6, 6)
settings = [(F(1, 2), F(1, 6)), (F(1), F(2)), (F(0), F(0)),
            (F(-2, 5), F(4, 9)), (F(7, 4), F(-1, 2)), (F(2, 3), F(-2, 3))]
restored = 0
for x, y in product(range(-3, 5), repeat=2):
    triangle = [(-2, 1), (4, -2), (x, y)]
    for a, b in settings:
        t = -(a + b) / (1 + 12 * a * b)
        factor = -F(1, 8) - F(3, 2) * (a * b + a * t + b * t)
        first = one_pass(triangle, a)
        second = one_pass(first, b)
        third = one_pass(second, t)
        assert centroid(triangle) == centroid(first) == centroid(second) == centroid(third)
        assert third == scaled(triangle, factor)
        if (a, b) == settings[0]:
            assert (t, factor) == (-F(1, 3), F(1, 12))
        if (a, b) == settings[1]:
            assert t == -F(3, 25)
        restored += 1

# With ab = -1/12 and a+b nonzero, the final A-arrow on the example
# is never parallel to its original. Its cross product is constant in t.
original = scaled(example, F(1))
gx, gy = centroid(original)
a, b = F(1), -F(1, 12)
second = one_pass(one_pass(original, a), b)
for t in [F(-7), F(-1, 3), F(0), F(2, 5), F(99)]:
    x, y = one_pass(second, t)[0]
    assert (-gx) * (y - gy) + gy * (x - gx) == F(11, 3)

# For exceptional opposite settings ±sqrt(1/12), the exact product and
# sum make both coefficients vanish before the third pass whatever it is.
ab, a_plus_b = -F(1, 12), F(0)
assert F(1, 4) + 3 * ab == 0 and -a_plus_b / 2 == 0
print(f'{restored} exact three-pass checks and all supplementary checks passed.')
