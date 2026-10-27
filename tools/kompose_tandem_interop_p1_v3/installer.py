"""Conservative snapshot-pinned overlay installer, stdlib only. Tandem Kontexte/Kompose P1."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PKG = Path(__file__).resolve().parent
ROOT = PKG.parents[1]
MANIFEST = PKG / 'manifest.json'


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda:handle.read(1048576),b''):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str):
    raise RuntimeError(msg)


def relpath(raw: str) -> Path:
    p = Path(raw)
    if p.is_absolute() or not raw or ':' in raw or '\\' in raw or any(part in ('.','..','') for part in raw.split('/')):
        fail('Unsafe manifest path')
    return Path(*raw.split('/'))


def within(root: Path, path: Path):
    root = root.resolve(strict=True)
    cur = path
    while cur != root and cur != cur.parent:
        if cur.is_symlink():
            fail(f'Symlink cannot be modified: {path}')
        cur = cur.parent
    if cur != root:
        fail('Path escapes repository')


def manifests():
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if (ROOT / data['sentinel']).is_file() is False:
        fail(f"Not the expected repository root: {ROOT}")
    entries = data['entries']
    seen=set()
    for entry in entries:
        rel = relpath(entry['path'])
        if str(rel) in seen: fail('Duplicate manifest path')
        seen.add(str(rel))
        stage = PKG / 'payload' / rel
        within(PKG,stage)
        if not stage.is_file() or digest(stage)!=entry['new']:
            fail(f"Payload corrupted: {rel}")
    return data


def statuses(entries):
    result=[]
    for entry in entries:
        rel=relpath(entry['path'])
        dest=ROOT/rel
        within(ROOT,dest)
        existing = digest(dest) if dest.is_file() else None
        if dest.exists() and not dest.is_file():
            status='CONFLICT'
        elif existing == entry['new']:
            status='ALREADY_UPDATED'
        elif existing == entry['old']:
            status='READY'
        else:
            status='CONFLICT'
        result.append((entry, status))
        print(f'[{status}] {rel.as_posix()}')
    if any(state=='CONFLICT' for _,state in result):
        fail('Snapshot SHA-256 divergence: installation refused without overwriting files')
    return result


def test_code(data, *, patched: bool):
    with tempfile.TemporaryDirectory(prefix='tandem-' + data['id'] + '-') as d:
        temp=Path(d)/'repo'; temp.mkdir()
        # Explicit small allowlist, not a recursive copy of credentials or test artifacts.
        for src_rel in data['test_copy']:
            rel = relpath(src_rel)
            src = ROOT / rel
            if not src.is_dir() and not src.is_file():
                if patched and src_rel in {item['path'] for item in data['entries']}:
                    continue  # a new source supplied by this overlay
                fail('Missing test source: ' + src_rel)
            within(ROOT,src)
            dest = temp/rel
            if src.is_dir():
                shutil.copytree(src,dest,symlinks=False,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.pytest_cache'))
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src,dest)
        if patched:
            for entry in data['entries']:
                rel=relpath(entry['path']); target=temp/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(PKG/'payload'/rel,target)
        for command in data['commands']:
            print('[TEST]', ' '.join(command))
            env = dict(os.environ, PYTHONPATH=str(temp/'src'), PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
            cp=subprocess.run([sys.executable, *command],cwd=str(temp),stdin=subprocess.DEVNULL,
                              env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',timeout=100)
            print(cp.stdout[-4500:])
            if cp.returncode:
                fail('Isolated test failure: '+ ' '.join(command))
    print('[PASS] Validations sur copie temporaire')


def backup_root(data):
    return ROOT.parent/'Tandem_Local'/data['id']/'backups'


def save_atomic(path:Path,body:bytes):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='wb',dir=path.parent,prefix='.tandem-',delete=False) as f:
        tmp=Path(f.name); f.write(body)
    os.replace(tmp,path)


def rollback(data):
    root=ROOT.parent/'Tandem_Local'/data['id']
    pointer=root/'current.json'
    if not pointer.is_file(): fail('No recorded installation backup to roll back')
    state=json.loads(pointer.read_text(encoding='utf-8'))
    directory=(root/'backups'/state['backup_id'])
    if not directory.is_dir(): fail('Backup missing')
    for entry in state['files']:
        dest=ROOT/relpath(entry['path']);within(ROOT,dest)
        if not dest.is_file() or digest(dest)!=entry['new']:
            fail('Rollback refused; installed file changed: '+entry['path'])
        if entry['old'] is not None:
            old=directory/relpath(entry['path']);within(directory,old)
            if not old.is_file() or digest(old)!=entry['old']:
                fail('Backup changed: '+entry['path'])
    for entry in state['files']:
        dest=ROOT/relpath(entry['path'])
        if entry['old'] is None:
            dest.unlink()
        else:
            old=directory/relpath(entry['path'])
            save_atomic(dest,old.read_bytes())
        print('[RESTORED]',entry['path'])
    pointer.unlink()
    print('[OK] Rollback termine; nouvelles sources restaurees ou retirees')


def install(data, checked):
    changed=[e for e,s in checked if s=='READY']
    if not changed:
        print('[OK] Deja installe; aucun fichier modifie, aucune nouvelle sauvegarde')
        return
    test_code(data,patched=True)
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    root=backup_root(data)/stamp;root.mkdir(parents=True,exist_ok=False)
    backup=[]
    try:
        for entry in changed:
            rel=relpath(entry['path']);dest=ROOT/rel
            if entry['old'] is not None:
                b=root/rel;b.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(dest,b)
                if digest(b)!=entry['old']: fail('Backup integrity error')
            backup.append(entry)
        for entry in changed:
            rel=relpath(entry['path']);dest=ROOT/rel
            # Recheck immediately before replacement
            actual=digest(dest) if dest.is_file() else None
            if actual!=entry['old']: fail('Concurrent source change')
            save_atomic(dest,(PKG/'payload'/rel).read_bytes())
        statuses(data['entries'])
        test_code(data,patched=False)
    except Exception:
        for entry in reversed(backup):
            rel=relpath(entry['path']);dest=ROOT/rel
            if entry['old'] is None:
                if dest.is_file() and digest(dest)==entry['new']: dest.unlink()
            else:
                b=root/rel
                if b.is_file(): save_atomic(dest,b.read_bytes())
        raise
    state={'backup_id':stamp, 'files':backup}
    pointer=ROOT.parent/'Tandem_Local'/data['id']/'current.json'
    save_atomic(pointer,(json.dumps(state,indent=2)+'\n').encode())
    print('[OK] Correctif installe; sauvegarde:',root)


def main():
    mode=sys.argv[1].upper() if len(sys.argv)>1 else 'PREVIEW'
    data=manifests()
    print(f"=== {data['title']} / {mode} ===")
    print('[REPO]',ROOT)
    print('[PORTEE] Code local uniquement; aucune DB, Docker, VPS ou API externe')
    if mode=='ROLLBACK':rollback(data);return
    checked=statuses(data['entries'])
    if mode=='PREVIEW':print('[OK] Apercu lecture seule; empreintes conformes');return
    if mode=='INSTALL':install(data,checked);return
    if mode=='VERIFY':
        if any(s!='ALREADY_UPDATED' for _,s in checked): fail('Correctif incomplet ou absent')
        test_code(data,patched=False)
        print('[OK] Sources et tests conformes; aucune qualification runtime externe');return
    fail('Unknown mode')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('[ECHEC]',exc)
        sys.exit(1)
