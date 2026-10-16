"""Export a glyph for vector editing; the TTX outline remains the build source.

SPDX-License-Identifier: MIT
"""
from pathlib import Path
import argparse
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('character',help='One character, for example 常')
ap.add_argument('--output',type=Path,default=ROOT/'build/glyph.svg')
args=ap.parse_args()
if len(args.character)!=1: ap.error('Provide exactly one Unicode character.')
f=TTFont(ROOT/'fonts/CoupleOANote8105-Regular.ttf')
name=f.getBestCmap().get(ord(args.character))
if name is None: ap.error('This character is not covered.')
glyphs=f.getGlyphSet(); pen=SVGPathPen(glyphs);glyphs[name].draw(pen)
width=f['hmtx'][name][0]
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 1260"><title>U+{ord(args.character):04X}</title><path transform="translate(0 980) scale(1 -1)" d="{pen.getCommands()}"/></svg>\n',encoding='utf-8')
print(args.output)
