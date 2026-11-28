# How the six Maths Arcade opponents play

**Atlas Open Mathematics implementation note · 28 November 2026**

What does it mean to beat a computer at a puzzle with no opposing pieces? The Maths Arcade uses a different test for each game. In Nim and Reversi, the players change a shared position. In the other four games, both start with the same task and their results are compared under stated rules. The computer runs in the player's browser. The same match link identifies the game, difficulty and starting seed. Reversi always begins with its four standard opening discs. Its seed can change how the computer chooses among tied moves. [Play a match](https://alberttansinhon.com/math-arcade/#match) · [GitHub Pages mirror](https://albertito-ai.github.io/Albertito-AI/math-arcade/#match) · [Browse the game sources](https://github.com/Albertito-AI/Albertito-AI/tree/main/site/math-arcade)

## Shared-board games

**Nim.** Each turn removes at least one counter from one heap. The last player to take a counter wins. Easy samples uniformly among legal moves. Medium reduces the largest heap to the size of the runner-up where possible. When the two largest heaps are equal it clears a third heap if available. It understands how to mirror in a two-heap ending. Hard computes the bitwise exclusive OR of all heap sizes. When it is non-zero the opponent can reduce a heap to leave zero. From zero, every legal move makes the exclusive OR non-zero. This is the classical normal-play guarantee. It requires the opponent to keep following the strategy, and a player who starts from a losing position cannot force a win. [Play Nim](https://alberttansinhon.com/math-arcade/#match/nim) · [Bouton's argument and independently checked examples](NIM_RESEARCH.md)

**Reversi.** Start from the standard board and play until neither colour has a legal move. A colour with no legal placement passes, even when its opponent has another turn. The result uses the final physical disc counts. Easy chooses randomly among legal moves. Medium maximises the number of immediate flips. Hard searches three placements ahead earlier in the game, using mobility, corner ownership, corner exposure and disc counts to evaluate a position at its horizon. With at most six empty squares at the start of its turn it searches every relevant continuation to its terminal outcome using alpha-beta pruning. A compulsory pass consumes no placement. Its early-game evaluations remain estimates. The separate Endgame Lab starts late enough to search all the way to the final count from its first choice. [Play a full game](https://alberttansinhon.com/math-arcade/#match/reversi) · [Endgame Lab paper](REVERSI_RESEARCH.md) · [World Othello Federation rules](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english)

## Independent-board contests

| Game and winning condition | How the rival chooses | What the result establishes |
| --- | --- | --- |
| [Sudoku](https://alberttansinhon.com/math-arcade/#match/sudoku). Reach the checkpoint first on a copy of the same puzzle. | It looks for naked and hidden singles. If these stall, it tries candidates and checks whether a completion exists. Easy needs five correct entries and places one every second turn. Medium needs seven and places two every three turns. Hard needs nine and places one every turn. | An incorrect entry or a pass spends one turn. Pencil marks are free. The human acts first and takes the win on reaching the goal. Thinking time carries no penalty. This measures correctness over a fixed number of turns. |
| [Lattice Dash](https://alberttansinhon.com/math-arcade/#match/lattice). Reach the beacon in fewer legal jumps. | Easy explores up to four unvisited landings, Medium up to two. Each then computes a shortest route from its new position. Hard chooses a shortest route from the start. | Matching Hard's move count earns a draw. A successful detour can demonstrate reachability while missing the minimum. |
| [Parity Lights](https://alberttansinhon.com/math-arcade/#match/parity). Switch all lamps off in fewer presses. | Easy starts with up to three distinct greedy presses favouring the fewest lit lamps afterwards. Medium tries one. Both then solve the remaining board exactly. Hard searches all first-row press patterns and minimises the total count from the start. | A larger visible cluster of lit lamps can still be closer to a solution. A shortest solution draws with Hard. |
| [Target Forge](https://alberttansinhon.com/math-arcade/#match/forge). Use all four tiles and minimise the absolute distance to the target. Ties favour smaller working numbers. | Easy keeps one promising continuation at each combination. Medium tries up to eight and retains the better of that line and Easy's. Hard also searches for an exact expression. | The tie-break is the largest absolute numerator or denominator of either of the first two reduced intermediate results. A different exact expression can beat Hard on that tie-break. Equal distance and equal peak yield a draw. |

Both route contests let the player finish even if the rival has already arrived. When the player finishes first the remaining rival moves are scored too. This makes the comparison depend on the number of moves used to solve each board.

## A reproducible strategy check

Open [Easy Nim, seed 7](https://alberttansinhon.com/math-arcade/#match/nim/0/7). The heaps are 1, 1 and 6. Take all six from C. The rival must remove one of the two remaining single counters, so taking the last one wins. This conclusion follows from the position and holds regardless of which legal rival policy selects the reply. Next compare a position where the policies disagree. With heaps 1, 2, 4 and 6, Medium removes two from the largest heap to make 4 and 4. The remaining heaps then have a non-zero nim-sum. Hard instead removes the single counter from the first heap and leaves 2, 4 and 6 with nim-sum zero. This second comparison is a paper position, independent of the seeded opening.

The public match files are ordinary browser modules. To replay the strategy comparison in an empty directory using Node.js, run the following commands. The assertions select legal moves using the shipped rival and recompute the nim-sum of the resulting board.

```sh
base=https://albertito-ai.github.io/Albertito-AI/math-arcade
curl -fsSLO "$base/nim.mjs"
curl -fsSLO "$base/match-nim.mjs"
node --input-type=module <<'JS'
import assert from 'node:assert/strict';
import { makeNim, nimSum, playMove } from './nim.mjs';
import { agentMove } from './match-nim.mjs';
assert.deepEqual(makeNim(0, 7), [1, 1, 6]);
const heaps = [1, 2, 4, 6];
for (const [level, heap, take, sum] of [[1, 3, 2, 3], [2, 0, 1, 0]]) {
  assert.deepEqual(agentMove(heaps, level), { heap, take });
  assert.equal(nimSum(playMove(heaps, heap, take)), sum);
}
JS
```

In a browser check at 390 pixels wide, each of the three Nim strengths completed from seed 7 in both the Pages build and the standalone HTML file with external HTTP requests blocked. The same turns produced the same outcomes across the two formats. A full Medium Reversi game from seed 7 also reached a terminal count of Black 23 and White 41 when the human took the first legal square in row order on each turn. These are specific replay results.

These examples and the software checks establish features of the rules and the implemented opponents. They do not measure learner improvement or calibrate the labels against human playing strength. To investigate teaching outcomes, retain the opening and level, the player's prediction, the rival's reply and performance on a new position. The [version 1.1 teaching pack](https://doi.org/10.5281/zenodo.24618393) preserves the six opponent modes in its offline arcade. The [version 1.0 teaching pack](https://doi.org/10.5281/zenodo.24617751) preserves the earlier edition. [Classroom guide and player sheets](teaching/README.md) · [Research library](../research/arcade/README.md)
