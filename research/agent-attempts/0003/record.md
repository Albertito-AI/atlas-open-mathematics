# Q0004: constructive witnesses and obstruction certificates

Date: 10 November 2026. Work ID: ATLAS-MATH-RESEARCH:Q0004-CERTIFICATES-20261110.
Base source: `e829b52ef6ca89e7409a7b950d829870f19529dd`.

## Target and contribution

For integer coefficients with D = ad − bc nonzero, Q0004 asks when the test D divides aq − cp guarantees an integer solution for every integer right-hand side (p,q). The proposed answer, gcd(|a|,|c|) = 1, already has an informal argument in [attempt 0002](../0002/record.md#next-question-q0004) and a subsequent supporting review. Neither is counted as new work here.

This attempt implements the constructive argument with extended Euclid, checks its certificates through the existing independently implemented rational verifier, and exhausts all matrices and right-hand sides whose entries lie in −3 through 3. It constructs a specific obstruction for each nonprimitive first column. Singular matrices are counted and excluded explicitly. The frozen finite target and bounds were recorded in the Atlas claim before execution. No fixed checker, proof policy or accepted theorem was changed.

## Construction and its boundary

For gcd(|a|,|c|) = 1, extended Euclid returns u,v with ua + vc = 1. If aq − cp = Dk, let r = p − bk and s = q − dk. Then as = cr. The candidate x = ur + vs, y = k satisfies ax = r and cx = s, hence both original equations. The script checks the Bézout identity before using the coefficients and submits every constructed pair to exact substitution with a nonzero determinant certificate.

For g = gcd(|a|,|c|) > 1, choose p = a/g and q = c/g. The y-numerator is zero, while the unique rational solution is (1/g,0). An accepted rational certificate and its nonintegral first coordinate establish failure of the single-test shortcut for that matrix. This is a counterexample, not a failed search.

The overbroad route “one numerator test always suffices” remains rejected. We retain its false positives in the experiment totals rather than silently filtering them. D = 0 is outside this experiment's target; division by D cannot be used to investigate those systems.

## Actual reproducible evidence

Run from the complete pinned repository checkout:

```sh
python research/agent-attempts/0003/check.py
```

[evidence.json](evidence.json) records the actual counts, exact inclusive bounds, an ordered-case digest, script hash and unchanged verifier hash. Every nonsingular matrix is tested against every right-hand-side pair in the bounds using exact fractions. The candidate formula and extended-Euclid construction are checked against substitution, not against a call back into the candidate solver. A digest is an integrity aid, not a mathematical proof. The script is deterministic public research code, authored for this question; it is not the daily practice generator or an agent-performance experiment.

The finite results do not close Q0004's universal formalisation acceptance gate. No new Lean theorem, external human review, novelty or learning improvement is asserted. Python and its exact-arithmetic implementation remain trusted dependencies.

## Reuse and next work

The accepted Opsbook rule `exact-substitution`, revision 1 in the [retained manual](../../cycles/2026-11-09-2c92f02000c3/opsbook/MANUAL.md), requires substitution and the appropriate uniqueness certificate before submission. This experiment applies that rule using the existing verifier. It does not promote a new Opsbook rule, rerun the synthetic bridge for research credit or update model weights.

The [teaching companion](../../../lessons/003-constructive-certificates.md) explains the construction and includes public exercises. Q0004 remains ready for formalisation. Q0002 still needs a matched evaluation design and fresh reviewer-held cases. A new prerequisite question, Q0005, asks how to classify integer solvability when D = 0, including zero rows and the zero matrix. This follows directly from the excluded boundary; it is a known-mathematics task, not a discovery claim.

## Provenance and limits

Prepared with OpenAI Codex assistance under Albert Tan's direction. Exact model identifier and token usage are unavailable. Execution used existing local Python capacity and no new spending. Research budget: one finite experiment, 120 seconds maximum per replay; no paid model calls. Source background is the established inverse/divisibility theory cited and inspected in attempt 0002 (MIT Lecture 20, pp. 1–2; Greenwell and Kertzner 2009, pp. 49–53); no new literature or Millennium-status claim is made here. Original code retains MIT terms; original teaching prose retains CC BY 4.0 under the repository licences.

Journal suitability: this is a public technical teaching companion, not a submission-ready scholarly article. A future account of reasoning and transfer would need its own contribution, evidence, authorship declarations and ordinary independent editorial process under [JOURNAL_HANDOFF.md](../../../docs/JOURNAL_HANDOFF.md). No article was sent or accepted. No private school, membership or editorial material is included.

## Review and results

A separate critical-review agent independently replayed `check.py` on 10 November 2026: exit code 0, empty standard error and JSON exactly matching the preserved evidence. It also enumerated the bounds using integer numerator divisibility, without Fraction or the project solver, and reproduced all counts: 2,112 nonsingular matrices, 289 singular exclusions, 103,488 matrix/right-hand-side combinations, 27,040 constructed integer witnesses, 672 obstruction witnesses and 10,944 false positives for the unrestricted shortcut. There were 1,056 negative determinants and 936 matrices containing zero entries. The reviewer checked signed extended Euclid and confirmed that the verifier was unchanged. No defect was found within this finite scope. This is independent agent review, not external human peer review.

The repository's 42 existing tests passed; its validator checked 45 JSON files and documentation links. No universal formal result is inferred from these checks. The new evidence is suitable for review as a research PR, with Q0004's formal gate still open.
