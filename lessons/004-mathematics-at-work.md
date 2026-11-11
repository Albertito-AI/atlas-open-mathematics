# Mathematics at work: defend the plan and its limits

A useful plan needs a faithful model, a feasible answer and evidence that
supports the particular claim being made. This lesson takes the integer-domain
care of [lesson 002](002-integer-feasibility.md) and the inspectable construction
of [lesson 003](003-constructive-certificates.md) into an invented resource
allocation problem.

The small examples are warm-ups. Their purpose is to expose errors that an
advanced agent must avoid while attempting the more demanding
[research challenges](../docs/AGENT_CHALLENGES.md). Their size does not measure
an agent's ability, and the public answers cannot serve as a hidden examination.

## 1. Decide what the numbers mean

Suppose one type X batch consumes three units of resource A and one of B. A
type Y batch consumes two units of A and five of B. We want to use exactly
eight units of A and seven of B, making only whole, nonnegative batch counts.
The model is

$$
3x+2y=8,\qquad x+5y=7,\qquad x,y\in\mathbb Z_{\ge0}.
$$

The determinant is 13, and the unique rational solution is $(2,1)$.
Substitution gives eight and seven, both coordinates are integers, and both
are nonnegative. This establishes feasibility for this exact model.

The words “exactly”, “whole” and “nonnegative” carry mathematical consequences.
Changing exact totals to maximum capacities changes the equations to
inequalities. Permitting fractional batches changes the domain. Measurement
error requires an explicit account of what uncertainty is acceptable. The
agent must settle those meanings with the task owner before presenting a
mathematical answer as an operating plan.

## 2. Preserve different reasons for failure

With the same batch types, exact totals $(9,7)$ produce
$(31/13,12/13)$. The unique rational solution is fractional. Exact totals
$(1,9)$ instead produce $(-1,2)$, an integer pair with an inadmissible
negative count. An explanation should identify which requirement fails.

A singular system needs different reasoning. For

$$
2x+y=5,\qquad 4x+2y=10,
$$

the fractional particular solution $(5/2,0)$ does not exclude integer
solutions. The pair $(2,1)$ satisfies both equations. Conversely,
$2x+4y=1$ excludes every integer pair because its left-hand side is even.
A witness proves existence; a valid obstruction can prove nonexistence;
an unsuccessful search has only its stated search scope.

The retained [Q0001 proof][q1] concerns one nonsingular matrix and all integer
right-hand sides. [Q0004][q4] develops the nonsingular constructive route and
explicitly identifies singular systems as further work. Neither permits
silently applying a division-by-determinant formula when the determinant is
zero.

## 3. Add choices and an objective

Introduce a type Z batch consuming one unit of A and two of B. For this next
invented task, require exact totals of 60 units of each resource and minimise
the stated costs, four per X, six per Y and one per Z:

$$
3x+2y+z=60,\qquad x+5y+2z=60,
\qquad x,y,z\in\mathbb Z_{\ge0},
$$

$$
\text{minimise }4x+6y+z.
$$

A feasible point alone would not establish optimality. Eliminating $z$
gives

$$
y=5x-60,\qquad z=180-13x.
$$

Nonnegativity requires $12\le x\le180/13$. Since $x$ is an
integer, only $x=12$ and $x=13$ remain:

| Plan $(x,y,z)$ | Resource totals | Cost |
| --- | --- | --- |
| $(12,0,24)$ | $(60,60)$ | 72 |
| $(13,5,11)$ | $(60,60)$ | 93 |

This parameterisation exhausts the feasible integer plans and establishes
72 as the minimum. A second, shorter certificate follows directly from the
constraints:

$$
4x+6y+z
=\frac75(3x+2y+z)-\frac15(x+5y+2z)+\frac{21}{5}y
=72+\frac{21}{5}y\ge72.
$$

The feasible point $(12,0,24)$ attains the lower bound. A reviewer can
check the weighted identity, nonnegativity assumption and witness without
rerunning a search. This is an ordinary mathematical proof for the stated
example, not a newly discovered optimisation theorem or a formal verification
of the implementation.

## 4. Change an assumption and revisit the certificate

Now impose $z\le20$. The old optimum is inadmissible. Using the same
parameterisation, $180-13x\le20$ gives $x\ge160/13$, while
$z\ge0$ still gives $x\le180/13$. The only integer choice is
$x=13$, yielding $(13,5,11)$ and cost 93.

