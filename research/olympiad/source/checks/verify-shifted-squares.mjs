// Run with: node olympiad-stage/checks/verify-shifted-squares.mjs
// Independent direct calculations in Z[x]. Coefficients are in ascending order.
import assert from 'node:assert/strict';
import problem from '../arithmetic.mjs';

function trim(a) {
  while (a.length > 1 && a.at(-1) === 0n) a.pop();
  return a;
}
function multiply(a, b) {
  const product = Array(a.length + b.length - 1).fill(0n);
  for (const [i, ai] of a.entries()) {
    for (const [j, bj] of b.entries()) product[i + j] += ai * bj;
  }
  return trim(product);
}
function power(p, e) {
  let result = [1n];
  for (let i = 0; i < e; i++) result = multiply(result, p);
  return result;
}
function composeSquareShift(p, c) {
  let result = [0n];
  for (let i = p.length - 1; i >= 0; i--) {
    result = multiply(result, [BigInt(c), 0n, 1n]);
    result[0] += p[i];
  }
  return trim(result);
}
function divisible(dividend, divisor) {
  assert.equal(divisor.at(-1), 1n);
  const r = dividend.slice();
  for (let i = r.length - 1; i >= divisor.length - 1; i--) {
    const coefficient = r[i];
    const shift = i - (divisor.length - 1);
    for (let j = 0; j < divisor.length; j++) r[shift + j] -= coefficient * divisor[j];
  }
  return r.every(x => x === 0n);
}
function passes(p, c) {
  return divisible(composeSquareShift(p, 0), p) && divisible(composeSquareShift(p, c), p);
}
function unitNegative(a, b, d) {
  const first = multiply(power([1n, 1n], a), power([-1n, 1n], b));
  return multiply(first, power([0n, 1n], d));
}
function* monic(d, coefficients = []) {
  if (d === 0) { yield [...coefficients, 1n]; return; }
  for (let x = -3n; x <= 3n; x++) yield* monic(d - 1, [...coefficients, x]);
}
function key(c, p) { return String(c) + ':' + p.join(','); }
const actual = new Set();
let testedPairs = 0;
for (let d = 1; d <= 4; d++) {
  for (const p of monic(d)) {
    for (const c of [-4, -3, -2, -1, 1, 2, 3, 4]) {
      testedPairs++;
      if (passes(p, c)) actual.add(key(c, p));
    }
  }
}
const expected = new Set();
for (let k = 1; 2 * k <= 4; k++) expected.add(key(-2, power([-1n, 0n, 1n], k)));
expected.add(key(1, [1n, 0n, 1n, 0n, 1n]));
for (let a = 1; a <= 4; a++) {
  for (let b = a; b <= 2 * a; b++) {
    for (let d = b; d <= 2 * a; d++) {
      if (a + b + d <= 4) expected.add(key(-1, unitNegative(a, b, d)));
    }
  }
}
assert.deepEqual(actual, expected);
let boundaryTests = 0;
for (let a = 0; a <= 6; a++) {
  for (let b = 0; b <= 6; b++) {
    for (let d = 0; d <= 6; d++) {
      if (a + b + d === 0) continue;
      boundaryTests++;
      const valid = a > 0 && a <= b && b <= d && d <= 2 * a;
      assert.equal(passes(unitNegative(a, b, d), -1), valid);
    }
  }
}
const count = new Set();
for (let a = 0; a <= 36; a++) {
  for (let b = 0; a + b <= 36; b++) {
    const p = unitNegative(a, b, 36 - a - b);
    if (passes(p, -1)) count.add(key(-1, p));
  }
}
for (const [c, p] of [[-2, power([-1n, 0n, 1n], 18)], [1, power([1n, 0n, 1n, 0n, 1n], 9)]]) {
  assert.ok(passes(p, c));
  count.add(key(c, p));
}
const dChecks = Array.from({length: 12}, (_, d) => d).filter(d => passes(unitNegative(3, 4, d), -1));
assert.deepEqual(dChecks, [4, 5, 6]);
assert.deepEqual(problem.checkpoints.map(x => x.answer), ['1', '2', String(dChecks.at(-1))]);
assert.equal(problem.transfer.answer, String(count.size));
console.log(testedPairs + ' bounded polynomial/shift pairs checked directly; ' + actual.size + ' admissible.');
console.log(boundaryTests + ' multiplicity boundary cases verified. Degree-36 transfer: ' + count.size + '.');
