#!/usr/bin/env python3
"""Deterministically package an installable 4ndr0neering .skill archive."""
import hashlib,json,stat,zipfile
from pathlib import Path
root=Path(__file__).parent/'4ndr0neering'
out=Path('/mnt/data/4ndr0neering_v8.2.0.skill')
old=Path('/mnt/data/4ndr0neering(1).skill')
h=lambda b:hashlib.sha256(b).hexdigest()
files={}
for p in sorted(root.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='MANIFEST-SHA256.json':
        rel=p.relative_to(root).as_posix();data=p.read_bytes()
        files[rel]={'sha256':h(data),'size':len(data)}
manifest={'format':'4ndr0neering-skill-manifest-v1','skill_version':'8.2.0','base_v8_1_archive_sha256':h(old.read_bytes()),'files':files,'warning':'SHA-256 hashes validate package integrity, not publisher authenticity'}
(root/'MANIFEST-SHA256.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
for p in root.rglob('__pycache__'):
    if p.is_dir():
        import shutil
        shutil.rmtree(p)
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(root.rglob('*')):
        if not p.is_file():continue
        relative=p.relative_to(root).as_posix()
        info=zipfile.ZipInfo(relative,date_time=(2026,11,12,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=(stat.S_IFREG|(0o755 if relative.startswith('scripts/') else 0o644))<<16
        z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
print(json.dumps({'archive':str(out),'bytes':out.stat().st_size,'sha256':h(out.read_bytes()),'files':len(files),'uncompressed_content_bytes':sum(i['size'] for i in files.values())},sort_keys=True))
