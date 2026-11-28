# Reversi Endgame Lab

**A reproducible study of mobility, forced passes and disc margin on an 8 × 8 board**

Atlas Open Mathematics · Maths Arcade technical paper · 28 November 2026

## Abstract

With three empty squares left, can two moves that each flip two discs lead to opposite results? In the first position below, White can win by six or lose by eight. The difference is whether Black gets another turn. A second position shows how a player facing a forced loss can still improve the margin by 26 discs. The arcade lets readers play both positions, inspect every legal alternative and repeat the analysis on seeded positions. The contribution is an implementation and a pair of reproducible teaching examples using established finite-game methods. [Play the three-square example](https://alberttansinhon.com/math-arcade/#play/reversi/0/7).

## Game and objective

Black moves first from the usual four central discs. A legal placement must enclose at least one uninterrupted line of opposing discs between the new disc and an existing friendly disc. All discs bracketed in any of the eight directions flip. Passing is compulsory only when a player has no legal placement. Play ends when neither colour can move, even if squares remain empty. These are the World Othello Federation rules. [Official rules, especially rules 1, 2, 6 and 8](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english).

The arcade evaluates the terminal margin as the number of the player's discs minus the number of the opponent's discs. Empty squares contribute zero. Players maximise this signed margin. Thus two wins, or two losses, can have different values. The challenge is complete when the player achieves the opening position's best guaranteed margin against a computer that also maximises its own margin. A forced draw has a target of zero. A forced loss has a negative target.

## Exact finite search

Let $P$ be a board, $s$ the colour to act, $M(P,s)$ its set of legal squares and $P_m$ the board after placing at $m$ and flipping every bracketed disc. Let $D(P,s)$ be the current disc difference from the viewpoint of $s$. The implementation evaluates three exhaustive cases.

| Condition | Value $V(P,s)$ | Reason |
| --- | --- | --- |
| Neither side can move | $D(P,s)$ | The score is final. |
| Only the other side can move | $-V(P,-s)$ | A pass changes the perspective while leaving the board intact. |
| The player can move | $\max_{m\in M(P,s)}[-V(P_m,-s)]$ | Choose the move giving the highest guaranteed margin. |

After a pass the other side has a placement by definition. Every placement consumes an empty square, so recursion terminates. At a terminal node the formula gives the physical disc count. Moving backwards through the finite tree, negating an opponent's exact value expresses it in the current player's units. Maximising these values therefore yields an exact value at the parent. This is the zero-sum negamax form of minimax. The engine evaluates every continuation to its terminal score. It uses row order, then column order, to break equal-score ties when the computer moves. [UC Berkeley CS 188, section 3.2, “Minimax”](https://inst.eecs.berkeley.edu/~cs188/textbook/games/minimax.html).

If $e$ squares are empty, each sequence of $k$ placements is drawn without replacement from these squares. There are at most $e!/(e-k)!$ such sequences. For any sequence of placements, the compulsory passes are determined by its board states. The tree of placements has at most $\sum_{k=0}^{e} e!/(e-k)!$ nodes before counting pass nodes. At six empty squares this bound is 1,957. Illegal sequences and early terminal positions reduce it. This small search horizon permits full enumeration. The implementation makes no claim about its performance from the initial four discs.

## Two replayable positions

In each table the final margin is from the human player's perspective, with optimal responses by both sides thereafter. Columns A to H run from left to right and row 1 is at the top.

**Three empty squares, seed 7, White to play.** All three placements flip the same number of discs immediately. [Replay the position](https://alberttansinhon.com/math-arcade/#play/reversi/0/7).

| White's move | Discs flipped now | Final White margin |
| --- | ---: | ---: |
| G2 | 2 | +6 |
| H7 | 2 | −8 |
| H8 | 2 | −8 |

After G2, Black must pass. White plays H7, Black passes again, and White plays H8. White finishes with 35 discs and Black with 29. Playing a corner immediately at H8 would instead give Black a winning continuation. The move comparison in the game lets the reader trace that branch.

**Six empty squares, seed 7, Black to play.** Two legal moves are available. [Replay the position](https://alberttansinhon.com/math-arcade/#play/reversi/2/7).

| Black's move | Discs flipped now | Final Black margin |
| --- | ---: | ---: |
| A8 | 5 | −6 |
| B7 | 8 | −32 |

A rule that selects the move with the most immediate flips chooses B7. Against perfect replies Black then loses by 32. A8 reduces the loss to six. The example establishes a counterexample to that greedy rule. For a transfer exercise, try the five-square position and rank all four legal moves by final margin before opening **Compare moves**. The predicted margins can be checked separately for every move. [Play the transfer exercise](https://alberttansinhon.com/math-arcade/#play/reversi/1/7).

## Generation, verification and limits

The generator starts from the standard opening with Black to play. A seeded pseudorandom sequence selects among legal placements and records every compulsory pass. The target empty-square counts are 3, 5 and 6. The first sampled position with at least two legal moves of different values is accepted. After twelve unsuccessful playouts, the code uses the same bounded search with a known working seed. This construction gives replayable, reachable positions and deliberately selects for a meaningful choice. It supplies a finite, biased sample. Positions can repeat across seeds.

The accompanying test independently represents the two colours as 64-bit sets, computes captures by masked bit shifts and evaluates the game tree using alternating maxima and minima of Black's absolute margin. The browser implementation instead stores individual square values, scans precomputed rays and changes perspective at each turn. [Implementation](../research/arcade/reversi.mjs) · [Independent checker and regression tests](../research/arcade/reversi.test.mjs).

From the repository root, use the module and checker in the same Git revision as this paper. The recorded run used Node.js 24.22.3 on Linux x86_64.

```sh
node --test research/arcade/reversi.test.mjs
```

All six test groups passed. For seeds 0 through 127 in each tier, all 384 recorded starting positions replayed from the standard opening, and each tier contained 128 distinct boards with side to move. The checker compared the exact score of every initial alternative for seeds 0 through 15 in all three tiers, covering 48 positions. Additional fixtures cover all eight flip directions, compulsory passes, early termination, a draw and the two examples above. These counts describe the tested inputs. The work records software verification and mathematical examples. Learner outcomes and expert playing strength have yet to be measured. This is a project technical paper with no external peer-review claim.
