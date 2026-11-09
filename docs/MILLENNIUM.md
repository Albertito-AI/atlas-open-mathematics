# Millennium research programme

This programme organises reading, prerequisite learning and carefully scoped experiments around six Millennium Prize topics. The executable pilot currently covers exact rational linear systems. It has proved no Millennium conjecture and supplies no evidence that one is close to resolution.

The machine-readable register is [data/millennium.json](../data/millennium.json). Status labels were checked against the Clay Mathematics Institute on **9 November 2026**. They are dated observations and must be rechecked before a public status update.

## Official status and scope

| Topic | Clay status checked | Mathematical target, in brief |
| --- | --- | --- |
| [P versus NP](https://www.claymath.org/millennium/p-vs-np/) | Unsolved | Decide whether polynomial-time decision and polynomial-time certificate verification define the same class. |
| [Riemann hypothesis](https://www.claymath.org/millennium/riemann-hypothesis/) | Unsolved | All non-trivial zeros of the Riemann zeta function have real part one half. |
| [Navier–Stokes existence and smoothness](https://www.claymath.org/millennium/navier-stokes-equation/) | Active | Resolve an official existence or breakdown alternative for three-dimensional incompressible flow under its specified hypotheses. |
| [Hodge conjecture](https://www.claymath.org/millennium/hodge-conjecture/) | Unsolved | Rational Hodge classes on smooth complex projective varieties arise as rational combinations of algebraic-cycle classes. |
| [Birch and Swinnerton-Dyer conjecture](https://www.claymath.org/millennium/birch-and-swinnerton-dyer-conjecture/) | Unsolved | Relate an elliptic curve's rational-point rank to the order of vanishing of its L-function at one, with a refined leading-coefficient prediction. |
| [Yang–Mills existence and mass gap](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) | Unsolved | Construct the required non-trivial four-dimensional quantum theory and prove a positive mass gap. |

Navier–Stokes needs special care. Clay's [11 September 2026 announcement](https://www.claymath.org/news/navier-stokes-announcement/) describes an apparent resolution while retaining its prize evaluation process. The problem page currently says **Active**. This register does not independently assess the announced proof or infer that Clay has awarded a prize. It therefore does not describe all six topics as unsolved.

The seventh original problem, the [Poincaré conjecture](https://www.claymath.org/millennium/poincare-conjecture/), is listed by Clay as solved through Perelman's work. It can serve as a historical learning case, outside this six-topic research register. The brief descriptions above do not replace Clay's official technical problem statements, linked on each topic page.

## Proposed prerequisite map

These paths are this project's curriculum proposals. They are not Clay requirements or estimates of the work needed to solve a prize problem.

| Track | Prerequisites, in order | First bounded activity | Claim boundary |
| --- | --- | --- | --- |
| P versus NP | Logic and discrete mathematics; algorithms; asymptotic complexity; reductions; complexity theory | Implement a small satisfiability certificate checker and compare it with exhaustive enumeration on explicitly bounded inputs. | Faster search on a finite sample establishes neither equality nor separation of complexity classes. |
| Riemann | Proof-based calculus; complex analysis; number theory; analytic continuation; analytic number theory | Reproduce elementary number-theory proofs, then teach the domain of convergence and continuation of the zeta function. | Finite zero computations cannot establish the hypothesis for all non-trivial zeros. |
| Navier–Stokes | Multivariable calculus; real analysis; differential equations; functional analysis; Sobolev spaces and PDE estimates | Check a simple energy identity under explicitly stated boundary and regularity assumptions; audit the scope of the 2026 announcement. | A numerical fluid simulation or a simplified equation cannot settle the official alternatives. |
| Hodge | Linear and abstract algebra; topology; differential geometry; complex manifolds; cohomology and algebraic geometry | Explain cohomology and algebraic cycles in elementary examples, with assumptions stated in full. | An example or altered coefficient system cannot establish the rational Hodge conjecture. |
| Birch and Swinnerton-Dyer | Number theory; abstract algebra; algebraic curves; elliptic curves; L-functions and arithmetic geometry | Count points on explicitly chosen nonsingular elliptic curves over small finite fields and distinguish these counts from rational-point rank. | Finite-field counts and numerical L-values do not prove the general rank or leading-coefficient assertions. |
| Yang–Mills | Analysis and geometry; Lie groups; classical field theory; quantum mechanics; rigorous quantum field theory | Study spectral gaps in finite-dimensional operators and identify which features fail to transfer to the continuum theory. | A matrix spectral gap, simulation or Higgs-mechanism discussion does not construct the required quantum Yang–Mills theory. |

## Progress that can be reported honestly

Each work item should have one precise deliverable: a checked lemma, corrected formal statement, reproducible finite computation, literature note, teaching exercise or documented failed approach. Store its dependencies and the exact scope of verification. Learning material should show the assumptions and the reason the conclusion follows.

Novel conjectures may be generated, but they remain candidates until definitions are checked, counterexamples sought and the literature reviewed. A new expression of a known result is not a discovery. Demonstrating an existing theorem independently is valuable learning and must be credited as such.

Before announcing a proposed research breakthrough, apply [VERIFICATION.md](VERIFICATION.md), obtain independent mathematical review and distinguish proof checking from novelty assessment and prize recognition. Clay's [prize rules](https://www.claymath.org/millennium-problems/rules/) require qualifying publication, at least two years after publication and general acceptance before consideration. Repository activity does not satisfy those conditions by itself.

## Initial stage

The linear-system pilot develops the operational habits required for more demanding work: exact statements, independently checked certificates, preserved failures and reproducible lessons. Its present output is educational and methodological. Advancement to any track requires demonstrated competence in the prerequisites and a specific tractable subproblem; the existence of this roadmap is not a claim that such advancement has occurred.
