# SPDX-License-Identifier: MIT
"""Build the frozen, editable TTX master without a model or network access."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/fonts')
    args = parser.parse_args()
    project = json.loads((ROOT / 'project.json').read_text('utf-8'))
    dest = args.output.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    font = TTFont(recalcTimestamp=False)
    font.importXML(ROOT / project['master'])
    rows = json.loads((ROOT / 'data/characters.json').read_text('utf-8'))
    expected = {row['codepoint'] for row in rows}
    if set(font.getBestCmap()) != expected:
        raise ValueError('Source cmap and data/characters.json disagree.')
    if len(expected) != project['mapped_codepoints']:
        raise ValueError('Character count and project.json disagree.')
    outputs = []
    for suffix in ['ttf', 'woff']:
        font.flavor = None if suffix == 'ttf' else suffix
        path = dest / f'{project["stem"]}.{suffix}'
        font.save(path)
        outputs.append({'file': path.name, 'bytes': path.stat().st_size,
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    print(json.dumps({'status': 'built', 'files': outputs}, indent=2))


if __name__ == '__main__':
    main()
