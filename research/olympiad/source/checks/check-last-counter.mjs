import assert from 'node:assert/strict';
import problem from '../algebra.mjs';

function positions(benches, budget) {
  if (benches === 0) return [[]];
  const list = [];
  for (let first = 0; first <= budget; first++) {
    for (const rest of positions(benches - 1, budget - first)) {
      list.push([first, ...rest]);
    }
  }
  return list;
}

function nextPositions(state, price = 2) {
  const successors = [];
  for (const [index, counters] of state.entries()) {
    if (counters < price) continue;
    const next = state.slice();
    next[index] -= price;
    next[(index + 1) % state.length]++;
    successors.push(next);
  }
  return successors;
}

function legalClosure(start) {
  const seen = new Set([start.join(',')]);
  const stack = [start];
  while (stack.length) {
    for (const next of nextPositions(stack.pop())) {
      const key = next.join(',');
      if (seen.has(key)) continue;
      seen.add(key);
      stack.push(next);
    }
  }
  return seen;
}

function theorem(start, target) {
  if (target.every(value => value === 0)) return start.every(value => value === 0);
  const weightedDifference = start.reduce((sum, x, i) => sum + (x - target[i]) * 2 ** i, 0);
  let count = weightedDifference / (2 ** start.length - 1);
  if (!Number.isInteger(count) || count < 0) return false;
  for (let i = start.length - 1; i >= 1; i--) {
    count = target[i] - start[i] + 2 * count;
    if (count < 0) return false;
  }
  return true;
}

let comparisons = 0;
for (const [benches, budget] of [[2, 12], [3, 10], [4, 8], [5, 7]]) {
  const states = positions(benches, budget);
  const labels = states.map(state => state.join(','));
  for (const start of states) {
    const reachable = legalClosure(start);
    for (const [i, target] of states.entries()) {
      assert.equal(theorem(start, target), reachable.has(labels[i]),
        `Reachability disagrees: ${start} -> ${target}`);
      comparisons++;
    }
  }
}

const sum = state => state.reduce((total, value) => total + value, 0);
const asStates = set => Array.from(set, key => key.split(',').map(Number));
const first = asStates(legalClosure([8, 0, 0]));
assert.equal(String(8 - Math.min(...first.map(sum))), problem.checkpoints[0].answer);
const terminal = asStates(legalClosure([15, 0, 0, 0])).filter(state => !nextPositions(state).length);
assert.deepEqual(terminal, [[1, 1, 1, 1]]);
assert.equal(String(sum(terminal[0])), problem.checkpoints[1].answer);

// For the ternary transfer use a separate legal-play search in reverse.
// Track which of the four trades occurred; stop at the first all-A pile
// in breadth-first order (each expansion increases the total by two).
const startOfReverse = [0, 2, 0, 1];
let frontier = [{ state: startOfReverse, mask: 0 }];
let minimum = null;
while (frontier.length && minimum === null) {
  const next = new Map();
  for (const { state, mask } of frontier) {
    if (mask === 15 && state.slice(1).every(count => count === 0)) {
      minimum = state[0];
      break;
    }
    for (let bench = 0; bench < 4; bench++) {
      const source = (bench + 1) % 4;
      if (state[source] === 0) continue;
      const result = state.slice();
      result[source]--;
      result[bench] += 3;
      const nextMask = mask | (1 << bench);
      next.set(`${result}|${nextMask}`, { state: result, mask: nextMask });
    }
  }
  assert.ok(!next.size || sum(next.values().next().value.state) <= 115, 'Transfer bound exceeded');
  frontier = [...next.values()];
}
assert.equal(String(minimum), problem.transfer.answer);
console.log(`Last Counter: ${comparisons} ordered binary state pairs, both checkpoints and the ternary minimum passed.`);
