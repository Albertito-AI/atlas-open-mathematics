// Generate the interchange file from the same content modules as the web edition.
import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import counters from './source/algebra.mjs';
import squares from './source/arithmetic.mjs';
import triangle from './source/geometry.mjs';
import lamps from './source/combinatorics.mjs';
import investigations from './source/investigations.mjs';
import applications from './source/applications.mjs';

const problems = [counters, squares, triangle, lamps];
const ids = problems.map(p => p.id);
const strings = list => assert(Array.isArray(list) && list.length && list.every(v => typeof v === 'string' && v.trim()));
assert.equal(new Set(ids).size, problems.length);
for (const extension of [investigations, applications]) {
  assert.deepEqual(Object.keys(extension).sort(), [...ids].sort());
}
for (const p of problems) {
  assert.match(p.id, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
  strings([p.title, p.subject, p.level, p.time, p.intro, p.credit, investigations[p.id]]);
  for (const key of ['statement', 'hints', 'rubric']) strings(p[key]);
  assert(p.checkpoints.length && p.proof.length);
  for (const {prompt, answer, explanation} of [...p.checkpoints, p.transfer]) strings([prompt, answer, explanation]);
  for (const {title, body} of p.proof) strings([title, body]);
  const app = applications[p.id];
  strings([app.title, app.scenario, app.question, app.limitation, app.investigate]);
  strings(app.model);
  if (p.diagram) {
    assert.match(p.diagram, /^[a-z0-9-]+\.svg$/);
    const svg = await readFile(new URL('./source/' + p.diagram, import.meta.url), 'utf8');
    strings([p.diagramAlt]);
    assert(svg.includes('<svg'));
  }
}
const edition = {
  title: 'Atlas Math Olympiad: Proof Edition',
  version: '1.0.0',
  date: '2026-11-28',
  doi: '10.5281/zenodo.24620475',
  direction: {name: 'Albert Tan Sin Hon', orcid: 'https://orcid.org/0009-0001-8996-7933', project: 'Atlas Open Mathematics'},
  provenance: 'These exercises were prepared for this programme using established mathematics. The collection makes no claim of first discovery or official contest provenance.',
  verification: 'The worked arguments support the general conclusions. The executable checks provide separate evidence for specified finite cases. The challenge bands are editorial judgements and have not been calibrated against human contest performance.',
  licences: {educational_content: 'CC-BY-4.0', code: 'MIT'},
  canonical: 'https://alberttansinhon.com/math-arcade/olympiad/',
  mirror: 'https://albertito-ai.github.io/Albertito-AI/math-arcade/olympiad/',
  problems, investigations, applications
};
const bytes = JSON.stringify(edition, null, 2) + '\n';
const url = new URL('./edition.json', import.meta.url);
if (process.argv.slice(2).join(' ') === '--write') {
  await writeFile(url, bytes, 'utf8');
} else {
  assert.equal(process.argv.length, 2, 'Use --write to update edition.json.');
  assert((await readFile(url, 'utf8')) === bytes, 'edition.json differs from its sources. Run compile-edition.mjs --write.');
}
console.log('Four problem records, investigations and applications agree with the source modules.');
