# 🧠 Notes — Companion to SucklessCodeGPT

> A modular knowledge base for use alongside `debugger.py`, `optimize-v2.md`, and all SucklessGPT-aligned tools.

---

## 1. Purpose & Scope

**Purpose**  
- Explain core design decisions.  
- Capture useful patterns, gotchas, and enhancements.  
- Serve as a durable reference sheet for contributors and users alike.

**Scope**  
- Applies to: Shell, Python, C, Markdown.  
- Focuses on: CLI workflows, testing, performance, reproducibility.

---

## 2. Design Principles

### 2.1 Minimalism  
- Use lean, dependency-free code.  
- Prefer native Unix tools and POSIX shell.  
- Eliminate unnecessary abstraction.

### 2.2 Composability  
- Favor single-responsibility utilities.  
- Combine behaviors via pipes and text streams.  
- Scripts should return stdout, stderr, and exit codes cleanly.

### 2.3 Transparency  
- Log actions in plain text and structured formats.  
- Expose operations and decisions at each layer.

### 2.4 Reproducibility  
- Pin tool versions (e.g., `bash 5.1.16`, `python 3.11`).  
- Document environment in `config.md` or Dockerfile.  
- Use containerized execution for batch and CI workflows.

---

## 3. Key Usage Patterns

### 3.1 Interactive Sessions  
- Prompt user with feature overview.  
- Show available commands after each action.  
- Store user history in: `~/.sucklessgpt/history`

### 3.2 Batch Execution  
- Accept line-delimited scripts or file paths.  
- Run with `xargs`, `parallel`, or a loop.  
- Emit aggregated result summaries in JSON or table format.

### 3.3 Automation  
- Schedule daily runs via `cron` or `systemd`.  
- Alert on failures using `curl` to Slack/Matrix/email endpoints.  
- Archive outputs in timestamped folders.

---

## 4. Troubleshooting Reference

| Issue                            | Cause                             | Fix                                |
|----------------------------------|------------------------------------|-------------------------------------|
| `command not found`              | Missing program                    | Reinstall or run `init_env.sh`      |
| JSON parse failures              | Invalid HTML or script structure   | Refactor regex or use `pup`         |
| Sluggish script execution        | No pagination or rate limit        | Add batching, rate caps             |
| ShellCheck or pylint fails       | Not installed                      | `sudo pacman -S shellcheck pylint`  |
| `set -e` skips cleanup routines  | Early exit                         | Use `trap` to preserve final steps  |

---

## 5. Frequent Pitfalls & Fixes

- ❌ `echo $var` → ✅ `echo "$var"`  
- ❌ `cat file | grep foo` → ✅ `grep foo file`  
- ❌ Ignoring exit codes → ✅ `set -euo pipefail`  
- ❌ Token overflow → ✅ Tweak `adjust_tokens()` divisor in `debugger.py`

---

## 6. Pro Tips

### 6.1 Custom Configuration  
```sh
# ~/.config/sucklessgpt/config.sh
export DEBUG_LEVEL=2
export MAX_JOBS=8
````

### 6.2 Plugin Support

```sh
for plugin in "$HOME/.sucklessgpt/plugins"/*.sh; do
  [ -r "$plugin" ] && . "$plugin"
done
```

### 6.3 Help Lookup

```sh
sed -n '/^###/,/^###/p' README.md
```

### 6.4 Mini Dashboard

* Log metrics in Prometheus format.
* Serve via `python3 -m http.server` on `metrics/`.

---

## 7. Contributions

### Code Style

* Shell: 80 columns, POSIX-only.
* Python: PEP 8 + `black`.
* C: Google-style, `clang-format`.

### CI Tests

* Use `bats`, `pytest`, and `gcc -fsyntax-only`.

### Documentation

* Use Markdown → man pages via `ronn`.

### Issues

* Use labels: `bug`, `enhancement`, `perf`, `ux`.

---

## 8. Security

* Sanitize user input before eval or exec.
* Avoid wildcard file deletion.
* Use `chmod 600` on `.history`, `.tokens`, etc.

---

## 9. Glossary

* **KISS**: Keep It Simple, Stupid
* **MECE**: Mutually Exclusive, Collectively Exhaustive
* **O(n)**: Linear complexity
* **ShellCheck**: linter for shell scripts
* **Ronn**: Markdown to man converter

---

*End of `notes.md`*
