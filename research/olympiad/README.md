# Atlas Math Olympiad: Proof Edition

Four proof problems for individual solvers, teachers and maths circles. In each problem, write down a prediction, choose hints as needed and work through the checkpoints before opening the proof. Each page includes the complete argument, its assessment criteria and a transfer exercise with a worked answer. A separate application presents a decision before its model, then identifies the assumptions that limit its use. Each further investigation invites you to make and test a new claim.

**Edition 1.0.0 · 28 November 2026.** Direction: Albert Tan Sin Hon, Atlas Open Mathematics. The problems and proofs were prepared with AI assistance. [Author and project](https://alberttansinhon.com/) · [ORCID](https://orcid.org/0009-0001-8996-7933) · [Interactive Olympiad](https://alberttansinhon.com/math-arcade/olympiad/) · [Independent GitHub Pages edition](https://albertito-ai.github.io/Albertito-AI/math-arcade/olympiad/)

| Problem and full solution | What you will prove |
| --- | --- |
| [The Last Counter](problems/last-counter.md) | Decide when one counter placement on a directed ring can reach another, and prove that the required trades can be ordered legally. |
| [The shifted squares](problems/shifted-squares.md) | Classify every integer shift and monic polynomial that satisfy two divisibility tests, including the variant that assumes only infinitely many successes. |
| [The Three-Turn Triangle](problems/three-turn-triangle.md) | Find when three operations restore every labelled triangle up to scale, including degenerate settings. |
| [The Two Missing Lamps](problems/two-missing-lamps.md) | Maximise the number of complete eight-point affine cubes among a set of lit lamps and classify every extremal configuration. |

The [machine-readable edition](edition.json) preserves the complete problem text, responses, hints, proofs, marking criteria, applications and investigation questions. A title such as *Summit* describes the intended challenge. Human timing, difficulty and learning gains have yet to be measured. “Olympiad” describes the programme's proof-based format. These programme-written exercises use established mathematics. Their inclusion makes no claim of a new theorem, independent contest endorsement or journal peer review. The geometry construction retains its labelled [diagram and coordinates](source/geometry.svg).

## Verification

Run these commands inside `research/olympiad` after checking out the repository or extracting the archive. They use standard-library Python and Node.js only. This edition was checked with Python 3.12.14 and Node.js 24.22.3.

```sh
node compile-edition.mjs
python3 build.py
node source/checks/check-last-counter.mjs
node source/checks/verify-shifted-squares.mjs
python3 source/checks/geometry.py
python3 source/checks/check-two-missing-lamps.py
node source/checks/variations-check.mjs
python3 source/checks/verify-applications.py
```

| Check | Scope of the reproduced evidence |
| --- | --- |
| Counter reachability | A legal-play search and the proposed criterion agreed on 962,366 ordered pairs of positions. The rings and starting budgets were (2 benches, 12 counters), (3, 10), (4, 8) and (5, 7). A separate reverse search checked the ternary transfer minimum. |
| Shifted squares | Direct polynomial division checked 22,400 bounded polynomial/shift pairs and found five admissible pairs. A further 342 multiplicity boundary cases and a degree-36 transfer count of 17 were checked. |
| Labelled triangles | Exact rational coordinates checked 384 three-pass configurations. The supplementary checks cover the diagram, special settings, centroid preservation and the transfer calculation. |
| Affine cubes | Enumeration examined all 8,008 six-point and 11,440 seven-point subsets of the four-dimensional binary space. It checked all 120 two-hole patterns there, and all 134,596 extensions of a fixed cube to a fourteen-point set in dimension five. |
| Worked applications | Exact calculations check the exchange-ticket reachability decisions, aligned logger bins, printed icon coordinates and competing switch-test schedules. |
| Related practice | For each problem, 261 fixed seeds reproduced the generated answers by a separate calculation. Prompts can coincide for different seeds. |

These finite checks exercise concrete consequences and boundary cases. The general conclusions require the arguments on the individual proof pages. The [source modules](source/) retain the web edition's exact statements and proof steps. To update the derived file after an intentional source edit, run `node compile-edition.mjs --write`, then `python3 build.py --write`. Without those options both commands check the retained text.

## Archive and reuse

[Download the version 1.0.0 archive](https://raw.githubusercontent.com/Albertito-AI/atlas-open-mathematics/main/research/olympiad/releases/Maths_Olympiad_Proof_Edition_v1.0.0.zip) or build the same offline package by running the command below in this directory. It contains spoiler-free printable problem sheets, the four worked solutions, a labelled geometry diagram, source code, checks, a SHA-256 manifest, and both licence notices. Extract the ZIP, then open `research/olympiad/Problem_Sheets.html` in a browser to read or print the problem sheets. The complete proof pages are available as ordinary Markdown files.

```sh
python3 build.py --zip Maths_Olympiad_Proof_Edition_v1.0.0.zip
```

To cite: *Atlas Math Olympiad: Proof Edition*, version 1.0.0, Atlas Open Mathematics, directed by Albert Tan Sin Hon, 28 November 2026. Edition DOI: [10.5281/zenodo.24620475](https://doi.org/10.5281/zenodo.24620475). Include the title and link of the problem used and, where possible, the commit permalink of the edition consulted. Educational text and diagrams use [CC BY 4.0](../../LICENSE-CONTENT.md), and executable code uses the [MIT licence](../../LICENSE). Credit Albert Tan Sin Hon and named contributors and identify adaptations. Referenced publications retain their own rights.
