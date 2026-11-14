# Q0003: energy, gradients and the order of limits

14 November 2026. Work ID ATLAS-MATH-RESEARCH:Q0003-ENERGY-20261114.
Base `22607e972941e77195a923ad3a63afe71eec2c43`.
Prepared with OpenAI Codex assistance under Albert Tan's direction; exact model
identifier and token usage unavailable. Zero new spending. One bounded analytic
investigation, not a simulation or a learner experiment. Known mathematics.

## Frozen target and relationship to prior work

The [previous investigation](../0006/record.md) derived a conditional smooth
periodic energy identity and checked a shear solution. Here we test the invalid
inference that bounded total kinetic energy alone bounds spatial gradients.
We retain the energy identity, construct an obstruction to that inference, and
establish a positive-time estimate within the same special shear family.
This preserves the earlier result while specifying its limitation. No solver,
verifier, policy or accepted evidence is changed. No current Millennium status
or novelty claim is made; the earlier dated source-status observations remain
historical. The underlying equations and periodic assumptions are stated in
Fefferman's official description, pp. 1–2 and p. 6 errata, cited in attempt 0006.

## Fixed energy, unbounded gradients

All norms are over the unit torus, represented by [0,1]^3 with volume one.
For every positive integer m, put k_m=2*pi*m and

$$v_m(x)=(\sin(k_m x_2),0,0).$$

Each field is smooth, periodic, divergence-free and mean zero. Its divergence
is the x_1 derivative of the first component, which vanishes. Integration of
sin squared and cos squared over their integer numbers of periods gives

$$\|v_m\|_2^2=\tfrac12,\quad E_m=\tfrac14,
\qquad \|\nabla v_m\|_2^2=\tfrac{k_m^2}{2}=2\pi^2m^2.$$

Thus there is no finite universal bound on the gradient norm depending only
on this fixed energy, even for smooth mean-zero divergence-free fields on this
fixed domain. For example, doubling m preserves energy and quadruples the
squared gradient norm. This is a sequence of different initial fields, not a
single solution developing a singularity. None of these individual fields
has an infinite derivative.

## Evolution changes the comparison

Fix viscosity nu>0. For each m take zero pressure and force and define

$$u_m(x,t)=e^{-\nu k_m^2t}v_m(x).$$

Direct substitution checks the equations: convection is zero because the
only nonzero velocity component differentiates in x_1, while the field depends
only on x_2; divergence is zero; u_t=nu Delta u. Hence each member is a smooth
global shear solution, with a different initial datum. Its energy and squared
gradient norm are

$$E_m(t)=\tfrac14e^{-2\nu k_m^2t},\qquad
G_m(t)=\tfrac{k_m^2}{2}e^{-2\nu k_m^2t}.$$

Differentiation yields E'_m=-nu G_m. Independent integration in time yields

$$\int_0^T G_m(t)\,dt=\frac{1-e^{-2\nu k_m^2T}}{4\nu}
\leq\frac1{4\nu}.$$

At any fixed t>0, the function z exp(-2*nu*t*z), z>=0, has derivative
exp(-2*nu*t*z)(1-2*nu*t*z); its maximum is 1/(2*e*nu*t).
Consequently

$$G_m(t)\leq\frac1{4e\nu t}\quad\text{for all }m.$$

This is an upper bound from maximising over continuous z; an integer frequency
need not attain it. Also G_m(t) tends to zero as m tends to infinity for every
fixed t>0, whereas G_m(0) tends to infinity. At t_m=1/(nu*k_m^2), which tends
to zero, G_m(t_m)=k_m^2*exp(-2)/2 tends to infinity. These statements are
compatible: the time is fixed in one comparison and varies with m in another.
No estimate uniform down to t=0 follows from the displayed positive-time bound.
For T>0 the time integral tends to 1/(4*nu), despite pointwise convergence to
zero at each positive time. High gradients concentrate near the initial time;
interchanging this limit with the integral would be invalid.

## Failed routes and limitations

