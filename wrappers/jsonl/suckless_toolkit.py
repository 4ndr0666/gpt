#!/usr/bin/env python3
"""
jsonl_toolkit_v1.2.py — SucklessGPT Dataset Manager
Adds prompt_toolkit, colored prompts, --help, and all options via argparse.
"""

import os
import re
import json
import argparse
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML

MODULES_DIR = Path("knowledge")
DEFAULT_OUTPUT = Path("suckless_chunks.jsonl")


def extract_qa_pairs(md_text: str) -> list[dict]:
    pairs = []
    mcq_pattern = re.compile(
        r"(?s)>?\s?\*\*(Multiple Choice|True/False)\*\*:(.*?)✅\s.*?(\*\*Correct.*?:)?\s*\*\*(.*?)\*\*",
        re.IGNORECASE,
    )
    for match in mcq_pattern.finditer(md_text):
        q = match.group(2).strip()
        a = match.group(4).strip()
        if q and a:
            pairs.append({"user": q, "assistant": f"✅ Correct Answer: **{a}**"})
    gpt_note_block = re.compile(r"<!-- GPT-NOTE: (.*?) -->", re.IGNORECASE)
    for m in gpt_note_block.finditer(md_text):
        content = m.group(1).strip()
        if content:
            pairs.append(
                {
                    "user": "How should I fine-tune GPT on this?",
                    "assistant": f"🧠 GPT Instruction: {content}",
                }
            )
    return pairs


def process_modules(directory: Path) -> list[dict]:
    all_pairs = []
    for path in sorted(directory.glob("Module_*.md")):
        content = path.read_text(encoding="utf-8")
        pairs = extract_qa_pairs(content)
        for p in pairs:
            all_pairs.append(
                {
                    "messages": [
                        {"role": "user", "content": p["user"]},
                        {"role": "assistant", "content": p["assistant"]},
                    ]
                }
            )
    return all_pairs


def write_jsonl(pairs: list[dict], outfile: Path):
    with outfile.open("w", encoding="utf-8") as f:
        for item in pairs:
            f.write(json.dumps(item) + "\n")


def merge_jsonl(pairs: list[dict], outfile: Path):
    existing = []
    if outfile.exists():
        with outfile.open("r", encoding="utf-8") as f:
            existing = [json.loads(line) for line in f]
    combined = existing + pairs
    write_jsonl(combined, outfile)


def preview(pairs: list[dict]):
    for i, item in enumerate(pairs):
        print(f"--- {i+1} ---")
        print("🧑‍🎓 USER:", item["messages"][0]["content"])
        print("🤖 ASSISTANT:", item["messages"][1]["content"])
        print()


def validate_jsonl(file_path: Path):
    errors = []
    with file_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            try:
                obj = json.loads(line)
                if "messages" not in obj:
                    errors.append(f"Line {i}: missing 'messages'")
                    continue
                if not isinstance(obj["messages"], list) or len(obj["messages"]) != 2:
                    errors.append(f"Line {i}: invalid message pair")
            except json.JSONDecodeError as e:
                errors.append(f"Line {i}: JSON error - {e}")
    return errors


def interactive_builder(outfile: Path):
    print("🔧 Interactive GPT Q&A Entry")
    questions = []
    while True:
        user = prompt(
            HTML("<ansicyan>Enter <b>USER</b> message (blank to stop):</ansicyan>\n> ")
        ).strip()
        if not user:
            break
        assistant = prompt(
            HTML("<ansicyan>Enter <b>ASSISTANT</b> message:</ansicyan>\n> ")
        ).strip()
        questions.append(
            {
                "messages": [
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": assistant},
                ]
            }
        )
    if questions:
        merge_jsonl(questions, outfile)
        print(f"✅ {len(questions)} entries saved to {outfile}")


def main():
    parser = argparse.ArgumentParser(
        description="📦 SucklessGPT JSONL Toolkit v1.2 — Create, validate, and preview training files.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--preview", action="store_true", help="Preview extracted message pairs"
    )
    parser.add_argument("--write", action="store_true", help="Write JSONL to disk")
    parser.add_argument(
        "--merge", action="store_true", help="Merge with existing output"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate an existing JSONL file"
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Manually create Q&A entries"
    )
    parser.add_argument(
        "--file", type=str, default="suckless_chunks.jsonl", help="Output file path"
    )

    args = parser.parse_args()
    outpath = Path(args.file)

    if args.interactive:
        interactive_builder(outpath)
        return

    if args.validate:
        errors = validate_jsonl(outpath)
        if errors:
            print("❌ Validation errors found:")
            for err in errors:
                print(" -", err)
        else:
            print("✅ File passed validation.")
        return

    print(f"📦 Parsing modules from: {MODULES_DIR}")
    pairs = process_modules(MODULES_DIR)
    print(f"✅ Found {len(pairs)} entries.")

    if args.preview:
        preview(pairs)

    if args.write:
        if args.merge:
            merge_jsonl(pairs, outpath)
        else:
            write_jsonl(pairs, outpath)
        print(f"📝 Written to: {outpath}")


if __name__ == "__main__":
    main()
