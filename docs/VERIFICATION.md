# Verification and claims

The executable pilot checks finite systems of two linear equations in two unknowns using Python's exact rational arithmetic. Its result is a checked certificate for one input system. A separate [formal pilot](../formal/README.md) supplies four elementary integer statements and a pinned Lean checking workflow. This release does not contain a Lean proof of its Python implementation or a solution to a Millennium Prize Problem.

## What an accepted certificate establishes

Write the input as `A x = b`, over the rational numbers. The verifier reads the coefficients and checks the following identities directly. It does not call the candidate solver.

| Candidate status | Certificate checked | Consequence for this input |
| --- | --- | --- |
| `unique` | A proposed solution satisfies both equations; the supplied determinant equals the determinant of `A` and is nonzero. | The proposed solution is the unique rational solution. |
| `underdetermined` | A proposed solution satisfies both equations; a supplied nonzero vector `v` satisfies `A v = 0`. | Every `x + t v`, for rational `t`, is a solution, so there are infinitely many. The certificate need not describe every null direction. |
| `inconsistent` | Row weights `w` satisfy `w A = 0` and `w b != 0`. | Any putative solution would imply `0 = w b`, a contradiction. |

These consequences follow from elementary linear algebra. The implementation tests the displayed finite identities. Python, the standard library, the execution environment and this verifier remain part of the trusted implementation. Passing unit tests increases confidence in the implementation; it does not constitute a machine-checked universal proof of its correctness.

The case's `kind` is generation metadata. A verifier must derive acceptance from the coefficients and certificate. Relabelling a singular system as `unique` must never make a false uniqueness certificate acceptable.

## Input contract

Cases contain exactly `id`, `A`, `b` and `kind`. `A` has two rows of two entries, and `b` has two entries. Supported kinds are `unique`, `inconsistent` and `underdetermined`. Identifiers must satisfy the implementation's safe-character rule and its 96-character limit.

Scalars are integers, excluding booleans, or exact integer/rational strings. Floating-point inputs are rejected. Case numerators and denominators are bounded by `10^9`; certificate numerators and denominators are bounded by `10^120`; scalar strings have a 256-character limit. A denominator must be nonzero. Unknown fields and malformed dimensions are rejected. Invalid cases cause `solve` to raise `ValueError`; `verify` returns a rejection for malformed cases or candidates.

Input limits make this pilot's work bounded and reproducible. They do not establish a security boundary for running arbitrary code. Candidate data must remain data. Do not evaluate candidate strings as Python or shell expressions.

## Checks required before accepting a run

Run the standard-library test suite from the repository root:

```sh
python -m unittest discover -s tests -v
```

The tests use hand-constructed rational examples and independently check the identities of generated certificates. They include a zero initial pivot, singular consistent and inconsistent systems, the zero matrix, wrong answers, false determinants, zero null vectors, invalid contradiction certificates, misleading metadata, malformed inputs, booleans, floats, excessive values, deterministic generation and existing-record protection. A patched solver that raises during verification tests the separation between solver and verifier.

Run `python3 scripts/replay_research.py` to reproduce the retained Q0001 finite
examples, Q0004 bounded construction and Q0002 exact calibration. Each script's
parsed JSON must match its retained evidence exactly. A failed process, changed
result or missing record fails the check. The ordinary verification workflow
includes these replays. They establish reproducibility within the stated finite
bounds; the calibration remains a design check with no learner observations.

Attempt records are content-addressed. Repeating a deterministic run should preserve the existing bytes. A collision or inconsistent existing file must stop the write rather than replace the evidence. Content addressing helps detect changes; an operator with write access can still delete or alter files. Retain Git history and backups before treating records as a durable audit trail.

## Evidence labels

| Label | Permitted claim |
| --- | --- |
| Candidate | A proposed statement or answer awaiting verification. |
| Rejected certificate | The checker rejected this submission; the reason and input remain available. Rejection alone does not prove the mathematical statement false. |
| Exact instance checked | The stated finite identities passed this release's rational checker. |
| Computational evidence | A documented experiment produced results within specified bounds. |
| Formal theorem checked | A proof assistant successfully checked the exact stated theorem under a disclosed axiom policy and pinned environment. Source code and a configured workflow alone do not justify this label. |
| Research result reviewed | A precisely scoped novelty and correctness claim has received documented independent review. |

A new random exercise is a new instance, not automatically a new theorem or research contribution. Neither many successful examples nor a chart of them proves a universal statement. A verifier's rejection reason must not be rewritten as a successful result in teaching material.

## Elementary formal pilot and future extension

The included formal pilot fixes four statements over the integers about `x + y = s` and `x - y = d`: consequences for `2x` and `2y`, uniqueness, one concrete solution, and one parity obstruction. The parity obstruction has rational solutions, which makes preservation of the integer domain essential. These statements support teaching; they do not verify the Python algorithm or all rational matrices.

Lean 4.24.0 is pinned in [formal/lean-toolchain](../formal/lean-toolchain); this small pilot uses Lean's bundled arithmetic tactic and does not depend on mathlib. The checking script validates the version, rejects diagnostics and audits all four expected theorem reports. Its unit tests exercise the audit parser, including missing, duplicated and forbidden-axiom reports. Those tests do not execute Lean.

