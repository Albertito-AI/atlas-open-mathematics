# Research protocol

**Version 0.1. Research records, verification and cumulative learning.**

This protocol is an interchange and review contract for people and agents. A JSON record documents a claim; it does not execute an agent or certify a result. Use a pull request to submit a proposed record and its reproduction files.

## 1. Define the question before searching for an answer

A problem card identifies the exact task and its relationship to prior work. Use a stable identifier. If the statement changes materially, retain the old version and issue a new revision with the reason.

```json
{
  "problem_id": "example-linear-001",
  "revision": 1,
  "title": "Solve a coupled linear system exactly",
  "statement": "Find rational x and y satisfying 2x + y = 5 and x + 3y = 5.",
  "domain": "rational numbers",
  "assumptions": ["Both equations must hold simultaneously."],
  "sources": [],
  "prior_work": "An original exercise in established linear algebra.",
  "novelty_status": "known-mathematics-exercise",
  "acceptance": "Substitution into both equations must produce exact equality.",
  "resource_limit": {"new_external_spend": 0, "time_minutes": 15}
}
```

This example has solution `x = 2`, `y = 1`. Its empty source list is appropriate for a newly written exercise; research cards need the relevant primary sources and precise locations. Record whether you read the full source, an abstract or metadata only.

### Supported pilot submissions

The implemented CLI checks 2 by 2 systems over the rationals. Save this instance as `case.json`:

```json
{
  "id": "example-linear-001",
  "A": [[2, 1], [1, 3]],
  "b": [5, 5],
  "kind": "unique"
}
```

Save a proposed answer as `candidate.json`:

```json
{
  "status": "unique",
  "solution": ["2", "1"],
  "certificate": {"determinant": "5"}
}
```

Run:

```sh
python -m atlas_math verify --case case.json --candidate candidate.json
```

The exit status is 0 for a verified candidate, 1 for a rejected mathematical claim, and 2 for malformed input. Include the original inputs and actual output in your pull request. Accepted scalars are integers or canonical rational strings; floating-point inputs are inappropriate for this exact checker.

The other supported candidate statuses are `inconsistent`, with `certificate.row_weights`, and `underdetermined`, with a particular `solution` and `certificate.null_vector`. The checker tests the corresponding equalities and non-zero conditions. A candidate's asserted status is not accepted merely because it agrees with a label in the input.

Generate a practice instance with `python -m atlas_math generate --seed 31 --output case-31.json`. This command refuses to overwrite an existing file. The generator's examples are established mathematics and have no claim to research novelty.

## 2. Record an attempt

Keep a finite, understandable account of the mathematical work: hypotheses, derivations, computations, rejected possibilities and evidence. The record is an authored research account. It need not contain every intermediate token or claim to expose inaccessible model internals.

An external attempt record should include:

| Field | Required content |
| --- | --- |
| `attempt_id` | Stable unique identifier. |
| `problem_id`, `problem_revision` | Exact target. |
| `actor` | Responsible contributor, assistance disclosure and actual model version if available. |
| `inputs` | Source commit, relevant files, sources and manual revision. |
| `hypothesis` | The proposition or method being investigated. |
| `method` | Reproducible steps, code or proof artefacts. |
| `candidate` | The proposed answer, construction, proof or counterexample. |
| `checks` | Commands, checker versions, outputs and their scope. |
| `outcome` | What the evidence establishes and what remains unresolved. |
| `resources` | Recorded elapsed time and known compute or model usage; use `unknown` where unavailable. |
| `lesson` | A reusable insight, its conditions and a counterexample to overgeneralisation, if justified. |
| `supersedes` | Earlier record identifier and reason when correcting a record. |

The exact-arithmetic pilot has its own generated record format. Preserve that original output when adding a wider research account; do not rewrite it to imply that a live agent produced the scripted candidate.

## 3. Keep status dimensions separate

| Dimension | Examples |
| --- | --- |
| Verification | `unreviewed`, `check-failed`, `finite-check-passed`, `certificate-checked`, `formal-proof-checked`, `independently-reviewed` |
| Novelty | `known-result`, `known-mathematics-exercise`, `literature-check-pending`, `potentially-new`, `novelty-independently-assessed` |
| Publication | `working-record`, `preprint`, `submitted`, `accepted`, `published`, `corrected`, `retracted` |

These are descriptive labels requiring evidence. They are not automatic promotion stages. An independently reviewed numerical experiment may establish no universal theorem. A formally checked proof can depend on an inaccurately translated statement. A public GitHub record has not thereby undergone journal peer review.

## 4. Verify independently

Retain the original instance or statement outside the solver's authority. The verifier checks the candidate against that target. Where possible, use a method different from the candidate producer, such as exact substitution to check a solution obtained by elimination.

For finite search, record the search space and whether it was exhausted. A found example establishes existence within its stated scope. Failure to find an example may establish only the limits of the search.

For formal proofs, record the theorem statement, definitions, axioms, toolchain and library versions. Check for unfinished dependencies and unapproved assumptions. Have a qualified reviewer compare the formal statement with the original question. For significant claims, add independent proof replay and broader expert scrutiny.

Source, checker and statement changes must be reviewed separately from an attempted proof that depends on them. A solver cannot weaken a check to promote its own result.

## 5. Learn from the attempt

Retain useful successes and failures. Distinguish a mathematical counterexample, a programming error, an unsupported assumption, an inconclusive search and exhausted resources.

An Opsbook candidate needs an observed case, an instruction, conditions for applying it and cases testing both the intended repair and unaffected behaviour. Promotion of a procedural rule means that it passed the specified evaluation. Its validity beyond those cases remains an empirical question.

Once an agent has seen an assessment case or its outcome, treat it as exposed material. Use later cases or independent projects to evaluate broader transfer. Do not call public seeded cases a hidden exam. When model training data are unknown, disclose possible prior exposure rather than claiming a clean benchmark.

## 6. Select the next problem

Propose a next question because it clarifies an assumption, generalises a supported result, investigates an obstruction or meets an identified educational need. Check the literature and existing register for duplicates. Explain its mathematical significance and likely verification method.

Automatically generated variants remain exercises unless there is evidence of a genuinely new research question. Difficulty estimates are provisional. Selection should balance significance, tractability, verification cost and teaching value.

## 7. Preserve and communicate

Keep accepted evidence in version control. Append corrections and link superseded records. Cite exact commits in reports and lessons so readers can recover the evidence used at publication. Record necessary external dependencies and licence conditions.

Prepare human explanations under the [teaching protocol](TEACHING.md). A journal candidate follows the [editorial handoff](JOURNAL_HANDOFF.md). No worker may assign journal acceptance or a Millennium solution status to its own output.

The initial resource policy permits zero new external spending. Work pauses with a recorded reason when authorised capacity is unavailable. Scheduled work must leave evidence of its actual execution and outcome.
