# How does the Maths Arcade make a Sudoku with exactly one solution?

**Atlas Open Mathematics technical white paper, version 1.0 · 28 November 2026**  
Project directed by Albert Tan Sin Hon

## Abstract

A Sudoku can have one solution and still feel quite different to two players. The Maths Arcade makes a narrower, testable promise about each difficulty level. A Warm-up can be finished by inspecting the candidates of individual cells. A Tricky puzzle also requires looking across a row, column or box. An Expert puzzle has one solution even after both of those techniques run out. This paper derives the three conditions, works through two opening moves and establishes the scope of the arcade's protection against repeat deals. [Play Sudoku](https://alberttansinhon.com/math-arcade/#play/sudoku/0/0)

## Two ways to recognise a forced digit

Each of the nine rows, nine columns and nine $3\times3$ boxes must contain every digit in $D=\{1,\ldots,9\}$ exactly once. For an empty cell in row $r$, column $c$ and box $b$, let $R_r$, $C_c$ and $B_b$ contain the digits already present in those three units. The legal candidates are

$$
A(r,c)=D\setminus(R_r\cup C_c\cup B_b).
$$

A **naked single** occurs when $A(r,c)$ contains just one digit. A **hidden single** occurs when a missing digit belongs to the candidate set of just one cell in a unit. In the first case the cell has only one possible digit. In the second the digit has only one possible location. Both arguments apply to every completion consistent with the clues. [Peter Norvig, *Solving Every Sudoku Puzzle*, “Constraint Propagation”](https://norvig.com/sudoku.html)

### Warm-up, seed 0

In the game, **Hint** selects a cell and suggests what to examine. **Explain the digit** reveals the forced value and the reason. The player can enter the value independently or choose **Place hinted digit**. When neither kind of single is available, **Reveal checked digit** instead offers the value from the unique solution.

The first row reads `. 8 . 5 . 4 . . 1`, where a dot denotes an empty cell. Consider **row 1, column 3**. The row allows $\{2,3,6,7,9\}$. Column 3 already contains $3,4,6,7,9$, leaving only $2$. The upper-left box contains $1,3,4,5,8$ and also permits $2$. A player can therefore enter **2** in that cell. This is the engine's first deduction for the 42-clue opening. [Open the same Warm-up](https://alberttansinhon.com/math-arcade/#play/sudoku/0/0)

### Tricky, seed 2

The second row reads `2 . 8 6 1 5 . . .`. Computing candidates from each cell's row, column and box gives the following four sets.

| Empty cell in row 2 | Column 2 | Column 7 | Column 8 | Column 9 |
| --- | --- | --- | --- | --- |
| Legal candidates | 7, 9 | 3, 7, 9 | 3, 7 | 3, 4, 7 |

Each cell admits several digits, but the row must eventually contain a 4. Only column 9 can hold it. **Row 2, column 9 is 4**, the first deduction for this 33-clue opening. [Open the same Tricky puzzle](https://alberttansinhon.com/math-arcade/#play/sudoku/1/2)

## How generation establishes uniqueness

The generator starts with an empty grid and builds one complete solution by backtracking, trying legal digits in a seeded, shuffled order. It then visits clues in a shuffled order and tentatively removes each one. The completed grid remains a witness that at least one solution exists. The acceptance test for each removal depends on the selected level.

| Level | When the generator keeps a removal | What the final puzzle must satisfy |
| --- | --- | --- |
| Warm-up | Repeated naked singles fill the board. | Naked singles solve every empty cell. |
| Tricky | Naked and hidden singles together fill the board. | The solver reaches a point with no naked single and uses at least one hidden single. |
| Expert | Counting completions up to two returns exactly one. | Repeated naked and hidden singles leave at least one cell empty. |

**Why deduction proves uniqueness.** Take any two completions of a Warm-up or Tricky opening. They agree with the clues. Each single forces the same next digit in both completions. By induction they agree at every cell the solver fills. When the solver fills all 81 cells, the two completions coincide. The Tricky solver always looks for a naked single first, so the recorded hidden single marks a genuine gap in what naked singles alone can achieve.

**Why counting to two suffices.** At an empty cell with the fewest candidates, the search branches on every legal digit. Each completion belongs to exactly one branch, determined by the digit it places there. A contradiction contributes zero completions and a legal full grid contributes one. If $N$ is the number of completions, stopping once two are found returns $\min(N,2)$. A return value of one therefore proves uniqueness. Expert certifies a limit of the two implemented deductions. A player might still find another logical technique that finishes the grid.

The clue counts the generator aims for are 40–43, 31–34 and 25–28 respectively. The reasoning tests determine which board can be returned. If eight construction attempts miss the requested tier, Tricky and Expert each have a prechecked fallback puzzle. The engine permutes digit labels, bands, rows within bands, stacks and columns within stacks, and may transpose the grid. Each change is invertible and preserves the units. It therefore gives a bijection between completions, and carries single deductions to single deductions. [Generation, counting and fallback boards](https://alberttansinhon.com/math-arcade/sudoku-engine.mjs)

## What a fresh deal guarantees

A share link fixes the difficulty and an unsigned 32-bit seed. Reopening it under the same engine reproduces the same clues. For fresh deals the browser starts a separate stream at each level. With a random start and an odd increment $d$, the next candidate seed is $s_{n+1}=(s_n+d)\bmod 2^{32}$. A return to the starting seed after $k>0$ steps requires $2^{32}$ to divide $kd$. Since $d$ is odd, the smallest possible $k$ is $2^{32}$. This proves the period of the candidate seeds. Multiple seeds can still map to the same clue grid.

Before serving a fresh board, the dealer compares its actual 81-character clue string with the 64 most recent successful fresh deals at that level. It skips matches and the currently active seed. After 32 unsuccessful candidates it advances the stream and asks the player to retry. IndexedDB coordinates fresh deals across tabs sharing the same browser storage. If storage is unavailable, the dealer keeps a history for the current page session. Explicit replays bypass this history. Clearing browser data or changing device starts a different history, and digit relabellings count as different openings. These facts support frequent fresh play while leaving the lifetime repeat rate and the distribution of human solving times unmeasured. [Dealer and storage](https://alberttansinhon.com/math-arcade/arcade-state.mjs) · [Game routing and fresh deals](https://alberttansinhon.com/math-arcade/arcade.mjs)

## Reproducibility and attribution

From the repository root, run `python3 tools/verify_arcade_whitepapers.py` using Python 3.10 or later. An independent exact-cover implementation counts completions for the two fixed openings above and checks the worked moves. With Python 3.12.14, the check found one completion for each opening. Naked singles filled all 39 empty Warm-up cells. The Tricky opening had no naked single and its row forced the 4 above. Separate control grids returned zero and multiple completions as expected. The corresponding game calls are `makeSudoku(0, 0)` and `makeSudoku(1, 2)`. The SHA-256 digest of the game engine used for this edition is `094324e1384a9ea11503fe2ac2406d4b16ed2a25c13d717b2b151715ef47d130`. The examples are deterministic checks. The general uniqueness argument rests on the acceptance tests and the bijections proved above. [Verification script and fixed openings](../tools/verify_arcade_whitepapers.py) · [Archived game engine](../research/arcade/snapshots/2026-11-28/sudoku-engine.mjs) · [Published game engine](https://alberttansinhon.com/math-arcade/sudoku-engine.mjs)

**Suggested citation.** Atlas Open Mathematics (2026). *How does the Maths Arcade make a Sudoku with exactly one solution?* Version 1.0, 28 November. Project directed by Albert Tan Sin Hon. Cite the GitHub commit permalink for the edition consulted.

OpenAI Codex assisted with drafting and mathematical checks. This project technical paper documents an application of established Sudoku methods. The repository's [educational content licence](../LICENSE-CONTENT.md) covers the original exposition. [Report a correction](https://github.com/Albertito-AI/atlas-open-mathematics/issues/new?template=correction.yml)
