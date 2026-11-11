# Integer certificate protocol

This is the implemented data contract for
[`atlas_math/challenges.py`](../atlas_math/challenges.py). The
[research briefs](AGENT_CHALLENGES.md) explain the wider work programme.
The laboratory checks bounded mathematical claims using exact arithmetic;
it does not run an agent, execute candidate code, or establish that a model
fits a real operating situation.

```sh
python -m atlas_math.challenges describe
```

Use the command's output and the implementation at the revision being tested
when constructing a candidate.

## 1. A complete runnable example

The following uses the public demonstration's actual case and
`reference_candidate`. It invents no case identifier. Choose a new directory
if `/tmp/atlas-certificate-example` already exists.

```python
import json
from pathlib import Path
import subprocess
import sys

directory = Path("/tmp/atlas-certificate-example")
directory.mkdir()
run = subprocess.run(
    [sys.executable, "-m", "atlas_math.challenges", "demo"],
    check=True, text=True, capture_output=True,
)
report = json.loads(run.stdout)
record = next(item for item in report["records"] if item["family"] == "branching")
for filename, value in (
    ("demo.json", report),
    ("case.json", record["case"]),
    ("candidate.json", record["reference_candidate"]),
):
    with (directory / filename).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")
print(record["case"]["case_id"])
print(json.dumps(record["reference_candidate"], indent=2))
```

From the source checkout, check the extracted candidate:

```sh
python -m atlas_math.challenges verify \
  --case /tmp/atlas-certificate-example/case.json \
  --candidate /tmp/atlas-certificate-example/candidate.json
```

The demonstration also supplies `allocation` and `obstruction` records. Change
the selected family in a fresh directory to inspect those certificates. This
reproduces published constructions and is not an unseen challenge.

To obtain a problem without its candidate in the output:

```sh
python -m atlas_math.challenges generate \
  --family allocation --size 8 --seed 7 \
  --output /tmp/atlas-allocation-case.json
```

`generate` requires an existing parent directory and refuses to overwrite its
output. The generator's source remains public. Keeping its answer out of one
output file does not turn it into a protected examination.

## 2. Exact case fields

The case contains exactly these fields:

| Field | Required value |
| --- | --- |
| `schema_version` | The string `atlas-integer-work-v1`. |
| `case_id` | The identifier computed from the exact case payload. |
| `A` | A rectangular integer matrix with at least one row and column. |
| `b` | One integer right-hand side per row. |
| `lower`, `upper` | Integer lower and upper bounds, one per variable. |
| `cost` | Integer objective coefficients, one per variable; the objective is minimisation. |

Every variable is an integer. All equations $Ax=b$ and component bounds
must hold simultaneously. A lower bound greater than its corresponding upper
bound represents an empty box, for which a suitable infeasibility certificate
can be supplied.

The identifier is `integer-` followed by the SHA-256 digest of the case payload
excluding `case_id`, using the module's canonical JSON representation. Use
`generate_challenge()` or `make_case()` to create it instead of inventing or
manually editing the digest:

```python
from atlas_math.challenges import make_case, verify_certificate

case = make_case(
    A=[[3, 2], [1, 5]], b=[8, 7],
    lower=[0, 0], upper=[10, 10], cost=[1, 1],
)
candidate = {
    "case_id": case["case_id"],
    "claim": "feasible",
    "solution": [2, 1],
}
verdict = verify_certificate(case, candidate)
assert verdict["accepted"] is True
assert verdict["optimality_proved"] is False
```

This example asks only for feasibility. It deliberately supplies no optimality
proof. The case hash binds the mathematical input bytes; it does not establish
authorship, provenance of external data or correctness of the model.

## 3. Candidate fields

Unknown fields are rejected. Every candidate copies `case_id` from its target
and declares one supported `claim`:

| Claim | Additional fields | Review performed |
| --- | --- | --- |
| `feasible` | `solution` | Check an integer vector against every original equality and bound. |
| `bound` | `solution`, `row_weights` | Check feasibility, then compute a justified rational and integer objective lower bound. |
| `optimal` | `solution`, `proof` | Check feasibility and a proof that no admissible vector is cheaper. |
| `infeasible` | `proof` | Check that the entire bounded integer domain is excluded. |

`solution` has one integer per column. `row_weights` has one entry per row.
For objective bounds and interval contradictions, weights may be integers or
canonical reduced rational strings, such as `"7/5"` or `"-1/5"`. Floating-point
numbers and unreduced strings such as `"2/4"` are rejected. An integral rational
string uses the canonical integer spelling, such as `"2"`, rather than `"2/1"`.

A `bound` verdict reports `objective`, `lower_bound`, `integer_lower_bound`,
`rational_gap`, `integer_gap` and `optimality_proved`. An accepted bound may
retain a positive gap. Acceptance then establishes that bound, not optimality.
When the feasible objective equals the rounded-up lower bound, the same
certificate establishes optimality.

