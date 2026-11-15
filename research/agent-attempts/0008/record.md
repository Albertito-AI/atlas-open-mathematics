# Q0003: when energies add, and when they do not

15 November 2026. Work ID `ATLAS-MATH-RESEARCH:Q0003-FOURIER-20261115`.
Source base `cc5fd56936442b93cf17cbab68a24635a50637ae`.
Prepared with OpenAI Codex assistance under Albert Tan's direction. Exact model
identifier, token usage and total compute cost are unavailable; new spending is
zero. This is an original exposition of known mathematics, not a novelty claim,
formal PDE proof, simulation, model-training result or measured learner trial.

## Frozen question and sources

Extend [attempt 0007](../0007/record.md) from one shear frequency to a finite
sum. Freeze the unit-volume torus, positive viscosity, real coefficients,
distinct positive integer frequencies, constant mean in the first component,
zero force and zero pressure. Establish the exact energy identity and a
positive-time gradient estimate relative to initial fluctuation energy.
Test the proposed shortcut of adding the energies of arbitrarily listed modes.
Budget: one finite proof/teaching slice, 625 exact coefficient cases and two
duplicate-frequency controls; no infinite-series theorem in this iteration.

Primary equation source: Charles L. Fefferman,
[Existence and Smoothness of the Navier–Stokes Equation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf),
pp. 1–2, equations (1)–(3), (8)–(11), and p. 6 periodic-pressure errata.
Re-read the equation/periodic formulation on 15 November 2026. This citation
supports the equation and boundary conditions, not a current problem-status
claim or attribution of a new theorem. The computations and proof below are
self-contained. No assertion about a Millennium resolution is made.

## Candidate argument

Let F be a finite set of positive integers, including the possibility F is
empty. For m in F let k_m=2*pi*m and let a_m,b_m,c be real. With nu>0 set

$$h(y,t)=c+\sum_{m\in F}e^{-\nu k_m^2t}
\{a_m\sin(k_my)+b_m\cos(k_my)\},\qquad
u(x,t)=(h(x_2,t),0,0).$$

Every sum is finite, so all derivatives and integrals used here can be taken
term by term. The field is smooth and periodic. Its divergence is zero, and
(u dot grad)u=h partial_1 u=0. Each nonconstant mode satisfies h_t=nu h_yy;
the constant does too. Thus direct substitution verifies the unforced
Navier–Stokes equations with p=0. The mean is (c,0,0), independent of time.

To justify adding energies, use the product-to-sum identities. Integrals over
[0,1] of sin(2*pi*n*y) and cos(2*pi*n*y) vanish for nonzero integer n.
Consequently distinct sine modes are orthogonal, distinct cosine modes are
orthogonal, every sine is orthogonal to every cosine, and each is orthogonal
to the constant. Each nonconstant sine or cosine has squared norm 1/2.
These assertions include the same-frequency sine/cosine pair; they exclude
two copies of the same sine. Integrating in x_1 and x_3 contributes factors 1.
Writing A_m=a_m^2+b_m^2 gives

$$\|u(t)\|_2^2=c^2+\frac12\sum_{m\in F}A_m e^{-2\nu k_m^2t},
\qquad G(t):=\|\nabla u(t)\|_2^2
=\frac12\sum_{m\in F}k_m^2 A_m e^{-2\nu k_m^2t}.$$

Define total energy E(t)=||u(t)||_2^2/2 and fluctuation energy
E_fl(t)=E(t)-c^2/2. Exact differentiation gives E'(t)=-nu G(t), while direct
integration for T>=0 gives

$$\int_0^T G(t)\,dt=
\frac1{4\nu}\sum_{m\in F}A_m(1-e^{-2\nu k_m^2T})
=\frac{E_{\rm fl}(0)-E_{\rm fl}(T)}{\nu}
\leq\frac{E_{\rm fl}(0)}{\nu}.$$

The constant mean carries energy but no gradient and is not dissipated.
For fixed t>0, differentiating z exp(-2*nu*t*z), z>=0, shows its maximum is
1/(2*e*nu*t), attained at z=1/(2*nu*t). Multiplying this bound by each
nonnegative A_m/2 and adding yields

$$G(t)\leq\frac{\|u(0)-(c,0,0)\|_2^2}{2e\nu t}
=\frac{E_{\rm fl}(0)}{e\nu t}.$$

The coefficient is consistent with attempt 0007: one unit sine has initial
fluctuation norm squared 1/2, giving G(t)<=1/(4*e*nu*t). The estimate is
uniform over finite F and coefficients at fixed initial fluctuation norm.
It need not be attained at a prescribed t because the frequencies are
discrete. It does not generally bound G(0); when E_fl(0)>0 its right side
diverges as t decreases to zero. For F empty or all coefficients zero,
G=E_fl=0 and all formulae hold.