On 9 November 2026, all four statements passed an actual local run of the pinned Lean checker. The downloaded official release archive matched the recorded SHA-256 digest. Every theorem's transitive axiom report contained only `propext`, `Classical.choice` and `Quot.sound`. The [verification evidence](../formal/evidence/2026-11-09.json) preserves the complete compiler version, theorem-source hash and printed reports. The ordinary release URL initially returned HTTP 504; GitHub's official release-asset API delivered the same archive successfully. Remote CI completion remains a separate claim requiring its own successful workflow run.

The next formal stage requires a reviewed mathematical statement, pinned Lean and mathlib revisions, proof source, a build that includes the theorem module, and a transitive axiom audit. The standard allowlist is a subset of `propext`, `Classical.choice` and `Quot.sound`. Reject `sorryAx` and unapproved custom axioms. A proof that relies on native computation needs a separate, explicitly disclosed trust category; it does not pass the strict kernel-only policy.

From the 11 November maintenance change, the workflow also runs the separate
[Q0001 checker](../scripts/check_integer_criterion.py) over the unchanged module
whose original source hash appears in its [local evidence](../research/agent-attempts/0002/formal-evidence.json).
The new checker pins that source hash and reuses the existing axiom auditor.
The original pilot's checker and the axiom allowlist are unchanged. Q0004's
universal formalisation and Q0002's actual learner evaluation remain open.

For unreviewed generated proofs, use a sandbox without credentials or unnecessary network access. Replay proofs with `lean4checker`. For major claims, compare against a separately trusted challenge statement with `comparator` and an external checker. Even successful formal checking does not show that a mistranslated statement matches the intended conjecture. Review quantifiers, domains, assumptions, definitions and vacuous hypotheses independently.

Official guidance: [Lean proof validation](https://lean-lang.org/doc/reference/latest/ValidatingProofs/), [Lean community proof checklist](https://leanprover-community.github.io/did_you_prove_it.html), and [Formal Conjectures proof contribution policy](https://github.com/google-deepmind/formal-conjectures/blob/main/PROOFS.md). These links describe evolving tools; consult version-specific documentation before extending the pinned pilot. A general submission checker and independent external kernel are not yet implemented here.

## Research memory and evaluation

Retain the statement, source, exact input, proposal, verifier version, result, rejection reason, costs and superseding corrections. Reusing these records is retrieval-based learning. It does not imply that a model has been retrained.

Keep training examples, retrieved worked solutions and held-out evaluation problems separately labelled. Record any known overlap. Freeze benchmarks before comparison, report all attempted cases, and do not select only successful runs for public metrics. For a novelty claim, check the literature and known databases independently, retaining the search date and sources.

Verification policy reviewed on 9 November 2026.

## Applications and advanced certificate lab, 11 November 2026

The [application module](../atlas_math/applications.py) adds exact integer and
nonnegative-integer interpretations to the existing rational pilot. Its
rank-one branch uses a gcd obstruction or an integer parameter family. A
fractional particular solution returned by a rational solver is never alone
treated as proof of integer infeasibility. The constructive branch implements
the recorded Bézout argument and checks its output by substitution. The paired
evaluation example checks an exact tail against enumeration; it contains no
learner observations. The source references identify the earlier research
commit, not the later application implementation.

The separate [challenge module](../atlas_math/challenges.py) checks
`A x = b`, integer `x`, explicit integer lower and upper bounds, and an integer
linear objective. It verifies witnesses, lower bounds, integer rounding,
modular and interval obstructions, and complete binary branch proofs. It never
calls a solver while verifying or executes candidate code. The
[protocol](CHALLENGE_PROTOCOL.md) states the identities, supported certificates
and implementation bounds. A refused certificate can be incomplete or outside
the supported language; refusal does not establish that the underlying claim
is false.

Reproduce the new demonstrations with:

```sh
python -m atlas_math applications
python -m atlas_math.challenges demo
python -m unittest discover -s tests -v
```

The tests include independent enumeration of small integer problems, feasible
but suboptimal candidates, a coupled modular obstruction despite primitive
individual rows, integrality gaps, signed coefficients, fixed variables,
branch coverage, changed-target identities, malformed data and bounded input
handling. Tests establish their recorded finite scope. The Python checker has
no universal formal correctness proof. Existing Lean targets and accepted
mathematical evidence are unchanged.

All bundled constructions and captured outputs are exposed synthetic material.
They establish no frontier-agent difficulty calibration, model-weight update,
causal learning effect, real-world deployment or novel mathematical result.
The research programme above the lab includes proof and transfer questions that
require their own evidence and independent review.

Observed local verification on 11 November 2026 used Python 3.12.14: **96 tests
passed**, the repository validator checked 97 JSON files, and Q0001's finite
record, Q0004's finite construction record and Q0002's calibration replayed
exactly. A separate agent added and ran seven independent review tests,
including exhaustive checks on 90 small signed rectangular models, forged
claims, branch separation and the exact proof-node and depth boundaries.
No unsound acceptance was found within those finite checks. The recorded
example in lesson 004 was also executed. Existing Lean source and proof
policies were not changed or rerun locally for this application work; hosted
workflow results are separate evidence at the GitHub revision being reviewed.
