#!/usr/bin/env python3
"""Independently enumerate affine flats and lit sets for The Two Missing Lamps.

No dependency beyond Python 3. No use of the extremal proof to count a flat.
For the n=5, k=4 census, any set attaining a positive maximum contains a
3-flat. An invertible affine change of coordinates takes that flat to the
fixed one. We exhaust every possible extension of that fixed flat.
"""
from collections import Counter
from itertools import combinations
from math import comb


def mask(points):
    return sum(1 << x for x in points)


def affine_flats(n, d):
    points = range(1 << n)
    spaces = {frozenset({0})}
    for _ in range(d):
        spaces = {
            space | {x ^ v for x in space}
            for space in spaces
            for v in points
            if v not in space
        }
    return {mask(x ^ a for x in space) for space in spaces for a in points}


def whole_space_census(n, size, dimension):
    flats = affine_flats(n, dimension)
    frequency = Counter()
    winners = []
    best = -1
    for points in combinations(range(1 << n), size):
        chosen = mask(points)
        count = sum((flat & chosen) == flat for flat in flats)
        frequency[count] += 1
        if count > best:
            best, winners = count, []
        if count == best:
            winners.append(chosen)
    return best, winners, frequency


def check_plane_bounds():
    three_flats = affine_flats(4, 3)
    for size, expected, how_many in [(6, 3, 840), (7, 7, 240)]:
        best, winners, frequency = whole_space_census(4, size, 2)
        assert sum(frequency.values()) == comb(16, size)
        assert best == expected and len(winners) == how_many
        assert all(any((lit & flat) == lit for flat in three_flats) for lit in winners)
        print(f'Four-dimensional space, {size} lit: {sum(frequency.values())} sets; '
              f'most planes {best}; extremisers {len(winners)}.')


def check_cube_count():
    best, winners, _ = whole_space_census(4, 14, 3)
    assert best == 7 and len(winners) == comb(16, 2)
    print('Four-dimensional space: all 120 two-hole patterns contain exactly seven cubes.')

    fixed = mask(range(8))
    cubes = affine_flats(5, 3)
    four_flats = affine_flats(5, 4)
    assert fixed in cubes and len(cubes) == 620 and len(four_flats) == 62
    # A cube is contained precisely when its points outside the fixed flat are lit.
    needed = Counter(cube & ~fixed for cube in cubes)
    assert set(k.bit_count() for k in needed) == {0, 4, 6, 8}
    assert needed[0] == 1
    histogram = Counter()
    all_top_in_a_four_flat = True
    best = -1
    top_count = 0
    for extension in combinations(range(8, 32), 6):
        extra = mask(extension)
        count = needed[0] + needed[extra] + sum(needed[mask(four)] for four in combinations(extension, 4))
        histogram[count] += 1
        if count > best:
            best, top_count, all_top_in_a_four_flat = count, 0, True
        if count == best:
            lit = fixed | extra
            top_count += 1
            all_top_in_a_four_flat &= any((lit & flat) == lit for flat in four_flats)
    assert sum(histogram.values()) == 134596 == comb(24, 6)
    assert best == 7 and top_count == 84 and all_top_in_a_four_flat
    # Every globally maximal set has seven cubes. Double-count (lit set, marked cube).
    total_maximisers = len(cubes) * top_count // best
    assert total_maximisers == 7440 == len(four_flats) * comb(16, 2)
    print(f'Five-dimensional space: all {sum(histogram.values())} extensions of a fixed '
          f'cube; maximum {best}; {top_count} extremisers contain that cube; '
          f'{total_maximisers} extremisers overall, all two-hole four-flats.')


if __name__ == '__main__':
    check_plane_bounds()
    check_cube_count()