The rejected energy-only bound on the gradient L2 norm at each time fails by explicit formula,
not because a finite search missed a proof. Another rejected route mistakes a
uniform time-integrated dissipation bound for a uniform bound at every time.
The example disproves that implication. A third route treats m as the time
of one solution: that changes the initial data and does not exhibit blow-up.
Finally, the positive-time bound above applies only to this family, whose
nonlinear convection vanishes. It does not supply a corresponding estimate
for arbitrary three-dimensional Navier–Stokes solutions, prove global
regularity, or assess the announced resolving proof. The L2 energy identity
remains valid under the assumptions of attempt 0006.

## Teaching companion and exposed exercises

Total energy measures squared speed accumulated over space. A gradient measures
how rapidly neighbouring velocities differ. Finer oscillations can preserve
speed while making those differences much sharper. In this shear family,
viscosity damps the finer oscillations faster. All these claims have the exact
formulae above; they are not measured outcomes in a real fluid or classroom.

1. Compare m=1 and m=10 at time zero. Both energies are 1/4; squared gradient
   norms are 2*pi^2 and 200*pi^2, a ratio of 100.
2. Does the bound 1/(4*e*nu*t) prove bounded gradients at t=0? No, it diverges
   as t decreases to zero and was derived only for t>0.
3. Why does the dissipation integral not converge to zero even though G_m(t)
   does at each t>0? Its mass concentrates in a shrinking interval near zero;
   pointwise convergence alone does not permit exchanging limit and integral.
4. Do these formulae show one flow blows up? No. Every fixed m gives a globally
   smooth, exponentially decaying solution with its own initial data.

Next prerequisite: for a finite sum of distinct shear Fourier modes, derive the
same positive-time gradient estimate relative to initial L2 norm using
orthogonality. State the regularity/convergence conditions needed before any
infinite-series extension. This is known mathematics, not a proposed discovery.

## Verification, memory and editorial status

The proof consists of exact differentiation, elementary trigonometric integration
and one-variable maximisation. Review is recorded below. No floating-point
experiment or formal prover was used. Existing rational certificate tools do
not verify this PDE argument. The accepted Opsbook exact-substitution rule,
retained revision 1, remains scoped to linear certificates; direct substitution
here is an analogy, not a promoted general PDE rule or measured improvement.

Original prose CC BY 4.0; no third-party source text, private school records,
confidential manuscripts or reviewer records are copied. Follow
[JOURNAL_HANDOFF.md](../../../docs/JOURNAL_HANDOFF.md) for any future independent
editorial assessment, private manuscript and authorship/AI/rights declarations.
This is a public teaching companion, not a submitted or accepted journal paper.

Public promotion description: "The same total energy can hide very different
spatial gradients. An exact shear-flow example explains the distinction and
why the order of limits matters." Learner value: four worked exercises and a
reproducible analytic argument. Link to this record at its containing source
commit, supplied in the operations receipt. GitHub Adoption owns profile
consideration; Daily Website Resource Refresh selects material for
[Albert's website](https://www.alberttansinhon.com/); Website Care and Reach
owns publishing/readback. [Atlas Open Mathematics](https://github.com/Albertito-AI/atlas-open-mathematics),
[Opsbook](https://github.com/Albertito-AI/atlas-opsbook) and
[The Human Question](https://thehumanquestionjournal.com/) retain their distinct
research, procedural and editorial roles. These handoffs confer no publication,
independent use, journal acceptance, training or learning evidence.

## Review receipt

A separate critical-review agent checked the exact formulae, PDE substitution,
energy derivative, time integral, scalar maximisation and order-of-limits
statements. It found no mathematical error within this scope. This is distinct
agent review, not external human peer review or machine-checked formal proof.
The 96 existing repository tests passed; the repository validator checked 131
JSON files and local links. Those software checks do not verify this analytic
argument. No numerical or formal verification is asserted.

Review clarification: wording now explicitly names the gradient L2 norm at each
time, avoiding confusion with a spatial pointwise gradient bound.
