#!/usr/bin/env python3
"""Finite checks for the classic one-known-heavier balance model, Python 3.10+."""
from collections import Counter
from fractions import Fraction


def inspection_budget(count):
    """Least integer d with 3**d >= count, including d = 0."""
    if count < 1:
        raise ValueError('At least one candidate is required.')
    capacity = 1
    inspections = 0
    while capacity < count:
        capacity *= 3
        inspections += 1
    return inspections


def divide(candidates):
    """Return the left, right and unweighed candidates for the constructive proof."""
    size = len(candidates)
    if size < 2:
        raise ValueError('Already identified.')
    per_pan = (size + 1) // 3
    left = candidates[:per_pan]
    right = candidates[per_pan:2 * per_pan]
    aside = candidates[2 * per_pan:]
    assert 0 < len(left) == len(right)
    assert max(map(len, (left, right, aside))) == (size + 2) // 3
    return left, right, aside


def reading(masses, left, right):
    """An independent physical balance with no information about the candidate sets."""
    difference = sum(masses[i] for i in left) - sum(masses[i] for i in right)
    if difference > 0:
        return 0
    if difference < 0:
        return 1
    return 2


def follow_fixed_culprit(count, culprit):
    ordinary_mass = 100
    masses = [ordinary_mass] * count
    masses[culprit] += 3
    candidates = tuple(range(count))
    used = 0
    while len(candidates) > 1:
        groups = divide(candidates)
        outcome = reading(masses, groups[0], groups[1])
        candidates = groups[outcome]
        assert culprit in candidates
        used += 1
    assert candidates == (culprit,)
    return used


def replay_largest_branches(count):
    """Verify every legal tie choice against the candidate's complete physical transcript."""
    depth_counts = Counter()
    stack = [(tuple(range(count)), ())]
    while stack:
        candidates, transcript = stack.pop()
        if len(candidates) == 1:
            masses = [100] * count
            masses[candidates[0]] += 3
            assert all(reading(masses, left, right) == outcome for left, right, outcome in transcript)
            depth_counts[len(transcript)] += 1
            continue
        left, right, aside = divide(candidates)
        largest = max(len(left), len(right), len(aside))
        for outcome, survivors in enumerate((left, right, aside)):
            if len(survivors) == largest:
                stack.append((survivors, transcript + ((left, right, outcome),)))
    return depth_counts


def main():
    total_cases = 0
    tie_transcripts = 0
    for count in range(1, 101):
        budget = inspection_budget(count)
        depths = Counter(follow_fixed_culprit(count, culprit) for culprit in range(count))
        assert sum(depths.values()) == count
        assert max(depths) == budget
        largest_depths = replay_largest_branches(count)
        assert set(largest_depths) == {budget}
        tie_transcripts += sum(largest_depths.values())
        total_cases += count
        if count == 12:
            assert depths == {2: 6, 3: 6}
            assert Fraction(sum(depth * n for depth, n in depths.items()), count) == Fraction(5, 2)

    assert total_cases == 5050
    for depth in range(12):
        assert inspection_budget(3 ** depth) == depth
        assert inspection_budget(3 ** depth + 1) == depth + 1
    assert inspection_budget(10) == 3
    assert inspection_budget(24) == 3
    assert inspection_budget(14) == 3 and inspection_budget(28) == 4

    masses = [100] * 24
    left, right, _ = divide(tuple(range(24)))
    masses[right[0]] += 3  # True target, with the extra washer.
    assert reading(masses, left, right) == 1
    masses[left[0]] += 4   # Extra carton tare violates the equal-baseline premise.
    assert reading(masses, left, right) == 0
    assert sum(masses[i] for i in left) - sum(masses[i] for i in right) == 1

    print(f'{total_cases:,} fixed culprits at N = 1 through 100 identified. All worst depths matched the capacity bound.')
    print(f'{tie_transcripts:,} complete largest-branch transcripts agreed with a fixed culprit.')
    print('N = 12: six leaves at depth 2 and six at depth 3. Uniform fixed-culprit mean 5/2.')
    print('N = 24: three inspections. A 4 g carton can reverse the 3 g washer outcome by 1 g.')


if __name__ == '__main__':
    main()
