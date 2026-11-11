# Formal supporting algebra

This pilot checks four statements about a particular pair of integer equations:

\[
x+y=s,\qquad x-y=d.
\]

1. Every solution satisfies \(2x=s+d\) and \(2y=s-d\).
2. Any two integer solutions with the same \(s,d\) coincide.
3. For \(s=11,d=3\), the equations hold exactly when \(x=7,y=4\).
4. There is no integer solution for \(s=10,d=3\).

The last statement is specific to integers. Over the rationals, \(x=13/2,y=7/2\)
does solve that system. This distinction is a useful lesson about preserving a
problem's domain during formalisation.

These are established elementary results. They provide a small example of
formal proof checking alongside the Python experiments. They do not verify the
Python solver, arbitrary rational matrices or any Millennium Prize Problem.

## Reproduce

Install the official Lean version in `lean-toolchain`, then run from the
repository root:

```sh
python3 scripts/check_formal.py --lean /path/to/lean
```

The optional `--output runs/formal/evidence.json` saves an immutable evidence
file. The script checks the compiler version, runs the proof file, rejects
warnings and audits every theorem's transitive axioms against an explicit
allowlist. It accepts no unfinished proof or extra axiom. The `omega` tactic
constructs proof terms checked by Lean's kernel.

The workflow [formal.yml](../.github/workflows/formal.yml) uses an exact official
release archive and its SHA-256 digest, checked against GitHub's release
metadata on 9 November 2026. It downloads the pinned release asset through
GitHub's official release-asset API with `Accept: application/octet-stream`.
The ordinary release download URL returned HTTP 504 during the first run;
the API route retrieved the same checksum-verified archive. It has read-only repository permissions, no model
keys, no extra packages and a fifteen-minute timeout. The binary is downloaded
afresh to the disposable runner. Dependency download availability can prevent a
run; it does not change proof status.

## Additional fixed module: Q0001

The [Q0001 module](../research/agent-attempts/0002/IntegerCriterion.lean)
states necessary divisibility, an explicit integer witness, the exact
solvability criterion and uniqueness for `2x+3y=p` and `-x+4y=q`.
Its [original evidence](../research/agent-attempts/0002/formal-evidence.json)
records local checking on 9 November 2026. The module and the original pilot
are separate proof targets.

Run its dedicated check from the repository root:

```sh
python3 scripts/check_integer_criterion.py --lean /path/to/lean
```

The checker requires the reviewed source SHA-256 before executing Lean,
then checks the same pinned compiler and original axiom allowlist. A changed
statement requires a separate review before that source digest is updated.
All four expected reports must be present exactly once, with no warning,
compiler failure or unapproved axiom. The hosted formal workflow runs both
checkers. Unit tests use a compiler stub to test rejection paths; only actual
Lean execution checks the mathematics.

This extension does not formalise the general Q0004 theorem or verify any
Python implementation. It does not collect human or agent-learning outcomes.
The [11 November local replay](evidence/2026-11-11-q0001-local.json) records
actual execution of the dedicated checker against the checksum-verified Lean
distribution. Hosted execution is evidenced separately by its Actions run.

## Trust and review

Read the Lean statements in [Atlas.lean](Atlas.lean) and compare them with the
four claims above. Human review of their intended meaning remains necessary.
The current checks use Lean's own kernel and assumption audit; an independent
external checker is not part of this pilot. See the official
[Lean proof-validation guidance](https://lean-lang.org/doc/reference/latest/ValidatingProofs/).

`check_formal.py` is specific to this small, reviewed file. Its lexical checks
are a review aid and do not make arbitrary generated Lean code safe. Broader
automated proof submissions require a separate trusted challenge, sandboxed
execution and stronger independent verification. Do not send secrets into a
proof-building environment.

A successful local or GitHub run is the evidence for acceptance of these
statements under the recorded assumptions. The existence of this workflow or
documentation alone is not evidence that it passed.

## Recorded local verification

On 9 November 2026, the official archive's SHA-256 matched the pinned digest
and all four statements passed Lean 4.24.0 locally. Every printed dependency
report contained only `propext`, `Classical.choice` and `Quot.sound`.
The [machine-readable record](evidence/2026-11-09.json) preserves the full
compiler version, source hash and assumption reports. GitHub CI status must be
read separately from its workflow run; local success does not establish that a
remote run completed.
