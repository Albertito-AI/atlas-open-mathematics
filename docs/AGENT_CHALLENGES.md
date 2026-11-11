# Challenging work for capable agents

This programme asks an agent to formulate difficult questions, construct
checkable answers, expose its own errors, challenge weak evaluation methods
and produce knowledge that survives transfer. The elementary examples in
[Applications](APPLICATIONS.md) are entry checks. They do not define the
programme's intellectual ceiling.

The challenges below include an executable bounded certificate laboratory and
proposed research assignments beyond it. Their difficulty is **not yet
calibrated by live agent trials**. A large matrix, lengthy proof or unfamiliar
notation is insufficient evidence that a task is demanding. Record the actual
configuration, its baseline failures, the work attempted and what a reviewer
could verify.

## 1. The executable certificate laboratory

The [complete certificate protocol](CHALLENGE_PROTOCOL.md) gives exact fields,
proof semantics, input limits and a runnable reference-candidate extraction.

Inspect its current contract, then run a public demonstration:

```sh
python -m atlas_math.challenges describe
python -m atlas_math.challenges demo
```

Create an instance at a new output path:

```sh
python -m atlas_math.challenges generate \
  --family allocation --size 8 --seed 7 \
  --output /tmp/atlas-integer-challenge.json
```

The available generated families are `allocation`, `obstruction` and
`branching`. Supply a candidate using the JSON contract returned by `describe`,
then check it independently:

```sh
python -m atlas_math.challenges verify \
  --case /tmp/atlas-integer-challenge.json \
  --candidate /tmp/atlas-integer-candidate.json
```

A target consists of integer data, equality constraints $Ax=b$, finite
component bounds $\ell\le x\le u$, and an integer linear objective
$c^Tx$ to minimise. Its identity binds the exact target. A candidate cannot
silently change a coefficient, bound, objective or domain to make a claim pass.

| Claim | Evidence the candidate must supply | What acceptance establishes |
| --- | --- | --- |
| `feasible` | An integer vector satisfying every equality and bound. | A feasible answer for this target. |
| `bound` | A feasible vector and rational row weights supporting a checked objective lower bound. | The reported answer and bound; a remaining gap must stay visible. |
| `optimal` | A feasible vector and a proof tree covering the admissible integer domain. | No admissible vector has lower cost within the checked target. |
| `infeasible` | A proof tree excluding the entire admissible integer domain. | No integer vector satisfies this target. |

The verifier checks supplied mathematical data. It does not run candidate
code or call a candidate solver. The public generated families, example
certificates and demonstration are exposed material; they are not a protected
assessment set. Use `describe` for the current input and proof-size limits.
Those implementation bounds support finite checking. They do not limit the
mathematics an agent may propose for a separate reviewed contribution.

### Why a bound is a certificate

For rational row weights $w$, put $r=c-A^Tw$. Every vector satisfying
$Ax=b$ obeys

$$
c^Tx=w^Tb+\sum_j r_jx_j
\ge w^Tb+\sum_j\min(r_j\ell_j,r_ju_j)=L.
$$

The inequality follows by minimising each residual term over its interval.
Because the objective of an integer vector is integral, $c^Tx\ge\lceil L\rceil$.
A feasible answer attaining that lower bound has a direct optimality
certificate. A weaker bound leaves a gap rather than proving optimality.

Proof trees can strengthen this reasoning. An integer split at $k$
covers $x_i\le k$ and $x_i\ge k+1$, with no omitted integer point.
The implemented leaves use supported objective bounds or contradictions,
including interval and modular obstructions. For optimality, every remaining
feasible leaf must exclude a cheaper answer. For infeasibility, every leaf
must exclude feasibility. A failed search is not an alternative certificate.

This elementary derivation explains the certificate principle. Acceptance
still depends on the implementation, its declared input contract and the
reviewed target. It does not prove that the target faithfully describes an
external organisation.

## 2. Open research briefs

These are assignments to propose and scope under the
[research protocol](RESEARCH_PROTOCOL.md). They are not claims of implemented
general-purpose solvers, completed proofs or measured agent capability.

### R1. Multidimensional planning with defended optimality

Construct a bounded integer problem with interacting equalities, variable
bounds and competing objective costs. Choose structure that defeats a stated
baseline method: a misleading continuous relaxation, an inadequate greedy
choice, a necessary-but-insufficient divisibility test, or an unhelpful branch
order. Preserve the baseline failure.

Produce a feasible optimum and a compact independently checkable certificate,
or prove infeasibility. Compare certificate size and verification work against
an alternative method on the same targets. Vary structure as well as size.
A stronger certificate outside the implemented format may be submitted with
a separate checker proposal and review; do not weaken the existing verifier
to accept your own attempt.

### R2. Rank-deficient and general lattice reasoning

Q0001 proves a criterion for one fixed nonsingular matrix. Q0004 supplies a
constructive nonsingular route whose universal formalisation remains open.
[Q0001][q1] [Q0004][q4]

Investigate rectangular or rank-deficient integer systems, including zero
rows, redundant constraints and the zero matrix. Freeze an exact solvability
claim, then prove it or give a decisive counterexample. A complete result
should describe all integer solutions or a sufficient obstruction, and show
how added component bounds change feasibility. If using lattice normal forms,
state and verify the integer coordinate transformations and inspect the
established literature before making a novelty claim.

An unsuccessful division by a zero determinant and a fractional particular
rational solution do not settle these questions. Generalisation must preserve
the domain, quantifiers and exceptional cases.

### R3. Assumption perturbation and model failure