## Failed shortcuts and boundary cases

**Failure: square coefficients before consolidating repeated frequencies.**
At t=0, sin(2*pi*y)-sin(2*pi*y)=0. Adding the two individual squared norms
predicts 1, although the true squared norm is 0. Reversing the sign gives
2*sin(2*pi*y), whose true squared norm is 2, although naive addition again
predicts 1. Cross terms can decrease or increase the answer. Combine the
coefficients of each repeated frequency before invoking orthogonality.
At later times identical frequencies have identical damping, so the same
failure persists. This corrects a tempting generalisation, not prior evidence:
attempt 0007 used only one mode and remains valid.

**Failure: assume all divergence-free fields have vanishing convection.**
Take w=(sin(2*pi*x_2),sin(2*pi*x_1),0), also smooth and divergence-free.
Its first convection component is
2*pi*sin(2*pi*x_1)*cos(2*pi*x_2), which is not identically zero.
This disproves the proposed implication, not existence of a pressure-adjusted
solution for w. The proof above depends on the specific shear geometry.
It establishes no corresponding bound for arbitrary three-dimensional flows.

**Unfinished route: replace the finite set by all positive integers.**
Uniform bounds for partial sums do not alone justify differentiating a series
or identifying its initial trace. An extension must specify initial coefficient
summability, convergence in the stated norm, positive-time derivative convergence,
and the sense of the equation and initial condition. None of these gates is
waived by a successful finite example. Infinite-series extension is deferred.

## Reproducible exact corroboration

The following standard-library script represents trigonometric polynomials as
finite Laurent polynomials with exact rational complex coefficients. It obtains
the spatial integral of a product from its zero-frequency coefficient, rather
than assuming the claimed sum-of-squares formula. Differentiation is divided
by 2*pi, so the reported gradient quantity is G/(2*pi)^2. This checks finite
normalisation and cross terms at t=0, not exponentials, the universal proof or
the implementation of any existing certificate verifier.

Save the Python block as `/tmp/atlas_fourier_audit.py` and run
`python /tmp/atlas_fourier_audit.py`. Inputs are frozen in the block.

```python
from fractions import Fraction as Q
from itertools import product
import json

ZERO = (Q(0), Q(0))
def add(z, w):
    return (z[0] + w[0], z[1] + w[1])
def mul(z, w):
    return (z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0])
def polynomial(c, terms):
    p = {0: (Q(c), Q(0))}
    for m, a, b in terms:
        for n, z in [(m, (Q(b)/2, -Q(a)/2)),
                     (-m, (Q(b)/2, Q(a)/2))]:
            p[n] = add(p.get(n, ZERO), z)
    return p
def derivative(p):
    return {n: mul((Q(0), Q(n)), z) for n, z in p.items()}
def integral_square(p):
    # The integral of exp(2*pi*i*n*y) is 0 unless n=0.
    value = ZERO
    for n, z in p.items():
        for m, w in p.items():
            if n + m == 0:
                value = add(value, mul(z, w))
    assert value[1] == 0
    return value[0]

count = 0
for a, b, d, e in product(range(-2, 3), repeat=4):
    p = polynomial(Q(1, 3), [(1, a, b), (2, d, e)])
    assert integral_square(p) == Q(1, 9) + Q(a*a+b*b+d*d+e*e, 2)
    assert integral_square(derivative(p)) == Q(a*a+b*b+4*d*d+4*e*e, 2)
    count += 1
cancel = polynomial(0, [(1, 1, 0), (1, -1, 0)])
reinforce = polynomial(0, [(1, 1, 0), (1, 1, 0)])
assert integral_square(cancel) == 0
assert integral_square(reinforce) == 2
assert integral_square(derivative(cancel)) == 0
assert integral_square(derivative(reinforce)) == 2
constant = polynomial(Q(-7, 3), [])
assert integral_square(constant) == Q(49, 9)
assert integral_square(derivative(constant)) == 0
print(json.dumps({"distinct_frequency_cases": count,
                  "duplicate_cancel_norm_squared": str(integral_square(cancel)),
                  "duplicate_reinforce_norm_squared": str(integral_square(reinforce)),
                  "naive_duplicate_norm_squared": "1",
                  "constant_gradient_squared": "0"}, sort_keys=True))
```

Observed on Python 3.12.14, exit 0:

```json
{"constant_gradient_squared": "0", "distinct_frequency_cases": 625, "duplicate_cancel_norm_squared": "0", "duplicate_reinforce_norm_squared": "2", "naive_duplicate_norm_squared": "1"}
```

