# ⚙️ Optimize — Suckless Profiling & Tuning Guide

> Lean optimization principles for POSIX Shell, Python, and C projects.

---

## 1. Philosophy

- **Do more with less**: reduce lines, increase throughput.  
- **Measure before modifying**: always baseline performance.  
- **Minimal wins**: low complexity beats deep stacks.

---

## 2. Optimization Lifecycle

### 2.1 Baseline First

1. **Standardize Environment**
   - Docker: `alpine`, `archlinux:base-devel`  
   - Pin versions for reproducibility

2. **Benchmark Core Metrics**
   | Metric      | Tool                     |
   |-------------|--------------------------|
   | Latency     | `time`, `hyperfine`      |
   | Throughput  | `perf stat`              |
   | Memory      | `/usr/bin/time -v`       |
   | CPU         | `top`, `htop`, `ps`      |
   | I/O         | `iostat`, `iotop`        |

3. **Record**
   ```csv
   phase,latency_s,mem_kb,cpu_pct
   baseline,0.224,5120,5.2
````

---

### 2.2 Static Profiling

| Language | Tools                 | Command Example                     |
| -------- | --------------------- | ----------------------------------- |
| Shell    | `shellcheck`, `shfmt` | `shellcheck -x script.sh`           |
| Python   | `flake8`, `mypy`      | `flake8 main.py`                    |
| C        | `gcc`, `cppcheck`     | `gcc -Wall -fsyntax-only program.c` |

---

### 2.3 Dynamic Profiling

1. **CPU**

   * `perf record -g ./binary` → `perf report`
   * `gprof`, `callgrind`

2. **Memory**

   * `valgrind --tool=massif ./binary`
   * Visualize with `ms_print massif.out.*`

3. **Runtime**

   * `strace`, `ltrace`
   * Instrument with `LD_PRELOAD` if needed

---

### 2.4 Tuning Workflow

```bash
for bs in 32 64 128; do
  /usr/bin/time -f "%e,%M" ./mytool -b $bs > /dev/null 2>> metrics.csv
done
```

* Visualize using `pandas`, `gnuplot`, or `csvkit`

---

### 2.5 CI Integration

```yaml
jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: sudo apt install time valgrind
      - run: bash bench/run_all.sh
      - run: python3 bench/compare.py baseline.csv current.csv
```

* Alert if delta > 10% latency or 20% memory

---

## 3. Advanced Topics

### 3.1 Bytecode & AOT

* Python: `__pycache__`, `pyinstaller`
* Shell: Optional `shc`
* C: `-O3`, `-march=native`, LTO

### 3.2 Concurrency

* GNU Parallel

  ```bash
  parallel -j4 ./job.sh ::: input1 input2
  ```

* POSIX xargs

  ```bash
  xargs -P4 -n1 ./script.sh < list.txt
  ```

### 3.3 File I/O

* `read -r` over `cat` pipelines
* `dd if=input of=output bs=1M` for block copies

---

## 4. Patterns & Refactors

| Before                    | After                      |                 |
| ------------------------- | -------------------------- | --------------- |
| \`cat file                | grep foo\`                 | `grep foo file` |
| `for f; do; done < <(ls)` | `for f in *; do ...; done` |                 |
| `wc -l file`              | `awk 'END{print NR}' file` |                 |

---

## 5. Safety & Sanity

* Always quote variables: `"${var}"`
* Enable safe mode: `set -euo pipefail`
* Redirect logs: `exec > >(tee logfile) 2>&1`

---

## 6. Tool References

| Tool           | Use Case                   |
| -------------- | -------------------------- |
| `perf`         | Sample-based CPU profiling |
| `shellcheck`   | Lint shell scripts         |
| `valgrind`     | Memory profiler            |
| `pyinstrument` | Python profiler            |
| `clang-tidy`   | Modern C best practices    |

---

## 7. Extensibility

* Add benchmark scripts under `bench/` as `bench_*.sh`
* Use config-driven flag maps for tuning automation

---

## 8. Glossary

* **Throughput:** Units per second
* **Latency:** Time per task
* **Peak RSS:** Maximum memory held
* **GIL:** Python's Global Interpreter Lock
* **AOT:** Ahead-of-Time compilation

---

*End of `optimize.md`*
