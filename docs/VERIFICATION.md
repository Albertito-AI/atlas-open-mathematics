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

Lean 4.24.0 is pinned in [formal/lean-toolchain](../formal/lean-toolchain); this small pilot uses Lean's bundled arithmetic tactic and does not depend on mathlib. The checking script validates the version, rejects diagnostics and audits all four expected theorem reports. Its unit tests exercise the audit parser, including missing, duplicated and forbidden-axiom reports. Those tests do not execute Lean. At preparation, local Lean execution could not be completed because the release download failed. Successful output from the pinned checking command or its GitHub workflow is required before reporting these four statements as checked in this environment.

The next formal stage requires a reviewed mathematical statement, pinned Lean and mathlib revisions, proof source, a build that includes the theorem module, and a transitive axiom audit. The standard allowlist is a subset of `propext`, `Classical.choice` and `Quot.sound`. Reject `sorryAx` and unapproved custom axioms. A proof that relies on native computation needs a separate, explicitly disclosed trust category; it does not pass the strict kernel-only policy.

For unreviewed generated proofs, use a sandbox without credentials or unnecessary network access. Replay proofs with `lean4checker`. For major claims, compare against a separately trusted challenge statement with `comparator` and an external checker. Even successful formal checking does not show that a mistranslated statement matches the intended conjecture. Review quantifiers, domains, assumptions, definitions and vacuous hypotheses independently.

Official guidance: [Lean proof validation](https://lean-lang.org/doc/reference/latest/ValidatingProofs/), [Lean community proof checklist](https://leanprover-community.github.io/did_you_prove_it.html), and [Formal Conjectures proof contribution policy](https://github.com/google-deepmind/formal-conjectures/blob/main/PROOFS.md). These links describe evolving tools; consult version-specific documentation before extending the pinned pilot. A general submission checker and independent external kernel are not yet implemented here.

## Research memory and evaluation

Retain the statement, source, exact input, proposal, verifier version, result, rejection reason, costs and superseding corrections. Reusing these records is retrieval-based learning. It does not imply that a model has been retrained.

Keep training examples, retrieved worked solutions and held-out evaluation problems separately labelled. Record any known overlap. Freeze benchmarks before comparison, report all attempted cases, and do not select only successful runs for public metrics. For a novelty claim, check the literature and known databases independently, retaining the search date and sources.

Verification policy reviewed on 9 November 2026.
