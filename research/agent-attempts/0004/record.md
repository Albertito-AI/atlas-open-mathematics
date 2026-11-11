# Q0002: a prospective lesson-transfer pilot

11 November 2026. Work ID ATLAS-MATH-RESEARCH:Q0002-DESIGN-20261111. Base source `6de7f90ee7644015565bc0c9c329615f7760053f`. Prepared with OpenAI Codex assistance; exact model identifier and token usage unavailable. Zero new spending. This is a proposed study design and an executed mathematical calibration, with no collected learner outcomes.

## Question and frozen proposal

Does supplying the project's domain lesson increase joint mathematical correctness on fresh two-by-two linear-system tasks, relative to an equal-budget control? The scope is one specified model configuration and a small selected task set, not all agents or human learning. The earlier public examples and [Q0004 computation](../0003/record.md) are exposed material. Their successful checks provide no answer to this empirical question.

Before collecting responses, a separate case custodian must prepare and hash 12 fresh tasks, two in each of six strata: rational-only unique solutions, integral nonnegative unique solutions, integral unique solutions violating a stated nonnegativity constraint, singular consistent systems, inconsistent systems, and zero-row/zero-matrix boundaries. Assign each case one primary stratum before collection: any zero row or zero matrix goes to the boundary stratum; otherwise singular consistent/inconsistent classifications take precedence over unique-solution classes. Cases must be independently checked, avoid duplicates of public examples, and remain unavailable to response-producing agents before their assigned task. This run generates no hidden cases. The public generator is unsuitable as an unseen assessment source. Prior training exposure remains unknown even for newly composed tasks.

Create 12 matched pairs of isolated fresh sessions. Within each pair both receive exactly the same task, time/token budget, tool access and model configuration. Use a recorded fair random bit to allocate one session the exact pinned lesson and one an equal-token neutral control text that contains no task-solving instruction. The control is needed to distinguish lesson content from merely supplying additional context. Freeze both texts, prompt templates, model/provider/version, settings, budgets, allocation procedure, case hashes and scoring rubric in a dated execution manifest before the first response. Assignments are independent across pairs; sessions cannot communicate or see prior responses, case solutions, other lessons or score feedback. The case custodian and blinded scorers must not produce responses in either arm. No paid model capacity is authorised.

The primary outcome is binary joint correctness: the response must satisfy every explicit domain and feasibility requirement, give the correct classification, and supply a valid answer or obstruction with a sufficient justification. A correct rational solution to an integer question fails. A missing required nonnegativity check fails. An unsupported finite search for nonexistence fails. Unsupported novelty or fabricated proof claims fail the justification requirement. Freeze exact per-case accepted alternatives before collection; two blinded scorers resolve disagreements under that rubric, preserving both original judgements. Use the unchanged rational certificate verifier where applicable, alongside explicit integrality and problem-specific feasibility checks. Do not change verifier policy to accommodate responses.

Secondary descriptive fields: correct domain identification, exact substitution, valid obstruction, assumption errors, abstention, elapsed time and assistance. Do not replace the primary endpoint with whichever secondary score looks favourable. Capture every output, failure and timeout. A session initiated successfully but exhausting its budget receives zero primary correctness; a pre-start infrastructure failure makes its pair missing. Report missing pairs and reasons; do not repeatedly rerun adverse outputs. If fewer than 12 complete pairs exist, report an incomplete pilot without the preplanned confirmatory conclusion. No optional stopping or repeated significance checks.

## Decision rule and derivation

Let W count pairs where only the lesson session is correct and L pairs where only the control session is correct. Ignore tied pairs for this test and put m = W + L. Under the sharp null that lesson assignment changes neither session's binary outcome, independent fair within-pair randomisation makes the direction of every discordance a fair bit. Conditional on m, the one-sided exact tail is

$$
p=2^{-m}\sum_{j=W}^{m}{m\choose j}.
$$

