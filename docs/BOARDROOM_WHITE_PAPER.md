# When does an emissions bonus reward the worse proposal?

**Atlas Open Mathematics technical white paper, version 1.0 · 28 November 2026**  
Project director: Albert Tan Sin Hon

## Abstract

Under what conditions does a manager earn a bonus by choosing the higher-emissions proposal? In the Boardroom Bonus game, both parties have complete and accurate figures. The manager's contract counts emissions from the firm's own operations. The board also counts suppliers. For the two proposals in the game, no positive threshold applied to own operations alone can reward the board's preferred proposal exclusively. Counting both columns makes that possible at every permitted threshold from 0.1% through 12%. A sensitivity analysis finds that the proposals change rank when the rule counts two fifths of supplier emissions. The calculations distinguish changing an incentive from changing the outcome it is supposed to improve.

[Play the case](https://alberttansinhon.com/math-arcade/boardroom/) · [Participant sheet and facilitator key](BOARDROOM_PILOT.md)

## The decision and its scientific basis

Let $O$ denote emissions from own operations and $S$ emissions attributed to suppliers. Both options deliver the same product in the same quantity over the same period. All entries are fictional emissions units. Within this example the two columns are exhaustive and disjoint. The board's objective is to minimise $T=O+S$ over two proposals. The baseline supplies the comparison for the contract.

| Position | $O$ | $S$ | $T$ | Reduction in $O$ | Reduction in $T$ |
|---|---:|---:|---:|---:|---:|
| Baseline | 80 | 20 | 100 | 0% | 0% |
| A. Upgrade equipment | 68 | 20 | 88 | 15% | 12% |
| B. Outsource work | 50 | 65 | 115 | 37.5% | −15% |

For a measured quantity $M$ with positive baseline $M_0$, define its percentage reduction as $r_M(i)=100(M_0-M_i)/M_0$. The contract pays a fixed bonus if $r_M(i)\geq \tau$, where $\tau$ is the threshold in percentage points on this scale. Under the opening contract, $\tau=25$ and $M=O$. The maximum eligible value is $80(1-0.25)=60$. Only B qualifies. The board chooses A because $88<115$. Choosing B therefore raises combined emissions by 15 units against the baseline and by 27 units against the available upgrade. Those comparisons answer different questions.

Baker's analysis of performance measures asks how the measure used in a contract relates to the principal's objective. Holmström and Milgrom show how the relative rewards for measurable tasks can redirect effort across a job. The game isolates one mechanism from that literature. A supplier component enters the board's objective and falls outside the original contract. A manager who values the bonus and faces equal private costs for the two options has reason to choose B. Inferring an actual choice would require evidence about costs, discretion and other objectives. [Baker (1992), pp. 598–600](https://doi.org/10.1086/261831) · [Holmström and Milgrom (1991), pp. 24–25](https://doi.org/10.1093/jleo/7.special_issue.24)

## Which thresholds work?

For a binary bonus to pay A alone, its threshold must satisfy $r_M(B)<\tau\leq r_M(A)$. The first inequality is strict because an option at the threshold earns the bonus. The game's numerical input admits $0.1\leq\tau\leq100$.

| Measured quantity | Threshold $\tau$ (%) | Proposals earning the bonus |
|---|---|---|
| Own operations | $0.1\leq\tau\leq15$ | A and B |
| Own operations | $15<\tau\leq37.5$ | B only |
| Own operations | $37.5<\tau\leq100$ | Neither |
| Own operations and suppliers | $0.1\leq\tau\leq12$ | A only |
| Own operations and suppliers | $12<\tau\leq100$ | Neither |

For own operations, $r_O(B)=37.5>15=r_O(A)$, so the required interval is empty. For the combined boundary, $r_T(B)=-15<12=r_T(A)$, and the permitted interval is $[0.1,12]$. Switching the boundary while retaining the original 25% threshold pays neither proposal. This illustrates why choosing what to measure and setting the threshold are separate decisions.

## How much of the omitted component changes the decision?

As a paper extension, let $M_\lambda=O+\lambda S$, for $0\leq\lambda\leq1$. The browser game implements the two endpoints. Intermediate weights let us examine how sensitive the ranking is to partial coverage. They represent a modelling assumption rather than a recommended accounting convention.

The measured difference between proposals is

$$M_\lambda(B)-M_\lambda(A)=(50-68)+\lambda(65-20)=-18+45\lambda.$$

At $\lambda=2/5$ the two proposals tie. Below that fraction, B appears cleaner. Above it, A appears cleaner. In general, if B cuts own emissions relative to A by $d>0$ and increases supplier emissions by $s>0$, the full-boundary ranking reverses precisely when $s>d$. The tie occurs at $\lambda=d/s$ when that value lies in the chosen interval. This comparison survives any common change to the baseline because it compares the options directly.

Two other cut-offs answer different questions. Against the baseline, B's measured emissions fall by $30-45\lambda$ units, which reaches zero at $\lambda=2/3$. Under the original 25% threshold B earns the bonus when $30-45\lambda\geq 0.25(80+20\lambda)$, or $\lambda\leq1/5$. Thus the contract stops paying B well before the board's preferred proposal begins to rank first. For instance, at $\lambda=1/2$, A measures 78, B measures 82.5 and the baseline is 90. A ranks first, both options improve on the weighted baseline, and neither earns a 25% bonus.

## Evidence a reviewer would need

A payment register shows who received money. Checking whether the contract ought to have paid requires records for the measured activities. For a combined boundary, match the firm's meter or fuel records to supplier activity records, check the conversion and allocation assumptions, and reconcile both with production records for the agreed output and period. Check that transferring work across entities leaves the activity represented exactly once. If a supplier record is missing, the combined result is unresolved unless the remaining evidence supplies a sufficient bound.

For example, if A's two figures and B's own figure of 50 are verified, B's unknown supplier figure $s_B$ must exceed 38 for A to beat B on total emissions. A defensible lower bound of 40 would settle that comparison. A range of 35–45 would leave both rankings possible. Whether B itself increases emissions relative to the 100-unit baseline is a separate question, requiring $s_B>50$. The game's evidence selector models this review by requiring the option for matched own and supplier records plus output. Selecting that option in a fictional case certifies no company's emissions.

## A different measurement error in the transfer case

The bus exercise changes a denominator. Let $q$ be the share of scheduled services that operate, and let $p$ be the share of operated services that arrive on time. The on-time share of all scheduled services is $qp$. Both periods contain 100 scheduled services. Initially 90 arrive on time, 10 late and none are cancelled. Subsequently 88 arrive on time, two late and ten are cancelled.

| Measure | Initially | Subsequently |
|---|---:|---:|
| Operated / scheduled, $q$ | $100/100=1$ | $90/100=0.9$ |
| On time / operated, $p$ | $90/100=90\%$ | $88/90\approx97.8\%$ |
| On time / scheduled, $qp$ | $90/100=90\%$ | $88/100=88\%$ |

The reported punctuality can improve while the chance of an on-time arrival for a randomly chosen scheduled service falls. The arithmetic establishes compatibility of those outcomes. Explaining why ten buses were cancelled requires operational evidence. Estimating the incidence on passengers would also require passenger weights. In the emissions example the contract omits a component of a sum. In the bus example it conditions on a subset of scheduled services. A learner who identifies that difference has gone beyond repeating that “metrics can mislead”.

## Reproducibility and scope

The numbers and endpoints above can be checked with the repository's [verification script](../tools/verify_arcade_whitepapers.py). To compare with the published game, inspect its exported function `evaluateRule(boundary, threshold, evidence)`. The function returns each proposal's eligibility, whether the rule pays A alone, and whether the specified evidence qualifies. The combined rule at exactly 12% passes with reconciled evidence. At 12.01% it pays neither proposal. At 12% with only the payment register it identifies the same eligible proposal and fails the evidence check. The SHA-256 digest of the JavaScript used for this edition is `94a6d97d19d29f832af932f42a651b133eb8f9b52aaecb1b3cf9c9dbbeb5b6d5`. [Archived implementation](../research/arcade/snapshots/2026-11-28/boardroom/game.mjs) · [Published implementation](https://alberttansinhon.com/math-arcade/boardroom/game.mjs)

This paper establishes results about the specified ledger and decision rule. Assessing how often managers respond this way, whether the exercise improves reasoning, or whether institutions value facilitated delivery would require separate observations. The [pilot protocol](BOARDROOM_PILOT.md) sets out how to distinguish a correct fresh-case explanation, a repeat teaching session and a paid session. No participant outcomes enter these calculations.

## References and attribution

- Baker, George P. (1992). ‘Incentive Contracts and Performance Measurement’. *Journal of Political Economy*, 100(3), 598–614. [DOI](https://doi.org/10.1086/261831)
- Holmström, Bengt, and Paul Milgrom (1991). ‘Multitask Principal–Agent Analyses: Incentive Contracts, Asset Ownership, and Job Design’. *Journal of Law, Economics, & Organization*, 7, special issue, 24–52. [DOI](https://doi.org/10.1093/jleo/7.special_issue.24)

**Suggested citation.** Atlas Open Mathematics (2026). *When does an emissions bonus reward the worse proposal?* Version 1.0, 28 November. Project directed by Albert Tan Sin Hon. Cite the GitHub commit permalink for the edition consulted.

OpenAI Codex assisted with the drafting and mathematical checks. The repository's [educational content licence](../LICENSE-CONTENT.md) covers the original exposition. [Report a correction](https://github.com/Albertito-AI/atlas-open-mathematics/issues/new?template=correction.yml)
