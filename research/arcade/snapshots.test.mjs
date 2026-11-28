import assert from 'node:assert/strict';
import test from 'node:test';
import { evaluateRule } from './snapshots/2026-11-28/boardroom/game.mjs';
import { countSolutions, findLogicalHint, makeSudoku } from './snapshots/2026-11-28/sudoku-engine.mjs';

test('the published Sudoku seeds deal the openings in the paper', () => {
  const examples = [
    {
      level: 0, seed: 0, index: 2, digit: 2, kind: 'naked',
      clues: '080504001513078090004300000020100063049863125136209000090005640400012500307080019',
    },
    {
      level: 1, seed: 2, index: 17, digit: 4, kind: 'hidden',
      clues: '003020001208615000410000000004801026062000018800076049080090200100700400306000090',
    },
  ];
  for (const example of examples) {
    const { puzzle } = makeSudoku(example.level, example.seed);
    assert.equal(puzzle.join(''), example.clues);
    assert.equal(countSolutions(puzzle), 1);
    const hint = findLogicalHint(puzzle);
    assert.equal(hint.index, example.index);
    assert.equal(hint.digit, example.digit);
    assert.equal(hint.kind, example.kind);
  }
});

test('the shipped bonus rule reproduces both boundaries and the evidence check', () => {
  const own = evaluateRule('own', 25, 'reconciled');
  assert.deepEqual(own.evaluations, [
    { id: 'A', reduction: 15, pays: false },
    { id: 'B', reduction: 37.5, pays: true },
  ]);
  assert.equal(own.aligned, false);
  const combined = evaluateRule('combined', 12, 'reconciled');
  assert.deepEqual(combined.evaluations, [
    { id: 'A', reduction: 12, pays: true },
    { id: 'B', reduction: -15, pays: false },
  ]);
  assert.equal(combined.passed, true);
  assert.equal(evaluateRule('combined', 12.01, 'reconciled').aligned, false);
  assert.equal(evaluateRule('combined', 12, 'bonus').passed, false);
});
