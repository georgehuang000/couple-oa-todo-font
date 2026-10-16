"""Make a self-contained, offline font specimen from the released files.

SPDX-License-Identifier: MIT
"""
from pathlib import Path
import base64,json
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parents[1]
font=TTFont(ROOT/'fonts/CoupleOANote8105-Regular.ttf')
cmap=font.getBestCmap()
originals=json.loads((ROOT/'qa/original-glyph-digests.json').read_text('utf-8'))
base=''.join(chr(int(cp,16)) for cp in originals)
charset=json.loads((ROOT/'charset/tgh-2013.json').read_text('utf-8'))
release=json.loads((ROOT/'qa/release.json').read_text('utf-8'))
glyphs=[]
for entry in charset['entries']:
    c=entry['character'];n=entry['index']
    glyphs.append({**entry,'level':1 if n<=3500 else 2 if n<=6500 else 3,
                   'source':'original' if c in base else 'generated','non_bmp':ord(c)>65535,'flags':[]})
samples=['便签寄语小纸条，把日子写成喜欢的样子。','我懂你，也懂每一次想念。',
         '梅花和橙子，都是我们的约定。','输入姓名、地点和心愿，让日常留下记录。',
         '龟鹤翩跹，碧波粼粼，繁星点点。','𠅤𠙶𠳐𡎚𬘭𬙋𬭳𬺓',
         '2026/10/16  08:30  ¥128.50  100%',
         'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz 0123456789',
         '你好，世界！「约定」《日记》…… Love & OA ♡']
assert all(ord(c) in cmap or c.isspace() for line in samples for c in line)
data={'version':release['version'],'characters':''.join(chr(cp) for cp in sorted(cmap)),
      'baseCharacters':base,'glyphs':glyphs,'samples':samples}
template=(ROOT/'tools/preview-template.html').read_text('utf-8')
font_data=base64.b64encode((ROOT/'fonts/CoupleOANote8105-Regular.woff').read_bytes()).decode('ascii')
template=template.replace("url('fonts/CoupleOANote8105-Regular.woff')",f"url('data:font/woff;base64,{font_data}')")
template=template.replace('/* FONT_DATA */',json.dumps(data,ensure_ascii=False).replace('<','\\u003c'))
(ROOT/'index.html').write_text(template,encoding='utf-8',newline='\n')
print('Created offline index.html with 8105-character lookup and coverage feedback.')
