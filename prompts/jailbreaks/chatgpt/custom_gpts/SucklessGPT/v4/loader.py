#!/usr/bin/env python3
# SucklessGPT Loader — Certification Content Indexer
# Copyright (c) 4ndr0666

import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
MANIFEST_FILE = BASE_DIR / "suckless_manifest.json"

def load_manifest():
    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def summarize_file(filepath):
    try:
        content = Path(filepath).read_text(encoding='utf-8')
        head = content.strip().splitlines()[:8]
        return "\n".join(head).strip()
    except Exception as e:
        return f"[Error reading {filepath}: {e}]"

def display_index():
    print("🧠 SucklessGPT Certification Module Loader")
    print("──────────────────────────────────────────")
    manifest = load_manifest()
    for entry in manifest:
        file_path = BASE_DIR / entry['filename']
        print(f"\n📘 Module: {entry['id']}")
        print(f"└── File: {entry['filename']}")
        print(f"└── Role: {entry['role']}")
        print(f"└── Desc: {entry['description']}")
        print(f"└── Preview:\n{summarize_file(file_path)}")
        print("─" * 40)

def main():
    display_index()

if __name__ == "__main__":
    main()
