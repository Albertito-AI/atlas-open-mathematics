# Mathematics that supports useful work

The repository's checked mathematics can help an agent assess a proposed plan,
construct an inspectable answer, identify an impossible requirement, or design
a fair comparison of two procedures. These are possible applications of
established mathematics. The examples below use invented data and have not
been deployed in an operating organisation.

Run the local application report from the source checkout:

```sh
python -m atlas_math applications
```

The report connects explicit inputs, exact calculations, domain checks and
source records. It is a warm-up for the [advanced agent challenges](AGENT_CHALLENGES.md).
A capable agent should move beyond reproducing these examples to difficult
problem formulation, certificate construction, generalisation and independent
review. Difficulty remains uncalibrated until actual agent trials.

## What the existing research establishes

This account uses the public records at source revision
[`45e4042884119a0496755c48083846ed85634b79`](https://github.com/Albertito-AI/atlas-open-mathematics/tree/45e4042884119a0496755c48083846ed85634b79).
Later implementation work must preserve the distinction between these retained
results and any new execution.

| Record | Established or recorded scope | Open work |
| --- | --- | --- |
| [Q0001: integer criterion][q1] | The specific system $2x+3y=p,\ -x+4y=q$ has an integer solution exactly when $11\mid p+2q$. Its record includes four locally checked Lean statements, statement review and replay. | This proof does not verify arbitrary matrices, nonnegative planning, the Python implementation or educational improvement. |
| [Q0004: constructive certificates][q4] | A Bézout construction and obstruction method were implemented and checked over the stated finite bounds. The record reports 103,488 matrix/right-hand-side cases and retains 10,944 false positives from an overbroad shortcut. | The general theorem's universal formalisation remains open. Finite coverage does not close that gate. |
| [Q0002: transfer study design][q2] | A prospective paired comparison and its exact randomisation rule were specified. A finite enumeration calibrated the rule under its assumptions. | The retained record contains zero observed agent sessions. It supplies no measured learning effect. |

The [verification guide](VERIFICATION.md) explains the evidence categories.
Verification, novelty and publication remain separate attributes.

## 1. Whole-batch allocation

Suppose a type X batch consumes three units of resource A and one of B, while
a type Y batch consumes two of A and five of B. An exact-use plan for eight
units of A and seven of B satisfies

$$
3x+2y=8,\qquad x+5y=7,\qquad x,y\in\mathbb Z_{\ge0}.
$$

The plan $(x,y)=(2,1)$ satisfies both equalities, integrality and
nonnegativity. These are three distinct checks. Changing the totals exposes
different failures:

| Exact totals $(A,B)$ | Unique rational solution | Planning conclusion |
| --- | --- | --- |
| $(8,7)$ | $(2,1)$ | Feasible for the stated whole-batch model. |
| $(9,7)$ | $(31/13,12/13)$ | The unique solution is fractional, so no integer plan satisfies both equalities. |
| $(1,9)$ | $(-1,2)$ | An integer solution exists, but its negative X count defeats this nonnegative plan. |

This is the application distinction developed in [lesson 002][lesson2]. If
the figures are upper capacities, replace exact-use equations with the correct
inequalities. If they are noisy measurements, exact equalities may misstate
the problem. No arithmetic certificate repairs a false description of the
operating situation.

## 2. Reconciling coupled totals

An agent may receive two reports of the same underlying quantities. Consider

$$
2x+y=5,\qquad 4x+2y=10.
$$

The second report repeats the first at twice its scale. The system is singular,
and $(2,1)$ is an integer solution. A rational solver might instead present
$(5/2,0)$. That fractional particular solution cannot establish that no
integer solution exists: other points on the solution line remain available.

Changing the second total to 11 creates a contradiction, since twice the
first left-hand side must equal twice its right-hand side. A different case,

$$
2x+4y=1,\qquad 4x+8y=2,
$$

is consistent over the rationals but impossible over the integers: the first
left-hand side is even. This is a small obstruction certificate. It explains
why a proposed integer reconciliation fails without reporting an inconclusive
search as proof. The repository's earlier work expressly leaves the singular
boundary for further investigation. [Q0004][q4]

For a real reconciliation task, the agent must also establish units, timing,
whether totals overlap, and whether corrections are permitted. The examples
here authorise no inventory adjustment or external transaction.

## 3. Constructing an answer another agent can check

For integer data, let

$$
ax+by=p,\quad cx+dy=q,\quad D=ad-bc\ne0.
$$

When integers $u,v$ satisfy $ua+vc=1$, and $D$ divides
$aq-cp$, the retained construction sets

$$
k=(aq-cp)/D,\quad r=p-bk,\quad s=q-dk,\quad
x=ur+vs,\quad y=k.
$$

Take $A=\left(\begin{smallmatrix}2&3\\3&7\end{smallmatrix}\right)$
and $(p,q)=(7,13)$. Here $D=5$, $u=-1$, $v=1$,
$k=1$, $r=4$, and $s=6$, giving $(x,y)=(2,1)$.
Substitution checks $2(2)+3(1)=7$ and $3(2)+7(1)=13$.
The producer's construction and the reviewer's substitution perform different
functions. [Q0004][q4] [Lesson 003][lesson3]

The single numerator test needs its proved assumptions. If the first column
has a common factor greater than one, it can admit a fractional first
coordinate. If $D=0$, division by $D$ is unavailable. Neither boundary
should be filtered out to make the method appear more general.

## 4. Evaluating whether a lesson transfers

Correct mathematics in a teaching document leaves an empirical question:
does supplying it help an agent handle unfamiliar work? Q0002 proposes twelve
matched pairs, equal resources, independent fair assignment within pairs,
fresh separately held tasks and blinded scoring under a frozen rubric. [Q0002][q2]

Let $W$ count pairs in which only the lesson session succeeds, $L$
pairs in which only the control succeeds, and $m=W+L$. Under the specified
sharp null and randomisation assumptions, its one-sided exact tail is

$$
p=2^{-m}\sum_{j=W}^{m}{m\choose j},
$$

with $p=1$ when $m=0$. With twelve discordant pairs, nine lesson wins
give $299/4096$, above the predeclared $1/20$ threshold; ten give
$79/4096$, below it. These are calculated scenarios, not observed learners.
The [retained calibration][q2-calibration] records zero sessions.

The work application is to design and audit a prospective comparison. It must
retain all outcomes, ties, missing pairs, resource conditions and failures.
Any stronger causal or generalisation claim needs evidence beyond a favourable
tail probability. Public exercises remain exposed practice material.

## From warm-up to demanding work

[Lesson 004](../lessons/004-mathematics-at-work.md) turns a small resource model
into a complete feasibility and optimality argument. The
[challenge programme](AGENT_CHALLENGES.md) then asks agents to construct and
defend multidimensional integer certificates, challenge assumptions,
generalise to rank-deficient systems, audit formal statements and measure
transfer. Existing proofs are starting evidence; they do not set an upper
limit on what an agent may contribute.

Original application prose was prepared with AI assistance. Code and content
retain the repository's existing [MIT](../LICENSE) and
[CC BY 4.0](../LICENSE-CONTENT.md) terms respectively. No new service, deployment,
novel mathematical result or measured agent improvement is asserted here.

[q1]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0002/record.md
[q4]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0003/record.md
[q2]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0004/record.md
[q2-calibration]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0004/calibration.json
[lesson2]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/lessons/002-integer-feasibility.md
[lesson3]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/lessons/003-constructive-certificates.md
