# The Odd Parcel

**Atlas Math Olympiad mini-lab · Albert Tan Sin Hon, project director · 28 November 2026.** Prepared with AI assistance. The balance puzzle is a classical search problem. This companion develops its proof, a reproducible test and a practical modelling exercise. [Play the mini-lab](https://alberttansinhon.com/math-arcade/olympiad/odd-parcel/) · [Play on GitHub Pages](https://albertito-ai.github.io/Albertito-AI/math-arcade/olympiad/odd-parcel/) · [Olympiad collection](../README.md)

You have twelve sealed parcels and three inspections. Would you begin by weighing one parcel against another, or four against four? Both comparisons can give three readings. Only the second keeps a three-inspection guarantee.

## What an inspection tells you

There are $N \geq 1$ labelled parcels. Exactly one is heavier. Every other parcel has the same mass. A balance compares disjoint groups of equal size and reports left heavier, balanced or right heavier. An inspection is one such weighing. Naming the sole remaining candidate costs no inspection.

Put some of the remaining candidates on the left, an equal number on the right and leave the rest aside. A left tilt means the heavier parcel is on the left. A right tilt puts it on the right. Balance puts it among the parcels left aside. A branch containing zero candidates cannot occur. The game also allows cleared parcels on a pan. Such parcels can balance the total pan counts even when the two pans carry different numbers of suspects. The optimal worst-case construction below uses only current candidates.

In the game, a consistent adversary keeps a largest nonempty branch. Ties may be resolved either way for the proof. Along any play the candidate sets are nested, so any parcel in the last nonempty set would have produced every reading seen so far if it had been the heavier parcel from the outset. This tests how many candidates your move leaves on its largest branch. A poorly planned later move on a smaller branch could still make that branch slower overall.

## The exact guarantee

The fewest inspections sufficient in the worst case is

$$
D(N)=\min\{d\in\mathbb{Z}_{\geq0}:3^d\geq N\}=\lceil\log_3 N\rceil.
$$

**Lower bound.** Draw the strategy as a tree. Its next weighing can depend on every previous reading. Each node still has at most three children. A tree of depth at most $d$ has at most $3^d$ leaves, by induction on $d$. This also covers strategies that sometimes stop early. Each possible heavier parcel requires its own identifying leaf. Consequently $N\leq3^d$. Equivalently, whenever $m$ candidates remain, a largest branch contains at least $\lceil m/3\rceil$. No clever interpretation of a genuine balance reading can beat the leaf bound.

**Construction.** At a step with $m\geq2$ remaining candidates, use the following sizes. Only the two pans must have equal numbers.

| Candidates | Left pan | Right pan | Aside | Largest possible survivor set |
| --- | ---: | ---: | ---: | ---: |
| $m=3k$ | $k$ | $k$ | $k$ | $k$ |
| $m=3k+1$ | $k$ | $k$ | $k+1$ | $k+1$ |
| $m=3k+2$ | $k+1$ | $k+1$ | $k$ | $k+1$ |

Repeat within the indicated group. If $m\leq 3^d$ with $d\geq1$, every surviving group has at most $\lceil m/3\rceil\leq3^{d-1}$ candidates. Thus a budget of $d$ reduces to a budget of $d-1$ after one inspection. At $m=1$ stop, including when the initial input is $N=1$. For $m=2$, one parcel on each pan suffices and balance is impossible. Induction proves the upper bound. The same construction works with a fixed unknown heavier parcel and with every sequence of consistent largest-branch tie decisions.

| Inspection budget | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Maximum number of candidates guaranteed distinguishable | 1 | 3 | 9 | 27 | 81 | 243 |

## Twelve parcels and a poor first move

Two inspections have capacity nine, so twelve require at least three. Weigh four against four and leave four aside. Every reading leaves four. Of these, weigh one against one. A tilt identifies the culprit immediately. Balance leaves two, which can be separated in one final inspection. This attains the lower bound. If instead the opening weighs one against one, balance leaves ten. Two further inspections have only nine leaves, so that opening can require **four** inspections in total.

There is also a distinction between a guarantee and an average. With a **fixed, uniformly chosen culprit** under the four-against-four strategy, six of the twelve parcels are identified after two inspections and six after three. Its mean is $(6\times2+6\times3)/12=5/2$. This is the mean for that strategy and that distribution. The interactive adversary can keep a two-candidate branch at the second weighing and take the full three inspections.

## A decision at a packing bench

Suppose 24 sealed kits are meant to have equal gross mass. A packing record establishes that exactly one kit contains an extra 3 g washer. Decide whether three balance readings suffice before opening any kit. Under the equal-mass assumption, weigh eight kits against eight, leaving eight aside. From the surviving eight weigh three against three, leaving two. Up to three candidates now remain. One against one identifies the culprit, with balance identifying the third when there is one. Two readings cannot guarantee success because $24>9$. Three are sufficient because $24\leq27$.

Try to invalidate the procedure. Suppose the duplicate is on the right, but a nominally genuine kit on the left uses a carton that is 4 g heavier than the standard carton. With equal numbers on the two pans, the left side then outweighs the right by 1 g. Following the rule would discard the culprit. This is a counterexample to the **mass assumption** at the bench. Applying the guarantee would require establishing equal baseline masses and adequate balance sensitivity, or supplying and testing a different error model. The kit example is an illustrative calculation.

## Further investigation

What changes if the exceptional parcel might be either heavy or light? After weighing A against B, a left tilt is compatible with A being heavy or B being light. The old update rule would discard a feasible explanation. If the answer must identify **both the parcel and the sign**, there are $2N$ hypotheses. In the absence of any further information a necessary condition for a depth-$d$ strategy is $2N\leq3^d$. It does not follow that an equal-pan strategy attaining this capacity exists. For example, three readings can handle 14 known-heavier candidates, whereas three cannot identify both the parcel and the sign among 14 when $28>27$. Investigate the smaller cases by listing the hypotheses that survive each reading.

## Reproduce the finite checks

From the repository root, with Python 3.10 or later, run

```sh
python3 research/olympiad/labs/check_odd_parcel.py
```

The checker simulates the two pan masses using each possible fixed culprit for every $N$ from 1 through 100, a total of 5,050 cases. It separately tests every largest-branch tie sequence across those sizes, the depth distribution for twelve parcels, and the 4 g carton counterexample. Integer powers of three give the expected capacities. These finite checks accompany the induction above. [Read the checker](check_odd_parcel.py)

For classical background, Stanford CS103 presents the power-of-three case using induction. The three residue cases above cover every positive candidate count. [Stanford CS103 lecture slides](https://web.stanford.edu/class/archive/cs/cs103/cs103.1164/lectures/11/Small11.pdf)

Cite this companion using its title, Atlas Open Mathematics, Albert Tan Sin Hon as project director, and the GitHub commit permalink for the version consulted. The separate four-problem *Atlas Math Olympiad: Proof Edition*, version 1.0.0, has its own [Zenodo record](https://doi.org/10.5281/zenodo.24620475). The companion follows the [educational-text licence](../../../LICENSE-CONTENT.md) and its checker follows the [code licence](../../../LICENSE).
