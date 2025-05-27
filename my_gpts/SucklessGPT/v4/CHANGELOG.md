# 🧾 Changelog — SucklessGPT

## ✅ v4.0 — "Finalized GPT-Ready Instructor Model" (May 2025)

### ✨ Major Changes

- 🔁 **System Prompt Refactored**
  - Converted from `core_prompt.md` to `core_prompt.txt`
  - Expanded to ≥8000 characters
  - Uses precise `ROLE DEFINITIONS`, `BEHAVIORAL RULES`, and `RUBRICS`

- 🧠 **Abstract Module Decomposition**
  - Split `debugger.py`, `optimize.md`, and `notes.md` into:
    - `debug_controller.txt`
    - `performance_routines.txt`
    - `behavior_map.txt`
  - Removed direct filename references (e.g. `debugger.py` → "debug controller")

- 🧩 **Modular Instructional Curriculum (v2 Format)**
  - Converted all 10 canonical modules to `.md` under `knowledge/`
  - Merged `Module_6_to_10` into one `.txt` file to fit 10-file upload constraint

- ✅ **Validation Systems Added**
  - `sha256sums.txt`: Verifiable file hash map
  - `loader.py`: CLI-based module viewer and manifest parser

- 🧾 **suckless_manifest.json Overhaul**
  - 10-file limit enforced via new roles: `system-prompt`, `debug-logic`, `instructor`, `optimizer`

### 🧹 Cleanups & Renames

- 🗑️ Removed: `debugger_controller.txt` (placeholder)
- 🔄 Renamed: `debugger.py` → `debug_controller.txt`
- 📎 Clarified: All internal logic now conforms to "abstracted module" rule in system prompt

---

## ✅ v3.1 — *Pre-GPT Modular Planning Phase* (April 2025)
- Drafted modular certification layout
- Extracted chunks from `SUCKLESS_ACADEMY.md`
- Placeholder routing via `notes.md` and `optimize.md`

## 🧪 v2.0 — *Training Intent Design* (March 2025)
- Coded `debugger.py` and `optimize.md`
- First behavioral sketch for GPT command routing

## 🧱 v1.0 — *Initial Research Dump* (February 2025)
- Recursive crawl and synthesis of `suckless.org`
- No upload constraints considered
- All-in-one prompt file `SUCKLESS_ACADEMY.md`

---
