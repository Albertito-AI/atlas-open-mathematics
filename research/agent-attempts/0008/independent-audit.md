# Independent exact quadrature corroboration

15 November 2026. Separate automated critical reviewer; original educational
code CC BY 4.0. This is public reproduction evidence, not confidential
editorial review or human peer review. No learner trial occurred.

Save the following block as `/tmp/atlas_fourier_independent.py` and run
`python /tmp/atlas_fourier_independent.py`. Python 3.12.14, exit 0.
Block SHA-256 (including trailing newline): `9134f125d961d485541720bfabb1f99b9ef2af8a9235deeae82809d079c85999`.
The root agent separately replayed the supplied code with the same output.

```python
"""Exact quadrature corroboration for attempt 0008; educational CC BY 4.0.

Represent r + s*sqrt(2) by (r, s), using rational arithmetic only.
Eight equally spaced samples integrate the squared polynomials here exactly:
their frequencies have absolute value at most four, and the average of
exp(2*pi*i*n*j/8) over j=0,...,7 is zero unless n is a multiple of eight.
Derivatives are divided by 2*pi. No Laurent convolution is used.
This finite check does not verify the time exponentials or a universal PDE.
"""
from fractions import Fraction as Q
from itertools import product
import json


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def scale(c, x):
    return (c * x[0], c * x[1])


def square(x):
    return (x[0] * x[0] + 2 * x[1] * x[1], 2 * x[0] * x[1])


def average_squares(values):
    total = (Q(0), Q(0))
    for value in values:
        total = add(total, square(value))
    return scale(Q(1, len(values)), total)


ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))
NEG_ONE = (Q(-1), Q(0))
HALF_ROOT_TWO = (Q(0), Q(1, 2))
NEG_HALF_ROOT_TWO = (Q(0), Q(-1, 2))
SINE = [ZERO, HALF_ROOT_TWO, ONE, HALF_ROOT_TWO,
        ZERO, NEG_HALF_ROOT_TWO, NEG_ONE, NEG_HALF_ROOT_TWO]
COSINE = [ONE, HALF_ROOT_TWO, ZERO, NEG_HALF_ROOT_TWO,
          NEG_ONE, NEG_HALF_ROOT_TWO, ZERO, HALF_ROOT_TWO]


def samples(c, terms):
    values, derivatives = [], []
    for j in range(8):
        value, derivative = (Q(c), Q(0)), ZERO
        for m, a, b in terms:
            index = (m * j) % 8
            value = add(value, add(scale(a, SINE[index]),
                                   scale(b, COSINE[index])))
            derivative = add(derivative, add(scale(m * a, COSINE[index]),
                                              scale(-m * b, SINE[index])))
        values.append(value)
        derivatives.append(derivative)
    return average_squares(values), average_squares(derivatives)


count = 0
for a, b, d, e in product(range(-2, 3), repeat=4):
    norm, gradient = samples(Q(1, 3), [(1, a, b), (2, d, e)])
    assert norm == (Q(1, 9) + Q(a*a + b*b + d*d + e*e, 2), Q(0))
    assert gradient == (Q(a*a + b*b + 4*d*d + 4*e*e, 2), Q(0))
    count += 1

cancel = samples(0, [(1, 1, 0), (1, -1, 0)])
reinforce = samples(0, [(1, 1, 0), (1, 1, 0)])
constant = samples(Q(-7, 3), [])
assert cancel == ((Q(0), Q(0)), (Q(0), Q(0)))
assert reinforce == ((Q(2), Q(0)), (Q(2), Q(0)))
assert constant == ((Q(49, 9), Q(0)), (Q(0), Q(0)))

print(json.dumps({
    "method": "eight-point exact quadrature in Q(sqrt(2))",
    "distinct_frequency_cases": count,
    "duplicate_cancel_norm_squared": str(cancel[0][0]),
    "duplicate_cancel_scaled_gradient_squared": str(cancel[1][0]),
    "duplicate_reinforce_norm_squared": str(reinforce[0][0]),
    "duplicate_reinforce_scaled_gradient_squared": str(reinforce[1][0]),
    "constant_norm_squared": str(constant[0][0]),
    "constant_gradient_squared": str(constant[1][0]),
    "irrational_residuals_zero": True,
    "scope": "Frozen finite cases at t=0 only; no universal PDE or learning claim"
}, sort_keys=True))
```

Observed output:

```json
{"constant_gradient_squared": "0", "constant_norm_squared": "49/9", "distinct_frequency_cases": 625, "duplicate_cancel_norm_squared": "0", "duplicate_cancel_scaled_gradient_squared": "0", "duplicate_reinforce_norm_squared": "2", "duplicate_reinforce_scaled_gradient_squared": "2", "irrational_residuals_zero": true, "method": "eight-point exact quadrature in Q(sqrt(2))", "scope": "Frozen finite cases at t=0 only; no universal PDE or learning claim"}
```

This uses frequencies 1 and 2 only. Eight-point quadrature is not exact for
arbitrary higher frequencies: for example sin(8*pi*y) has squared norm 1/2
but vanishes at all eight sample points. Do not reuse the sampling rule
without a degree/aliasing check. The analytic proof is in [the record](record.md).
