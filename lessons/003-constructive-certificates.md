# Construct a solution, then check it

The [previous lesson](002-integer-feasibility.md) explained when a divisibility test works. This lesson shows how to build a checkable answer.

Consider ax + by = p and cx + dy = q, with integer data and D = ad − bc nonzero. Suppose the greatest common divisor of a and c is 1. Find integers u,v such that ua + vc = 1. When D divides aq − cp, put

$$
k=(aq-cp)/D,\quad r=p-bk,\quad s=q-dk,\quad x=ur+vs,\quad y=k.
$$

The identity as = cr gives ax = r and cx = s. Thus this construction satisfies both original equations. Substituting the result provides a separate check on arithmetic mistakes in its construction.

For 2x + y = 5 and 3x + 2y = 8, the determinant is 1. Choose u = −1,v = 1. Then k = 1,r = 4,s = 6, and x = 2,y = 1. Substitution gives 5 and 8 exactly. Neither first-column entry needs to be 1: their greatest common divisor is what matters.

Now consider 2x + y = 1 and 4x + 3y = 2. The determinant is 2 and the y-numerator vanishes, yet the unique rational solution is (1/2,0). Here the first-column greatest common divisor is 2. Passing one divisibility test cannot certify a pair of whole quantities.

## Public exercises

1. Use u = 1,v = 1 to solve −2x + y = −1 and 3x + y = 4 by the construction. Check both equations.
2. For 2x + y = 1 and 4x + 2y = 2, explain why dividing by the determinant fails. Describe the integer solutions directly.
3. If variables represent numbers of indivisible batches, what must be checked after integrality?

Answers: (1) D = −5, k = 1,r = −2,s = 3, giving (x,y) = (1,1). Both equations hold. (2) D = 0; the second equation is twice the first. For any integer t, x = t,y = 1 − 2t is a solution. (3) Check nonnegativity and any capacity or other operational constraints. An integer solution alone does not establish practical feasibility.

The [research experiment](../research/agent-attempts/0003/record.md) constructs and checks many finite examples, including negative determinants and zero entries. Its certificates are inspectable. Its sample size does not prove the universal result or demonstrate that someone learned from this explanation. Formalisation of the general theorem remains pending. These are public practice exercises, not unseen evaluation cases.

Prepared with AI assistance. Established mathematics, with no novelty claim. Original educational content: CC BY 4.0 under [the project content licence](../LICENSE-CONTENT.md).
