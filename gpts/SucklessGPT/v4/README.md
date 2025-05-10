# 🧠 SucklessGPT v4

This GPT instance is engineered for strict compliance with the [Suckless](https://suckless.org) philosophy—minimal, composable, and production-ready tooling only.

## 🔍 Files & Roles

| File                          | Role                                |
|-------------------------------|-------------------------------------|
| `core_prompt.txt`            | Defines system personality and logic|
| `debug_controller.txt`       | Internal debugger and static checker|
| `knowledge/behavior_map.txt` | Dispatch rules and output heuristics|
| `knowledge/performance_routines.txt` | Profiling and benchmarking logic|

## 📁 Directory Structure

```

SucklessGPT/v4/
├── core\_prompt.txt
├── debugger.py
├── debug\_controller.txt
├── suckless\_manifest.json
└── knowledge/
├── behavior\_map.txt
└── performance\_routines.txt

```

## ⚙️ Usage

Upload all files to the GPT deployment interface that supports:
- ≥ 10 onboard files
- Instruction-tuned models
- System prompt ingestion from file (`core_prompt.txt`)

## 🚀 Purpose

This assistant:
- Refactors shell/C code to suck less
- Grades alternatives using the suckless rubric
- Provides static patching and benchmarking strategies
- Instructs users on how to think like a suckless dev

---
© MIT License — Crafted by 4ndr0666 and SucklessCodeGPT
