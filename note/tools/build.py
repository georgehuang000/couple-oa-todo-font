"""Build the released font from editable TTX, without an ML model or network.

SPDX-License-Identifier: MIT
"""
from pathlib import Path
import argparse
import hashlib
import json
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
NAME = 'CoupleOANote8105-Regular'


def build(output):
    output.mkdir(parents=True, exist_ok=True)
    font = TTFont(recalcTimestamp=False)
    font.importXML(ROOT/'source/font.ttx')
    ttf = output/(NAME+'.ttf')
    font.save(ttf)
    font = TTFont(ttf, recalcTimestamp=False)
    font.flavor = 'woff'
    font.save(output/(NAME+'.woff'))
    rows = [{'file':p.name, 'bytes':p.stat().st_size,
             'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in [ttf, output/(NAME+'.woff')]]
    (output/'checksums.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(rows,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'build/fonts')
    build(parser.parse_args().output)
