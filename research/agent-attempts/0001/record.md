# Agent-assisted research exercise 0001

Date: 9 November 2026. Contributor: ChatGPT coding/research agent, under
Albert Tan Sin Hon's direction. Activity: known mathematical exercise and
teaching design. No claim of new mathematics or a measured model improvement.

The agent proposed the exact solution to 2x + 3y = 7 and -x + 4y = -2.
Twice the second equation plus the first gives 11y = 3, hence y = 3/11.
Substitution gives x = 34/11. The determinant is 11, so this rational solution
is unique. Over integers there is no solution, since 11y = 3 has no integral y.

The candidate in candidate.json was submitted to the separately implemented
exact verifier; verification.json contains its actual output. Reproduce with:

```sh
python -m atlas_math verify --case research/agent-attempts/0001/problem.json --candidate research/agent-attempts/0001/candidate.json
```

This is a live agent-authored candidate checked during the project launch.
The scripted demo's baseline/corrected comparison is a separate exercise.
This single result does not measure autonomous learning or human understanding.

Follow-up question: for integer p and q, when do 2x+3y=p and -x+4y=q
have an integer solution? The [teaching companion](../../../lessons/001-domain-matters.md)
develops the criterion and invites independent reproduction.
