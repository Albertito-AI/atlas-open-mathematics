# When a rational answer is not an integer solution

**Question Q0001.** Given integers $p$ and $q$, when do the equations

$$
2x+3y=p,\qquad -x+4y=q
$$

have a solution in integers $x$ and $y$?

This lesson develops the [first domain lesson](001-domain-matters.md) into a
criterion that covers every integer pair $(p,q)$. You need substitution,
elimination and the meaning of divisibility: $11\mid n$ means that
$n=11k$ for some integer $k$, which may be positive, zero or negative.
The mathematics is established. This is a teaching and verification exercise,
with no novelty or Millennium Prize claim.

## Prove both directions

The exact criterion is

$$
\bigl(\exists x,y\in\mathbb Z:\ 2x+3y=p\ \text{and}\ -x+4y=q\bigr)
\quad\Longleftrightarrow\quad 11\mid p+2q.
$$

**Necessity.** Suppose an integer solution exists. Add the first equation to
twice the second:

$$
(2x+3y)+2(-x+4y)=p+2q,
\qquad 11y=p+2q.
$$

Since $y$ is an integer, $p+2q$ must be divisible by 11. This direction
can rule out solutions, but alone does not establish that passing the test is
enough.

**Sufficiency.** Suppose $p+2q=11k$ for an integer $k$. Construct

$$
y=k,\qquad x=4k-q.
$$

Both values are integers. Check each original equation:

$$
2(4k-q)+3k=11k-2q=p,
\qquad -(4k-q)+4k=q.
$$

This explicit witness proves that the divisibility condition is sufficient.
Moreover, every solution must have $y=(p+2q)/11$, and the second equation
then fixes $x=4y-q$. The solution, when it exists, is unique.

| Integer right-hand side | Divisibility check | Conclusion |
| --- | --- | --- |
| $p=5,\ q=3$ | $p+2q=11$, so $k=1$ | $(x,y)=(1,1)$; substitution gives $5$ and $3$. |
| $p=7,\ q=-2$ | $p+2q=3$, which is not divisible by 11 | No integer solution. The rational solution remains $(34/11,3/11)$. |

The coefficient determinant is $2\cdot4-3(-1)=11$. Its nonzero value
ensures a unique rational solution for every rational right-hand side.
Integer feasibility asks an additional question about that solution's domain.

## Why one divisibility test works here

For an arbitrary integer matrix and integer right-hand side, write

$$
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
A\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}p\\q\end{pmatrix},
\qquad \Delta=ad-bc\ne0.
$$

The inverse formula, or Cramer's rule, gives

$$
x=\frac{dp-bq}{\Delta},\qquad
y=\frac{aq-cp}{\Delta}.
$$

MIT's Lecture 20 summary derives the inverse and determinant-ratio formulas
on pp. 1–2.[^mit] Consequently, an integer solution exists exactly when
$\Delta$ divides **both** numerators. This divisibility conclusion follows
by applying those formulas over the integers; it is not a separate empirical
finding from our examples.

In Q0001, checking $y$ suffices because $x=4y-q$. Once $y$ and $q$
are integers, that expression is an integer too. The proof explains why the
second check is redundant for this family. It does not authorise dropping a
check for an arbitrary matrix.

Consider the dense matrix example

$$
\begin{pmatrix}2&2\\2&4\end{pmatrix}
\begin{pmatrix}x\\y\end{pmatrix}
=\begin{pmatrix}1\\2\end{pmatrix}.
$$

Here $\Delta=4$, the numerator for $x$ is $4(1)-2(2)=0$, and the
numerator for $y$ is $2(2)-2(1)=2$. Checking only the first numerator
would pass: 4 divides 0. Nevertheless, the unique rational solution is
$(0,1/2)$, which is not an integer pair. Indeed, $2x+2y=1$ cannot hold
for integers, since its left-hand side is even. This example specifically
refutes checking only the **$x$-numerator**. With the same matrix and
right-hand side $(1,1)$, the solution $(1/2,0)$ instead shows that
checking only the **$y$-numerator** can also fail.

For larger integer systems, Smith normal form provides a systematic route:
integer changes of coordinates reduce the equations to divisibility and
consistency conditions. Greenwell and Kertzner explain that framework and
give conditions for integer matrix solutions on pp. 49–53.[^greenwell]
Their general treatment supplies context; the direct proof above establishes
the particular Q0001 criterion without requiring that machinery.

## A practical toy model: indivisible batches

Suppose one whole batch of type X uses three units of material A and one
unit of material B. One whole batch of type Y uses two units of A and five
units of B. To use **exactly** eight units of A and seven units of B, solve

$$
3x+2y=8,\qquad x+5y=7.
$$

The determinant is $3\cdot5-2\cdot1=13$, so

$$
x=\frac{5(8)-2(7)}{13}=2,\qquad
y=\frac{3(7)-8}{13}=1.
$$

Two X batches and one Y batch satisfy both totals exactly. The counts are
integers, and they are also nonnegative. These are separate requirements:
an integer solution with a negative count cannot describe making whole
batches. This is an illustrative model, not a study of an operating process.
If the totals are capacity limits rather than exact requirements, the model
needs inequalities; the equations would answer a different question.

## Public practice

Try these before reading the solutions. They are visible practice material,
not a hidden assessment set.

1. For Q0001, take $(p,q)=(9,1)$. Decide whether an integer solution exists,
   construct it and check both equations.