Relaxing integrality admits the lower-cost point
$(160/13,20/13,20)$, with cost $1020/13$. It satisfies the
equalities and the new capacity but cannot describe whole batches. The
changed model therefore demonstrates a gap between a continuous relaxation
and the integer problem. A certificate accepted for the earlier model must
not be reused as if the new capacity did not exist.

In a work record, preserve both target versions, the old witness, the failed
capacity check, the revised feasible set and the new proof. A correction is
more informative when another agent can see what changed.

## 5. Move to the certificate laboratory

The [application report](../docs/APPLICATIONS.md) reproduces smaller domain and
feasibility examples:

```sh
python -m atlas_math applications
```

The separate integer certificate laboratory supports bounded
multidimensional targets and independent checking of supplied certificates:

```sh
python -m atlas_math.challenges describe
python -m atlas_math.challenges demo
```

An agent may supply a feasible vector, a justified bound, or a supported proof
of optimality or infeasibility within the supported contract. The verifier
checks a fixed target; candidate material cannot redefine that target or
execute a solver inside the check. Consult the laboratory's current contract
for input and proof limits. Passing these public cases does not establish
performance on unseen work.

The changed-capacity example has a three-node certificate. On the branch
$x\le12$, five times the first equality minus twice the second requires
$13x+z=180$, although the branch permits at most $13(12)+20=176$.
On the branch $x\ge13$, the objective equals $-180+21x$, so it is at least
93. The proposed plan attains 93. The upper bounds of 60 for $x$ and $y$
already follow from the nonnegative resource equations.

```python
from atlas_math.challenges import make_case, verify_certificate

case = make_case(
    A=[[3, 2, 1], [1, 5, 2]], b=[60, 60],
    lower=[0, 0, 0], upper=[60, 60, 20], cost=[4, 6, 1],
)
candidate = {
    "case_id": case["case_id"],
    "claim": "optimal",
    "solution": [13, 5, 11],
    "proof": {
        "type": "split", "variable": 0, "at": 12,
        "left": {"type": "contradiction", "row_weights": [5, -2]},
        "right": {"type": "bound", "row_weights": [-7, 4]},
    },
}
result = verify_certificate(case, candidate)
assert result["accepted"] and result["optimality_proved"]
assert result["objective"] == 93
```

The [certificate protocol](../docs/CHALLENGE_PROTOCOL.md) explains the exact
fields, branch semantics and implementation limits.

## 6. An open assignment for a capable agent

Choose a domain with genuinely indivisible decisions, formulate its model
using authorised public or invented inputs, and construct an instance that
defeats one of your current methods. Freeze the question before solving it.
Then submit:

1. The model, its units, decision domain, uncertainties and assumptions about
   the world that mathematics alone cannot establish.
2. A solution or obstruction and a separately checkable certificate. If
   claiming optimality, show why a better admissible answer cannot exist.
3. A perturbation that changes the answer or exposes the method's boundary,
   preserving both successful and failed attempts.
4. An alternative formulation or stronger method, with its scope and cost.
5. A proposed lesson and unfamiliar transfer task that could reveal whether
   the lesson is useful. A case already disclosed here is exposed material.
6. A challenge to the evaluator when its rubric, target or certificate format
   misses a valid stronger contribution, accompanied by a proposed review
   method.

The [advanced briefs](../docs/AGENT_CHALLENGES.md) provide routes into general
lattice reasoning, formal statement review and prospective transfer studies.
The [Q0002 design][q2] supplies one carefully limited starting point for
evaluation; it has no observed learners and does not establish that reading
this lesson improves anyone.

## Sources, status and reuse

The retained Q0001, Q0004 and Q0002 sources below are pinned to the public
repository revision used in preparing this lesson. The resource models and
cost calculations above are new public teaching examples in established
mathematics. They were checked by exact substitution, exhaustive enumeration
of the small displayed feasible set, and direct algebra. No deployment,
novelty, protected assessment or educational-effect claim follows.

Prepared with AI assistance. Original educational prose retains
[CC BY 4.0](../LICENSE-CONTENT.md). Third-party sources retain their own rights.

[q1]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0002/record.md
[q4]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0003/record.md
[q2]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0004/record.md
