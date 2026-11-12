#!/usr/bin/env python3
"""Verify extracted 4ndr0neering 8.2 handoff file inventory and hashes."""
import hashlib,sys
from pathlib import Path
base=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
manifest=base/'SHA256SUMS.txt'
files=[]
for line in manifest.read_text().splitlines():
    digest, sep, name=line.partition('  ')
    if len(digest)!=64 or not sep or not name or '..' in Path(name).parts:raise SystemExit('bad manifest line')
    p=(base/name).resolve()
    if not p.is_relative_to(base) or not p.is_file():raise SystemExit('missing member: '+name)
    if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise SystemExit('hash mismatch: '+name)
    files.append(name)
actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
if actual!=set(files)|{'SHA256SUMS.txt'}:raise SystemExit('extra/missing file in handoff')
print(f'HANDOFF VERIFIED: {len(files)}/{len(files)} files')
