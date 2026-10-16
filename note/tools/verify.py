"""Check coverage, preserved originals, licensing, outlines and optional rendering.

SPDX-License-Identifier: MIT
"""
from pathlib import Path
import argparse
import hashlib
import json
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

ROOT=Path(__file__).resolve().parents[1]
NAME='CoupleOANote8105-Regular'


def signature(font,name):
    data=font['glyf'][name].compile(font['glyf'])
    data+=json.dumps(list(font['hmtx'][name]),separators=(',',':')).encode('ascii')
    return hashlib.sha256(data).hexdigest()


def verify(directory,render=False,compare_release=False):
    target=(ROOT/'charset/han-8105.txt').read_text('utf-8').strip()
    originals=json.loads((ROOT/'qa/original-glyph-digests.json').read_text('utf-8'))
    expected=json.loads((ROOT/'qa/release.json').read_text('utf-8'))
    assert len(target)==len(set(target))==8105
    font=TTFont(directory/(NAME+'.ttf'),recalcTimestamp=False,checkChecksums=2)
    cmap=font.getBestCmap()
    assert len(cmap)==8234 and set(map(ord,target))<=set(cmap)
    assert sum(cp>65535 for cp in cmap)==196
    for table in font['cmap'].tables:
        if table.isUnicode() and table.format==12: assert table.cmap==cmap
    assert any(t.format==12 and t.platformID==3 and t.platEncID==10 for t in font['cmap'].tables)
    assert font['OS/2'].fsType==0
    for nid in [0,13,14]: assert font['name'].getDebugName(nid)
    assert 'SIL OPEN FONT LICENSE' in font['name'].getDebugName(13)
    assert 'georgehuang000' in font['name'].getDebugName(0)
    assert 'Adobe' in font['name'].getDebugName(0)
    assert font['name'].getDebugName(1)=='Couple OA Note 8105'
    assert font['name'].getDebugName(5)=='Version '+expected['version']
    assert font['name'].getDebugName(11)=='https://github.com/georgehuang000/couple-oa-todo-font'
    assert font['name'].getDebugName(13)==(ROOT/'OFL.txt').read_text('utf-8').strip()
    for cp,digest in originals.items():
        assert signature(font,cmap[int(cp,16)])==digest, 'Changed original: '+cp
    glyphs=font.getGlyphSet()
    for cp,name in cmap.items():
        pen=BoundsPen(glyphs); glyphs[name].draw(pen)
        if chr(cp).isspace(): continue
        assert pen.bounds is not None, f'Empty U+{cp:04X}'
        x0,y0,x1,y1=pen.bounds
        advance=font['hmtx'][name][0]
        assert x0>=-0.05 and x1<=advance+0.05, f'Horizontal overflow U+{cp:04X}'
        assert y0>=-280 and y1<=980, f'Vertical overflow U+{cp:04X}'
    woff=TTFont(directory/(NAME+'.woff'),recalcTimestamp=False,checkChecksums=2)
    assert woff.getBestCmap()==cmap
    for cp,name in cmap.items(): assert signature(font,name)==signature(woff,name)
    for record in font['name'].names:
        other=woff['name'].getName(record.nameID,record.platformID,record.platEncID,record.langID)
        assert other is not None and other.toUnicode()==record.toUnicode()
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [directory/(NAME+'.ttf'),directory/(NAME+'.woff')]}
    if compare_release:
        # TTF is platform-independent; WOFF's zlib stream can vary by platform.
        assert hashes[NAME+'.ttf']==expected['sha256'][NAME+'.ttf'], 'Rebuilt TTF differs from release'
    rendered=0
    if render:
        from PIL import Image,ImageDraw,ImageFont
        for size in [24,48]:
            face=ImageFont.truetype(str(directory/(NAME+'.ttf')),size)
            for c in target:
                im=Image.new('L',(size*3,size*3),0)
                ImageDraw.Draw(im).text((size,size),c,font=face,fill=255)
                assert im.getbbox(),f'No rendered ink at {size}px: {c}'
                rendered+=1
    report={'status':'passed','mapped_characters':len(cmap),'han':8105,'non_bmp':196,
            'preserved_originals':len(originals),'rendered_glyphs':rendered,'sha256':hashes}
    print(json.dumps(report,indent=2))
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--fonts',type=Path,default=ROOT/'fonts')
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--compare-release',action='store_true')
    args=ap.parse_args()
    verify(args.fonts,args.render,args.compare_release)
