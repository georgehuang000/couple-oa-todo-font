"""Render publication specimens from the actual font. Requires Pillow.

SPDX-License-Identifier: MIT
"""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parents[1]
fontpath=ROOT/'fonts/CoupleOANote8105-Regular.ttf'
font=TTFont(fontpath);cmap=font.getBestCmap()
face=lambda size:ImageFont.truetype(str(fontpath),size)
release=json.loads((ROOT/'qa/release.json').read_text('utf-8'))
ink='#334235'; muted='#80735f'; paper='#f5f1e9'
lines=['便签寄语小纸条，把日子写成喜欢的样子。','我懂你，也懂每一次想念。',
       '梅花和橙子，都是我们的约定。','输入姓名、地点和心愿，让日常留下记录。',
       '常常记得，小小的美好也值得收藏。','Hello, life. Love & OA 2026/10/16',
       'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789',
       '𠅤𠙶𠳐𡎚𬘭𬙋𬭳𬺓']
assert all(ord(c) in cmap or c.isspace() for s in lines for c in s)
im=Image.new('RGB',(1440,1160),paper);d=ImageDraw.Draw(im)
d.text((70,118),'便签 寄语 小纸条',font=face(90),fill=ink,anchor='ls')
d.text((75,186),'Couple OA Note 8105 / v'+release['version']+' / OFL 1.1',font=face(30),fill=muted,anchor='ls')
d.line((75,220,1365,220),fill='#c9c2b2',width=2)
for i,line in enumerate(lines):
    f=face(48 if i<6 else 42)
    assert f.getlength(line)<1290,line
    d.text((75,300+i*88),line,font=f,fill=ink,anchor='ls')
d.text((75,1116),'8105 汉字 / 8234 字符 / TTF + WOFF',font=face(26),fill=muted,anchor='ls')
(ROOT/'assets').mkdir(exist_ok=True)
im.save(ROOT/'assets/specimen.png')
im=Image.new('RGB',(1440,900),paper);d=ImageDraw.Draw(im)
d.text((70,76),'便签手记 8105 / 字号参考',font=face(46),fill=ink,anchor='ls')
for row,size in enumerate([16,24,32,40,48,64]):
    y=170+row*125
    d.text((70,y),str(size)+'px',font=face(25),fill=muted,anchor='ls')
    d.text((225,y),'常常记得美好 e 0123',font=face(size),fill=ink,anchor='ls')
im.save(ROOT/'assets/sizes.png')
print('Rendered specimen.png and sizes.png from the released TTF.')
