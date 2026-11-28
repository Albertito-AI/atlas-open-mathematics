import assert from 'node:assert/strict';
import { makeVariation } from '../variations.mjs';

function counters(text) {
  const n = Number(text.match(/Number (\d+) benches/)[1]);
  const [, pile, start] = text.match(/Put (\d+) counters at bench (\d+)/).map(Number);
  const benches = Array(n).fill(0);
  let i = start - 1;
  let trades = 0;
  benches[i] = pile;
  while (benches[i] > 1) {
    const next = (i + 1) % n;
    while (benches[i] >= 2) {
      benches[i] -= 2;
      benches[next]++;
      trades++;
    }
    i = next;
  }
  assert.equal(benches.reduce((a,b)=>a+b), 1);
  return text.includes('largest possible') ? trades : i + 1;
}

function exponents(text) {
  const degree = Number(text.match(/degree exactly (\d+)/)[1]);
  let count = 0;
  for (let a = 1; a <= degree; a++) {
    for (let b = a; b <= degree; b++) {
      for (let d = b; d <= 2 * a; d++) if (a + b + d === degree) count++;
    }
  }
  for (const divisor of [2, 4]) {
    for (let power = 1; power <= degree; power++) if (divisor * power === degree) count++;
  }
  return count;
}

function triangle(text) {
  const b = Number(text.match(/settings 0, (\d+), then/)[1]);
  const size = Number(text.match(/is (\d+) (?:square )?units/)[1]);
  const isArea = text.includes('triangle area');
  let points = isArea ? [[0,0],[8,0],[0,size/4]] : [[size,0],[0,size],[-size,-size]];
  for (const s of [0,b,-b]) {
    points = points.map((_,i)=>{
      const p = points[(i+1)%3];
      const q = points[(i+2)%3];
      return [(p[0]+q[0])/2-s*(q[1]-p[1]),(p[1]+q[1])/2+s*(q[0]-p[0])];
    });
  }
  const [a,c,d] = points;
  return isArea ? Math.abs((c[0]-a[0])*(d[1]-a[1])-(c[1]-a[1])*(d[0]-a[0]))/2 : Math.hypot(...a);
}

const cachedSpaces = new Map();
function flats(text) {
  const dimension = Number(text.match(/dimension (\d+)/)[1]);
  const k = text.includes('affine planes') ? 2 : 3;
  const key = dimension + ',' + k;
  if (!cachedSpaces.has(key)) {
    const points = 2**dimension;
    let directions = [[0]];
    for (let i = 0; i < k; i++) {
      const next = new Map();
      for (const direction of directions) {
        for (let x = 1; x < points; x++) if (!direction.includes(x)) {
          const subspace = [...direction, ...direction.map(v=>v^x)].sort((a,b)=>a-b);
          next.set(subspace.join(','), subspace);
        }
      }
      directions = [...next.values()];
    }
    const counts = [0,0,0];
    for (const direction of directions) {
      const seen = new Set();
      for (let offset=0;offset<points;offset++) if (!seen.has(offset)) {
        const flat = direction.map(v=>v^offset);
        flat.forEach(v=>seen.add(v));
        counts[Number(flat.includes(0)) + Number(flat.includes(1))]++;
      }
    }
    cachedSpaces.set(key, counts);
  }
  return cachedSpaces.get(key)[Number(text.includes('exactly one'))];
}

const tests = {'last-counter': counters, 'shifted-squares': exponents, 'three-turn-triangle': triangle, 'two-missing-lamps': flats};
for (const [id, check] of Object.entries(tests)) {
  const samples=new Set();
  for (const seed of [...Array(260).keys(), 0x7fffffff]) {
    const item=makeVariation(id, seed);
    assert.match(item.answer,/^\d+$/);
    assert.deepEqual(item, makeVariation(id, seed));
    assert.equal(item.answer,String(check(item.prompt)),id+' '+seed);
    samples.add(item.prompt);
  }
  console.log(id+': 261 seeds matched an independent calculation ('+samples.size+' distinct prompts).');
}
for (const invalid of [-1,0x80000000,1.2,NaN,'1']) assert.throws(()=>makeVariation('last-counter',invalid),RangeError);
assert.throws(()=>makeVariation('unknown',0), RangeError);
