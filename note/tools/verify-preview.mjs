// SPDX-License-Identifier: MIT
// DOM logic checks, not a claim of real browser, font loading or layout testing.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const dir=path.resolve(process.argv[2]||'.');
const html=fs.readFileSync(path.join(dir,'index.html'),'utf8');
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const release=JSON.parse(fs.readFileSync(path.join(dir,'qa/release.json'),'utf8'));
const manifest={fonts:Object.entries(release.sha256).map(([name,sha256])=>({file:'fonts/'+name,sha256}))};
const embedded=Buffer.from(html.match(/data:font\/woff;base64,([^']+)/)[1],'base64');
const woff=manifest.fonts.find(r=>r.file.endsWith('.woff'));
assert.equal(hash(embedded),woff.sha256);
assert.equal(hash(fs.readFileSync(path.join(dir,manifest.fonts[0].file))),manifest.fonts[0].sha256);
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
assert(!html.includes('/* FONT_DATA */'));
class Element{
 constructor(){this.children=[];this.events={};this.value='';this._text='';this.style={setProperty(){}};}
 append(...xs){for(const x of xs)this.children.push(x);}
 replaceChildren(...xs){this.children=xs;this._text='';}
 set textContent(v){this._text=String(v);this.children=[];}
 get textContent(){return this._text+this.children.map(x=>x.textContent).join('');}
 addEventListener(n,f){this.events[n]=f;}
 setAttribute(n,v){this[n]=v;}
}
const ids=new Map();for(const [,id] of html.matchAll(/\bid="([^"]+)"/g)){assert(!ids.has(id),id);ids.set(id,new Element());}
const el=id=>{assert(ids.has(id),'Missing element '+id);return ids.get(id);};
el('size').value='38';el('spacing').value='0';el('level').value='all';el('source').value='all';el('color').checked=true;
const document={getElementById:el,createElement:()=>new Element(),createDocumentFragment:()=>new Element(),documentElement:new Element(),fonts:{load:async()=>[{family:'CoupleNote'}]}};
const context=vm.createContext({document});new vm.Script(code).runInContext(context);await new Promise(resolve=>setTimeout(resolve,0));
assert.equal(el('specimen').textContent,el('input').value);assert.match(el('coverage').textContent,/均由本字库覆盖/);assert.match(el('results').textContent,/8105/);
const input=text=>{el('input').value=text;el('input').events.input();assert.equal(el('specimen').textContent,text);};
input('𠅤𬘭𬺓 常 e 美 可');assert.match(el('coverage').textContent,/7 个字符，均由本字库覆盖/);
input('你𰻞🙂<script>');assert.match(el('coverage').textContent,/𰻞 🙂/);
input('');assert.match(el('coverage').textContent,/0 个字符/);
el('query').value='U+'+'𬺓'.codePointAt(0).toString(16).toUpperCase();el('query').events.input();assert.equal(el('grid').children[0].children.length,1);
const b=el('grid').children[0].children[0];b.onclick();assert.equal(el('input').value,'𬺓');
el('query').value='U+10FFFF';el('query').events.input();assert.match(el('results').textContent,/没有符合/);assert(el('prev').disabled&&el('next').disabled);
el('clear').onclick();el('source').value='nonbmp';el('source').events.input();assert.match(el('results').textContent,/196/);
el('clear').onclick();el('source').value='original';el('source').events.input();assert.match(el('results').textContent,/606/);
el('clear').onclick();el('level').value='3';el('level').events.input();assert.match(el('results').textContent,/1605/);
el('clear').onclick();el('next').onclick();assert.match(el('pageLabel').textContent,/2 \/ 82/);el('prev').onclick();assert.match(el('pageLabel').textContent,/1 \/ 82/);
for(let i=0;i<81;i++)el('next').onclick();assert.match(el('pageLabel').textContent,/82 \/ 82/);assert.equal(el('grid').children[0].children.length,5);assert(el('next').disabled);
el('sample').value='1';el('sample').onchange();assert.equal(el('specimen').textContent,el('input').value);el('restore').onclick();assert(el('input').value.includes('\n'));
el('size').value='24';el('size').events.input();assert.equal(el('sizeValue').value,'24 px');
const r={status:'passed',font_sha256:manifest.fonts[0].sha256,html_sha256:hash(Buffer.from(html)),embedded_woff_sha256:hash(embedded),checks:['editable known text','supplementary Han counted once','unsupported Han/emoji explicitly flagged','literal HTML remains text','empty input','non-BMP search and insertion','zero results','level/source filters','first and last catalog pages','sample restore','size change','embedded WOFF byte identity'],scope:'Node VM with DOM doubles; browser rendering and layout not verified'};
fs.writeFileSync(path.join(dir,'qa/preview-logic.json'),JSON.stringify(r,null,2)+'\n');console.log(JSON.stringify(r));
