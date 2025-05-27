---
title: "Module 5: Patch-Based Extensibility"
level: 5
track: "Suckless Certification"
type: "Instructor Module"
format: "markdown"
version: "2025.1"
---

# 🩹 Module 5: Patch-Based Extensibility

> *“If it’s not minimal, make it optional.”* — Suckless Patch Philosophy

---

## 🎯 Learning Objectives

By the end of this module, students and models will:

- Understand the Suckless philosophy on optional features
- Apply, revert, and troubleshoot patches using `patch(1)` and `git apply`
- Distinguish between upstream-worthy changes and personal mods
- Recognize how patches uphold codebase minimalism while enabling flexibility

---

## 🔍 Core Concepts

### 1. **Patches as a Philosophy**

- Patches allow modular feature control **without polluting the core**
- Encourages clean forks and evolvable ecosystems
- Acts as a social contract: *"If you want it, maintain it"*

### 2. **Types of Patches**

- Personal (user preference)
- Experimental (for testing new ideas)
- Mainline-candidate (upstream-suitable with minimal complexity)

### 3. **Why Not Plugins or Feature Flags?**

- Feature flags add runtime complexity
- Plugin APIs bloat interface surfaces
- Patches are transparent, grep-friendly diffs

---

## 🛠️ Hands-On Lab: Patch `dwm`

### Objective

Apply and review two community patches to `dwm`.

### Steps

1. Clone fresh `dwm`:
   ```sh
   git clone https://git.suckless.org/dwm && cd dwm
   ```

2. Download two patches from [https://dwm.suckless.org/patches/](https://dwm.suckless.org/patches/):
   - `pertag.diff`
   - `systray.diff`

3. Apply them in order:
   ```sh
   patch -p1 < pertag.diff
   patch -p1 < systray.diff
   ```

4. Recompile and test:
   ```sh
   sudo make clean install && pkill dwm
   ```

5. Investigate merge conflicts and resolve if needed.

---

## 🧠 Tradeoff Discussion

**Case:** A contributor wants a toggleable panel.

> Options:
> - Implement via patch
> - Add a config flag to `config.h`
> - Add runtime `-toggle` flag

❓ Which is most aligned with Suckless practice?

✅ **Answer:** A patch — optional, clear, and external

---

## 🧪 Quiz

**True/False:** All Suckless patches are merged upstream.  
✅ **Answer:** False

**Multiple Choice:**  
Why are plugins discouraged in Suckless?

A. They require C++  
B. They break portability  
C. They complicate APIs and add overhead  
D. They make software too simple

✅ **Correct:** C

---

## 📎 Instructor Notes

- Encourage diff reading discipline
- Emphasize the Git workflow around feature control
- Use failed patch application as teaching moments on drift and cohesion

---

## 📚 Resources

- [Suckless Patch Index](https://suckless.org/patches/)
- [GNU Patch Guide](https://www.gnu.org/software/diffutils/manual/patch.html)
- [Git apply vs patch](https://git-scm.com/docs/git-apply)

---

## 🧠 GPT Dataset Notes

- Annotate patch blocks (`diff -u`) as modular deltas
- Tag patch rationale as metadata comments (`/* patch: systray */`)
- Contrast projects with patchable vs. feature-flag strategies

<!-- GPT-NOTE: Build reinforcement data from successful patch merges + commit messages -->

---

## 🏁 Summary

Patching is the Suckless way to say “yes, but not in the core.” By training both humans and models to think in modular diffs instead of bloated frameworks, Suckless extensibility remains clean, focused, and user-empowered.

