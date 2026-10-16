# SPDX-License-Identifier: MIT
"""Package only reviewed, tracked repository files for a GitHub release."""
from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    project = json.loads((ROOT / 'project.json').read_text('utf-8'))
    result = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, check=True, capture_output=True)
    tracked = [Path(p) for p in result.stdout.decode('utf-8').split('\0') if p]
    if not tracked or any(p.is_absolute() or '..' in p.parts for p in tracked):
        raise ValueError('Expected a reviewed, tracked repository.')
    # This is the Todo package. Note has its own package tool and license.
    excluded = {'README.todo.md', 'families.json', 'docs/COLLECTION.md'}
    tracked = [p for p in tracked if p.parts[0] not in {'note', '.github'}
               and p.as_posix() not in excluded]
    dest = ROOT / 'dist'
    dest.mkdir(exist_ok=True)
    small_roots = {'fonts', 'assets', 'docs', 'licenses', 'data'}
    small_files = {'README.md', 'OFL.txt', 'LICENSE', 'FONTLOG.md', 'CONTRIBUTING.md', 'index.html', 'project.json'}
    packages = {}
    for kind in ['install', 'source']:
        entries = tracked if kind == 'source' else [p for p in tracked if p.parts[0] in small_roots or p.as_posix() in small_files]
        target = dest / f'CoupleOATodo-v{project["release"]}-{kind}.zip'
        with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for rel in sorted(entries):
                path = ROOT / rel
                if path.is_symlink() or not path.is_file():
                    raise ValueError(f'Not a regular file: {rel}')
                item = zipfile.ZipInfo(f'CoupleOATodo-v{project["release"]}/{rel.as_posix()}', (2026, 10, 16, 0, 0, 0))
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o100644 << 16
                content_path = ROOT / 'README.todo.md' if rel.as_posix() == 'README.md' else path
                archive.writestr(item, content_path.read_bytes(), compresslevel=9)
        with zipfile.ZipFile(target) as archive:
            if archive.testzip() is not None or len(archive.namelist()) != len(entries):
                raise ValueError('ZIP integrity check failed.')
        packages[target.name] = {'bytes': target.stat().st_size, 'files': len(entries),
                                 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'crc_passed': True}
    all_files = [dest / name for name in packages] + sorted((ROOT / 'fonts').glob('*')) + [ROOT / 'OFL.txt']
    (dest / 'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n' for p in all_files), encoding='utf-8')
    (dest / 'package-verification.json').write_text(json.dumps(packages, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(packages, indent=2))


if __name__ == '__main__':
    main()
