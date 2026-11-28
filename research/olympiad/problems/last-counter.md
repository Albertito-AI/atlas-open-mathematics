# The Last Counter

**Invariants · Ascent · Untimed**

Put eight counters on one bench. Spend two to send one to the next bench. Can you make seven trades? Can you predict exactly which positions are reachable on any ring?

[Try this problem](https://alberttansinhon.com/math-arcade/olympiad/#last-counter) · [Play on GitHub Pages](https://albertito-ai.github.io/Albertito-AI/math-arcade/olympiad/#last-counter) · [Proof collection](../README.md)

## Problem

Arrange n benches in a clockwise ring, where n ≥ 2. A position lists a nonnegative integer number of counters at each bench. A trade at a bench removes two of its counters and puts one counter at the next bench. A bench needs at least two counters to trade. After the last bench comes the first.

Given any starting position x and proposed finishing position y on the same labelled ring, find a necessary and sufficient test for reaching y from x. Your test must use the two lists of numbers without searching through possible orders of trades. Prove both directions, including the case of an empty target. You may stop at any time or make zero trades.

## Staged hints

1. A trade has a direction. How could multiplying the counts at successive benches by 1, 2, 4, 8, … make a trade invisible? What happens at the wrap from the last bench to the first?

2. Label the benches 0 through n − 1. Let f[i] count the trades at i. A bench spends twice its own trade count and receives the previous bench’s trade count. Try determining the last trade count first.

3. A list of nonnegative trade counts balances the books. You still have to prove the counters can be spent in a legal order. What happens if you run the proposed trades backwards, starting with y?

4. In reverse, trade i needs one counter at bench i + 1. If trade i is still owed but bench i + 1 is empty, what does the balance equation at i + 1 imply about the reverse trades still owed there? Follow that implication around the ring.

## Checkpoints and answers

### Checkpoint 1

Three benches A, B, C start at (8, 0, 0). What is the greatest number of trades you can make?

**Answer.** 7

Trade four times at A, twice at B and once at C. One counter returns to A. Each trade reduces the total by one and leaves at least one counter, so seven is the maximum.

### Checkpoint 2

Four benches A, B, C, D start at (15, 0, 0, 0). Play until no trade is legal. How many counters remain?

**Answer.** 4

Give counters at A, B, C and D weights 1, 2, 4 and 8. Trades at A, B and C preserve total weight. A first trade at D would need weight at least 16, but the total before it would still be 15. At the end each bench holds at most one counter, and all four weights are needed to make 15.

## Worked proof

### 1. Count the trades across the last edge

Number the benches 0 through n − 1. Give a counter at bench i weight 2ⁱ and write W(z) for the sum of these weights in position z. A forward trade at any bench except the last preserves W. At the last bench it spends weight 2ⁿ and creates weight 1. Thus its trade count must be f[n − 1] = (W(x) − W(y))/(2ⁿ − 1).

### 2. Recover a unique candidate

Set f[n − 1] to that quotient. For i decreasing from n − 1 to 1, compute f[i − 1] = y[i] − x[i] + 2f[i]. These are the balance equations y[i] = x[i] − 2f[i] + f[i − 1]. The equation for bench 0 also holds, with f[−1] interpreted as f[n − 1]. Indeed, the predicted final position from these counts has weight W(x) − (2ⁿ − 1)f[n − 1] = W(y). It already agrees with y on benches 1 through n − 1, so it agrees on bench 0 as well.

### 3. State the test

An empty target is reachable exactly when the start is empty. Every actual trade puts a counter on the next bench. For a nonempty target, accept exactly when every candidate f[i] is a nonnegative integer. Any legal play has these counts by the preceding equations, proving necessity.

### 4. Construct a legal order backwards

Start at z = y with r[i] = f[i] reverse trades still owed at each bench. A reverse trade of type i takes one counter from bench i + 1 and puts two at i. Perform any owed reverse trade whose source holds a counter, then decrease its r[i] by one. Throughout, x[j] = z[j] + 2r[j] − r[j − 1], with indices read around the ring. If some r[i] > 0 and no owed trade is legal, then z[i + 1] = 0. Applying the equation at i + 1 gives 2r[i + 1] = x[i + 1] + r[i] > 0. The same reasoning goes all the way around the ring. Every reverse type is owed and every bench is empty. Yet y began nonempty and each reverse trade increases the total by one. This contradiction guarantees a legal move until all debts vanish. The equations then give z = x. Read the moves in reverse order to obtain legal forward play from x to y.

## Proof rubric

- Choose weights that identify the exact number of trades from the last bench to the first.

- Derive all remaining trade counts, justify the equation at the first bench and test for nonnegative integers.

- Settle the empty target separately and prove that any accepted nonempty target has a legal sequence of trades.

## Transfer exercise

Change the price to three counters for one at the next bench. On a four-bench ring A, B, C, D, start with counters only at A. Finish with exactly two at B and one at D. Every bench must have traded at least once. What is the smallest possible starting pile?

**Answer.** 113

Use weights 1, 3, 9 and 27. The target weighs 33. A trade at D decreases weight by 80, and trades elsewhere preserve it. At least one trade at D forces a starting pile of at least 113. From 113, trade 37 times at A, 12 at B, 4 at C, once at D and once more at A. The successive positions are (2, 37, 0, 0), (2, 1, 12, 0), (2, 1, 0, 4), (3, 1, 0, 1) and (0, 2, 0, 1).

## Application: Which ticket bundle can the club promise?

A games club is trying a three-colour ticket exchange. Two red tickets buy one blue, two blue buy one gold, and two gold buy one red. A visitor has eight red tickets. The organiser wants to advertise one of two four-ticket bundles.

**Decision question.** Which bundle can the visitor obtain without borrowing tickets: two red, one blue and one gold, or two red and two blue? Predict whether either, both or neither is possible.

### Worked model

The first bundle is possible. Make three red exchanges to get two red and three blue. Exchange two of those blue for one gold. The visitor now has two red, one blue and one gold.

Give red, blue and gold tickets weights 1, 2 and 4. The first two exchanges preserve weight, and a gold exchange reduces weight by 7. The starting weight is 8. The second bundle weighs 6, a reduction of 2, so no legal exchange sequence can produce it.

**Model limits.** The conclusion depends on the club enforcing the three rates exactly. A free ticket, a reverse exchange or a loan changes which promises it can keep.

**Try the model.** Use three labelled cups and paper tickets. Start with eight red, record the counts after each trade, and check the weight after each step. Repeat from nine red and try to build the two advertised bundles again.

## Further investigation

Let the price of a trade vary from bench to bench: on successive benches require 2, 3 and 2 counters to send one onwards. Find weights that stay unchanged at the first two benches. Enumerate small starting positions and look for a reachability test. Which part of your argument still works for an arbitrary cyclic list of integer prices at least two?

## Provenance and verification

Atlas Open Mathematics, directed by Albert Tan Sin Hon. Prepared with AI assistance. These exercises were prepared for this programme using established mathematics. The collection makes no claim of first discovery or official contest provenance.

Designed for the Atlas Math Olympiad.

The worked arguments support the general conclusions. The executable checks provide separate evidence for specified finite cases. The challenge bands are editorial judgements and have not been calibrated against human contest performance. [Reproduce the checks and inspect their scope](../README.md#verification).

Edition 1.0.0, 2026-11-28. [Edition DOI](https://doi.org/10.5281/zenodo.24620475) · [Project educational licence](../../../LICENSE-CONTENT.md) · [Code licence](../../../LICENSE)