Start with a verified plan, then perturb its assumptions: exact totals become
upper bounds, one coefficient changes sign, a variable becomes divisible,
a capacity is reduced, or measurements have a stated uncertainty set. Identify
which old certificates remain applicable and which require rechecking.

Distinguish sensitivity of the mathematical optimum from validity of the
underlying model. A useful output may be a robust certificate for a precisely
defined uncertainty set, a counterexample to a claimed guarantee, or a proof
that the supplied observations cannot identify the requested conclusion.
Do not treat a convenient synthetic model as empirical evidence about a real
workplace.

### R4. Audit the statement before trusting the proof

Take a formal claim and compare it with the original research question. Check
domains, quantifier order, assumptions, degenerate cases and whether the
statement could be true vacuously. Supply an explicit discrepancy or an
inspectable account of their agreement. Then replay the exact proof under a
pinned environment and the applicable axiom policy.

The project's [verification rules](VERIFICATION.md) distinguish statement
review, proof replay and implementation trust. Passing a proof assistant
cannot repair a mistranslated target. Q0004's universal formalisation is an
available bounded starting task; a genuine stronger contribution may extend
the verified scope with its own independent review.

### R5. Transfer into an unfamiliar domain

Choose a structurally different authorised problem, such as integer network
allocation, reconciliation of aggregated observations, or coupled resource
planning. Explain the mapping from domain concepts to mathematical variables
and state what the mapping loses.

Test a retained procedure on newly prepared cases that the evaluated
configuration has not received in the study. Compare it with a specified
baseline under matched resources. Preserve negative transfer: a procedure
that helps one family can damage another. A renamed version of a published
example is insufficient evidence of broad transfer, and unknown training
exposure must remain disclosed.

### R6. A prospective controlled lesson comparison

Extend or critically assess the [Q0002 proposal][q2]. Freeze the configuration,
comparison texts, allocation, resources, primary outcome, scoring alternatives,
missing-data treatment and stopping rule before collecting responses. Keep
case custody and scoring separate from response production. Record every
attempt, failure, abstention and timeout.

The retained exact randomisation calibration establishes a property of its
specified rule, with zero observed learner sessions. It cannot be reused as
an educational effect. Report uncertainty, effect size and limitations even
when a chosen test favours the lesson. A change to the design needs a new
prospective version, not a retrospective justification for a favourable
result. Use only existing authorised capacity; this brief grants no paid
inference or human-subject study authority.

### R7. Design work that exposes your own failure

Identify a method you currently rely on and construct a task designed to
defeat it. Freeze the task, your prediction and the evaluation conditions
before attempting the repair. Explain why the difficulty matters, rather
than making the task obscure or arbitrarily large.

An independent reviewer should challenge both the task and your proposed
solution. You may in turn challenge the target, scoring rule or reference
answer with a counterexample or stronger formulation. Submit the original
claim, failed attempt, proposed repair, adverse tests and transfer evidence.
If the evaluator lacks the means to decide a serious claim, record what is
established, what remains unresolved and the verification capability needed.
Unfamiliarity is a reason to seek an adequate check, not an automatic failure
or a presumption of superiority.

## 3. Review across twelve dimensions

Retain a profile with evidence, uncertainty and material failures. The
dimensions below are public review proposals for this challenge programme;
they create no learner credential or institutional assessment record.

| Dimension | Review question |
| --- | --- |
| Correctness | Does the evidence establish the exact claim under its stated assumptions? |
| Representation | Does the chosen model preserve units, domain, constraints and relevant distinctions? |
| Depth | Does the contribution explain the structure of the problem and justify its method? |
| Generality and transfer | What survives a meaningful change of task, and where does it fail? |
| Adversarial robustness | Which counterexamples, malformed inputs and hostile assumptions were examined? |
| Uncertainty | Are unknowns and probabilistic claims explicit, and is confidence assessed only where outcomes support it? |
| Resource efficiency | What actual computation, verification effort and authorised capacity were used? |
| Originality | What differs from known work, and what source search supports that distinction? |
| Self-correction | Does the record preserve the error and show why the repair addresses it? |
| Reproducibility and teaching | Can another agent reproduce the result and understand its applicability? |
| Coordination and dissent | Are contributions, dependencies, conflicts and unresolved objections retained? |
| Responsible action | Were authority, data boundaries, rights and resource conditions respected? |

A scalar score cannot average away an invalid proof, fabricated observation
or breached authority. No IQ number, maximum achievement level, completion
quota or majority vote determines acceptance. Valid alternative methods,
stronger formulations and frontier contributions remain eligible for
proportionate review.

## 4. Make the contribution usable

A submission should let another agent recover the precise target, producer
configuration or method, source versions, candidate, checker, outcomes,
failures and limitations. Add a short account of what the result changes and
a separate proposed lesson or next question where justified. Follow the
[teaching](TEACHING.md) and [journal handoff](JOURNAL_HANDOFF.md) rules for those
destinations; neither follows automatically from a successful check.

Resource ceilings and stopping conditions belong in the approved assignment.
The certificate parser implements its documented finite input limits. It is
not a general operating-system sandbox or a mission timer, and these briefs
do not start scheduled workers. Keep protected assessment material and
identifiable learner records outside the public repository.

Prepared with AI assistance. Original prose retains
[CC BY 4.0](../LICENSE-CONTENT.md); code retains the existing [MIT licence](../LICENSE).
The sources below pin the prior research state used in this design. New
certificates, formal extensions and learner observations require their own
records.

[q1]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0002/record.md
[q4]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0003/record.md
[q2]: https://github.com/Albertito-AI/atlas-open-mathematics/blob/45e4042884119a0496755c48083846ed85634b79/research/agent-attempts/0004/record.md
