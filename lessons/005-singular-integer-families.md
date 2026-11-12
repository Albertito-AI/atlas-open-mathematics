# When two equations describe one constraint

Suppose batches of two types consume 2 and 1 units of a resource, and a second
total counts exactly twice the same consumption. The equations 2x+y=5 and
4x+2y=10 are dependent. There is no unique plan. A rational solver may return
(5/2,0), but whole batches are still possible: (2,1) works.

Choose one nonzero equation, check the other agrees with it, then ask whether
the greatest common divisor of its coefficients divides its total. Here the
gcd is 1. From the particular solution (0,5), every integer solution is
(x,y)=(k,5-2k). Whole nonnegative batches require 0 <= k <= 2, leaving exactly
three plans: (0,5), (1,3), (2,1). Substitution checks every plan in both equations.
This is a synthetic explanation, not a deployed allocation service.

The order matters. A conflicting second total makes even rational solutions
impossible. An agreeing second total can still leave a divisibility obstruction.
For 2x+4y=1, the left side is even and the right side is odd. No integer plan
exists, although rational plans do. A zero matrix with zero totals imposes no
constraint at all; a nonzero total beside it makes the system inconsistent.

## Public exercises with answers

1. Classify 3x+6y=9 and x+2y=3. Answer: (3-2k,k) for every integer k;
   nonnegative plans correspond to k=0,1.
2. Replace the first total by 10. Answer: inconsistent even over the rationals,
   since three times the second equation would have total 9.
3. Classify 0x+0y=0 and -2x+4y=6. Answer: (-3+2k,k); nonnegative plans
   require k >= 2. The zero row must not be selected as the gcd equation.
4. Why is a fractional particular solution insufficient to rule out whole
   batches? Answer: another point in its null-direction family may be integral.
5. If both rows and both totals vanish, can one affine family z+k*w, with fixed
   integer vectors z,w and integer k, describe every integer pair? Answer: no;
   x and y are independently arbitrary integers. This does not exclude a
   non-affine enumeration of all integer pairs by a single integer.

The [research record](../research/agent-attempts/0005/record.md) supplies the full
argument, computational bounds and limitations. Checking these exercises is
practice; no human learning outcome has been measured. Prepared with OpenAI
Codex assistance under Albert Tan's direction. Known mathematics; CC BY 4.0.