2. For Q0001, take $(p,q)=(0,1)$. Explain why there is no integer solution
   without searching through candidate pairs.
3. In the batching model, replace the exact totals by one unit of A and nine
   units of B. Find the unique solution. Distinguish rational solvability,
   integer feasibility and feasibility as nonnegative batch counts.
4. A proposed general solver checks only that $\Delta\mid dp-bq$.
   Use the dense matrix example to explain precisely what this check misses.

### Solutions and assessment guide

1. $9+2(1)=11$, so $k=1$, $y=1$ and $x=4-1=3$.
   Then $2(3)+3(1)=9$ and $-3+4(1)=1$.
2. Any solution would satisfy $11y=2$. No integer $y$ does, because
   11 does not divide 2. An unsuccessful finite search is unnecessary.
3. The determinant remains 13. The formulas give
   $x=(5-18)/13=-1$ and $y=(27-1)/13=2$.
   Substitution gives $3(-1)+2(2)=1$ and $-1+5(2)=9$.
   This is the unique rational solution and is an integer pair, but its
   negative X count makes the stipulated batching task infeasible.
4. For $A=\left(\begin{smallmatrix}2&2\\2&4\end{smallmatrix}\right)$
   and $(p,q)=(1,2)$, the checked numerator is 0 and is divisible by 4.
   The unchecked numerator is 2, leaving $y=1/2$. A certificate of an
   integer pair must establish integrality of both coordinates, either
   directly or through a proved implication between them.

An explanation should identify the domain, justify necessity and sufficiency
where applicable, check the proposed witness and preserve practical
constraints. Publishing this lesson does not establish improved human or
agent performance. A transfer study would need separately prepared tasks,
a stated rubric and recorded observations.

## What has been checked

The [Lean source](../research/agent-attempts/0002/IntegerCriterion.lean)
contains four universal statements over the integers: necessary divisibility,
the explicit witness, the solvability equivalence and uniqueness. The
[formal evidence](../research/agent-attempts/0002/formal-evidence.json)
records their successful local check with pinned Lean 4.24.0, the exact
source hash and the transitive axiom reports. This verifies those precise
statements under the recorded assumptions. It does not verify the Python
implementation, the arbitrary-matrix discussion or a teaching outcome.

The separate [finite evidence](../research/agent-attempts/0002/finite-evidence.json)
records 529 pairs with $-11\le p,q\le11$, the counterexample and the
batching practice case. These computations support their stated finite scope;
the universal result rests on the proof, not the size of that sample.

From the repository root, reproduce the finite checks with:

```sh
python research/agent-attempts/0002/check_examples.py
```

With the pinned Lean 4.24.0 distribution specified in
[the toolchain manifest](../formal/toolchain.json), reproduce the formal
check with:

```sh
lean research/agent-attempts/0002/IntegerCriterion.lean
```

Compare the theorem names and axiom reports with the evidence record.
An arbitrary executable named `lean` is not a substitute for the pinned
toolchain. This lesson has not undergone journal peer review.

## The next formalisation question

For a nonsingular integer matrix
$A=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)$, when does
an integer $y$ force an integer $x$ for **every integer right-hand side**?
The proposed next generalisation is

$$
\bigl[\text{for every }p,q\in\mathbb Z,\ y\in\mathbb Z
\text{ in the unique rational solution implies }x\in\mathbb Z\bigr]
\quad\Longleftrightarrow\quad \gcd(|a|,|c|)=1.
$$

Here is the ordinary mathematical argument. If the greatest common divisor
is 1, Bézout's identity supplies integers $u,v$ with $ua+vc=1$.
Thus $x=u(p-by)+v(q-dy)$ is an integer whenever $y$ is. Conversely,
if $g=\gcd(|a|,|c|)>1$, choose the integer right-hand side
$(a/g,c/g)$. Its unique rational solution is $(1/g,0)$, which defeats
the implication. Nonsingularity excludes $a=c=0$, so $g$ is positive;
the argument also covers one of $a,c$ being zero.

This is a standard consequence of Bézout's identity, proposed for the
project's next formalisation, not a new discovery. Its machine verification
is pending and is not included in the four checked Q0001 statements.

## Sources and reuse

[^mit]: MIT OpenCourseWare, *18.06SC Linear Algebra*, Fall 2011,
    [Lecture 20 summary, “Cramer's rule, inverse matrix, and volume”](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/f6e46da0d783d8f9c0a25c407c76166a_MIT18_06SCF11_Ses2.7sum.pdf),
    pp. 1–2. The two-by-two inverse appears on p. 1 and Cramer's rule on
    p. 2.

[^greenwell]: Raymond N. Greenwell and Stanley Kertzner,
    [“Solving Linear Diophantine Matrix Equations Using the Smith Normal Form (More or Less)”](https://sites.hofstra.edu/raymond-greenwell/wp-content/uploads/sites/9/2019/07/Smith_Normal_Form.pdf),
    *International Journal of Pure and Applied Mathematics* 55(1) (2009),
    49–60, especially pp. 49–53: the integer-domain motivation, Smith normal
    form and solvability conditions.

Original educational prose: [CC BY 4.0](../LICENSE-CONTENT.md). Prepared with
AI assistance for Atlas Open Mathematics. Linked third-party sources retain
their own rights; this licence does not relicense them.
