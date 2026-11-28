# Nim Lab: when does removing fewer counters lose the game?

**Atlas Open Mathematics technical white paper, version 1.0 · 28 November 2026**  
Project directed by Albert Tan Sin Hon

## The experiment

Two players alternate. On each turn a player chooses one heap and removes any positive number of counters from it. The player who takes the last counter wins. Can a player tell whether they can force a win before making the first move? The arcade tests Charles L. Bouton's classical binary criterion through playable examples, an optimal opponent and a calculator for comparing legal moves. A winning position here means that the player **about to move** can force victory against every reply. [Play the worked example](https://alberttansinhon.com/math-arcade/#play/nim/0/7)

## A calculation that settles the outcome

Write each heap size $h_i$ in binary. In each binary column keep the parity of its ones, giving the bitwise exclusive OR, or nim-sum, $S=h_1\oplus\cdots\oplus h_n$. A position is losing precisely when $S=0$. Two observations give a proof for any finite number of heaps.

1. From zero, reducing a heap $h$ to $k<h$ changes the sum to $S'=0\oplus h\oplus k$. Since $h$ and $k$ differ in at least one bit, $S'\ne0$.
2. From non-zero $S$, consider its most significant one-bit. At least one heap $h$ has a one in that column. Set $k=h\oplus S$. All more significant bits stay the same and the chosen bit changes from one to zero, so $k<h$. Reducing that heap to $k$ brings the nim-sum to $S'=S\oplus h\oplus (h\oplus S)=0$.

The empty board has sum zero and offers no move. Every move decreases the total, so induction on the number of counters completes the proof. Each move from zero passes a winning position to the opponent. From a non-zero position at least one move passes a losing one. Bouton presented the binary strategy for three heaps and noted its extension to any number of piles. [Original article, pp. 35–39](https://sites.ualberta.ca/~hayward/cgt/asn/bouton1901.pdf)

## Reproduce two competing predictions

Warm-up seed 7 opens with heaps A, B and C of sizes $1,1,6$. Their nim-sum is $001\oplus001\oplus110=110$ in binary, or 6. Before playing, predict which move gives the opponent a losing position. Open **Compare moves using binary** to test both candidates without altering the board. [Replay seed 7](https://alberttansinhon.com/math-arcade/#play/nim/0/7)

| Your first move | Heaps left | Nim-sum | Consequence under perfect play |
| --- | --- | ---: | --- |
| Take two from C | $(1,1,4)$ | 4 | The opponent can empty C and leave you $(1,1,0)$. |
| Take six from C | $(1,1,0)$ | 0 | The opponent must empty A or B. You take the last counter from the other heap. |

**A further investigation.** How many distinct winning moves can one position offer? Each heap that has a one at the most significant one-bit of $S$ admits exactly one winning reduction, to $h\oplus S$. For every other heap that proposed value is larger than the original heap. Since the distinguished column has odd parity, the number of winning moves is odd whenever $S\ne0$. Try $(3,3,3)$ by hand. There are three winning first moves, one for each labelled heap. In contrast, $(2,2,2,2)$ has eight legal moves and zero winning moves.

## What the arcade and checks establish

Warm-up starts with three heaps of at most six counters and always gives the first player a winning position. Tricky uses four heaps of at most seven counters. Expert uses five of at most fifteen. At the latter two levels an unsigned integer seed divisible by four deliberately produces a zero nim-sum. Other seeds can also produce zero. The opening is deterministic for a given level and seed, and different seeds can share an opening. On a losing opening, switch seats to practise the second player's strategy. Atlas takes a winning move whenever one exists. When all moves lose against perfect play, it removes one counter from the first non-empty heap. [Game and public calculation functions](https://alberttansinhon.com/math-arcade/nim.mjs)

The independent check defines a position as winning if **any** legal move gives the next player a losing position. It enumerates reductions directly and memoises that recurrence, starting with the empty position as losing. The comparison covers all 512 labelled three-heap positions with entries 0–7, all 1,296 four-heap positions with entries 0–5 and all 1,024 five-heap positions with entries 0–3. In these **2,832 positions**, the recurrence agreed with the nim-sum outcome and Atlas chose a legal outcome-optimal move wherever a move existed. The finite check tests the software. The induction establishes the general mathematical result. [Atlas Open Mathematics](https://github.com/Albertito-AI/atlas-open-mathematics)

## Primary reference

Charles L. Bouton. “Nim, A Game with a Complete Mathematical Theory.” *Annals of Mathematics*, second series, vol. 3, 1901–1902, pp. 35–39. [DOI 10.2307/1967631](https://doi.org/10.2307/1967631) · [Scanned article](https://sites.ualberta.ca/~hayward/cgt/asn/bouton1901.pdf)
