# Maths Arcade player sheets

Atlas Open Mathematics · Albert Tan Sin Hon, project director · 28 November 2026

[Download the six player sheets (PDF)](https://raw.githubusercontent.com/Albertito-AI/atlas-open-mathematics/main/docs/teaching/Maths_Arcade_Player_Sheets.pdf) · [Open the six-game teaching pack](https://alberttansinhon.com/math-arcade/teaching/)

Work through each opening before trying the second position. These pages reproduce the prompts and starting positions from the printable edition. Record predictions, moves and reasons on paper or in your own document.

## Sudoku

**When does the board force a digit?**

Use each digit 1 to 9 exactly once in every row, column and 3 × 3 box. Count rows down from the top and columns from the left. Keep hints closed until you have made a prediction.

### Opening · Warm-up, seed 0

An empty cell is shown as a dot.

| Row / column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | · | 8 | · | 5 | · | 4 | · | · | 1 |
| 2 | 5 | 1 | 3 | · | 7 | 8 | · | 9 | · |
| 3 | · | · | 4 | 3 | · | · | · | · | · |
| 4 | · | 2 | · | 1 | · | · | · | 6 | 3 |
| 5 | · | 4 | 9 | 8 | 6 | 3 | 1 | 2 | 5 |
| 6 | 1 | 3 | 6 | 2 | · | 9 | · | · | · |
| 7 | · | 9 | · | · | · | 5 | 6 | 4 | · |
| 8 | 4 | · | · | · | 1 | 2 | 5 | · | · |
| 9 | 3 | · | 7 | · | 8 | · | · | 1 | 9 |

Start at row 1, column 3. Which digits does the row allow? Test each against the column and box. [Play this position](https://alberttansinhon.com/math-arcade/#play/sudoku/0/0)

### Transfer · Tricky, seed 8

An empty cell is shown as a dot.

| Row / column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 2 | · | · | 8 | · | 1 | · | 9 |
| 2 | 3 | · | · | · | 1 | 7 | · | · | 4 |
| 3 | 1 | 7 | · | · | · | 4 | 2 | · | · |
| 4 | 8 | 3 | · | 9 | 4 | 1 | 6 | · | 7 |
| 5 | · | · | 7 | 6 | · | · | · | 8 | · |
| 6 | · | 6 | · | · | · | · | · | · | 3 |
| 7 | 7 | 8 | 1 | · | · | · | · | · | · |
| 8 | · | 4 | · | · | 2 | · | 7 | · | · |
| 9 | · | · | · | · | · | · | · | · | · |

In the upper-middle box, where must 9 go? Examine rows 1–3 and columns 4–6. [Play this position](https://alberttansinhon.com/math-arcade/#play/sudoku/1/8)

### Record your reasoning

1. **Build a candidate list.** Write the digits missing from row 1. Cross out the ones column 3 or the box excludes.
2. **Give a checkable reason.** State your entry and name the clues a partner can use to verify it. Find a second forced move.
3. **Transfer your reasoning.** List the empty squares in the transfer box. For each rejected square, record the clue that excludes 9.

## Lattice Dash

**How can you prove a route is shortest?**

Each jump adds a fixed vector to your coordinates. Stay on the grid and land only on open points. Each position below identifies the start, beacon and blocked landings.

### Opening · Warm-up, seed 2

Coordinates run from 0 to 5 on both axes. Start at (1, 3). The beacon is at (0, 5). Blocked landings: none. Jump keys: 1 = (-1, +1), 2 = (-1, +0), 3 = (+1, -1), 4 = (+1, +0).

Keys 1–4 add (−1, +1), (−1, 0), (+1, −1), (+1, 0). Move from (1, 3) to (0, 5). [Play this position](https://alberttansinhon.com/math-arcade/#play/lattice/0/2)

### Transfer · Tricky, seed 55

Coordinates run from 0 to 6 on both axes. Start at (1, 5). The beacon is at (4, 2). Blocked landings: (3, 0), (3, 1), (3, 3), (2, 2), (4, 0). Jump keys: 1 = (+1, +1), 2 = (+1, -1), 3 = (-1, -1), 4 = (-1, +1).

Keys 1–4 point NE, SE, SW, NW. Each jump moves one column and one row. Go from (1, 5) to (4, 2). [Play this position](https://alberttansinhon.com/math-arcade/#play/lattice/1/55)

### Record your reasoning

1. **Record a witness.** Write your opening key sequence and every landing. Which reordered sequence can you also play?
2. **Rule out shorter routes.** Use the required change in height and horizontal position to explain why every shorter attempt fails.
3. **Investigate the obstacle.** On the transfer board, sketch a detour and justify its length. Which single cross would you remove to shorten it?

## Target Forge

**Can different calculations make the same target?**

Use all four original tiles exactly once. Combine two tiles with +, −, × or ÷, and put their result back. Subtraction and division depend on the order. You may use exact fractions.

### Opening · Warm-up, seed 2

Target: **23**. Tiles: 3, 4, 2, 5.

Make two routes to the opening target. In one route, try keeping an original tile until the last move. [Play this position](https://alberttansinhon.com/math-arcade/#play/forge/0/2)

### Transfer · Expert, seed 1

Target: **81**. Tiles: 8, 2, 7, 12.

Find a nearby product. Reserve a tile as your final multiplier. What value must the other tiles supply? [Play this position](https://alberttansinhon.com/math-arcade/#play/forge/2/1)

### Record your reasoning

1. **Opening route 1.** Record all three combinations. Mark which original tiles each intermediate number contains.
2. **Opening route 2.** Show a genuinely different calculation. Compare its final operation with the first route.
3. **Transfer calculation.** Leave three lines another player can replay. Check each fraction and each of the four tile uses.

## Parity Lights

**Can a useful first press switch more lights on?**

Pressing a square flips that lamp and its immediate neighbours above, below, left and right. A lamp that is on turns off, and a lamp that is off turns on. Clear every lamp.

### Opening · Warm-up, seed 7

| Row / column | 1 | 2 | 3 |
| --- | --- | --- | --- |
| A | on | on | off |
| B | on | off | on |
| C | off | on | on |

Predict the effect of each proposed press. Mark your chosen switches on the diagram. [Play this position](https://alberttansinhon.com/math-arcade/#play/parity/0/7)

### Transfer · Warm-up, seed 4

| Row / column | 1 | 2 | 3 |
| --- | --- | --- | --- |
| A | off | off | off |
| B | off | off | off |
| C | off | on | off |

Only C2 is lit. Predict the effect of pressing it. Can any first press leave fewer lamps on? Try to clear the board. [Play this position](https://alberttansinhon.com/math-arcade/#play/parity/0/4)

### Record your reasoning

1. **Before pressing.** Choose an opening switch. Name all the lamps it changes and predict which lamps will remain lit.
2. **Clear the opening.** List your presses, then try them in reverse order. Why can one press alone never clear this opening?
3. **Question a greedy move.** Record your transfer sequence and the lit count after each press. How would you check whether an even shorter plan exists?

## Nim Lab

**Which choices still work against the best reply?**

Players alternate. On each turn remove one or more counters from exactly one heap. Taking the last counter wins. State whose turn comes next whenever you describe a position.

### Opening · Warm-up, seed 7

| Heap | Counters |
| --- | --- |
| A | 1 |
| B | 1 |
| C | 6 |

Compare taking five from C with taking six from C. Keep the binary comparison closed for your prediction. [Play this position](https://alberttansinhon.com/math-arcade/#play/nim/0/7)

### Transfer · Tricky, seed 2

| Heap | Counters |
| --- | --- |
| A | 6 |
| B | 3 |
| C | 2 |
| D | 4 |

Write each heap as a sum of 4, 2 and 1, using each weight at most once. Test different opening moves. [Play this position](https://alberttansinhon.com/math-arcade/#play/nim/1/2)

### Record your reasoning

1. **Try both opening choices.** For each choice, write the remaining heap sizes and whose turn comes next.
2. **Test every reply.** Choose a line you think wins. Describe a response for every legal reply the opponent could make.
3. **Change to four heaps.** List every opening move you think gives the opponent a losing position. Which binary columns are even after each?

## Reversi Endgame Lab

**Which first move survives the strongest reply?**

Place a disc to bracket at least one opposing disc in a straight line with your colour at the far end. Flip every bracketed line. Pass if you have no legal move. When neither side can move, count the discs.

### Opening · Warm-up, seed 7

White to move. W = white disc, B = black disc, dot = empty square.

| Row / column | A | B | C | D | E | F | G | H |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | W | W | W | W | W | W | W | W |
| 2 | B | B | W | B | W | B | · | W |
| 3 | B | B | W | B | B | W | B | W |
| 4 | B | B | B | W | W | B | W | W |
| 5 | B | B | W | W | W | W | W | W |
| 6 | B | B | W | W | B | B | B | B |
| 7 | B | B | B | B | B | B | B | · |
| 8 | B | B | B | B | B | B | B | · |

White to play. Compare G2, H7 and H8. For each, count the discs it would flip immediately. [Play this position](https://alberttansinhon.com/math-arcade/#play/reversi/0/7)

### Transfer · Warm-up, seed 14

Black to move. W = white disc, B = black disc, dot = empty square.

| Row / column | A | B | C | D | E | F | G | H |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | W | W | W | W | B | B | B | B |
| 2 | · | W | B | W | B | B | B | B |
| 3 | B | W | W | B | B | B | B | B |
| 4 | B | W | B | B | B | B | B | B |
| 5 | B | W | B | B | B | W | B | B |
| 6 | B | B | B | B | B | B | B | B |
| 7 | B | W | W | B | B | W | B | B |
| 8 | · | · | B | B | B | B | B | B |

Black to play. Compare A2, A8 and B8. Which move forces a pass? Which gives the best final lead? [Play this position](https://alberttansinhon.com/math-arcade/#play/reversi/0/14)

### Record your reasoning

1. **Predict before comparing.** Rank the opening moves using immediate flips. Mark at least one captured line on the board.
2. **Play two continuations.** Record both sides’ choices, including passes. Give the final White-minus-Black margin for each line.
3. **Defend a prediction.** On the transfer board, choose a move for Black and state its strongest opposing reply or forced pass. Score the finish from Black’s side.

## After the exercises

Teachers and independent learners can consult the [worked solutions and assessments](TEACHING_GUIDE.md).

[Teaching resources](https://alberttansinhon.com/math-arcade/teaching/) · [Play the arcade](https://alberttansinhon.com/math-arcade/) · [Research papers on GitHub Pages](https://albertito-ai.github.io/Albertito-AI/maths-arcade-research/) · [Research archive and reproducibility](../../research/arcade/README.md)

Original educational text and diagrams are available under [Creative Commons Attribution 4.0](../../LICENSE-CONTENT.md). Credit Albert Tan Sin Hon and the named contributors, link to the source version and identify any adaptations.
