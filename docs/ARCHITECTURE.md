# Architecture and development boundaries

Atlas Open Mathematics connects research records, independent checks, procedural memory and teaching. The project begins with a small exact-arithmetic pilot so that each boundary can be inspected before broader research is attempted.

## Components

| Layer | Initial responsibility | Development boundary |
| --- | --- | --- |
| Problem register | Identify a question, sources, assumptions and scope. | The Millennium map is a research plan, not evidence of progress on its conjectures. |
| Attempt producer | Produce a candidate answer and a reproducible record. | The initial solver is deterministic. Live model adapters require separately documented authorised capacity. |
| Verifier | Check the candidate against the original instance using exact arithmetic. | Its guarantee is limited to the supported class of problem and the checker's implementation. |
| Formal pilot | Check a small, reviewed family of integer-equation statements in Lean. | This separate pilot does not prove the Python implementation correct or accept arbitrary generated proofs. |
| Evidence store | Retain attempts, results and version information. | A content hash detects changed bytes; it does not prove a claim true or establish authorship. |
| Procedural memory | Use Opsbook to test and retain conditions for useful checks. | A procedural instruction is not a mathematical theorem or a change to model weights. |
| Teaching | Explain the method, assumptions, mistakes and applications. | Improved learning requires observation and assessment, beyond publication of an explanation. |
| Editorial handoff | Prepare a candidate article with a reproducible evidence package. | The Human Question makes its own human editorial decisions. |

## Separation of responsibilities

The candidate producer and verifier must remain separate. A solver may propose an answer; it cannot declare that its own proposal has passed an independent check. A proposed change to the checker, problem statement or acceptance threshold needs separate review.

Research memory has two parts. The evidence archive retains what happened. The accepted operations manual selects instructions for later work. A failed attempt may justify retaining a warning or a narrower method; it does not automatically justify a universal rule.

## Existing Atlas connections

[Atlas Opsbook](https://github.com/Albertito-AI/atlas-opsbook) provides revisioned procedural memory and evaluation of proposed rules. The integration must record the exact upstream version and retain its licence. Run records should identify the manual revision used.

[RegNav Source Watch](https://github.com/Albertito-AI/regnav-source-watch) offers evidence relationship and change-detection patterns. Adapting these to theorem dependencies requires new mathematics-specific code. A changed source should trigger review of dependent claims; it should not silently rewrite their truth status.

[CommCode](https://github.com/Albertito-AI/CommCode) offers a controlled editing and checking workflow. Any integration must retain its applicable licence and execution boundaries. It is not a proof checker.

Atlas Agent School informs the curriculum design. Only deliberately selected and appropriately licensed public exports belong here. Its private assessments, learner records and institutional material remain outside this repository.

## Formal proof development

The [elementary formal pilot](../formal/README.md) contains four statements about integer equations, a pinned Lean toolchain and a theorem-specific checker with an axiom audit. Its documentation identifies the precise scope and trust assumptions. A successful check must be evidenced by an actual local or GitHub run.

A broader Lean and mathlib track must preserve a trusted target statement, pin toolchain and library versions, inspect transitive axiom dependencies and replay proofs independently. Rejecting unfinished proofs is necessary. It is also necessary to inspect whether the statement and definitions express the intended mathematics. Accepting arbitrary generated code requires additional isolation and a trusted challenge statement; the reviewed pilot's source checks do not provide that boundary.

Lean's [proof validation guidance](https://lean-lang.org/doc/reference/latest/ValidatingProofs/) explains these boundaries. The [Formal Conjectures project](https://github.com/google-deepmind/formal-conjectures) offers an existing corpus to consult, with its own warnings about formalisation accuracy and its own licences.

No local formal proof file, empty checker scaffold or passing unrelated build can establish a Millennium result.

## Scheduling and resources

Each worker needs a bounded assignment, a deadline, a checkpoint and an explicit record of resource use. Repeated work must be idempotent or identify why a new attempt is warranted. Exhausted capacity leaves a paused task with a reason, rather than silently switching to paid services.

Ordinary repository checks can run through GitHub Actions. Live research requires an actual executing agent and authorised model capacity. A schedule alone does not establish either. Public status should distinguish scheduled, started, completed, failed and paused work.

## Initial acceptance milestone

The first milestone is an inspectable cycle: generate a known-mathematics exercise, observe a flawed answer, reject it with a separate check, record a useful lesson, test a corrected method on additional cases and publish an explanation. Broader claims of transfer or research ability need independent trials designed before results are seen.
