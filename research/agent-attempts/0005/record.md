# Q0005: integer solutions at the singular boundary

12 November 2026. Work ID `ATLAS-MATH-RESEARCH:Q0005-AUDIT-20261112`.
Base source `8702e9b444a8bdd0eb84836b25f67fcff9d4a571`.
AI-assisted research account prepared with OpenAI Codex under Albert Tan's direction;
exact model identifier and token use unavailable. No new external spending.

## Frozen target and new contribution

For integer A = ((a,b),(c,d)) with ad = bc, classify all integer solutions
of A(x,y) = (p,q). The applications module already implements the construction.
This contribution adds its explicit completeness argument and a new exhaustive
audit, rather than claiming that implementation as new work. No solver,
verifier, acceptance policy or formal theorem is changed.

## Classification and argument

If A is zero, a solution exists exactly when p = q = 0; then every integer
pair is a solution. Otherwise choose a nonzero row (u,v) with total r, and
write the other row as (s,t) with total h. Rational consistency is equivalent
to uh = sr and vh = tr. Necessity follows by substitution and ut = vs.
For sufficiency, if u is nonzero, the other equation is s/u times the chosen
equation; uh = sr supplies its total. If u is zero, v is nonzero and the
same argument uses t/v and vh = tr. This covers a zero other row explicitly.

Put g = gcd(|u|,|v|) > 0. Under consistency, integer feasibility is equivalent
to g dividing r. Necessity follows because g divides ux + vy. For sufficiency,
choose integers alpha,beta with alpha*u + beta*v = g. Then
z = (alpha*r/g, beta*r/g) is an integer particular solution of both equations.
All integer solutions are exactly

$$z + k(v/g,-u/g),\qquad k\in\mathbb Z.$$

To prove completeness, put U = u/g, V = v/g. Differences (X,Y) of solutions
satisfy UX + VY = 0 and gcd(|U|,|V|) = 1. If U is nonzero, Euclid's lemma
gives U dividing Y; writing Y = -Uk yields X = Vk. If U = 0, then V = 1 or
-1, Y = 0 and X = Vk for an integer k. Negative and zero coefficients are
therefore included. The direction is nonzero, so every feasible rank-one
system has infinitely many integer solutions.

For nonnegative solutions, each coordinate z_i + k*w_i supplies a lower
bound ceil(-z_i/w_i) when w_i > 0, an upper bound floor(-z_i/w_i) when w_i < 0,
or the condition z_i >= 0 when w_i = 0. Intersect these integer bounds.
An empty intersection is infeasible; otherwise any integer in it is a witness.
This establishes the mathematical construction, not formal correctness of Python.

## Reproducible audit

Run `python research/agent-attempts/0005/audit.py` from the complete checkout.
The [captured output](evidence.json) records source hashes, bounds, counts and
an ordered-result digest. All 289 singular matrices with entries -3 through 3
are paired with all 49 right-hand sides in those bounds: 14,161 systems.
For each matrix, an independent oracle enumerates integer points in [-12,12]^2
by direct substitution, without calling the solver. The audit compares integer
and nonnegative feasibility, checks each returned family and obstruction, and
checks that every enumerated solution lies in the returned family.

Results: 12,528 rational inconsistencies; 256 rationally consistent systems
excluded by a row gcd; 1,377 integer-feasible systems, including the zero
system; 1,025 nonnegative-feasible systems. All 23,808 enumerated points in
rank-one solution sets belong to the returned integer family. The finite oracle
does not prove absence of a solution outside its search box; the separate
classification argument supplies that general reasoning. No mismatch was found.

## Failed shortcuts and scope

Determinant zero alone does not imply feasibility: x+y=1 and 2x+2y=3 conflict.
Rational consistency alone does not imply integer feasibility: 2x+4y=1 and
4x+8y=2 have rational solutions but no integer pair. A fractional particular
solution alone does not exclude integers: 2x+y=5, 4x+2y=10 has the rational
particular (5/2,0) and integer solution (2,1). These are counterexamples to
methods, not observed learner failures. Dividing by the determinant is
inapplicable here. Rejected routes remain documented rather than relabelled.

The accepted Opsbook `exact-substitution` rule, revision 1 in the
[retained manual](../../cycles/2026-11-09-2c92f02000c3/opsbook/MANUAL.md), is applied
to original equations and null directions. The gcd/domain check is explicit:
the rational verifier alone cannot certify integer infeasibility. No new
Opsbook instruction is promoted. Public practice is exposed, not a hidden test.

This is established linear Diophantine mathematics, with no novelty or
Millennium-status claim. Background is the integer normal-form material cited
in [attempt 0002](../0002/record.md); the argument above is self-contained.
No new Lean proof, model training or measured human/agent transfer occurred.
Q0004 formalisation and Q0002's independent execution manifest remain open.
The [teaching companion](../../../lessons/005-singular-integer-families.md)
contains exercises and a synthetic whole-batch interpretation.

Original code retains MIT and original prose CC BY 4.0. No third-party text,
private school material or confidential editorial records were copied.
Budget: one bounded finite audit (120 seconds per replay), local tests and
separate critical review. Verification evidence and review are recorded below.
Journal status: public working companion, not submitted or accepted. A future
educational article follows [JOURNAL_HANDOFF.md](../../../docs/JOURNAL_HANDOFF.md),
with private authorship declarations and independent editorial decisions.

Next question: for rank-one systems with integer box constraints and a linear
cost, derive endpoint optimality and independently check feasibility, optimality
and unboundedness certificates, including zero-cost directions. Existing lab
features must be reused and audited rather than rebuilt.

## Checks, review and correction history

Executed using Python 3.12.14. The 96 existing repository tests passed;
`python scripts/validate_repository.py` passed, and
`python scripts/replay_research.py` reproduced the three earlier retained
experiments exactly. No new research credit is assigned to those replays.

A separate critical-review agent replayed this audit with exit status 0,
empty standard error and exact JSON equality. Its independently implemented
augmented-row/gcd classification and point enumeration, without importing the
applications module, reproduced every reported count. It checked signed and
zero coefficients, the completeness argument, nonnegative bounds and unchanged
solver/verifier source. This is agent review, not external human peer review.

One teaching error was identified and corrected before the PR: exercise 5
initially said one parameter cannot describe all integer pairs. That is too
broad because a non-affine enumeration exists. It now asks specifically about
one affine family z+k*w, which cannot cover the two-dimensional integer lattice.
The original error and correction are retained here; no computation changed.
