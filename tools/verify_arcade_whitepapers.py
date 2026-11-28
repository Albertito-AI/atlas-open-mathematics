#!/usr/bin/env python3
"""Recheck fixed Sudoku positions and fictional Boardroom Bonus data offline.

Run with Python 3.10+ (standard library only):
    python3 tools/verify_arcade_whitepapers.py

Sudoku fixtures were transcribed from the 28 November 2026 game release,
makeSudoku(0, 0) and makeSudoku(1, 2). Zeros denote empty squares.
The exact-cover search below is a separate implementation from the game's
bit-mask solver. It checks these specific fixtures, not all possible seeds.
"""

from fractions import Fraction


WARM_UP = (
    "080504001" "513078090" "004300000"
    "020100063" "049863125" "136209000"
    "090005640" "400012500" "307080019"
)
TRICKY = (
    "003020001" "208615000" "410000000"
    "004801026" "062000018" "800076049"
    "080090200" "100700400" "306000090"
)
DIGITS = set(range(1, 10))
ROWS = [set(range(row * 9, row * 9 + 9)) for row in range(9)]
COLUMNS = [set(range(column, 81, 9)) for column in range(9)]
BOXES = [
    {(top + r) * 9 + left + c for r in range(3) for c in range(3)}
    for top in (0, 3, 6) for left in (0, 3, 6)
]
UNITS = ROWS + COLUMNS + BOXES


def check(condition, message):
    """Keep verification active even when Python is invoked with -O."""
    if not condition:
        raise ValueError(message)


def parse_grid(text):
    check(len(text) == 81 and set(text) <= set("0123456789"), "Invalid Sudoku encoding")
    return tuple(map(int, text))


def candidates(grid, cell):
    if grid[cell]:
        return set()
    peers = set().union(*(unit for unit in UNITS if cell in unit))
    return DIGITS - {grid[other] for other in peers}


