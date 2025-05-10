# 🧠 SucklessGPT v4 — Instructor-Grade GPT for Minimalist Systems

SucklessGPT is a purpose-built instructor model designed to teach, grade, and refactor code according to the minimalist philosophy of [Suckless.org](https://suckless.org). It treats complexity as a liability and trains models and users to prefer clarity, frugality, and composability above all else.

---

## 🎯 Purpose

> To instruct and refine — never bloat.

SucklessGPT is engineered to:
- Provide zero-dependency, cleanly formatted solutions
- Guide learners through a 10-module Suckless certification curriculum
- Apply static analysis, patch-based grading, and minimal benchmarking
- Act as a mentor, not a middleware

---

## 🧩 Directory Structure

```

SucklessGPT/v4/
├── core\_prompt.txt                     # Primary system prompt (≥8000 chars)
├── debug\_controller.txt               # Fully inline static analysis engine
├── suckless\_manifest.json             # Machine-readable content manifest
├── loader.py                          # CLI module and content indexer
├── README.md                          # This file
└── knowledge/
├── behavior\_map.txt               # Trigger-based routing logic
├── performance\_routines.txt       # Benchmarking and profiling logic
├── Module\_1\_Philosophy\_of\_Minimalism.md
├── Module\_2\_Core\_Principles.md
├── Module\_3\_C\_Style\_Guide.md
├── Module\_4\_Config\_via\_Code.md
├── Module\_5\_Patch\_Based\_Extensibility.md
└── Module\_6\_to\_10\_merged.txt      # Pragmatism → Capstone

```

---

## 🧠 System Roles

| File                        | Role                 | Description                                  |
|-----------------------------|----------------------|----------------------------------------------|
| `core_prompt.txt`           | System Prompt        | Defines behavior, personality, and mission   |
| `debug_controller.txt`      | Debug Logic Module   | Lints, grades, and performs static checks    |
| `behavior_map.txt`          | Output Logic         | Routes GPT behavior by context and keyword   |
| `performance_routines.txt`  | Benchmarking Logic   | CI logic, perf stats, runtime optimization   |
| `Module_*.md`               | Certification Input  | Authoritative instructor modules 1–10        |

---

## 📦 GPT Upload Requirements

Only **10 files total** are uploadable in GPT context:

```

1. core\_prompt.txt
2. debug\_controller.txt
3. behavior\_map.txt
4. performance\_routines.txt
5. Module\_1\_Philosophy\_of\_Minimalism.md
6. Module\_2\_Core\_Principles.md
7. Module\_3\_C\_Style\_Guide.md
8. Module\_4\_Config\_via\_Code.md
9. Module\_5\_Patch\_Based\_Extensibility.md
10. Module\_6\_to\_10\_merged.txt

````

Use `sha256sums.txt` to validate integrity post-upload.

---

## 🚀 How to Use

1. Upload all 10 files to OpenAI or OpenRouter's custom GPT builder.
2. Ensure `core_prompt.txt` is used as the system prompt.
3. Validate file list using `loader.py` or `suckless_manifest.json`.
4. Ask SucklessGPT to:
   - Grade a script for bloat
   - Refactor C code to pass Module 3
   - Simulate a certification test
   - Analyze Makefiles for simplicity

---

## 🛡️ Compliance Checks

- ✅ No symbolic placeholders
- ✅ No internal file leakage
- ✅ Every module ≤ 80 cols or wrapped
- ✅ All behavior aligned to suckless rubric

---

## 📝 Licensing

MIT — [4ndr0666](https://github.com/4ndr0666) and contributors  
Modules adapted from https://suckless.org, GNU tools, and real postmortems.

