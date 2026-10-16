# SPDX-License-Identifier: MIT
"""Export a local script so the preview requires no JSON fetch or server API."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = json.loads((root / 'data/characters.json').read_text('utf-8'))
public = [{k: row[k] for k in ['character', 'codepoint', 'unicode', 'category']} for row in rows]
body = '// SPDX-License-Identifier: MIT; character data belongs to the OFL font.\nwindow.FONT_CHARACTERS = ' + json.dumps(public, ensure_ascii=True, separators=(',', ':')) + ';\n'
(root / 'assets/characters.js').write_text(body, encoding='utf-8')
print(f'Exported {len(public)} characters.')