The 96 existing repository tests passed. The repository validator checked 147
JSON files, retained provenance/certificates/manifests and local links. The
three existing research replays matched their retained evidence exactly.
Those checks concern repository integrity and earlier finite work, not this
universal analytic argument. Existing verifiers, policies and Lean targets
were unchanged. No new formal proof was run for this PDE result.

A separate critical-review agent independently checked the proof, quantifiers,
boundary cases and all five exercise answers. It replayed the embedded block
on Python 3.12.14 and independently checked the same 625 cases and controls
using exact eight-point quadrature in the field Q(sqrt(2)), rather than Laurent
convolution. Its [independent audit](independent-audit.md) includes executable
code, exact output and an aliasing counterexample. It found no substantive
mathematical error. Its minor correction
is retained here: the original sentence said the bound's right side diverges
as time decreases to zero without qualifying positive fluctuation energy.
For constant-only data it stays zero; the sentence now states E_fl(0)>0.
The reviewer read the amended sentence and confirmed the issue closed.
This is distinct automated review, not external human peer review, protected
assessment, mathematical novelty assessment or formal kernel checking.

## Teaching companion and exposed exercises

Energy can be added mode by mode because the cross terms integrate to zero,
not merely because we wrote a velocity as a sum. Orthogonality is the missing
condition. Viscosity damps fine oscillations faster, allowing a positive-time
gradient estimate in this shear family even when the initial gradient is large.
The mean survives and should be separated from the fluctuating part.

1. For c=3, a_1=2, b_2=1, all other coefficients zero, find E(0), E_fl(0)
   and G(0). Answer: 23/4, 5/4 and 16*pi^2 respectively.
2. For the same data, state the bound at t>0. Answer: G(t)<=5/(4*e*nu*t).
3. Explain why two opposite unit sine terms cannot have total squared norm 1.
   Answer: they cancel; their cross term is -1. Two equal unit sine terms have
   cross term +1. Consolidation gives the correct answers 0 and 2.
4. If c is changed from 3 to 30, what changes? Total energy increases by 891/2;
   fluctuation energy, gradients and their dissipation remain unchanged.
5. Would zero divergence alone justify the heat equation reduction? No; the
   explicit w above has nonzero convection. Check its first component directly.

These are public worked exercises, not held-out tests or measured transfer.
Next mathematical question: can an L2 initial shear profile, represented by
square-summable Fourier coefficients, be obtained as a norm-convergent limit,
with positive-time smoothness and this gradient estimate? Specify initial-trace
and convergence claims before attempting that extension.

## Scoped memory, rights and promotion preparation

Accepted Opsbook manual revision 1 at
`research/cycles/2026-11-14-249da205ab05/opsbook/MANUAL.md` requires independent
substitution for linear-system certificates. That scope remains unchanged.
Its bytes match the previously retained 9 November revision 1 manual exactly.
Here direct PDE substitution and a separate Laurent-product calculation apply
the same checking discipline by analogy. Candidate lesson: consolidate repeated
frequencies and verify orthogonality before summing squared norms. Its positive
and negative cases are above. No Opsbook rule promotion or empirical improvement
is claimed; wider application needs its own evaluation.

Original teaching prose and embedded educational example: CC BY 4.0 under the
repository content licence. No third-party code or private source text is copied.
No confidential school, member, manuscript or editorial material is included.
Any later standalone software extraction must retain these notices and have its
licensing checked explicitly.

Promotion copy: "When can we add the energies of separate waves? A finite shear
example proves the condition, shows cancellation failures and explains how
viscosity controls gradients at positive times." Value: a checkable proof,
reproducible rational-algebra exercise and five worked questions. Limits: known
mathematics, special shear geometry, no general regularity or learning claim.
Bind this copy to the actual saved source commit before downstream adoption.

Relevant links: [Atlas Open Mathematics](https://github.com/Albertito-AI/atlas-open-mathematics),
[Atlas Opsbook](https://github.com/Albertito-AI/atlas-opsbook),
[The Human Question](https://thehumanquestionjournal.com/), and
[Albert Tan](https://www.alberttansinhon.com/).
GitHub Adoption selects profile material; Daily Website Resource Refresh selects
website material; Website Care and Reach owns publication/readback. This record
is a public companion prepared for possible editorial consideration under
[JOURNAL_HANDOFF.md](../../../docs/JOURNAL_HANDOFF.md), not a submitted manuscript.
Private manuscript preparation, authorship/AI/rights declarations, independent
handling and normal external review remain prerequisites to journal publication.
No acceptance, endorsement, outside use or engagement is inferred.
