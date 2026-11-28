"""Reproduce the Markdown teaching pages and the offline edition using Python 3.10+."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
WEB = "https://alberttansinhon.com/math-arcade/olympiad/"
MIRROR = "https://albertito-ai.github.io/Albertito-AI/math-arcade/olympiad/"
CREDIT = "Atlas Open Mathematics, directed by Albert Tan Sin Hon. Prepared with AI assistance."
LICENCE = "Original problem text, explanations and diagrams: CC BY 4.0. Executable checks: MIT."


def markdown_problem(problem: dict, edition: dict) -> str:
    pid = problem["id"]
    lines = [f'# {problem["title"]}', '', f'**{problem["subject"]} · {problem["level"]} · {problem["time"]}**',
             '', problem["intro"], '', f'[Try this problem]({WEB}#{pid}) · [Play on GitHub Pages]({MIRROR}#{pid}) · [Proof collection](../README.md)',
             '', '## Problem', '', *separate(problem['statement']), '## Staged hints', '']
    if 'diagram' in problem:
        insert_at = lines.index('## Staged hints')
        lines[insert_at:insert_at] = [f'![{problem["diagramAlt"]}](../source/{problem["diagram"]})', '', problem["diagramAlt"], '']
    for n, hint in enumerate(problem['hints'], 1):
        lines.extend([f'{n}. {hint}', ''])
    lines.extend(['## Checkpoints and answers', ''])
    for n, item in enumerate(problem['checkpoints'], 1):
        lines.extend([f'### Checkpoint {n}', '', item['prompt'], '', f'**Answer.** {item["answer"]}', '', item['explanation'], ''])
    lines.extend(['## Worked proof', ''])
    for n, step in enumerate(problem['proof'], 1):
        lines.extend([f'### {n}. {step["title"]}', '', step['body'], ''])
    applied = edition['applications'][pid]
    lines.extend(['## Proof rubric', '', *separate(['- ' + value for value in problem['rubric']]),
                  '## Transfer exercise', '', problem['transfer']['prompt'], '', f'**Answer.** {problem["transfer"]["answer"]}', '',
                  problem['transfer']['explanation'], '', f'## Application: {applied["title"]}', '',
                  applied['scenario'], '', f'**Decision question.** {applied["question"]}', '',
                  '### Worked model', '', *separate(applied['model']), f'**Model limits.** {applied["limitation"]}', '',
                  f'**Try the model.** {applied["investigate"]}', '', '## Further investigation', '', edition['investigations'][pid], '', '## Provenance and verification', '',
                  f'{CREDIT} {edition["provenance"]}', '', problem['credit'], '', f'{edition["verification"]} [Reproduce the checks and inspect their scope](../README.md#verification).', '',
                  f'Edition {edition["version"]}, {edition["date"]}. [Edition DOI](https://doi.org/{edition["doi"]}) · [Project educational licence](../../../LICENSE-CONTENT.md) · [Code licence](../../../LICENSE)'])
    if pid == 'two-missing-lamps':
        lines.extend(['', 'For the four-point characterisation used in the proof, see Marcus Brinkmann, '
                      '[Classification of Almost Perfect Nonlinear Functions up to Dimension Five]'
                      '(https://www.nds.ruhr-uni-bochum.de/media/nds/veroeffentlichungen/2019/03/18/apn.pdf), '
                      'Ruhr-Universität Bochum (2007), chapter 3, propositions 3.1 and 3.2.'])
    return '\n'.join(lines) + '\n'


def separate(values: list[str]) -> list[str]:
    return [line for value in values for line in [value, '']]


def print_sheet(edition: dict) -> bytes:
    esc = html.escape
    title = 'Olympiad proof practice: problem sheets'
    sections = []
    for p in edition['problems']:
        paras = ''.join(f'<p>{esc(value)}</p>' for value in p['statement'])
        if 'diagram' in p:
            paras += f'<figure><img src="source/{esc(p["diagram"])}" alt="{esc(p["diagramAlt"])}"><figcaption>{esc(p["diagramAlt"])}</figcaption></figure>'
        app = edition['applications'][p['id']]
        checks = ''.join(f'<li>{esc(c["prompt"])}</li>' for c in p['checkpoints'])
        sections.append(f'<section><h2>{esc(p["title"])}</h2><p class="meta">{esc(p["subject"])} · {esc(p["level"])} · {esc(str(p["time"]))}</p>{paras}<h3>Check your approach</h3><ol>{checks}</ol><h3>Transfer exercise</h3><p>{esc(p["transfer"]["prompt"])}</p><h3>Application: {esc(app["title"])}</h3><p>{esc(app["scenario"])}</p><p>{esc(app["question"])}</p><p><a href="problems/{esc(p["id"])}.md">Read the hints, answers and complete proof</a></p></section>')
    doc = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>body{{max-width:48rem;margin:1.4rem auto;padding:0 1rem;font:1.08rem/1.6 Georgia,serif;color:#162d32}}h1,h2,h3,.meta{{font-family:system-ui,sans-serif;line-height:1.25}}h1{{font-size:2rem}}h2{{border-top:2px solid #2b6a63;padding-top:1rem}}.meta{{color:#38534c}}a{{color:#165d62}}figure{{margin:1rem 0}}figure img{{max-width:100%;max-height:13rem}}figcaption{{font-size:.85em}}@media print{{@page{{size:A4;margin:17mm}}body{{margin:0;padding:0;font-size:11pt}}section+section{{break-before:page}}h2,h3{{break-after:avoid}}section p,li{{orphans:2;widows:2}}}}</style>
<h1>{title}</h1><p>{esc(CREDIT)} Edition {esc(edition['version'])}, {esc(edition['date'])}. DOI {esc(edition['doi'])}. Original educational text and diagrams are licensed under CC BY 4.0.</p><p>Write a proof before opening the solutions. Each problem sheet includes a related exercise for a second attempt.</p>{''.join(sections)}</html>'''
    return doc.encode()


def archive(edition: dict, destination: Path):
    files = {f"research/olympiad/{f.relative_to(HERE).as_posix()}": f.read_bytes() for f in sorted(HERE.rglob('*'))
             if f.is_file() and '__pycache__' not in f.parts and f.suffix in {'.md', '.py', '.mjs', '.json', '.svg'}}
    for name in ['LICENSE', 'LICENSE-CONTENT.md']:
        files[name] = (ROOT / name).read_bytes()
    files['research/olympiad/Problem_Sheets.html'] = print_sheet(edition)
    files['README.md'] = (
        '# Atlas Open Mathematics: Olympiad proof practice\n\n'
        'Open [the problem sheets](research/olympiad/Problem_Sheets.html) in a browser to read or print the exercises without answers. '
        'Open [the proof collection](research/olympiad/README.md) to find the complete solutions, further investigations and offline verification commands. '
        'Plain Markdown and JSON files can also be read in a text editor.\n\n'
        f'{CREDIT} Edition {edition["version"]}, {edition["date"]}. {LICENCE}\n\n'
        'Each entry in SHA256SUMS records the SHA-256 digest of one other file in this archive.\n'
    ).encode()
    files['SHA256SUMS'] = ''.join(f'{hashlib.sha256(data).hexdigest()}  {name}\n' for name, data in sorted(files.items())).encode()
    with ZipFile(destination, 'w') as zipped:
        for name, data in sorted(files.items()):
            entry = ZipInfo(name, (2026, 11, 28, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = ZIP_STORED
            zipped.writestr(entry, data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='write the proof pages from edition.json')
    parser.add_argument('--zip', type=Path, metavar='FILE', help='package the verified text, sources and spoiler-free sheets')
    args = parser.parse_args()
    edition = json.loads((HERE / 'edition.json').read_text(encoding='utf-8'))
    expected = {}
    for item in edition['problems']:
        filename = HERE / 'problems' / (item['id'] + '.md')
        expected[filename] = markdown_problem(item, edition)
    if args.write:
        for path, source in expected.items():
            path.write_text(source, encoding='utf-8')
    stale = [f.name for f, contents in expected.items() if not f.exists() or f.read_text(encoding='utf-8') != contents]
    extra = sorted(f.name for f in (HERE / 'problems').glob('*.md') if f not in expected)
    if stale or extra:
        raise SystemExit(f'Proof pages differ from edition.json. Stale: {stale}. Unexpected: {extra}.')
    print(f'{len(expected)} complete proof pages match edition.json.')
    if args.zip:
        archive(edition, args.zip)
        print(f'{args.zip.name}  SHA-256 {hashlib.sha256(args.zip.read_bytes()).hexdigest()}')


if __name__ == '__main__':
    main()
