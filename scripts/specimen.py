# SPDX-License-Identifier: MIT
"""Render the release specimen and every mapped glyph using the released font."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / 'fonts/CoupleOATodo-Regular.ttf'


def face(size):
    return ImageFont.truetype(str(FONT), size)


def main():
    rows = json.loads((ROOT / 'data/characters.json').read_text('utf-8'))
    supported = {r['codepoint'] for r in rows}
    texts = ['待办事项', '今天我们一起去旅行。', '记得吃饭，也记得想我。', 'Hello, 2026!  0123456789', '604 HAN / 743 CHARACTERS / OFL 1.1']
    for text in texts:
        missing = {c for c in text if ord(c) not in supported}
        if missing:
            raise ValueError(f'Specimen contains unsupported characters: {missing}')
    im = Image.new('RGB', (1440, 900), '#f7f1e8')
    draw = ImageDraw.Draw(im)
    draw.text((92, 58), 'COUPLE OA TODO', font=face(24), fill='#a45b66')
    draw.text((87, 141), texts[0], font=face(156), fill='#40342f')
    draw.line((94, 355, 1345, 355), fill='#ded2c5', width=2)
    draw.text((92, 409), texts[1], font=face(68), fill='#40342f')
    draw.text((92, 523), texts[2], font=face(68), fill='#40342f')
    draw.text((92, 674), texts[3], font=face(44), fill='#a45b66')
    draw.text((92, 817), texts[4], font=face(22), fill='#756b62')
    (ROOT / 'assets').mkdir(exist_ok=True)
    im.save(ROOT / 'assets/specimen.png', optimize=True)
    (ROOT / 'verification/glyphs').mkdir(parents=True, exist_ok=True)
    font = face(54)
    pages = 0
    for offset in range(0, len(rows), 120):
        pages += 1
        board = Image.new('RGB', (1200, 1440), 'white')
        d = ImageDraw.Draw(board)
        for i, row in enumerate(rows[offset:offset + 120]):
            x, y = (i % 10) * 120, (i // 10) * 120
            d.rectangle((x, y, x + 119, y + 119), outline='#dedbd6')
            d.text((x + 16, y + 7), row['character'], font=font, fill='#322b27')
            d.text((x + 12, y + 88), row['unicode'], font=face(15), fill='#807770')
        board.save(ROOT / f'verification/glyphs/page-{pages:02}.png', optimize=True)
    output = {'status': 'rendered', 'characters': len(rows), 'pages': pages,
              'source': 'fonts/CoupleOATodo-Regular.ttf',
              'note': 'Actual font rendering; does not assert professional proofreading.'}
    (ROOT / 'verification/raster.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
