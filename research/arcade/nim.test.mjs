import test from 'node:test';
import assert from 'node:assert/strict';
import { legalMoves, makeNim, nimSum, optimalMove, playMove } from './nim.mjs';

// These helpers implement only the rules of play, without the XOR criterion.
function children(heaps) {
  const result = [];
  for (let heap = 0; heap < heaps.length; heap++) {
    for (let after = heaps[heap] - 1; after >= 0; after--) {
      const board = [...heaps];
      board[heap] = after;
      result.push({ heap, take: heaps[heap] - after, board });
    }
  }
  return result;
}

const memo = new Map();
function wins(heaps) {
  const key = heaps.join(',');
  if (!memo.has(key)) memo.set(key, children(heaps).some(child => !wins(child.board)));
  return memo.get(key);
}

function* boards(piles, cap, prefix = []) {
  if (prefix.length === piles) yield prefix;
  else for (let count = 0; count <= cap; count++) yield* boards(piles, cap, [...prefix, count]);
}

test('compare the theorem, every legal move and the optimal policy with an independent game tree', () => {
  let inspected = 0;
  for (const [piles, cap] of [[3, 7], [4, 5], [5, 3]]) {
    for (const heaps of boards(piles, cap)) {
      inspected++;
      const expected = children(heaps);
      assert.equal(nimSum(heaps) !== 0, wins(heaps));
      assert.deepEqual(legalMoves(heaps), expected.map(({heap,take}) => ({heap,take})));
      for (const {heap, take, board} of expected) assert.deepEqual(playMove(heaps, heap, take), board);
      const move = optimalMove(heaps);
      if (!expected.length) { assert.equal(move, null); continue; }
      const choice = expected.find(child => child.heap === move.heap && child.take === move.take);
      assert.ok(choice, `illegal computer move on ${heaps}`);
      assert.equal(wins(choice.board), !wins(heaps));
      const winningCount = expected.filter(({board}) => !wins(board)).length;
      assert.equal(winningCount % 2, Number(wins(heaps)));
    }
  }
  assert.equal(inspected, 2832);
});

test('seed 7 reproduces the example, its alternative and its winning line', () => {
  const opening = makeNim(0, 7);
  assert.deepEqual(opening, [1, 1, 6]);
  assert.deepEqual(optimalMove(opening), {heap: 2, take: 6});
  assert.equal(nimSum(playMove(opening, 2, 2)), 4);
  const reply = playMove(opening, 2, 6);
  assert.equal(nimSum(reply), 0);
  assert.equal(wins(reply), false);
  const move = optimalMove(reply);
  assert.deepEqual(move, {heap: 0, take: 1});
  assert.deepEqual(playMove(playMove(reply, move.heap, move.take), 1, 1), [0, 0, 0]);
  assert.deepEqual(opening, [1, 1, 6]);
});

test('seeded tiers form bounded, reproducible and varied openings, with opportunities from either seat', () => {
  for (const [level, cap] of [[0,6], [1,7], [2,15]]) {
    const unique = new Set();
    for (let seed = 0; seed < 512; seed++) {
      const heaps = makeNim(level, seed);
      assert.deepEqual(heaps, makeNim(level, seed));
      assert.equal(heaps.length, level + 3);
      assert.ok(heaps.every(count => Number.isInteger(count) && count >= 1 && count <= cap));
      if (level === 0) assert.notEqual(nimSum(heaps), 0);
      if (level > 0 && seed % 4 === 0) assert.equal(nimSum(heaps), 0);
      unique.add(heaps.join(','));
    }
    assert.ok(unique.size > 100);
  }
  assert.notEqual(nimSum(makeNim(1,7)), 0);
  assert.notEqual(nimSum(makeNim(2,7)), 0);
  assert.deepEqual(makeNim(2, 0xffffffff), makeNim(2, 0xffffffff));
});

test('invalid tiers, seeds and moves fail without changing the input board', () => {
  for (const level of [-1,3,0.5]) assert.throws(() => makeNim(level, 0), RangeError);
  for (const seed of [-1,0.5,2**32,NaN]) assert.throws(() => makeNim(1, seed), RangeError);
  const board = [1,0,3];
  for (const [heap,take] of [[0,0], [1,1], [0,2], [3,1], [-1,1], [0.5,1], [2,1.5]]) {
    assert.throws(() => playMove(board, heap, take), RangeError);
  }
  assert.deepEqual(board, [1,0,3]);
});
