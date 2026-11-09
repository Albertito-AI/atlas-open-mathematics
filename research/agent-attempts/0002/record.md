# Q0001: an exact integer-solvability criterion

9 November 2026. Attempt `live-agent-0002`, problem revision 1. Source base: [`0fcb42f3e52853a46116ce835338c3d9f84e8c1b`](https://github.com/Albertito-AI/atlas-open-mathematics/tree/0fcb42f3e52853a46116ce835338c3d9f84e8c1b).

**Outcome:** the parameterised system has an integer solution exactly when `11` divides `p + 2q`. Four supporting statements, including the equivalence and uniqueness, passed the pinned Lean kernel and axiom audit. A separate agent reviewed the statement and proof and replayed the same source. This is a reproduction of established elementary mathematics. The new contribution to this project is a checked, reusable record and a [human lesson](../../../lessons/002-integer-feasibility.md).

| Attribute | Status and evidence |
| --- | --- |
| Verification | Local formal checking, independent agent review and replay, and finite supporting computations. |
| Novelty | Known mathematics. No new theorem or Millennium result claimed. |
| Publication | Public research working record. No journal submission, acceptance or external expert peer review. |
| Knowledge transfer | Lesson and public exercises prepared. Transfer to humans or fresh agent tasks has not been measured. |

## Fixed question and proof

For every pair of integers `p,q`, determine whether integers `x,y` exist with

$$
2x+3y=p,\qquad -x+4y=q.
$$

The [problem card](problem-card.json) preserves the statement. The target was recorded in the private Atlas work claim before the proof was produced. Negative and zero integers are included; nonnegative quantities are a separate condition.

If both equations hold, adding the first equation to twice the second gives

$$
p+2q=11y.
$$

Thus divisibility by 11 is necessary. Conversely, if `p + 2q = 11k` for an integer `k`, take

$$
y=k,\qquad x=4k-q.
$$

Substitution gives `2x + 3y = 11k − 2q = p` and `−x + 4y = q`. Divisibility is sufficient. If two solutions exist, subtraction gives `11(y − v) = 0`, and then `x − u = 0`. The solution is unique.

Over the rationals the same calculation gives

$$
x=\frac{4p-3q}{11},\qquad y=\frac{p+2q}{11}.
$$

For `p = 5,q = 3`, the integer solution is `(1,1)`. For the earlier example `p = 7,q = −2`, `p + 2q = 3`, so there is no integer solution, although the rational solution `(34/11,3/11)` exists.

## What was checked

The producer created [IntegerCriterion.lean](IntegerCriterion.lean), importing only the arithmetic tactic bundled with Lean. Its four declarations establish necessity, an explicit witness, the full equivalence, and uniqueness. [Formal evidence](formal-evidence.json) records all declarations, complete compiler output, hashes and limitations. The [independent review](review.md) checks the quantifiers and domain against the original statement. A further [integration replay](integration-replay.json) reproduced the output.

The source SHA-256 is `8101d90754600546e65b344f2eb41fbc88b66f956e68addc318319f42c2629e9`. Lean is version 4.24.0, compiler commit `797c613eb9b6d4ec95db23e3e00af9ac6657f24b`, with the distribution pinned in [formal/toolchain.json](../../../formal/toolchain.json). All axiom reports contain only members of the existing allowlist: `propext`, `Classical.choice`, `Quot.sound`. No unfinished proof or custom axiom is present. The fixed pilot and acceptance checker were unchanged.

Use that pinned distribution from the repository root:

```sh
lean research/agent-attempts/0002/IntegerCriterion.lean
python research/agent-attempts/0002/check_examples.py
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

The first command is a direct build of this new theorem module. The existing hosted formal workflow builds the original `formal/Atlas.lean`, so its success must not be presented as hosted checking of this module. Replay used the same installed Lean distribution, without a separate external kernel implementation. The Python verifier is not formally proved correct by these theorems.

The [finite check script](check_examples.py) proposes exact rational solutions and sends them to the unchanged substitution verifier. It checked all 529 pairs `−11 ≤ p,q ≤ 11`; 49 had integer solutions and there were no criterion mismatches. Separately, enumerating all 121 pairs of residues modulo 11 produced an image of 11 pairs, exactly matching the divisibility condition. These are bounded checks supporting the teaching examples. The universal claim rests on the proof. [Finite evidence](finite-evidence.json) preserves the actual output and script/verifier hashes.

## A shortcut that fails

For a general integer system

$$
ax+by=p,\qquad cx+dy=q,\qquad D=ad-bc\ne0,
$$

Cramer's formula gives numerators `dp − bq` and `aq − cp`. Both must be divisible by `D` for the unique rational solution to be integral. One successful numerator check is insufficient in general.

Take `A = [[2,2],[2,4]]` and right-hand side `(1,2)`. Then `D = 4`, the first numerator is `0` and the second is `2`. The first test passes, but the unique rational solution is `(0,1/2)`. The equation `2x + 2y = 1` also directly rules out an integer solution. The existing verifier accepted the rational certificate; it did not certify integer feasibility. This counterexample rejects the broader shortcut, while Q0001 remains valid for its specified matrix.

## Next question Q0004

For nonsingular integer `A`, when does checking `D | aq − cp` alone guarantee integer solvability for **every** integer right-hand side?

The independently reviewed proposed classification is

$$
\left[\forall p,q\in\mathbb Z,\quad D\mid aq-cp\implies
\exists x,y\in\mathbb Z:\ ax+by=p,\ cx+dy=q\right]
\quad\Longleftrightarrow\quad \gcd(|a|,|c|)=1.
$$

For sufficiency, write `aq − cp = Dk`, set `r = p − bk`, `s = q − dk`, and observe `as = cr`. Bézout's identity supplies integers `u,v` with `ua + vc = 1`. Put `x = ur + vs` and `y = k`. Then `ax = r` and `cx = s`, which verifies both equations.

For necessity, `D ≠ 0` ensures that `g = gcd(|a|,|c|)` is positive. If `g > 1`, take `p = a/g`, `q = c/g`. The tested numerator vanishes, yet the unique rational solution `(1/g,0)` is not integral.

This generalisation has an informal proof reviewed by a separate agent. It has not been formalised in this attempt. It is classified as an elementary consequence of established Diophantine theory; the exact formulation was not located in a publication during a non-exhaustive search, and no novelty claim follows. The next bounded assignment is to freeze and formally verify both directions, including signed and zero coefficients.

## Teaching and possible use

The companion lesson explains indivisible batching with a different matrix and checked example. Integer feasibility can prevent a fractional answer from being mistaken for a plan involving whole items. Nonnegativity, capacities, measurement error and usefulness in an actual setting require additional modelling. No deployment or measured social benefit has occurred.

Q0002 remains a separate evaluation task: freeze fresh reviewer-held cases and a rubric before comparing agent responses. The exercises here are already public and cannot be treated as unseen assessment material. Remembering this procedure through Atlas records is retrieval-based learning; no model-weight update is evidenced.

## Sources and provenance

1. MIT OpenCourseWare, *18.06SC Linear Algebra*, Fall 2011, Lecture 20 summary, [“Cramer's rule, inverse matrix, and volume”](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/f6e46da0d783d8f9c0a25c407c76166a_MIT18_06SCF11_Ses2.7sum.pdf), pp. 1–2: the two-by-two inverse and Cramer's rule. The divisibility test is our elementary deduction for integer coefficients.
2. Raymond N. Greenwell and Stanley Kertzner, [“Solving Linear Diophantine Matrix Equations Using the Smith Normal Form (More or Less)”](https://sites.hofstra.edu/raymond-greenwell/wp-content/uploads/sites/9/2019/07/Smith_Normal_Form.pdf), *International Journal of Pure and Applied Mathematics* 55(1) (2009), 49–60, especially pp. 49–53, Theorems 1–2 and the full-rank case. This is established background on integer matrix solvability; the exact Q0004 formulation is not attributed to it.

Relevant source pages were inspected on 9 November 2026. The project lead is Albert Tan. This record, proof and lesson were produced with OpenAI Codex agents; a separate agent supplied mathematical review and replay. A precise underlying model identifier, token count and elapsed runtime were not exposed in the research record. Existing interactive capacity and local tools were used, with no paid API calls or new external spending. This is an authored mathematical account, with reproducible evidence rather than a transcript of inaccessible model internals. No earlier accepted record is superseded.
