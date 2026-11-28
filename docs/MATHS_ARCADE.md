# How short is the shortest solution?

**A technical white paper on the Atlas Maths Arcade**

Atlas Open Mathematics · Albert Tan Sin Hon, project director · 27 November 2026

Two players can clear the same board and disagree about whether either solution was the shortest. They can settle that question by exhibiting their moves and ruling out every shorter route. If every legal answer to an arithmetic puzzle takes three moves, what makes one hand harder than another?

Three browser games make these distinctions playable. Lattice Dash measures distance in a graph. Target Forge asks which numbers a set of tiles can express. Parity Lights asks how few switches must change. The three examples below are fixed puzzles. Open the links to challenge a friend on the same starting position, or use the checks at the end to reproduce the answers. [Play the Maths Arcade](https://alberttansinhon.com/math-arcade/)

Running these puzzles with a group? The companion guide gives each pair a one-page challenge sheet and the facilitator a separate answer and assessment key. [Print the 20-minute maths-circle guide](MATHS_ARCADE_CLUB_GUIDE.md)

## Lattice Dash and the three-jump lower bound

Each unblocked point is a vertex. Draw an edge whenever one of the four displayed jumps lands on another unblocked point inside the grid. A jump can pass over a blocked point. Each edge costs one move. The game searches outward in layers from the start. Layer zero contains the start, layer one contains its new neighbours, and induction places every reachable point in the layer numbered by its shortest distance. The first layer containing the goal gives the displayed par. [Implementation](https://alberttansinhon.com/math-arcade/lattice.mjs) · [Breadth-first paths, Sedgewick and Wayne, §4.1](https://algs4.cs.princeton.edu/41graph/BreadthFirstPaths.java.html)

**Try Warm-up, seed 2.** Start at $(1,3)$ and reach $(0,5)$. The four vectors are $(-1,1)$, $(-1,0)$ and their opposites. One legal route goes through $(0,4)$ and $(1,4)$ before reaching $(0,5)$. Three jumps suffice. For the lower bound, compare the vertical coordinates. Gaining two units of height in only two jumps would require two copies of $(-1,1)$. Their horizontal displacement would be $-2$, while the target requires $-1$. No two-jump route can work, and a single jump gains at most one vertical unit. [Play this position](https://alberttansinhon.com/math-arcade/#play/lattice/0/2)

## Why Target Forge needs a fraction

Start with four number tiles. Replace two distinct tiles by their sum, difference, product or quotient, consuming both. The order matters for subtraction and division, and division by zero is excluded. Each move reduces the tile count by one, so a completed expression has exactly three operations. The game keeps a reduced fraction for each intermediate value. The search can treat equal multisets of values as the same position, since the available arithmetic depends only on those values. It retains the expression for the player's chosen route.

**Try Expert, seed 0.** Make 55 from 7, 7, 8 and 9. Dividing 8 by one 7 gives $8/7$. Subtract that from 9 to obtain $55/7$. The other 7 completes the expression:

$$7\times\left(9-\frac{8}{7}\right)=55.$$

The expression proves that 55 is attainable. To check the stronger difficulty claim, repeat the finite search and discard any move whose result has denominator greater than one. For this hand that restriction removes every solution. A search over all ordered choices for the first combination, followed recursively by all choices for the remaining tiles, covers every legal expression. The hint system repeats the search after each move because an early choice can make a previously attainable target unreachable. [Play this hand](https://alberttansinhon.com/math-arcade/#play/forge/2/0) · [Implementation](https://alberttansinhon.com/math-arcade/forge.mjs)

## Press order in Parity Lights

A press flips its own light and its horizontal and vertical neighbours inside the board. Two presses of the same switch cancel. All presses commute, so a candidate answer is a set of pressed cells. If $b$ is the opening board, $p$ is a vector of press choices, and column $j$ of $A$ records the lights flipped by switch $j$, the final board is $b+Ap$ over the field of two elements. Clearing the board means $Ap=b$. A shortest solution uses a solution vector with the fewest ones. Anderson and Feil give a classical account of the linear-algebra model for *Lights Out*. [Anderson and Feil, *Mathematics Magazine* 71 (1998), 300–303](https://doi.org/10.1080/0025570X.1998.11996658)

**Try Warm-up, seed 7.** Rows are A–C, from the top, and columns are 1–3, from the left. The lit cells are A1, A2, B1, B3, C2 and C3. A1 flips the first three, and C3 flips the other three. Those presses clear all six lights. Any single press flips at most five lights, hence two is the minimum. [Play this board](https://alberttansinhon.com/math-arcade/#play/parity/0/7)

For an $n$ by $n$ board the game considers the $2^n$ choices of first-row presses. Once that row is fixed, a light still on in the top row forces a press immediately beneath it. Applying the same rule to each succeeding row leaves only the bottom row to check. Every successful first-row choice yields a solution. Taking the smallest press count among them gives the exact par. To generate a solvable puzzle, the game starts from an all-dark board and applies a set of presses. The same set clears that board, although another set might be shorter. [Implementation](https://alberttansinhon.com/math-arcade/parity.mjs)

## What was checked

The source checks ran on Linux using Node.js 24.22.3. The three game suites reported **nine tests passed, zero failed**. Each seeded count below contains three difficulty levels. These are finite software checks with public inputs. Learner performance and comparisons of human difficulty were outside their scope.

| Game | Checked inputs | Criterion |
| --- | --- | --- |
| Lattice Dash | 300 seeds per level, 900 boards | Independently enumerate reachable layers, compare the shortest distance with par and replay the returned jumps. |
| Target Forge | 120 seeds per level, 360 hands | Replay each solution exactly. Warm-up admits addition and multiplication alone. Tricky excludes that route but permits integer steps. Expert excludes every all-integer route. |
| Parity Lights | All 512 possible 3 × 3 openings and 400 seeded deals per level | Compare all 3 × 3 minima with a breadth-first traversal of board states. For the 1,200 generated deals, check solvability and the advertised par range. |

### Replay the three examples

The following commands download the three public game modules and check the worked positions. Run them in an empty directory with Node.js and curl. A hash identifies the exact source reviewed. Later site revisions may change the file hashes.

```sh
for game in lattice forge parity; do
  curl -fsSLo "$game.mjs" "https://alberttansinhon.com/math-arcade/$game.mjs" || exit 1
done
sha256sum lattice.mjs forge.mjs parity.mjs
node --input-type=module <<'JS'
import assert from 'node:assert/strict';
import { makeBoard, shortestRoute, landing } from './lattice.mjs';
import { makeForge, initialTiles, findRoute } from './forge.mjs';
import { generate, applyPresses, minimumSolution, bitCount } from './parity.mjs';

const board = makeBoard(0, 2);
const jumps = shortestRoute(board);
assert.equal(jumps.length, 3);
assert.equal(jumps.reduce((at, move) => landing(board, at, move), board.start), board.goal);

const hand = makeForge(2, 0);
assert.deepEqual(hand, { numbers: [7, 7, 8, 9], target: 55 });
const tiles = initialTiles(hand.numbers);
assert.equal(findRoute(tiles, 55).length, 3);
assert.equal(findRoute(tiles, 55, { integerOnly: true }), null);

const lights = generate(0, 7);
assert.deepEqual(lights, { size: 3, board: 427, par: 2 });
const corners = (1 << 0) | (1 << 8);
assert.equal(applyPresses(3, lights.board, corners), 0);
assert.equal(bitCount(minimumSolution(3, lights.board)), 2);
console.log('Three worked positions verified.');
JS
```

| Reviewed module | SHA-256 |
| --- | --- |
| `lattice.mjs` | `000a40f9c197588171b2c5a5e7a43f91da68502e36db6669f278c4237fcf0250` |
| `forge.mjs` | `45750c0b97c9cc1098479fc516cbcf249f3a0f32fc56efa09fc6fe83378fe835` |
| `parity.mjs` | `c98c52af3dcc8ac7e3fd3cfe77d278c37565dcd399af0ed748a7b7e82ee3aeb6` |

The replay prints `Three worked positions verified.` The full construction check was run in the website source checkout with `node --test checks/arcade-lattice.test.mjs checks/arcade-forge.test.mjs checks/arcade-parity.test.mjs`.

## A challenge to pass on

Give a friend the Parity Lights board above, then add diagonal neighbours to the cells flipped by a press. Do the same two corner presses still work? List exactly which cells each press flips before looking at the answer.

<details>
<summary>Check the variant</summary>

Yes. Each corner now also flips B2. The centre is flipped twice and returns to its original state. A single press still cannot clear this particular board. Every switch on a 3 × 3 board with diagonal neighbours flips the centre, which starts dark. Two presses remain optimal for this opening even though the earlier bound of five lights per press no longer applies.

</details>

Have a variant whose answer changes, or a shorter proof for one of the featured boards? Share the game, level, seed, changed rule and enough moves or reasoning for someone else to check. [Propose a mathematical question](https://github.com/Albertito-AI/atlas-open-mathematics/issues/new?template=problem.yml) · [Suggest a teaching improvement](https://github.com/Albertito-AI/atlas-open-mathematics/issues/new?template=teaching.yml)

**Publication and credit.** Atlas Open Mathematics project white paper, version 1, issued as a public technical working note. Its mathematical content is an exposition of established methods. Verification consists of the specified finite checks and worked derivations. Codex (OpenAI, GPT-6) assisted with the software, drafting and execution of the checks. Original educational prose is available under the project's content licence. [CC BY 4.0 and attribution](../LICENSE-CONTENT.md)

## Teach these positions

Start with the paired [Lattice Dash](teaching/PLAYER_SHEETS.md#lattice-dash), [Target Forge](teaching/PLAYER_SHEETS.md#target-forge) or [Parity Lights](teaching/PLAYER_SHEETS.md#parity-lights) positions, then compare the [worked solutions and assessments](teaching/TEACHING_GUIDE.md). · [Public teaching hub](https://alberttansinhon.com/math-arcade/teaching/)
