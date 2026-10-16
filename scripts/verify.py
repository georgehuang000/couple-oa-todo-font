# SPDX-License-Identifier: MIT
"""Validate release coverage, licenses, outlines, webfont parity and rebuilds."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def signature(font, name):
    coords, ends, flags = font['glyf'][name].getCoordinates(font['glyf'])
    return list(coords), list(ends), list(flags), tuple(font['hmtx'][name])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    project = json.loads((ROOT / 'project.json').read_text('utf-8'))
    rows = json.loads((ROOT / 'data/characters.json').read_text('utf-8'))
    expected = {r['codepoint'] for r in rows}
    require(len(rows) == len(expected) == project['mapped_codepoints'], 'Duplicate/missing mapping')
    han = sum(r['category'] == 'han' for r in rows)
    require(han == project['han'] and len(rows) - han == project['other'], 'Category counts')
    stem = project['stem']
    ttf_path = ROOT / f'fonts/{stem}.ttf'
    woff_path = ROOT / f'fonts/{stem}.woff'
    font = TTFont(ttf_path, recalcTimestamp=False)
    web = TTFont(woff_path, recalcTimestamp=False)
    cmap = font.getBestCmap()
    require(set(cmap) == expected == set(web.getBestCmap()), 'cmap coverage')
    require(set(range(32, 127)) <= expected, 'Printable ASCII coverage')
    require(font['OS/2'].fsType == 0, 'Font embedding metadata')
    for face in [font, web]:
        require(face['name'].getDebugName(1) == project['name'], 'Family name')
        require(face['name'].getDebugName(5) == 'Version ' + project['font_version'], 'Font version')
        require('SIL Open Font License' in (face['name'].getDebugName(13) or ''), 'Embedded font license')
        require(face['name'].getDebugName(14) == 'https://openfontlicense.org/', 'License URL')
    require(font['name'].compile(font) == web['name'].compile(web), 'TTF/WOFF names')
    spaces = {0x20, 0xA0, 0x3000}
    for row in rows:
        cp = row['codepoint']
        name = cmap[cp]
        coords, ends, flags, metrics = signature(font, name)
        require((coords, ends, flags, metrics) == signature(web, web.getBestCmap()[cp]), f'WOFF mismatch {cp:X}')
        require(bool(coords) == (cp not in spaces), f'Unexpected blank or nonblank {cp:X}')
        require(metrics[0] > 0, f'Non-positive width {cp:X}')
        if coords:
            require(min(y for x, y in coords) >= font['hhea'].descent, f'Below descent {cp:X}')
            require(max(y for x, y in coords) <= font['hhea'].ascent, f'Above ascent {cp:X}')
        svg_path = ROOT / row['svg']
        require(sha(svg_path) == row['svg_sha256'], f'SVG changed: {cp:X}')
    widths = {font['hmtx'][cmap[ord(c)]][0] for c in '0123456789'}
    require(len(widths) == 1, 'Digit widths differ')
    with tempfile.TemporaryDirectory(prefix='couple-oa-font-check-') as folder:
        subprocess.run([sys.executable, str(ROOT / 'scripts/build.py'), '--output', folder], check=True, capture_output=True)
        built_ttf = Path(folder) / ttf_path.name
        built_woff = Path(folder) / woff_path.name
        require(sha(built_ttf) == sha(ttf_path), 'TTX -> TTF rebuild is not byte identical')
        # WOFF zlib streams can vary across OS/zlib builds; compare table content too.
        built_web = TTFont(built_woff, recalcTimestamp=False)
        require(all(built_web[t].compile(built_web) == web[t].compile(web)
                    for t in font.keys() if t not in {'GlyphOrder', 'head', 'loca'}),
                'Rebuilt WOFF tables differ')
        woff_exact = sha(built_woff) == sha(woff_path)
    report = {'status': 'passed', 'release': project['release'], 'han': han,
              'mapped_codepoints': len(expected), 'blank_spaces': len(spaces),
              'printable_ascii_complete': True, 'equal_width_digits': True,
              'ttf_woff_outlines_metrics_names_equal': True,
              'offline_ttf_rebuild_byte_identical': True,
              'offline_woff_rebuild_tables_equal': True,
              'offline_woff_rebuild_byte_identical_on_this_runtime': woff_exact,
              'font_license_embedded': True,
              'files': [{'file': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
                        for p in [ttf_path, woff_path]]}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
