# Independent agent review of Q0001

Reviewed on 9 November 2026 by a separate OpenAI Codex agent assigned to mathematical review, followed by root integration replay. The reviewer did not write or edit the theorem source or its evidence. This is agent review, without a claim of external human peer review.

## Mathematical statement

The target is correct for all integer `p,q`. Necessity follows from `p + 2q = 11y`; sufficiency uses `y = k,x = 4k − q` when `p + 2q = 11k`. The determinant is 11, giving uniqueness over the rationals and hence uniqueness whenever an integer solution exists. Negative and zero inputs are included. Nonnegative allocations are outside the statement.

The general two-numerator criterion and the counterexample `A = [[2,2],[2,4]], (p,q) = (1,2)` were checked independently. The unique rational solution is `(0,1/2)` and the first numerator alone passes. The broader shortcut is false.

The proposed Q0004 classification by `gcd(|a|,|c|) = 1` was also independently assessed. The Bézout construction and the witness `(p,q) = (a/g,c/g)` for `g > 1` establish the two directions informally. The nonzero determinant excludes `g = 0`. This assessment does not constitute formal checking of Q0004 or novelty verification.

## Formal source and replay

Reviewed `IntegerCriterion.lean`, `formal-evidence.json`, the repository research/verification instructions and the relevant checker/toolchain files. The equivalence matches the frozen Q0001 statement: all variables and witnesses are `Int`, both equations are required, and the right side is exactly `11 ∣ p + 2*q`. No target theorem is assumed and no extra mathematical hypothesis is introduced.

There is no `sorry`, custom axiom, native computation or other proof escape in the inspected source. The four declarations establish necessity, the witness, equivalence and uniqueness. The reviewer independently executed:

```text
/tmp/atlas-lean-4.24/bin/lean research/agent-attempts/0002/IntegerCriterion.lean
```

Exit code was 0. All four printed axiom reports exactly matched `formal-evidence.json`, containing only existing allowed axioms. The source, compiler executable, audit script and toolchain manifest SHA-256 hashes matched the evidence. The compiler version matched Lean 4.24.0 and its recorded commit. The fixed checker and toolchain paths had no working-tree changes. A further root replay is preserved in `integration-replay.json`.

## Sources and limits

The reviewer inspected MIT OpenCourseWare's Lecture 20 summary, pp. 1–2, and Greenwell and Kertzner (2009), pp. 49–53, at the links and pinpoints in `record.md`. The former supports Cramer's rule; the latter documents existing integer matrix solvability theory. No exhaustive novelty search was performed, and no publication stating the exact Q0004 formulation was located and inspected.

No defect was found within this reviewed scope. Replay used the same installed Lean distribution, rather than an external kernel implementation. The review does not certify remote CI for this new module, Python correctness, future formalisation of Q0004, learning gains or a Millennium result. The final packaging review is recorded below.

## Final package review

The same independent reviewer subsequently inspected the final record, problem card, lesson 002, README, queue and finite-check script. It replayed the script and confirmed byte-equivalent JSON data: 529 parameter pairs, 49 integer solutions, 121 residue inputs, image size 11 and zero mismatches. The counterexamples, batching example and exercise solutions were checked. The repository validator passed 44 JSON files and local documentation links. No publication blocker was found in that scope. Final integration changed only mathematical display delimiters for GitHub rendering and removed a duplicate source link.
