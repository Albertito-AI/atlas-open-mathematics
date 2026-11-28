# Can you convince your partner?

**A 20-minute Maths Arcade circle. Facilitation and assessment white paper, version 1, 27 November 2026.** Atlas Open Mathematics, directed by Albert Tan Sin Hon.

[Download the two-page print edition](MATHS_ARCADE_CLUB_GUIDE.pdf) · [Read the puzzle field notes](https://alberttansinhon.com/math-arcade/field-notes/) · [Play the daily challenge](https://alberttansinhon.com/math-arcade/#daily)

**For the facilitator.** Give each pair page 1 of the print edition and keep page 2 as your key. The sheet includes the entire starting position for each activity. A device per pair is optional. Participants should be familiar with ordered pairs and simple fractions. Ask one partner to propose a solution and the other to check it. Swap roles for each new game.

## Pair sheet

| Time | Activity |
| --- | --- |
| 0–2 min | Agree on a question to ask whenever a partner proposes an answer: “How could I check that?” |
| 2–7 min | Lattice Dash. Draw the route and defend the jump count. |
| 7–12 min | Target Forge. Write an expression and trace its exact values. |
| 12–17 min | Parity Lights. List the switches and justify the minimum. |
| 17–20 min | Exchange one explanation with another pair. Ask them to mark the first step they cannot verify, or explain why each step follows. |

### 1. Lattice Dash

On an empty 6 × 6 grid with coordinates 0 to 5, move from (1,3) to (0,5). You may add any one of (−1,1), (−1,0), (1,−1) and (1,0) on each jump. Stay on the grid. What route can you exhibit? Why would a two-jump attempt fail even before you draw it? [Play Warm-up, seed 2](https://alberttansinhon.com/math-arcade/#play/lattice/0/2)

### 2. Target Forge

Make 55 with the four tiles 7, 7, 8 and 9. Each move replaces two tiles with their sum, difference, product or quotient. Use all four tiles exactly once. What intermediate result would make the last multiplication by 7 work? Ask your partner to trace both sevens separately. [Play Expert, seed 0](https://alberttansinhon.com/math-arcade/#play/forge/2/0)

### 3. Parity Lights

Rows are A, B and C from top to bottom. Columns run from 1 to 3 left to right. The six lit cells are A1, A2, B1, B3, C2 and C3. A press flips itself and its horizontal and vertical neighbours. Which switches clear the board? How many lights can one press possibly flip? [Play Warm-up, seed 7](https://alberttansinhon.com/math-arcade/#play/parity/0/7)

## Facilitator key

| Game | Question to ask when a pair stalls | Checkable evidence for a complete explanation |
| --- | --- | --- |
| Lattice Dash | Which moves gain one vertical unit? | One route is (1,3) → (0,4) → (1,4) → (0,5). The goal is two units higher. In two moves both jumps would have to be (−1,1), giving horizontal displacement −2 instead of −1. One jump gains at most one vertical unit. |
| Target Forge | If 7 times a value is 55, can the other three tiles make that value? | One solution is 7 × (9 − 8/7). The inner division gives 8/7, subtraction gives 55/7, and multiplication returns 55. Accept any legal expression whose exact intermediate values and four original tiles a partner can trace. |
| Parity Lights | What does A1 reach? Which lights remain? | A1 flips A1, A2 and B1. C3 flips B3, C2 and C3. The sets are disjoint and cover the six lit cells. One press flips at most five cells, so two presses are necessary and sufficient. |

**Assessment.** Mark each task separately: **0** if no correct candidate is shown, **1** if a correct candidate is shown, **2** if the partner can also verify the evidence in the last column. For the two shortest-solution tasks, a demonstration that clears the board earns 1 until a lower bound is given. Accept equivalent arguments. The marks describe these three responses in this session. The session and rubric are a proposed teaching design; learning gains have not been measured.

**If time is short.** Supply the candidate moves or expression from the key and retain the proof question. For a further meeting, use the daily challenge and ask what evidence from today's sheet still applies. [Daily challenge](https://alberttansinhon.com/math-arcade/#daily) · [Technical paper and worked verification](MATHS_ARCADE.md)

**For a governance session.** The [Boardroom case and pilot scorecard](BOARDROOM_PILOT.md) give pairs a new task on emissions boundaries, followed by a bus-timetable challenge to test the same reasoning in another setting.

## Citation and reuse

Suggested citation: Atlas Open Mathematics. *Can you convince your partner? A 20-minute Maths Arcade circle*. Facilitation and assessment white paper, version 1, 27 November 2026. Credit Albert Tan Sin Hon and named contributors, link to the source version and identify adaptations. The original educational prose is licensed under Creative Commons Attribution 4.0 International. Codex (OpenAI, GPT-6) assisted with drafting, layout and checks. [Content licence](../LICENSE-CONTENT.md) · [Share a teaching variation](https://github.com/Albertito-AI/atlas-open-mathematics/issues/new?template=teaching.yml)
