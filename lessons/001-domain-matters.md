# A correct answer needs the correct domain

Consider two simultaneous equations:

\[
2x+3y=7,\qquad -x+4y=-2.
\]

Multiplying the second equation by two and adding it to the first eliminates
x. We obtain 11y=3. Therefore y=3/11 and x=34/11. Substituting these values
into both original equations checks the calculation exactly. The nonzero
determinant, 11, establishes uniqueness over the rational numbers.

If x and y must be integers, the same elimination proves impossibility:
an integer multiple of 11 cannot equal 3. A computation has meaning within
its stated domain. The rational verifier in this repository answers the
rational question. It cannot silently certify an integer claim.

## A new exercise from the first result

Replace the right-hand sides by integers p and q:

\[
2x+3y=p,\qquad -x+4y=q.
\]

The same method gives y=(p+2q)/11 and x=(4p-3q)/11. Integer solutions
exist exactly when p+2q is divisible by 11. Necessity follows from 11y=p+2q.
For sufficiency, write p+2q=11k. Then y=k and x=4k-q are integers satisfying
both equations. This is a familiar elementary result, derived here as a
reusable lesson, with no novelty claim.

Try p=5 and q=3. Find the solution and check both equations. Then choose
your own pair p,q that fails the divisibility condition and explain why.
For an independent learning study, use fresh tasks prepared by a reviewer;
these public exercises are visible practice material.

## Reproduce and teach

The [original candidate and verification record](../research/agent-attempts/0001/record.md)
link the explanation to machine-readable evidence. Ask a learner to explain
why a rational solution can coexist with the absence of an integer solution,
then assess a fresh system with different coefficients. Record the rubric
and observed answer before claiming that the explanation improved learning.

Original educational prose: CC BY 4.0. AI assistance is disclosed in the
research record. This companion has not undergone journal peer review.
