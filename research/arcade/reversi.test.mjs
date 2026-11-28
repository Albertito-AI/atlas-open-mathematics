import test from 'node:test';
import assert from 'node:assert/strict';
import { BLACK, WHITE, EMPTY_COUNTS, coordinate, startBoard, flipsFor, legalMoves, playMove, solve, rankMoves, discMargin, makeEndgame } from './reversi.mjs';

// Independent reference model: two unsigned bit sets, masked directional shifts and an
// absolute Black-margin max/min recurrence. It uses no production move or score functions.
const FULL = (1n << 64n) - 1n;
const FILE_A = 0x0101010101010101n;
const FILE_H = FILE_A << 7n;
const dirs = [-9, -8, -7, -1, 1, 7, 8, 9];
const bit = square => 1n << BigInt(square);
function shift(bits, direction) {
  if ([-9, -1, 7].includes(direction)) bits &= FULL ^ FILE_A;
  if ([-7, 1, 9].includes(direction)) bits &= FULL ^ FILE_H;
  return direction > 0 ? (bits << BigInt(direction)) & FULL : bits >> BigInt(-direction);
}
function bitPosition(board) {
  let black = 0n, white = 0n;
  for (const [square, value] of board.entries()) {
    if (value === 1) black |= bit(square);
    if (value === -1) white |= bit(square);
  }
  return [black, white];
}
function refChildren(black, white, turn) {
  const own = turn === 1 ? black : white, other = turn === 1 ? white : black;
  const children = [];
  for (let square = 0; square < 64; square++) {
    const placed = bit(square);
    if (placed & (black | white)) continue;
    let flipped = 0n;
    for (const direction of dirs) {
      let next = shift(placed, direction), run = 0n;
      while (next & other) {
        run |= next;
        next = shift(next, direction);
      }
      if (next & own) flipped |= run;
    }
    if (flipped) {
      const nextOwn = own | placed | flipped, nextOther = other ^ flipped;
      children.push([square, ...(turn === 1 ? [nextOwn, nextOther] : [nextOther, nextOwn])]);
    }
  }
  return children;
}
function pop(bits) {
  let n = 0;
  while (bits) { bits &= bits - 1n; n++; }
  return n;
}
function refScore(black, white, turn) {
  const next = refChildren(black, white, turn);
  if (!next.length) {
    return refChildren(black, white, -turn).length ? refScore(black, white, -turn) : pop(black) - pop(white);
  }
  const scores = next.map(([, b, w]) => refScore(b, w, -turn));
  return turn === 1 ? Math.max(...scores) : Math.min(...scores);
}

test('opening moves match the official example and captures preserve the input', () => {
  const board = startBoard();
  assert.deepEqual(legalMoves(board, BLACK).map(coordinate), ['D3', 'C4', 'F5', 'E6']);
  assert.deepEqual(flipsFor(board, 26, BLACK), [27]);
  const next = playMove(board, 26, BLACK);
  assert.equal(board[26], 0);
  assert.equal(board[27], WHITE);
  assert.equal(next[27], BLACK);
  assert.equal(discMargin(next, BLACK), 3);
  assert.throws(() => playMove(board, 0, BLACK), RangeError);
  assert.throws(() => playMove(board, 27, BLACK), RangeError);
});

test('a placement can bracket all eight directions and cannot wrap around the edge', () => {
  const board = new Int8Array(64);
  for (const d of [-9,-8,-7,-1,1,7,8,9]) { board[27+d] = WHITE; board[27+2*d] = BLACK; }
  assert.deepEqual(flipsFor(board, 27, BLACK).sort((a,b) => a-b), [18,19,20,26,28,34,35,36]);
  const after = playMove(board, 27, BLACK);
  assert.equal(after.filter(x => x === BLACK).length, 17);
  const edge = new Int8Array(64);
  edge[8] = WHITE; edge[9] = BLACK;
  assert.deepEqual(flipsFor(edge, 7, BLACK), []);
});

test('forced passes change the player, while two immobile colours terminate with empty cells', () => {
  const board = new Int8Array(64);
  board[0] = BLACK; board[1] = WHITE;
  assert.deepEqual(legalMoves(board, WHITE), []);
  assert.deepEqual(legalMoves(board, BLACK), [2]);
  assert.equal(solve(board, WHITE), -3);
  const early = playMove(board, 2, BLACK);
  assert.deepEqual(legalMoves(early, WHITE), []);
  assert.deepEqual(legalMoves(early, BLACK), []);
  assert.equal(solve(early, BLACK), 3);
  const tie = new Int8Array(64); tie[0] = BLACK; tie[63] = WHITE;
  assert.equal(solve(tie, WHITE), 0);
});

test('opening histories reconstruct reachable endgames, including legal passes', () => {
  for (let level = 0; level < 3; level++) {
    const seen = new Set();
    for (let seed = 0; seed < 128; seed++) {
      const position = makeEndgame(level, seed);
      const same = makeEndgame(level, seed);
      assert.deepEqual(position, same);
      let board = startBoard(), turn = BLACK;
      for (const square of position.history) {
        if (square === -1) {
          assert.equal(legalMoves(board, turn).length, 0);
          assert.ok(legalMoves(board, -turn).length > 0);
        } else {
          board = playMove(board, square, turn);
        }
        turn = -turn;
      }
      assert.deepEqual(board, position.board);
      assert.equal(turn, position.side);
      assert.equal(board.filter(c => !c).length, EMPTY_COUNTS[level]);
      assert.ok(position.analysis.length >= 2);
      assert.ok(position.analysis[0].score > position.analysis.at(-1).score);
      seen.add(turn + '/' + board.join(','));
    }
    assert.equal(seen.size, 128);
  }
});

test('every opening alternative agrees with independent bitboard minimax', () => {
  for (let level = 0; level < 3; level++) {
    for (let seed = 0; seed < 16; seed++) {
      const { board, side, analysis } = makeEndgame(level, seed);
      const [black, white] = bitPosition(board);
      const expected = refChildren(black, white, side).map(([square,b,w]) => ({
        square, score: side * refScore(b,w,-side) || 0
      })).sort((a,b) => b.score - a.score || a.square - b.square);
      assert.deepEqual(analysis, expected);
      assert.equal(solve(board, side), expected[0].score);
      for (const [square, b, w] of refChildren(black, white, side)) {
        assert.deepEqual(bitPosition(playMove(board,square,side)), [b,w]);
      }
    }
  }
});

test('the published replay positions reproduce the margins, passes and illustrative losing line', () => {
  const example = makeEndgame(0, 7);
  assert.equal(example.side, WHITE);
  assert.deepEqual(example.analysis.map(({square,score}) => [coordinate(square),score]), [['G2',6],['H7',-8],['H8',-8]]);
  let board = example.board, turn = WHITE;
  for (const action of ['G2','pass','H7','pass','H8']) {
    if (action === 'pass') assert.equal(legalMoves(board,turn).length, 0);
    else {
      const { square } = rankMoves(board,turn)[0];
      assert.equal(coordinate(square), action);
      board = playMove(board,square,turn);
    }
    turn = -turn;
  }
  assert.equal(board.filter(c => c === WHITE).length, 35);
  assert.equal(board.filter(c => c === BLACK).length, 29);
  const hard = makeEndgame(2,7);
  assert.deepEqual(hard.analysis.map(({square,score}) => [coordinate(square),flipsFor(hard.board,square,hard.side).length,score]), [['A8',5,-6],['B7',8,-32]]);
});