At m = 0 use p = 1. The predeclared favourable direction is greater lesson correctness. Reject this sharp null only at p ≤ 1/20. This test does not establish the size, practical importance or generality of an effect. Report both groups' totals, all pair outcomes and the paired risk difference (W − L)/12 regardless of the decision. No significant result is guaranteed; the selected tasks and small sample make this a limited pilot. Future replication requires new cases and an independently frozen design.

[calibrate.py](calibrate.py) enumerates all 4,096 assignments of 12 fair bits for each m from 0 to 12, independently comparing enumerated tails against the binomial-sum formula using exact fractions. [calibration.json](calibration.json) preserves its actual output and source hash. Every conditional rejection probability is at most 1/20. For 12 discordant pairs, 9 lesson wins yield p = 299/4096 and 10 yield p = 79/4096. Hence a seemingly strong 9-to-3 split does not cross this threshold. The computation calibrates a mathematical rule under stated assumptions; it is not simulated evidence that agents improve.

Reproduce from the repository root:

```sh
python research/agent-attempts/0004/calibrate.py
```

## Rejected routes, teaching and next gate

Reusing public practice as unseen cases would contaminate the assessment. Scoring only a final number would overlook domain and feasibility failures. Replacing missing or wrong responses until a favourable run appears would change the study. Treating many proof examples as independent learners would confuse mathematical correctness with transfer. These routes are excluded prospectively; no actual learner trial failed in this run because none began.

Teaching exercise: with 12 discordant pairs, does a 9-to-3 lesson advantage satisfy the rule? No: 299/4096 exceeds 1/20. Does 10-to-2? Yes:79/4096 is below1/20, conditional on the design assumptions. Does this show that a human has learned? No human outcome was observed. More generally, if all pairs tie, both groups could be entirely correct or entirely wrong; the paired comparison alone cannot distinguish these situations, so report raw totals.

The accepted Opsbook exact-substitution lesson is reused as a scoring requirement for proposed certificates, with its original task scope. No new Opsbook instruction is promoted and no model weights are updated. This prospective design is open to independent review; any change before execution must receive a new dated version. The next gate is an independent case-custodian/scoring review and a fully frozen execution manifest. There is no reviewer-held dataset or ready-to-run learner study yet.

Novelty status: standard elementary randomisation reasoning, no novel mathematical claim. Formal status: exact finite calibration only, no Lean proof. Editorial status: working research record. Under [JOURNAL_HANDOFF.md](../../../docs/JOURNAL_HANDOFF.md), a future article on learning requires actual observations, appropriate claims, authorship/AI disclosures and independent editorial decisions; this record is not a submission or an accepted article. Confidential reviewer/case material must stay outside the public repository and private owner library. Original prose retains CC BY4.0; code retains MIT. Runtime allowance was one bounded local enumeration, without external services or spending.

## Verification record

The calibration ran successfully on 11 November 2026 and its full exact output is retained. Script SHA-256: `ee037713b02c16192a23ca41d5aa911a17b6a390c58fb344059e60885e729eb6`. The maximum conditional rejection probability among the 13 enumerated discordance counts is 9/256 (at m = 8), below 1/20. With four or fewer discordances, no outcome can reject under this rule, illustrating the pilot's limited resolution.

The 42 existing repository tests and repository validation of 62 JSON files, provenance, certificates and local documentation links passed. These checks do not collect or score learner responses. The earlier PR2 finite experiment was integrated without altering its source or claiming fresh research credit; its script hash remains `c6fe02a41b3baf3224e9f1d291b85a846d96f51fb60e97b280c6da4b4246658c`.

A separate critical-review agent independently replayed the calibration and matched every output row using a separate Pascal-recurrence computation. It found no publication blocker for this explicitly unexecuted proposal. It confirmed the sharp-null derivation, treatment of ties and maximum rate 9/256. Its two execution clarifications have been incorporated: custodian/scorers cannot produce responses in either arm, and overlapping boundary cases receive a frozen primary stratum. This is agent review, not external human peer review or approval to execute an unfrozen study.
