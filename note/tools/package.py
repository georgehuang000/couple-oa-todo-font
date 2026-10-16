"""Create use/source ZIPs from an explicit public-file allowlist.

SPDX-License-Identifier: MIT
"""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
version=json.loads((ROOT/'qa/release.json').read_text('utf-8'))['version']
out=ROOT/'dist';out.mkdir(exist_ok=True)
common=['README.md','README.en.md','OFL.txt','LICENSE-CODE','PROVENANCE.md',
        'FONTLOG.md','font.css','index.html','CONTRIBUTING.md']
folders=['fonts','licenses','charset','assets','qa']
use=[ROOT/name for name in common]
for folder in folders:use.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
source=list(use)+[ROOT/'requirements.txt',ROOT/'.gitattributes',ROOT/'.gitignore']
for folder in ['source','tools']:
    source.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
records=[]
for kind,files in [('Use',use),('Source',source)]:
    target=out/f'CoupleOANote8105-{version}-{kind}.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for file in sorted(set(files)):
            assert file.is_file(),file
            archive.write(file,file.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for file in set(files):assert archive.read(file.relative_to(ROOT).as_posix())==file.read_bytes()
    records.append({'file':target.name,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'files':len(set(files))})
checksums=''.join(f'{r["sha256"]}  {r["file"]}\n' for r in records)
for file in [ROOT/'fonts/CoupleOANote8105-Regular.ttf',ROOT/'fonts/CoupleOANote8105-Regular.woff',ROOT/'OFL.txt']:
    checksums+=hashlib.sha256(file.read_bytes()).hexdigest()+'  '+file.name+'\n'
(out/'SHA256SUMS').write_text(checksums,encoding='ascii')
(out/'packages.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
print(json.dumps(records,indent=2))