## 4. Proof nodes

A proof is one node or a nested tree with exactly the fields stated below.
Node bounds are inherited from the target and any ancestor splits.

| `type` | Other fields | Acceptance condition |
| --- | --- | --- |
| `bound` | `row_weights` | The rounded-up objective lower bound is at least the supplied feasible witness's cost. Available for an `optimal` claim. |
| `contradiction` | `row_weights` | A weighted equality requires a value outside the attainable interval of its left-hand side on this box. |
| `modular` | `row_weights`, `modulus` | An integer row combination, after fixed-variable substitution, has all free coefficients divisible by the modulus but a residual right-hand side that is not. |
| `empty` | No additional fields. | At least one inherited lower bound exceeds its upper bound. |
| `split` | `variable`, `at`, `left`, `right` | Both child proofs pass after an exhaustive integer split. |

### Objective lower bound

For row weights $w$, let $r=c-A^Tw$. The checker computes

$$
L=w^Tb+\sum_j\min(r_j\ell_j,r_ju_j).
$$

Every admissible integer vector has objective at least $\lceil L\rceil$.
An optimality leaf requires this integer bound to reach the claimed optimum's
cost. An objective bound alone cannot establish infeasibility.

### Interval contradiction

The weighted equality is $(w^TA)x=w^Tb$. Let its coefficient vector be
$a$. The current component bounds imply

$$
\sum_j\min(a_j\ell_j,a_ju_j)
\le a^Tx\le
\sum_j\max(a_j\ell_j,a_ju_j).
$$

The leaf succeeds only when $w^Tb$ lies strictly outside that interval.
This condition is sufficient for contradiction; failing this test does not
establish feasibility.

### Modular obstruction

Here row weights and the modulus must be integers. From
$a^Tx=r$, subtract $a_j\ell_j$ from the right-hand side for every
variable fixed by $\ell_j=u_j$. All remaining free coefficients must be
divisible by the modulus, while the adjusted right-hand side must have a
nonzero remainder. An integer solution would contradict those two conditions.

### Exhaustive branching

`variable` is a zero-based column index. `at` is an integer $k$ satisfying
the current $\ell_i\le k<u_i$. The left child replaces $u_i$ with
$k$; the right child replaces $\ell_i$ with $k+1$. These branches
are disjoint and cover every current integer value. Both must be proved.
Other coordinates and the original equalities remain unchanged.

For an optimality claim, contradiction leaves may exclude parts of the domain
and bound leaves must close the cost gap in every remaining part. For an
infeasibility claim, every branch must end in a permitted contradiction.

## 5. Current implementation limits

| Input | Limit |
| --- | --- |
| Rows and columns | Each from 1 through 64. |
| Case integers, solution coordinates, split values and modular row weights | Absolute value at most $10^{30}$; Boolean values are rejected. |
| Rational certificate weights | Numerator magnitude and denominator at most $10^{120}$, with at most 256 characters for a string. |
| Modular obstruction modulus | Integer from 2 through $10^{12}$. |
| Proof nodes | At most 257 over the whole tree. |
| Proof depth | At most 64 edges from the root. |
| Each CLI JSON input file | At most 2,000,000 bytes; duplicate keys are rejected. |
| Public generator size | From 4 through 64 variables; the branching family requires an even size. |
| Public generator seed | Integer from 0 through $2^{63}-1$. |

These are data and verification limits. They are not a general wall-clock
timeout, CPU quota, operating-system sandbox, measure of intelligence or
promise of difficulty. The Python API trusts the host process and operates
on supplied in-memory values; the CLI additionally bounds each input file.

## 6. Results and unsupported proofs

The command exits with 0 when the stated claim is accepted, 1 when a validly
formed certificate does not establish it, and 2 for invalid or unsupported
input or an input/output failure. A verifier verdict is JSON on standard
output; input-loading failures are reported on standard error. Preserve the
actual verdict and reason rather than rewriting rejection as mathematical
nonexistence.

The rejection of a proof format says nothing by itself about whether the
underlying claim is true. For a stronger construction, general lattice
argument, formal proof or other unsupported certificate, submit the exact
target and evidence through a separately reviewed research route. Propose
checker extensions independently from the candidate that needs them.
Do not modify acceptance rules retrospectively to make a result pass.

The implementation uses established certificate ideas with public synthetic
constructions. Its result concerns the submitted bounded model. Novelty,
semantic model adequacy, independent external proof checking and learner
improvement require their own evidence under the
[research protocol](RESEARCH_PROTOCOL.md) and [verification rules](VERIFICATION.md).

Prepared with AI assistance. Original prose retains
[CC BY 4.0](../LICENSE-CONTENT.md); implementation code retains
[MIT](../LICENSE) terms.
