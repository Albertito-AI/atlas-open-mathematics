# Q0003: pressure periodicity and the energy argument

13 November 2026. Work ID ATLAS-MATH-RESEARCH:Q0003-PRESSURE-20261113.
Base: `84d225e6ba6b3c5ee41e9d7a5496e66176638b68`.
Prepared with OpenAI Codex assistance under Albert Tan's direction. Exact model
identifier and token usage unavailable. Zero new spending; one bounded source
and mathematical argument review. Known mathematics, no novelty claim.

## Source audit

Read on 13 November 2026:

- [Clay topic page](https://www.claymath.org/millennium/navier-stokes-equation/): label Active.
- [Clay announcement](https://www.claymath.org/news/navier-stokes-announcement/),
  dated 11 September 2026: reports an apparent resolution, retaining evaluation.
  This is not our independent verification of an announced proof or a prize award.
- Charles L. Fefferman, [official problem description](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf),
  PDF pp. 1–2, equations (1)–(3), (8)–(11), alternatives A–D, and p. 6 errata.
  Text of these portions was inspected. The periodic formulation needs pressure
  periodicity, explicitly added by the errata. A/B concern universal smooth
  existence with zero force; C/D permit specified smooth forces in breakdown
  alternatives. A single tractable solution does not meet those quantifiers.

The announcement does not identify a proof manuscript in its text. This run
has not identified or audited the purported resolving theorem. That portion
of Q0003 remains open. No historical partial-result paragraph in the problem
statement is treated as a fresh 2026 survey. No source document is republished.

## Frozen supporting statement and derivation

Let u and p be smooth, spatially unit-periodic on R^3, for times in [0,T],
with div u=0, viscosity nu>0, force zero, and
u_t+(u dot grad)u=nu Delta u-grad p. All integrals below are over [0,1]^3.
Put E(t)=1/2 integral |u|^2. Then

$$ E'(t)=-\nu\int |\nabla u|^2. $$

Indeed differentiate under the integral and substitute the equation.
The convection integral is integral div(u |u|^2/2), since div u=0.
Opposite faces cancel by periodicity. Integration by parts gives
integral u dot Delta u = -integral |grad u|^2, with matching face terms.
Finally integral u dot grad p = integral div(pu)-integral p div u = 0,
because BOTH p and u are periodic. This proves the conditional smooth energy
identity. It assumes smoothness on the interval; it does not establish global
smooth existence or bound all derivatives. Integrating the momentum equation
also gives d/dt integral u=0, by the same cancellations.

## Counterexample to omitting pressure periodicity

Take u(x,t)=(t,0,0) and p(x,t)=-x_1 on R^3, with zero force and any nu>0.
Then u_t=(1,0,0), (u dot grad)u=0, Delta u=0, div u=0 and
-grad p=(1,0,0). Every equation holds pointwise, and u is periodic and smooth,
with zero initial velocity. But p is not periodic and is not a scalar pressure
on the torus. Over the unit cell, E=t^2/2, so E'=t, whereas the asserted
viscous dissipation is zero. The missing pressure boundary flux is exactly t:
-integral_boundary p u dot n = t. This is a counterexample to the weakened
energy claim, NOT to the official corrected problem.

A time-dependent additive pressure gauge cannot repair it: adding c(t) leaves
p(x+e_1,t)-p(x,t)=-1. A constant gradient can instead be represented as a
nonzero body force, changing the zero-force assumption. The failed route was
cancelling pressure boundary terms solely from periodic velocity.

## A valid comparison solution and teaching

For integer m>=1, set k=2*pi*m and
u(x,t)=(exp(-nu*k^2*t)*sin(k*x_2),0,0), p=0. Here the symbol nu in the
exponential denotes viscosity, while u denotes velocity. Convection vanishes
because the field is independent of x_1; divergence is zero; u_t=nu Delta u.
Both fields are periodic. E=exp(-2*nu*k^2*t)/4 and
integral |grad u|^2=k^2*exp(-2*nu*k^2*t)/2, so the identity agrees exactly.
This special shear family suppresses nonlinear interaction and cannot prove
the universal three-dimensional statement.

Exercise 1: find the missing boundary term for u=(t,0,0), p=-x_1.
Answer: the x_1=1 face contributes -t to integral_boundary p u dot n;
the x_1=0 face contributes zero, hence pressure work is t.
Exercise 2: can a periodic scalar have constant gradient (-1,0,0)?
Answer: integrate its first derivative across one period; the integral must
be zero, contradicting -1. Exercise 3: does decreasing total energy control
every derivative? No such implication has been proved here. The next task is
to construct smooth divergence-free periodic fields with fixed L2 norm and
unbounded gradient norm, and distinguish a sequence of fields from one evolving
solution. These are exposed exercises, not measured human learning.

## Verification, reuse and publication boundary

Verification consists of the displayed exact differentiations, face fluxes
and integrations, plus separate critical review recorded below. No numerical
simulation, formal prover or live learner evaluation was run. The existing
rational-system checker cannot verify these differential equations. The accepted
Opsbook exact-substitution lesson was read at its retained revision 1; its
linear-certificate scope is unchanged. Direct substitution is a methodological
analogy here, not promotion of an empirically tested PDE rule.

Original prose is CC BY 4.0. A possible human-facing contribution explains why
boundary assumptions change a mathematical claim. This working companion is
not a submission-ready journal article. Follow
[JOURNAL_HANDOFF.md](../../../docs/JOURNAL_HANDOFF.md) for private manuscript,
authorship/AI/rights declarations and independent editorial handling. No
submission, editorial acceptance or private reviewer record is included.

## Recorded review and checks

A separate critical-review agent independently read the official PDF errata
and current Clay pages, checked each differentiation and face cancellation,
and found no mathematical error. It confirmed the pressure jump, pressure-work
sign, gauge limitation, shear energy/dissipation and exercise answers. This is
agent mathematical review, not formal verification or external human peer review.
The repository validator passed 113 JSON files and local documentation links;
all 96 existing tests passed. These tests check existing software, not this PDE
argument. No solver/checker/policy changed, and no failed computation is hidden.

## Public promotion and next owners

Prepared description: "Why boundary conditions matter: an exact fluid-flow
example shows how omitting periodic pressure changes the energy calculation."
Learner value: three worked exercises and a source-linked proof audit. Known
mathematics; no novelty, global regularity or measured-learning claim.
Use the exact containing commit, recorded in the operations receipt after save.
[Atlas Open Mathematics](https://github.com/Albertito-AI/atlas-open-mathematics)
is the public source; [Opsbook](https://github.com/Albertito-AI/atlas-opsbook)
is the scoped procedure-memory connection. GitHub Adoption receives profile
consideration; Daily Website Resource Refresh selects material for
[Albert's website](https://www.alberttansinhon.com/); Website Care and Reach
alone publishes and reads it back. Those stages are queued, not acknowledged
or published by this record. [The Human Question](https://thehumanquestionjournal.com/)
retains independent editorial decisions. Original educational prose CC BY 4.0;
preserve attribution and AI provenance. No confidential manuscript is included.
