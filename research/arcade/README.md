# Maths Arcade research library

Start with a position you can play, make a prediction and follow the calculation that tests it. The papers belong to Atlas Open Mathematics, directed by Albert Tan Sin Hon. The browser links open at the same positions used in the papers. [Visit the Maths Arcade](https://alberttansinhon.com/math-arcade/)

| Game and worked position | Question | Paper |
| --- | --- | --- |
| [Lattice Dash, Warm-up 2](https://alberttansinhon.com/math-arcade/#play/lattice/0/2) | Can two jumps reach the goal? | [Shortest paths and a lower bound](../../docs/MATHS_ARCADE.md#lattice-dash-and-the-three-jump-lower-bound) |
| [Target Forge, Expert 0](https://alberttansinhon.com/math-arcade/#play/forge/2/0) | Can four tiles make 55 using only integer intermediates? | [Exact rational search](../../docs/MATHS_ARCADE.md#why-target-forge-needs-a-fraction) |
| [Parity Lights, Warm-up 7](https://alberttansinhon.com/math-arcade/#play/parity/0/7) | What proves that two presses are optimal? | [A linear system over two elements](../../docs/MATHS_ARCADE.md#press-order-in-parity-lights) |
| [Sudoku, Warm-up 0](https://alberttansinhon.com/math-arcade/#play/sudoku/0/0) | Why must row 1, column 3 contain a 2? How does the generator retain one solution? | [Singles and uniqueness](../../docs/SUDOKU_WHITE_PAPER.md) |
| [Nim Lab, Warm-up 7](https://alberttansinhon.com/math-arcade/#play/nim/0/7) | From heaps of 1, 1 and 6, which move forces a win? | [Nim-sums and winning moves](../../docs/NIM_RESEARCH.md) |
| [Reversi Endgame Lab, Warm-up 7](https://alberttansinhon.com/math-arcade/#play/reversi/0/7) | Which legal placement gives the best final disc margin against perfect replies? | [Exact endgame search](../../docs/REVERSI_RESEARCH.md) |
| [Boardroom Bonus](https://alberttansinhon.com/math-arcade/boardroom/) | Which emissions boundary and bonus threshold reward the board's preferred proposal? | [Incentives and measurement](../../docs/BOARDROOM_WHITE_PAPER.md) |

The [public playtest record](../../docs/ARCADE_PLAYTEST_2026-11-28.md) describes the moves tried on the website, the feedback shown and the changes prompted by play.

## Reproduce the results

Run these commands from the repository root with Python 3.10 or later and Node.js. The checks use only the standard libraries and run offline. This edition was checked with Python 3.12.14 and Node.js 24.22.3.

```sh
python3 tools/verify_arcade_whitepapers.py
node --test research/arcade/*.test.mjs
(cd research/arcade/snapshots/2026-11-28 && sha256sum -c SHA256SUMS)
```

The [Python verifier](../../tools/verify_arcade_whitepapers.py) counts completions of the two Sudoku openings by exact cover. It also checks the bonus thresholds, supplier-weight sensitivity and bus-punctuality transfer example using exact arithmetic. These checks run in the ordinary Python unit suite as well. [Snapshot tests](snapshots.test.mjs) check the same Sudoku openings and bonus decisions against the archived production code.

The [Nim tests](nim.test.mjs) compare the [Nim implementation](nim.mjs) with an independent search over labelled heaps. The [Reversi tests](reversi.test.mjs) compare the [Reversi implementation](reversi.mjs) with an independent bitboard search, including forced passes. Each paper states the inputs and conclusions of its tests. For the first three games, the original paper includes its own [source hashes and replay commands](../../docs/MATHS_ARCADE.md#replay-the-three-examples).

## Source editions

The archived Sudoku and Boardroom modules were checked byte for byte against the public website on 28 November 2026. The dated files preserve the exact implementations used in the papers. Later revisions of the live games may differ. The Boardroom module includes the browser interface and exports `evaluateRule` for use in Node.js.

| Archived source | Website source | SHA-256 |
| --- | --- | --- |
| [Sudoku engine](snapshots/2026-11-28/sudoku-engine.mjs) | [sudoku-engine.mjs](https://alberttansinhon.com/math-arcade/sudoku-engine.mjs) | `094324e1384a9ea11503fe2ac2406d4b16ed2a25c13d717b2b151715ef47d130` |
| [Boardroom Bonus](snapshots/2026-11-28/boardroom/game.mjs) | [boardroom/game.mjs](https://alberttansinhon.com/math-arcade/boardroom/game.mjs) | `94a6d97d19d29f832af932f42a651b133eb8f9b52aaecb1b3cf9c9dbbeb5b6d5` |

For a class or maths circle, the paired challenge sheet includes an answer key, and Boardroom Bonus has a separate participant brief. Cite a paper by its title, project, version and date, using GitHub's commit permalink to identify the edition consulted. [Maths-circle guide](../../docs/MATHS_ARCADE_CLUB_GUIDE.md) · [Boardroom pilot](../../docs/BOARDROOM_PILOT.md) · [Educational content licence](../../LICENSE-CONTENT.md) · [Code licence](../../LICENSE)