def completions(grid, limit=2):
    """Find at most 'limit' solutions. Cover all 324 requirements exactly once."""
    columns = {column: set() for column in range(324)}
    placements = {}
    for cell, clue in enumerate(grid):
        row, column = divmod(cell, 9)
        box = 3 * (row // 3) + column // 3
        for digit in (DIGITS if clue == 0 else {clue}):
            # One digit in this cell; one occurrence in its row, column and box.
            choice = (cell, digit)
            delta = digit - 1
            needs = (cell, 81 + 9 * row + delta, 162 + 9 * column + delta,
                     243 + 9 * box + delta)
            placements[choice] = needs
            for need in needs:
                columns[need].add(choice)

    found = []
    chosen = {}

    def visit(remaining):
        if not remaining:
            found.append(tuple(chosen[cell] for cell in range(81)))
            return
        # Branch on the least populated remaining constraint.
        smallest = min(remaining.values(), key=len)
        for choice in sorted(smallest):
            selected = placements[choice]
            excluded = set().union(*(remaining[need] for need in selected))
            child = {need: options - excluded for need, options in remaining.items()
                     if need not in selected}
            cell, digit = choice
            chosen[cell] = digit
            visit(child)
            del chosen[cell]
            if len(found) >= limit:
                break

    visit(columns)
    return found


def verify_sudoku():
    solutions = []
    for opening in (WARM_UP, TRICKY):
        grid = parse_grid(opening)
        found = completions(grid)
        check(len(found) == 1, "Expected exactly one completion")
        solution = found[0]
        check(all(clue in (0, answer) for clue, answer in zip(grid, solution)),
              "A clue was changed")
        check(all({solution[cell] for cell in unit} == DIGITS for unit in UNITS),
              "Invalid row, column or box")
        solutions.append(solution)

    warm = parse_grid(WARM_UP)
    check(sum(bool(d) for d in warm) == 42, "Warm-up clue count changed")
    check(candidates(warm, 2) == {2}, "Warm-up r1c3 is not forced to 2")
    grid = list(warm)
    steps = 0
    while 0 in grid:
        for cell in range(81):
            options = candidates(grid, cell)
            if len(options) == 1:
                grid[cell] = options.pop()
                steps += 1
                break
        else:
            raise ValueError("Naked singles exhausted before completion")
    check(tuple(grid) == solutions[0] and steps == 39, "Warm-up deduction trace failed")

    tricky = parse_grid(TRICKY)
    check(all(len(candidates(tricky, i)) != 1 for i in range(81)),
          "Tricky opening unexpectedly allows a naked single")
    check({i for i in ROWS[1] if 4 in candidates(tricky, i)} == {17},
          "Expected 4 only in r2c9 of row 2")
    check(solutions[1][17] == 4, "Completion disagrees with the hidden single")

    duplicate = (solutions[0][1],) + solutions[0][1:]
    check(not completions(duplicate), "Conflicting givens should be unsatisfiable")
    # Swapping digits 1 and 2 globally gives a second completion when both are removed.
    ambiguous = tuple(0 if d in (1, 2) else d for d in solutions[0])
    check(len(completions(ambiguous)) == 2, "Two-solution cutoff was not reached")
    print("Sudoku: two unique fixtures. Warm-up r1c3 = 2, 39 naked singles. "
          "Tricky r2c9 = 4, hidden single. Zero- and multiple-solution controls passed.")


def verify_boardroom():
    baseline = (80, 20)
    plans = {"A": (68, 20), "B": (50, 65)}

    def reductions(measure):
        before = measure(baseline)
        return {name: Fraction(100 * (before - measure(plan)), before)
                for name, plan in plans.items()}

    own = reductions(lambda plan: plan[0])
    both = reductions(sum)
    check(own == {"A": 15, "B": Fraction(75, 2)}, "Own-boundary calculation failed")
    check(both == {"A": 12, "B": -15}, "Combined-boundary calculation failed")
    # The classifier can change only at a reduction value. Test every boundary
    # in the game's domain [0.1%, 100%] and one interior point of each interval.
    edges = sorted({Fraction(1, 10), Fraction(100), own["A"], own["B"], both["A"]})
    thresholds = set(edges) | {(lo + hi) / 2 for lo, hi in zip(edges, edges[1:])}
    thresholds.update({Fraction(10), Fraction(25)})
    for threshold in thresholds:
        paid_own = {name for name, reduction in own.items() if reduction >= threshold}
        paid_both = {name for name, reduction in both.items() if reduction >= threshold}
        expected_own = set()
        if threshold <= 15:
            expected_own = {"A", "B"}
        elif threshold <= Fraction(75, 2):
            expected_own = {"B"}
        check(paid_own == expected_own, f"Own-boundary bonus failed at {threshold}%")
        check(paid_both == ({"A"} if threshold <= 12 else set()),
              f"Combined-boundary bonus failed at {threshold}%")

    # Paper-only extension. Weight supplier emissions by w in [0, 1].
    # Each comparison below is linear, so signs either side establish its direction.
    def weighted(plan, weight):
        own_emissions, supplier_emissions = plan
        return own_emissions + weight * supplier_emissions

    half = Fraction(1, 2)
    check([weighted(plan, half) for plan in (baseline, plans["A"], plans["B"])]
          == [90, 78, Fraction(165, 2)], "Half-weight comparison failed")
    rank_tie = Fraction(2, 5)
    baseline_tie = Fraction(2, 3)
    bonus_cutoff = Fraction(1, 5)
    for weight in (0, bonus_cutoff, rank_tie, half, baseline_tie, 1):
        start = weighted(baseline, weight)
        a, b = weighted(plans["A"], weight), weighted(plans["B"], weight)
        check((a == b) == (weight == rank_tie) and (a < b) == (weight > rank_tie),
              "Weighted ranking boundary failed")
        check((b == start) == (weight == baseline_tie) and (b < start) == (weight < baseline_tie),
              "Weighted baseline boundary failed")
        check((b <= Fraction(3, 4) * start) == (weight <= bonus_cutoff),
              "Weighted 25% bonus boundary failed")
    check(sum(plans["A"]) - plans["B"][0] == 38 and sum(baseline) - plans["B"][0] == 50,
          "Missing supplier-emissions breakpoints changed")

    # Triples are on time, late and cancelled. Compare both denominators exactly.
    old, new = (90, 10, 0), (88, 2, 10)
    operated = [Fraction(on, on + late) for on, late, cancelled in (old, new)]
    scheduled = [Fraction(trips[0], sum(trips)) for trips in (old, new)]
    check(operated == [Fraction(9, 10), Fraction(44, 45)], "Operated rate mismatch")
    check(scheduled == [Fraction(9, 10), Fraction(22, 25)], "Scheduled rate mismatch")
    check(operated[1] > operated[0] and scheduled[1] < scheduled[0], "Reversal failed")
    print("Boardroom: own reductions 15% and 37.5%; combined reductions 12% and "
          "-15%. Inclusive bonus thresholds checked. Bus punctuality: operated "
          "9/10 to 44/45; scheduled 9/10 to 22/25.")
    print("Weighted extension: ranking tie at 2/5; baseline tie at 2/3; B earns "
          "25% reduction bonus through 1/5. Unknown supplier breakpoints: 38, 50.")


if __name__ == "__main__":
    verify_sudoku()
    verify_boardroom()
