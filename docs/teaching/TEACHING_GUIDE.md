# Teaching mathematical thinking through play

Atlas Open Mathematics · Albert Tan Sin Hon, project director · 28 November 2026

[Download the 17-page teaching guide (PDF)](https://raw.githubusercontent.com/Albertito-AI/atlas-open-mathematics/main/docs/teaching/Maths_Arcade_Teaching_Guide.pdf) · [Player sheets without answers](PLAYER_SHEETS.md) · [Teaching resources on Albert’s website](https://alberttansinhon.com/math-arcade/teaching/)

Two learners may make exactly the same move for quite different reasons. One recognises a pattern. The other can explain why every alternative fails. Ask each to teach the position to a partner, then give them a different opening. That second board shows what they can carry forward.

Use the six accompanying player sheets for the first encounter. The chapters here provide the answers, rival strategies, common mistakes and a further mathematical investigation. Start with the game that fits the question your group wants to explore.

[Sudoku](#sudoku) · [Lattice Dash](#lattice-dash) · [Target Forge](#target-forge) · [Parity Lights](#parity-lights) · [Nim Lab](#nim-lab) · [Reversi Endgame Lab](#reversi-endgame-lab)

## Teach one position well

A 30-minute session for pairs, a class or a maths circle

| Time      | What the players do                                                                                                        | What to listen for                                                                             |
|-----------|----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| 0–4 min   | Play a few legal moves, then return to the shared position. One partner explains the rules to the other.                   | Can both predict what one move changes? In a two-player game, do both know whose turn follows? |
| 4–10 min  | Choose one of two plausible moves. Record the prediction and a reason before touching the controls.                        | Which detail of the position is the prediction using? What observation could overturn it?      |
| 10–18 min | Play, replay the alternative, and draw or describe the difference. Swap the person at the controls.                        | Can the learner identify the first decision where the two lines diverge?                       |
| 18–26 min | Open the chapter’s transfer position. Both partners make an individual prediction. Disclose hints only after recording it. | Does the explanation still work when the numbers, board or side to move changes?               |
| 26–30 min | Each partner teaches one claim and answers a challenge. Write down one question left open.                                 | Can a listener reproduce the result, and identify a limit on the claim?                        |

### Independent play and teaching in pairs

For a solo warm-up, stop after one justified decision. Leave the display untouched while you write “I expect \_\_\_ because \_\_\_”. Revisit it after the reply. For paired play, give one learner responsibility for the proposed move and the other responsibility for finding a counterexample. Exchange roles before the new board. In a large class, distribute competing openings or hypotheses across groups and compare the evidence.

### Choose an entry point

Start with counters, move cards or an enlarged board for learners still acquiring the notation. Ask for a spoken prediction or a sketch. Experienced players can begin at the transfer position and try to disprove a classmate’s rule. A completed board or a fast time gives little evidence of how either player reasoned. Record the move, the reason and any help used.

The use of representations, worked examples and explanations is consistent with recommendations 2 and 3 of the [Education Endowment Foundation’s mathematics guidance](https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/maths-ks-2-3/) and recommendations 2 and 7 of the [Institute of Education Sciences practice guide](https://ies.ed.gov/ncee/WWC/PracticeGuide/1/Published). The suggested timings are facilitation choices.

## Sudoku

A blank cell might accept several digits without immediately breaking a rule. A player still needs a reason to write one in ink. The lesson turns on two questions that sound similar but direct attention differently. **Which digits can go in this cell?** and **Where in this row, column or box can this digit go?** Moving between them develops a practical solving strategy and gives a class two ways to prove a claim.

### Play and investigate

**1. A five-minute warm-up.** The digits 1 to 9 must appear once each in every row, column and three-by-three box. Start at row 1, column 3. List the digits missing from the first row. Cross out any already used in column 3, then check the upper-left box. Before entering the surviving digit, give a partner a reason they could check without trusting you. Now find a second move of your own. Which of the three units did the most work in your argument? [Open Warm-up 0](https://alberttansinhon.com/math-arcade/#play/sudoku/0/0)

**2. Change the question.** In the Tricky opening, row 2 reads `2 . 8 6 1 5 . . .`. Build a four-column table for its empty cells. List every digit each cell permits. If each column of your table contains at least two digits, look across the table. Does one missing digit occur on only one list? Try to rule out every alternative position before playing. Then explain to your partner why several candidates for your chosen cell can coexist with certainty about the move. [Open Tricky 2](https://alberttansinhon.com/math-arcade/#play/sudoku/1/2)

**3. Transfer without a hint.** On a different board, inspect the upper-middle box, covering rows 1–3 and columns 4–6. Where must its 9 go? Mark every empty square in this box that can be excluded, and name a given clue that rules it out. Finally, find one other digit that appears locally possible in the square you chose. A correct explanation has to account for that apparent alternative. [Open Tricky 8](https://alberttansinhon.com/math-arcade/#play/sudoku/1/8)

For paired play, one person proposes a move and the other tries to put the same digit somewhere else in the unit. Swap roles after each justified entry. On paper, mark remaining candidates lightly and circle a digit only after its justification survives the challenge. On screen, arrow keys move between squares, **N** switches pencil marks on or off, and number keys enter digits. Read coordinates aloud so a partner can follow the reasoning without distinguishing colours.

### Facilitation and feedback

Give learners a moment to try their own deduction before using **Hint**. It directs attention to a square without naming its digit. **Explain the digit** reveals the value and reasoning for a single. **Place hinted digit** enters it. After an explanation, ask the learner to close the loop by finding and justifying the next move independently. A pencil mark records an option the player is considering. Omissions from a learner’s notes cannot establish a forced move.

If someone says “that digit fits”, ask, “Could a different digit fit as well?” If someone says “there are two candidates, so I have to guess”, ask them to switch from listing digits for that square to listing locations for one missing digit across the whole unit. A learner who wants a lighter round can stop after two explained entries. For a harder round, give another pair a completed candidate table with the conclusion removed and ask them to explain both why the proposed move works and why its closest rival fails.

### Facilitator key

**Warm-up 0.** Row 1 is missing 2, 3, 6, 7 and 9. Column 3 already has 3, 6, 7 and 9. The upper-left box permits 2. Row 1, column 3 therefore takes **2**. In a *naked single*, after checking the occupied digits in the row, column and box, just one candidate remains for the cell.

**Tricky 2.** The row-2 candidates are `c2 {7,9}`, `c7 {3,7,9}`, `c8 {3,7}` and `c9 {3,4,7}`. The row needs a 4, and column 9 is its only available place. Thus **r2c9 = 4**. This is a *hidden single*. The cell has three local candidates, but the digit has just one available location in the row. Across this opening no empty cell initially has a single candidate.

**Tricky 8.** The five empty squares in the box are r1c4, r1c6, r2c4, r3c4 and r3c5. The 9 at r1c9 rules out the first two. The 9 at r4c4 rules out r2c4 and r3c4. The only place left is **r3c5**. Its local candidates are 3, 5, 6 and 9. Choosing any of the other three would leave the box with nowhere to put 9. Two visible clues account for all four exclusions.

### From a move to a proof

If two completions respected the same clues, they would both have to agree with the first forced move. Apply this argument after every forced entry. If the deductions fill the entire board, the two completions coincide. One forced move establishes one entry. A chain reaching all 81 cells certifies uniqueness. A useful counterexample begins on paper with any completed grid. Erase every 1 and every 2. Ask for two completions. Restoring the original digits works, and interchanging 1 and 2 throughout also works.

Try the same singles procedure in Expert 0. Beginning with 27 clues, the arcade’s order makes 11 forced entries before stopping with 43 empty cells. Independent search counts one completion. At this point **Reveal checked digit** consults that solution. Ask what evidence would justify the revealed digit *from the grid*. A stalled pair of techniques establishes a limit of those techniques. Other deductions may still be available. [Open Expert 0](https://alberttansinhon.com/math-arcade/#play/sudoku/2/0)

**Evidence of learning.** Use the transfer box as an individual exit ticket. Check that the learner identifies the correct square and digit, supplies a clue-based exclusion for every other empty position, and explains why a second local candidate cannot be used. A correct digit with no exclusions tells the teacher exactly which part needs another example. The arcade’s completion message alone cannot establish whether the player made or understood these deductions.

The project’s white paper gives the generator’s conditions, fixed openings and independent verification. Norvig’s account develops the two directions of constraint propagation and explains how search extends them. [Project Sudoku paper](https://github.com/Albertito-AI/atlas-open-mathematics/blob/main/docs/SUDOKU_WHITE_PAPER.md) · [Peter Norvig, *Solving Every Sudoku Puzzle*](https://www.norvig.com/sudoku.html)

## Lattice Dash

The beacon is an invitation to make two different mathematical claims. A sequence of legal jumps shows that the destination can be reached in *at most* that many moves. A shortest-route claim also needs a reason that every shorter attempt fails. This game lets a player build both halves of that argument, first on an empty board and then on a board where an obstacle defeats the obvious route.

### Player challenges

**Opening round.** Start at (1, 3) and aim for (0, 5). On this 6 × 6 grid, the four keys add (−1, +1), (−1, 0), (+1, −1) and (+1, 0), in that order. Read the first coordinate across and the second up. Predict the landing after each key before pressing it. Record the key sequence and the successive coordinates. The screen shows par from the outset. Can you justify the number to a partner who cannot see it? [Play Warm-up, seed 2](https://alberttansinhon.com/math-arcade/#play/lattice/0/2)

**A second way there.** Keep the same opening and write your solution on three separate cards, one jump per card. Rearrange the cards. Which orders still reach the beacon? Which would send a player outside the grid? Make your prediction on paper before replaying. Reopen the same link to start a completed round again. During an unfinished round, **Undo** lets you change your last decision. One press of **Hint** gives the remaining displacement and distance. A second identifies one available first move on a shortest route.

**The obstacle round.** On a 7 × 7 grid, move from (1, 5) to (4, 2). The four keys now point north-east, south-east, south-west and north-west. The blocked landing points are (3, 0), (3, 1), (3, 3), (2, 2) and (4, 0). Predict the minimum with the board visible. Which first move would you choose and what alternative can you defend? Record a route, rule out shorter ones and name one blocked point whose removal would change your answer. On paper, test whether the same keys could ever reach (4, 3) from this start on an otherwise empty grid. [Play Tricky, seed 55, shown as Puzzle 1J](https://alberttansinhon.com/math-arcade/#play/lattice/1/55)

### Teaching the rounds

Allow about twenty minutes for the two positions. A useful pairing is a navigator who proposes a move and a checker who predicts its landing. After the first round, exchange roles. Ask the checker to record any failed prediction verbatim. “I thought every order worked” is more informative than a tally of missed taps because the next round can test that exact idea.

| If the learner says or does this | Ask this next |
| --- | --- |
| Reads (−1, +1) as a destination | “Starting at (1, 3), what does the −1 change? What does the +1 change? What if you began one square farther right?” |
| Reaches the goal and points to the par display | “Your route shows how many moves suffice. What could someone do in one fewer move, and why would *every* such attempt fail?” |
| Treats the shortest straight line on the page as the fewest jumps | “How many jumps does each key cost? Where would the proposed intermediate landing be?” Only the landing is checked, and every legal jump costs one. |
| Gives up after the direct route hits a cross | “Which coordinate changes on *every* jump? Sort possible route lengths into odd and even before searching for a detour.” |

For learners who need help with coordinates, use squared paper, a counter and arrow cards. Leave the board on screen and let a partner move the counter. For confident learners, hide the route history and ask for a proof that would still be persuasive if the software reported the wrong par.

### Facilitator's worked answers

**Warm-up.** The required displacement is (−1, +2). Two jumps could gain two units of height only if both were key 1. Their horizontal change would then be −2. One jump cannot gain two units of height. Keys **1, 4, 1** land at (0, 4), (1, 4), (0, 5), providing the matching upper bound of three. **4, 1, 1** also works. The remaining ordering, **1, 1, 4**, attempts to land at (−1, 5) on its second jump. The sum of the vectors survives a rearrangement. The legality of the intermediate positions can change.

**Tricky.** The goal lies three columns east and three rows south. Fewer than three jumps cannot gain three columns. In exactly three moves, all three would have to be south-east. The second landing would be (3, 3), which is blocked. Four moves cannot work either. Every jump changes the parity of the horizontal coordinate, so an even number of moves would leave the player on an odd column. The goal is on even column 4. Keys **1, 2, 2, 2, 3** reach (2, 6), (3, 5), (4, 4), (5, 3) and (4, 2). Five is therefore optimal. **2, 1, 2, 2, 3** supplies a second shortest route. The first route actually starts by going *up*, away from the goal row. Removing the cross at (3, 3) reopens the direct three-jump solution.

**A stronger impossibility.** All four diagonal moves preserve the parity of the *sum* of the coordinates. The start has sum 6 and the proposed paper target (4, 3) has sum 7. No sequence can reach it, however many obstacles are removed. This differs from the earlier argument about the parity of the *number of moves* needed to reach a particular column. Ask a learner to identify what stays fixed in each argument.

### Strategy, computation and assessment

A group can mimic the game's shortest-path search using paper counters. Mark the start as layer zero. For each layer mark every previously unmarked legal neighbour of its points. A point first marked in layer five has a five-move witness through its predecessor. If a shorter route existed, its previous point would already have exposed it in an earlier layer. This reasoning applies to a network of equal-cost transfers. A network with unequal travel times presents a different optimisation problem. [Technical paper and implementation](https://github.com/Albertito-AI/atlas-open-mathematics/blob/main/docs/MATHS_ARCADE.md#lattice-dash-and-the-three-jump-lower-bound)

Give one mark each for a legal recorded route, a lower bound that excludes *all* shorter lengths, and a correct prediction about removing the chosen obstacle with a reason. A learner who earns only the first mark has already demonstrated navigation. Revisit the exclusion argument with a partner. For an independent exit question, ask whether adding a blocked landing could ever make the shortest route between the same two open points *shorter*. Every route left after the change was available beforehand, so the minimum can stay the same, increase, or cease to exist if the goal becomes unreachable.

## Target Forge

**The question.** Can you make the target, explain why your first move helps, and show that a simpler class of solutions cannot work? Four tiles make this a small enough laboratory to distinguish constructing an answer, choosing a strategy and proving a claim.

### Player's investigation

Each turn, choose a tile, an operation and a different tile. The two chosen tiles disappear and their result becomes a new tile. Use all four original tiles exactly once. Subtraction and division respect the order of selection. The board keeps fractions exact. A target reached while another tile remains is an unfinished hand.

1. **Find two routes.** Make 23 from 3, 4, 2 and 5. Can your final operation add two products? Can a second route save a single original tile until the last turn? Draw both calculations as branching trees. Trace each original tile from its leaf to the answer. [Play Warm-up 2](https://alberttansinhon.com/math-arcade/#play/forge/0/2)
2. **Change what is allowed.** Make 28 from 4, 2, 3 and 3. Before touching the board, choose a factor of 28 that you could reserve. What would the other three tiles have to make? The game tells you that subtraction or division is needed. Decide how you would check that claim. [Play Tricky 0](https://alberttansinhon.com/math-arcade/#play/forge/1/0)
3. **Use a near miss.** Make 55 from 7, 7, 8 and 9. Label the sevens A and B on paper. If seven and nine suggest a useful product, how far is that product from 55? Can you move the correction *inside* the multiplication so that all four tiles contribute? Predict the result before each click. [Play Expert 0](https://alberttansinhon.com/math-arcade/#play/forge/2/0)
4. **Try a new hand unaided.** Make 81 from 8, 2, 7 and 12. There are no duplicate tiles. Write down a near miss, reserve one tile as the final multiplier and work backwards. Swap with a partner, who must be able to reproduce your route using only your three lines of working. [Play Expert 1](https://alberttansinhon.com/math-arcade/#play/forge/2/1)

### Running the session

Allow about 25 minutes for the four rounds, extending the proof investigation into a second session if needed. Pair a player who operates the board with a partner who checks the order, the remaining tiles and the arithmetic. Switch roles after the first round. Before a calculation, the partner asks, “Which number do you want to have left beside this one?” It is an invitation to plan the last move while the first is still reversible.

For an introductory group, write each tile on a slip. When learners combine two slips, place both beneath a new slip bearing the result. Physically revealing the slips under the answer settles disputes about reuse. For learners comfortable with fractions, make the first guess a commitment on paper and use **Undo** to compare it with another opening. **Hint** names a pair on a possible route. **More hint** gives an operation. Ask for the learner's reasoning between the two. If the game reports no route from the present position, record the move that led there before undoing it.

### Teacher's key and discussion

**Two constructions of 23.** The balanced tree gives $(3\times5)+(4\times2)=15+8=23$. A different tree gives $((4+2)\times3)+5=23$. One builds two branches independently. The other reserves the 5. Both take exactly three moves because each operation reduces the number of available tiles by one. For 28, reserve 4. The other three tiles can make $3\times3-2=7$, giving $4\times7=28$. An example using subtraction establishes that subtraction *can* help. Excluding every addition-and-multiplication route requires a further argument.

**The correction that uses both sevens.** Starting with $7\times9-8=55$ leaves one 7 unused. Write $55/7=9-8/7$ on paper. On the board, divide 8 by the first 7, subtract that fraction *from* 9, then multiply the resulting $55/7$ by the second 7. Distributing the multiplication explains why the fraction cancels. The shorter expression $7\times9-8$ checks the answer algebraically, but its three leaves would fail the game's four-tile rule. A learner who can explain that distinction understands both the arithmetic and the rules.

**Transfer to 81.** The near miss is $12\times7=84$. A reduction of 3 at the end means a reduction of $3/12=1/4$ inside the bracket. The two unused tiles supply $2/8=1/4$. The legal steps are $2\div8=1/4$, $7-1/4=27/4$, then $12\times27/4=81$. Reversing the first division gives 4 and changes the problem. The transferable idea is to scale a correction by the multiplier you have reserved.

### An investigation in exhaustive reasoning

For each non-empty subset of the four *labelled* tiles, keep the set of numbers it can make. A single tile gives its own value. For a larger subset, split it into two non-empty parts. Combine each value available from one part with each available from the other. Include both directions of subtraction and division, omitting division by zero. Every legal expression has a last operation joining two disjoint groups of leaves, so considering every split covers every possible last move.

Repeat with just addition and multiplication, or discard non-integer results **at every operation**. On Tricky 0, addition and multiplication give 26 distinct final values and none is 28. On Expert 0, integer-only intermediates give 134 distinct final values and none is 55. Unrestricted arithmetic gives 479, including 55. On Expert 1 the respective counts are 206 and 780, with 81 appearing only in the unrestricted set. These count distinct values, so two expressions giving the same result count once. A learner can check the principle by hand on a pair of tiles before running the four-tile calculation. [Technical paper and replay commands](https://github.com/Albertito-AI/atlas-open-mathematics/blob/main/docs/MATHS_ARCADE.md#why-target-forge-needs-a-fraction)

**What to assess.** Collect the transfer prediction, the three legal moves and a sentence explaining the factor of 12 in the correction. A correct expression demonstrates construction. A prediction that links a near miss to a scaled correction demonstrates strategic transfer. Explaining why every expression has a covered last split demonstrates exhaustive reasoning. If a learner says that trying several integer routes proves impossibility, ask which untried final operation their evidence rules out.

## Parity Lights

**Teaching question.** If only one lamp is lit and every first move turns on more lamps, what could count as progress? This lesson moves from predicting the effect of a switch to proving that a whole strategy is sufficient and shortest. Allow 20–30 minutes for the two main boards. The four-by-four investigation can occupy a second session.

### Player investigation

**Learn the controls.** The board starts with some lamps lit. Pressing *any* tile flips that lamp and each neighbour immediately above, below, left and right, where those neighbours exist. You may press an unlit tile. Rows run from A downwards and columns from 1 to the right. With a keyboard, use the arrow keys to select a square, then Enter or Space to press. The board reports both the move count and the number of lights on. Par is the minimum number of presses for the opening.

**1. Predict before pressing.** Open Warm-up 7. Six lamps are lit. One player calls a square and names every lamp that will change. A partner predicts which lamps will remain on. Exchange roles. On paper, find a way to turn everything off in two presses. Give two arguments. Show that your choice works, then rule out a solution in one press. Can you explain why the order of your two presses is immaterial? [Play Warm-up 7](https://alberttansinhon.com/math-arcade/#play/parity/0/7)

**2. Test a convincing but unreliable strategy.** Open Warm-up 4, which starts with just C2 lit. Predict the result of pressing C2 itself. Before trying anything else, decide whether any first press can leave fewer lights on. Your challenge is to clear the board anyway. Record each press and the lights left after it. Try the rule “keep the top row dark once its presses are settled”. How could a team divide the possible top-row choices so that each is tried exactly once? [Play Warm-up 4](https://alberttansinhon.com/math-arcade/#play/parity/0/4)

**3. Take the idea to a bigger board.** On Tricky 0, one pair should look for a five-press solution and a second pair should search independently. If the answers differ, can both be correct? Predict what would happen if you combined their two switch lists, striking out every switch appearing twice. Test on paper first. This lets both groups keep their opening boards. [Play Tricky 0](https://alberttansinhon.com/math-arcade/#play/parity/1/0)

### Teacher guide and worked answers

**Warm-up 7.** A1 flips A1, A2 and B1. C3 flips B3, C2 and C3. Those are precisely the six lit lamps, without overlap. A single press reaches at most five squares, even at the centre, so at least two are necessary. The construction attains that lower bound. For a learner still mapping the grid, draw the two footprints on tracing paper. For a learner who thinks order independence requires disjoint footprints, have them name the lamps flipped by A1 and A2. Their shared lamps flip twice whichever switch comes first.

**Warm-up 4.** Pressing C2 switches it off and switches B2, C1 and C3 on. More generally, a press reaches at least three cells. Starting with one lit lamp, every first press leaves at least two on. An improving move is impossible if improvement means “fewer lamps lit now”. One shortest sequence is **A1, A2, A3, B2**. The lit counts are **1 → 4 → 4 → 5 → 0**. All four selected switches are initially dark. A player who sees five lamps just before the last press can recognise the footprint of B2 and finish in one.

**Why four is the minimum.** Pressing a switch twice restores each lamp it affects. Presses can also be reordered because each lamp's final state depends only on whether its total number of flips is odd or even. A shortest solution therefore presses each switch at most once. Fix the press choices for row A. For each lamp still lit in row A, the only remaining switch capable of changing it is directly underneath in row B. Press those switches and repeat between rows B and C. Nothing below row C can repair a remaining light. In the table, the three bits indicate presses at A1, A2 and A3, reading left to right.

| Row A choices | Lamps left after the forced lower rows |
| --- | --- |
| 000 | C2 |
| 001 | C1 |
| 010 | C1, C3 |
| 011 | C2, C3 |
| 100 | C3 |
| 101 | C1, C2, C3 |
| 110 | C1, C2 |
| 111 | None |

Only 111 clears this opening. Once all three A switches are pressed, B2 is forced and no C switch is needed. This exhausts all possibilities for a shortest solution. A teacher can cover the second column until the groups have supplied their results.

**Tricky 0 and linear algebra.** Two shortest sets are {A1, A2, B1, C2, C3} and {A4, B1, B4, C1, D2}. A third is {A2, A3, A4, C4, D3}. Each clears the same opening. Write the opening as a column of zeros and ones, and let each column of a matrix $M$ describe the lamps flipped by one switch. If $p$ records the switches pressed, the final board is $b+Mp$, with addition modulo two. Thus a solution satisfies $Mp=b$. If $p$ and $q$ both solve the opening, then $M(p+q)=b+b=0$. Their combined presses, with duplicates cancelled, change **no** lamp in the final board, whatever the starting pattern. This connects the players’ switch lists to the kernel of a linear map. The generator works in the opposite direction, starting from dark and applying presses to create a solvable board. [Game source](https://alberttansinhon.com/math-arcade/parity.mjs) · [Anderson and Feil, *Turning Lights Out with Linear Algebra*](https://doi.org/10.1080/0025570X.1998.11996658) · [University-hosted copy](https://people.sc.fsu.edu/~jburkardt/classes/imps_2017/11_28/2690705.pdf)

**Assess the reasoning.** On a fresh sheet, ask “If two presses both affect a lamp that was originally lit, what happens to it? What if it was dark? Give an example from the board.” A learner who can trace both flips has moved beyond treating lit lamps as objects to remove. For independent transfer, give Warm-up 20, whose whole bottom row starts lit, and ask for a four-press plan and a reason the first move may look unhelpful. A2, B1, B2 and B3 clear it. Every one of those possible first moves increases the lit count. Ask the learner to distinguish a verified solution from a proof of shortest length. Their row-chase record can supply the latter. [Play the exit challenge](https://alberttansinhon.com/math-arcade/#play/parity/0/20)

## Nim Lab

Two players alternate. On a turn, remove any positive number of counters from **one** heap. Whoever takes the last counter wins. In the arcade, choose the heap, select the number to take, then press **Take counters**. Atlas replies immediately. A *winning position* means the player whose turn it is can force a win against every legal reply. A good starting question is “Whose turn is it on the board I am describing?”

Allow about 25 minutes for the investigations, with a further ten for the proof. Pairs can use labelled cups, large counters or spoken heap totals. One partner chooses a move, the other tries to defeat the prediction. Exchange roles before the transfer round.

### Investigations for players

**1. Play the same opening twice.** Set out A = 1, B = 1 and C = 6. Consider taking five or six from C. Sketch both resulting boards and say who will take the last counter in each case. Try taking five first. Read Atlas's reply and use **Undo my turn** to restore the opening, including the counters Atlas took. Then try taking six. Keep the binary comparison closed until you have written a prediction. What could Atlas have done differently after your second choice? [Play Warm-up 7](https://alberttansinhon.com/math-arcade/#play/nim/0/7)

**2. Invent a rule when just two heaps remain.** On paper play from (2, 2), then from (1, 3). Both boards contain four counters. In each game one partner chooses the seat, the other chooses every reply. Describe a way to win that still works if the opponent changes their mind. Test your rule on (4, 4). If using counters, place equal heaps opposite one another so a partner can point out which counters correspond.

**3. Transfer your rule to four heaps.** Open A = 6, B = 3, C = 2, D = 4. Which opening moves hand your opponent a losing position? Look for **every** such move. Work with three columns headed 4, 2 and 1. Represent a heap of six by marking 4 and 2. For each move you propose, write down which columns have an odd number of marks afterwards. Use **Compare moves using binary** to test two rival predictions without moving any counters. [Play Tricky 2](https://alberttansinhon.com/math-arcade/#play/nim/1/2)

**4. Choose the seat.** On a new board the four heaps are 2, 5, 3 and 4. Would you play first or second against someone who always makes a winning move when one is available? Commit before opening the comparison panel. Use **Restart with Atlas first** to test your second-player plan and explain the first reply you choose. [Play Tricky 8](https://alberttansinhon.com/math-arcade/#play/nim/1/8)

### Teaching notes and worked answers

**Start with replies the learner can see.** Taking five from C leaves three heaps of one. Atlas empties A, leaving two singletons for the learner. Either choice lets Atlas take the last. Taking six instead leaves A and B for Atlas. It must choose one, and the learner takes the other. This short argument covers *every* reply. Ask a learner who says “I won” to explain both possibilities without touching the controls.

**From copying a move to restoring a property.** With two equal heaps, the second player can mirror any removal from the other heap. The two heaps return to equality after each pair of turns, including the pair that empties them. With unequal heaps the first player can reduce the larger to match the smaller, then mirror. Thus (2, 2) and (1, 3) give opposite outcomes despite having the same total. Ask for these two examples when a learner proposes that an even total decides the winner. With more heaps, there may be no matching heap to copy. What else can the reply restore?

**Count odd binary columns.** Write each heap in binary. Count the ones down each column, recording 1 for odd and 0 for even. The resulting binary number is the *nim-sum*, also called bitwise exclusive OR or XOR. For Tricky 2 the rows are 110, 011, 010 and 100. Their column counts from left to right are 2, 3 and 1. The resulting nim-sum is 011, or 3. Here are all three moves that restore even counts throughout.

| Remove | Heaps after the move | Resulting nim-sum |
| --- | --- | --- |
| 1 from A | 5, 3, 2, 4 | 0 |
| 3 from B | 6, 0, 2, 4 | 0 |
| 1 from C | 6, 3, 1, 4 | 0 |

**Why the rule works.** Call the current nim-sum *S*. Changing a heap from *h* to *k* changes the nim-sum to *S* ⊕ *h* ⊕ *k*, because a bit paired with itself cancels. At zero, any legal change makes at least one column odd. When *S* is non-zero, choose a heap with a 1 at the highest odd column and set *k* = *h* ⊕ *S*. All higher bits stay unchanged and the chosen bit falls to 0, so this really is a reduction. The new nim-sum is zero. This also proves completeness in the table. To restore zero in a chosen heap, that value of *k* is the only candidate. The empty position has zero nim-sum and no move. Since every turn removes counters, repeatedly handing over zero eventually takes the last counter. This is Bouton's normal-play strategy. [Original paper, pp. 35–39](https://sites.ualberta.ca/~hayward/cgt/asn/bouton1901.pdf)

**A losing opening still contains a worthwhile decision.** Tricky 8 has nim-sum zero and four distinct heap sizes. Choose second. Atlas takes one from A, leaving (1, 5, 3, 4). The nim-sum is now 3. Empty C to leave (1, 5, 0, 4), with nim-sum zero again. Distinguish the opponent's observed choice from the general guarantee. You can force victory against every first move by restoring zero, though the reply will depend on that move. The player who starts from zero can still beat a fallible opponent.

### What counts as understanding?

Ask learners to label a position with the next player, give one reply that defeats a plausible losing move and explain how their winning method covers every counterplay. For beginners, accept a spoken demonstration on two equal heaps. For an advanced exit ticket, change the rule on paper so whoever takes the last counter **loses**. A single heap of one then gives the player to move a loss despite its non-zero nim-sum. Identifying exactly which terminal assumption changed shows where the proof stops applying.

The fixed openings and move counts above were checked against the shipped generator and an independent recursion that marks a position winning if it has a losing child. The technical paper and accompanying tests distinguish that finite verification from the general proof. [Nim Lab technical paper](https://github.com/Albertito-AI/atlas-open-mathematics/blob/main/docs/NIM_RESEARCH.md) · [Independent checker](https://github.com/Albertito-AI/atlas-open-mathematics/blob/main/research/arcade/nim.test.mjs)

## Reversi Endgame Lab

**Can the move that flips the fewest discs give you the greatest final lead?** An endgame short enough to calculate by hand lets players argue over this question, then settle it. A player who has understood the lesson can draw the relevant replies, score each ending from one colour’s perspective and explain which score they can guarantee.

### At the board

The dotted squares are legal placements. To find the reason for a dot, trace a straight line from that square through one or more opposing discs to a disc of your own colour. Check all eight directions. Every enclosed line flips. When one side has no legal move it must pass. When both sides have none, count the discs, even if empty squares remain. The lab’s target is your final number of discs minus your opponent’s against best replies. [Official rules](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english)

A first-time player can follow just the three empty squares on the warm-up board. Say a coordinate aloud before placing a disc. On a keyboard, use the arrow keys to explore and Enter or Space to place. In pairs, one player proposes a move, while the other speaks for the opposing colour and tries to refute it. Swap roles for the second position.

### Play before opening the key

1. **Trace the captures.** In Warm-up 7, White has G2, H7 and H8. For each candidate, write down the squares that would flip. Rank the candidates using immediate captures alone. Does that information settle which to play? Record a prediction before opening **Compare moves**. [Warm-up 7](https://alberttansinhon.com/math-arcade/#play/reversi/0/7)
2. **Give the opponent a voice.** Play your chosen move and record the computer’s reply, including a pass. Use **Replay position** to test a different opening. On paper, investigate one legal reply the computer passed over. If you wanted to promise a result to a team-mate, which opposing reply would your promise have to survive?
3. **Test your own rule.** Move to the second three-square position. Black can play A2, A8 or B8. Consider three predictions. Which move flips the most discs, which leaves White without a move, and which gives Black the largest final lead? Assign one opening to each member of a trio. Reassemble the three lines before comparing scores. [Warm-up 14, displayed as Puzzle E](https://alberttansinhon.com/math-arcade/#play/reversi/0/14)
4. **Defend a loss.** In Expert 7, Black’s target is negative. Choose between A8 and B7. Before exploring the continuations, write a sentence explaining what success could mean from this position. Check both opening values in **Compare moves**. How many discs of final margin does the better defence preserve? [Expert 7](https://alberttansinhon.com/math-arcade/#play/reversi/2/7)

### Teacher key and mathematical argument

White begins Warm-up 7 with 26 discs against Black’s 35. G2 flips F2 and G3. H7 flips G6 and H6. H8 flips G7 and F6. Each move adds one new White disc and converts two Black discs, so each improves White’s immediate margin by five. All three leave White four behind. The difference lies in the moves available afterwards.

The following are **all legal continuations** of this opening. Read each line left to right, keeping the score in White’s units throughout.

| First placement | Remaining play, in order | White discs | Black discs | White margin |
| --- | --- | ---: | ---: | ---: |
| White G2 | Black passes, White H7, Black passes, White H8 | 35 | 29 | +6 |
| White G2 | Black passes, White H8, Black H7 | 31 | 33 | −2 |
| White H7 | Black G2, White H8 | 28 | 36 | −8 |
| White H8 | Black G2, White H7 | 28 | 36 | −8 |
| White H8 | Black H7, White G2 | 31 | 33 | −2 |

After G2 and Black’s compulsory pass, **White** chooses between +6 and −2. White can secure +6 by continuing H7. After an immediate H8, **Black** chooses between −8 and −2 for White. Black selects −8. H7 also yields −8. Working back from the leaves therefore gives White a choice of +6, −8 and −8 at the root. Ask who controls each fork before accepting any numerical answer. Taking the largest number in every row silently gives White control of Black’s decisions. This backwards reasoning is minimax. [Berkeley’s introduction to minimax](https://inst.eecs.berkeley.edu/~cs188/textbook/games/minimax.html)

On **Warm-up 14**, Black’s A8 flips just B7. White must play B8, then Black plays A2 and wins 50–14, a margin of +36. Black’s A2 flips two, followed by White A8 and Black B8 for +30. Black’s B8 also flips two and forces White to pass, yet Black must then play A2, White plays A8, and the margin is again +30. This position supplies a counterexample to both “take the most discs” and “always force a pass”. It also gives the corner a fair hearing after Warm-up 7. A corner can be the right choice when the continuation supports it.

On **Expert 7**, A8 flips five discs and has an exact final margin of −6. B7 flips eight and its margin is −32. The better defence improves Black’s guaranteed margin by 26. As a numerical extension, a placement flipping $k$ discs changes the mover’s immediate margin by $1+2k$. Ask learners to derive that expression by counting both colours, then explain why it still cannot rank the two moves correctly.

### Evidence of learning

Give one mark each for a legal capture justified by a bracket, a correct forced pass or best opposing reply, an accurately signed final margin, and an argument comparing at least two openings on the transfer board. A learner can earn all four with a labelled paper tree. A completed online board alone shows the resulting line but leaves the reasoning unknown.

For a longer investigation, pairs can predict whether the move with the most flips is optimal on twelve preselected positions. Agree beforehand how to count ties and keep the losing examples. The endgame generator deliberately seeks positions with legal moves of unequal value. Any observed frequency describes those selected boards. The three-square counterexample above already settles whether the rule works *every* time. [Reversi research paper, generator and independent checks](https://github.com/Albertito-AI/atlas-open-mathematics/blob/main/docs/REVERSI_RESEARCH.md)

## What travels from one board to another?

Three paired investigations for a longer course

### Sudoku and Target Forge · Finding one versus ruling out all

Have one team offer a legal four-tile expression and another offer a legal Sudoku digit. Ask the class why the first team may already have finished its task. One expression proves the target is attainable. Checking a digit against its immediate neighbours establishes local consistency. The learner still has to show why the completed grid must put that digit there. Swap the burdens of proof. The Forge team now has to prove that integer-only steps cannot achieve its Expert target. The Sudoku team now has to exhibit one completed grid. Both teams should say when a single construction suffices and when an argument must cover alternatives.

### Lattice Dash and Parity Lights · When order matters

On the Lattice starter, rearrange the same three jump keys. Two orders stay on the board and one crosses its boundary. In Parity Lights, press two overlapping switches in opposite orders and compare the endings. Both games let a player add the effects algebraically. Only the lattice walk requires every intermediate landing to be legal. Ask for an example that breaks “if the sum is right, the plan works”. Then ask which game permits sorting an entire solution without rechecking its intermediate positions.

### Nim and Reversi · Making a promise against opposition

Give each pair the sentence “I can guarantee \_\_\_ provided \_\_\_”. In Nim a move can guarantee a win by handing the opponent a zero nim-sum and restoring it after each reply. The guarantee in an expert Reversi position can instead be a loss by at most six discs against optimal defence. Ask the other pair to choose the opponent’s replies. A guarantee survives that choice. A favourable sequence chosen by the player for both sides may collapse.

### A seminar extension

Give a claim without the game’s verdict. Invite one person to submit a witness, another to find a counterexample and a third to decide precisely what the evidence establishes. This format is also suitable for a reasoning seminar in law. A single counterexample defeats an unrestricted mathematical claim. A legal analogy would still need authority, facts and an account of its scope. Ask students to state where the analogy ends.

## Six investigations learners can own

Make one conjecture precise enough that a classmate could overturn it.

| Game                    | Investigation and record                                                                                                                                                            | What would settle the claim?                                                                                                                                                                               |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Sudoku**              | Does the number of given clues tell you whether naked singles suffice? Record the clue count, initial number of singles and the step at which a fixed singles-only procedure stops. | Two boards with equal clue counts but different outcomes refute sufficiency of clue count. If the sample contains no such pair, report which openings were examined.                                       |
| **Lattice Dash**        | On paper, remove one obstacle at a time from the same board. Predict which changes shorten the minimum. Retain the jump keys, start and destination.                                | A shorter route certifies improvement when it beats the proven old minimum. To establish that a removal leaves the minimum unchanged, also rule out shorter routes.                                        |
| **Target Forge**        | Keep the four tiles fixed and vary the target on paper. Catalogue values attainable using only integer intermediates. Repeat allowing fractions and compare the sets.               | For each new target, exhibit a legal fractional expression. To certify that it is new, show that the integer-only enumeration covers every possible final split of the tiles.                              |
| **Parity Lights**       | On a 3 × 3 board, construct openings that can be solved using two distinct switches. Group them by the number of lit lamps. Does that count determine the minimum?                  | To test the claim on all solvable 3 × 3 openings, include openings made by other numbers of switches. Seek equal light counts with different proven minima.                                                |
| **Nim Lab**             | Can one starting position have several winning moves? For each heap in a non-zero position, look for a smaller size that would make the new nim-sum zero.                           | For heap size *h* and current nim-sum *S*, the only possible new size is *h* ⊕ *S*. Count the heaps for which that value is smaller. This counts moves by labelled heap, even when heaps have equal sizes. |
| **Reversi Endgame Lab** | Preselect positions before viewing their values. Record the largest immediate flip count and the exact final margin of every legal opening. Keep tied moves visible.                | One position with a strictly worse highest-flip move refutes a universal greedy rule. A claim about how often that rule fails depends on how the positions were selected.                                  |

A replayable research note needs the game, level, decimal seed from the shared URL, rules used, conjecture, result and a worked check. For a modified paper position, also record the starting board and the exact change.

## Find out what the player learned

| Evidence to collect                       | Question for the teacher                                                                                                 |
|-------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| A legal move with its predicted effect    | Could another player reproduce it from the stated position?                                                              |
| A comparison of two choices               | Did the learner give a reason before the result appeared? Can they explain why the alternative behaves differently?      |
| A claim with an appropriate justification | Does a construction, lower bound, exhaustive check, invariant or opponent’s reply actually establish what was claimed?   |
| A fresh position, solved individually     | Can the learner reuse the idea or explain where it stops working? Record hints and peer assistance alongside the answer. |

For formative marking, record each item as **independent**, **with a prompt** or **not yet shown**. Keep the four observations separate. A learner can understand a proof while still needing help entering the move. Another can operate the board fluently while needing help defending the result.

### A researchable club question

Does asking for a prediction before play help learners reject a greedy strategy on a new board? Pick one game. In Parity Lights, for example, a player can learn that the number of lit lamps can rise en route to a shortest solution. Prepare two previously unseen positions matched for size, par and the feature under study. Before the lesson, get an individual prediction on the first position. After the worked comparison, give the second position without hints. Reverse their order for half the group if practical.

Retain the anonymous reasoning, move chosen and help used, including incomplete attempts. Mark the explanations against a rule agreed in advance, such as “predicts a temporary increase and explains which row the move helps settle”. At the next club meeting, try another unseen example before offering a reminder. Report the numbers attempted and the numbers meeting the criterion. Unequal puzzle difficulty, prior familiarity and repeated practice can all affect the result. This small comparison can guide the next lesson. Claims of a causal effect would need a stronger study design.

**Source note.** The six game modules used for the positions in this guide matched the public website on 28 November 2026. The chapters link to the fixed openings, their formal arguments or official rules, and independent checks where available. [Research archive and reproduction instructions](https://github.com/Albertito-AI/atlas-open-mathematics/tree/main/research/arcade).

[Teaching resources](https://alberttansinhon.com/math-arcade/teaching/) · [Play the arcade](https://alberttansinhon.com/math-arcade/) · [Research papers on GitHub Pages](https://albertito-ai.github.io/Albertito-AI/maths-arcade-research/) · [Research archive and reproducibility](../../research/arcade/README.md)

Original educational text and diagrams are available under [Creative Commons Attribution 4.0](../../LICENSE-CONTENT.md). Credit Albert Tan Sin Hon and the named contributors, link to the source version and identify any adaptations.
