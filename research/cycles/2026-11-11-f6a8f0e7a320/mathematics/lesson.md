# Exact linear systems: a reproducible teaching pilot

This run uses synthetic public cases and predetermined programs. No live AI
model was called, no language-model weights were updated, and no novel theorem
or Millennium Prize progress is claimed.

The deliberately flawed baseline treats each equation separately by dividing
its right-hand side by the corresponding diagonal coefficient. Coupled equations
also contain the other variable, so this shortcut can fail. It remains valid for
diagonal systems with nonzero diagonal entries; the lesson therefore has a scope.

The corrected solver handles unique solutions, inconsistency and infinitely many
solutions. A separate checker substitutes a proposed solution into every original
equation. Uniqueness additionally requires the correct nonzero determinant;
nonuniqueness requires a nonzero null vector; inconsistency requires a linear
combination of rows with zero coefficients and a nonzero right-hand side.

For seed 20261111, the baseline passed 0 of 6
exact checks and the predetermined corrected solver passed
6 of 6. These are results on six generated
public practice cases, not an estimate of general intelligence or learning.
Fresh generated variants exercise transfer of the procedure, but they are public
practice and are not a protected evaluation.

Inspect `attempts.jsonl` and each content-addressed record in `records/` to see
the actual matrices, candidate answers, certificates and rejection reasons.
To teach this result, ask a learner to explain the failure, solve a new coupled
case, handle singular cases, and justify why each certificate proves its claim.
Independent learner performance has not been measured by this demonstration.

All mathematical methods used here are standard elementary linear algebra.
An exact arithmetic certificate check is different from formalisation in a
general proof assistant. The implementation and its tests remain inspectable.
