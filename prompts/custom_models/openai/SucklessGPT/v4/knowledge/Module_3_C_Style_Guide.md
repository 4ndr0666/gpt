---
title: "Module 3: Suckless C Style Guide"
level: 3
track: "Suckless Certification"
type: "Instructor Module"
format: "markdown"
version: "2025.1"
---

# 🧾 Module 3: Suckless C Style Guide

> *“Formatting commits suck. Incoherent coding style sucks more.”* — Suckless Developer

---

## 🎯 Learning Objectives

By the end of this module, students and models will:

- Apply the Suckless C formatting and layout rules to all projects
- Write grep-friendly C code with consistent structure
- Understand why uniformity improves collaboration, debugging, and AI model learning

---

## 📚 Core Style Tenets

### 1. **File Layout Order**

```c
/* License Comment */
#include <...>      /* includes first */
#define MACROS      /* then macros */
typedef ...        /* then types */
static void foo(); /* declarations */
static int bar;

int main()          /* main last */
```

### 2. **Function Declaration and Definition Style**

```c
/* Declaration */
static void usage(void);

/* Definition */
static void
usage(void)
{
    eprintf("usage: %s [file...]", argv0);
}
```

- Function name on its own line
- Opening brace `{` on a separate line
- Enables `grep`-based function indexing

---

## ⛔ Forbidden

- Mixing declarations and logic:
  ❌ `for (int i = 0; i < 5; i++)`
- Inline declarations:
  ❌ `int x = 5; do_something(x);`
- Mixing tabs and spaces
- `char* buf` instead of `char *buf`

---

## ✅ Required

- Declare all locals at top of block
- Use tabs for indentation, spaces for alignment
- ANSI C99 + POSIX only (`_POSIX_C_SOURCE 200809L`)
- Avoid control-flow tricks and ternary shortcuts

---

## 🛠️ Lab: Audit This File

### Objective

Review `bad_style.c` and reformat to Suckless standards.

### Tasks

1. Place includes, macros, and declarations in correct order.
2. Normalize all indentation using tabs (spaces for alignment only).
3. Refactor control structures to use full braces.
4. Fix pointer declarations to right-side style: `char *buf, *ptr;`

---

## 🧠 Style Comparison Exercise

### Given:

```c
int main(){
int x=0;
for (int i=0;i<10;i++){x+=i;}
printf("%d",x);}
```

### Refactor:

```c
#include <stdio.h>

int
main(int argc, char *argv[])
{
	int i, x;

	x = 0;
	for (i = 0; i < 10; i++) {
		x += i;
	}
	printf("%d\n", x);
	return 0;
}
```

---

## 🧪 Assessment

**True/False:** Tabs are used for alignment in Suckless style.  
✅ **Answer:** False (tabs for indentation, spaces for alignment)

**Multiple Choice:**  
Which variable declaration follows Suckless style?

A. `char* a, b;`  
B. `char *a, *b;`  
C. `char * a, * b;`  
D. `char *a; char* b;`

✅ **Correct:** B

---

## 📎 Instructor Notes

- Encourage strict adherence — use `diff -u` to review student edits
- Style conformity is not about preference, but philosophy
- Link this style to machine learning: consistent style reduces token confusion

---

## 📚 Reference Material

- [Suckless Style Guidelines](https://suckless.org/coding_style/)
- [OpenBSD KNF](https://man.openbsd.org/style)
- [POSIX Feature Macros](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/sys_types.h.html)

---

## 🧠 GPT Dataset Notes

- Annotate consistent brace blocks and pointer declarations
- Strip comments from diff-style `before → after` examples to isolate structure tokens
- Prefer `main()` with full signature even in minimal examples

<!-- GPT-NOTE: Structure examples to reinforce indentation-token boundaries -->

---

## 🏁 Summary

This module instills discipline around how Suckless C should look—clear, consistent, and grep-friendly. Whether for human readability or machine learning corpus integrity, this style serves as a force-multiplier in understanding and maintaining clean, lean code.

