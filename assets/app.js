// SPDX-License-Identifier: MIT
'use strict';
const rows = window.FONT_CHARACTERS;
const supported = new Set(rows.map(row => row.codepoint));
const $ = id => document.getElementById(id);
const defaultText = $('text').value;
let page = 0;
const pageSize = 64;

function updateCoverage() {
  const chars = Array.from($('text').value);
  const missing = [...new Set(chars.filter(char => !supported.has(char.codePointAt(0)) && !['\n', '\r', '\t'].includes(char)))];
  $('coverage').classList.toggle('missing', missing.length > 0);
  $('coverage').textContent = missing.length
    ? `以下 ${missing.length} 个字符未收录，正在使用系统字体：${missing.map(char => /\s/u.test(char) ? 'U+' + char.codePointAt(0).toString(16).toUpperCase() : char).join(' ')}`
    : (chars.length ? '这段文字已全部收录。' : '输入你想查看的文字。');
}

function renderGrid() {
  const query = $('query').value.trim();
  const code = /^(?:U\+|0x)([0-9a-f]{2,6})$/i.exec(query);
  const chars = new Set(Array.from(query));
  const category = $('category').value;
  const filtered = rows.filter(row => (category === 'all' || row.category === category)
    && (!query || (code ? row.codepoint === parseInt(code[1], 16) : chars.has(row.character))));
  const pages = Math.max(1, Math.ceil(filtered.length / pageSize));
  page = Math.max(0, Math.min(page, pages - 1));
  $('count').textContent = `共 ${filtered.length} 个字符`;
  $('glyphs').replaceChildren();
  const spaceNames = {32: '普通空格', 160: '不换行空格', 12288: '全角空格'};
  for (const row of filtered.slice(page * pageSize, (page + 1) * pageSize)) {
    const tile = document.createElement('div');
    tile.className = 'glyph';
    const glyph = document.createElement('b');
    glyph.className = 'font' + (spaceNames[row.codepoint] ? ' space' : '');
    glyph.textContent = spaceNames[row.codepoint] || row.character;
    const label = document.createElement('small');
    label.textContent = row.unicode;
    tile.append(glyph, label);
    $('glyphs').append(tile);
  }
  if (!filtered.length) {
    const message = document.createElement('p');
    message.className = 'empty';
    message.textContent = '当前版本没有收录这些字符。';
    $('glyphs').append(message);
  }
  $('page').textContent = `${page + 1} / ${pages}`;
  $('prev').disabled = page === 0;
  $('next').disabled = page >= pages - 1;
}

$('text').addEventListener('input', updateCoverage);
$('size').addEventListener('input', () => {
  $('size-value').textContent = $('size').value;
  $('text').style.fontSize = `${$('size').value}px`;
});
$('reset').addEventListener('click', () => {
  $('text').value = defaultText;
  $('size').value = '40';
  $('size').dispatchEvent(new Event('input'));
  updateCoverage();
});
for (const id of ['query', 'category']) $(id).addEventListener(id === 'query' ? 'input' : 'change', () => { page = 0; renderGrid(); });
$('prev').addEventListener('click', () => { page--; renderGrid(); });
$('next').addEventListener('click', () => { page++; renderGrid(); });
document.fonts.load('40px Todo', '待办事项').then(faces => {
  $('font-status').textContent = faces.length ? '字体已加载 · Regular' : '字体未加载，当前为系统字体';
}).catch(() => { $('font-status').textContent = '字体加载失败，当前为系统字体'; });
updateCoverage();
renderGrid();
