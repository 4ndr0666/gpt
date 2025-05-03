# optimize-v2.md

## 1. Introduction

This document, **Optimize v2.0**, provides a comprehensive guide to performance tuning, resource optimization, and benchmarking for command-line tools, scripts, and small C programs in the Suckless philosophy. It covers static and dynamic analysis, metrics collection, automated tuning loops, and integration with CI pipelines. 

- **Target Audience:** Developers seeking to squeeze maximum efficiency from minimalistic codebases.
- **Scope:** Shell scripts, Python utilities, C modules, CI workflows, containerized environments.
- **Philosophy:** “Do more with less”—measure, optimize, repeat.

---

## 2. Core Phases of Optimization

### 2.1 Baseline Measurement

1. **Environment Standardization**  
   - Use Docker/Podman container (`alpine:latest` or `archlinux:base-devel`).  
   - Pin tool versions (`bash-5.1.16`, `gcc-12.2.1`, `python-3.11.2`).

2. **Define Metrics**  
   - **Latency:** Wall-clock time (`time` command).  
   - **Throughput:** Items processed per second.  
   - **Memory:** Peak resident set size (`/usr/bin/time -v`).  
   - **CPU Utilization:** `%CPU` from `ps` or `top`.  
   - **I/O:** Block reads/writes (`iostat`, `/usr/bin/time`).  

3. **Instrumentation**  
   - Wrap commands:  
     ```bash
     /usr/bin/time -v ./my_script.sh input.txt > /dev/null
     ```  
   - Use `perf stat` for hardware counters:  
     ```bash
     perf stat -e cycles,instructions,cache-references,cache-misses ./fastgrep pattern file.txt
     ```

4. **Record Baseline**  
   - Save to CSV:  
     ```csv
     phase,latency_s,mem_kb,cpu_pct,io_read_kb,io_write_kb
     baseline,1.234,10240,15,500,100
     ```  
   - Store under `metrics/baseline.csv`.

### 2.2 Static Analysis

1. **Shell Scripts**
   - Run `shellcheck --format=json` to detect inefficiencies:  
     ```bash
     shellcheck -x script.sh
     ```  
   - Check for unnecessary `grep | sed` chains; suggest `awk`.

2. **Python Code**
   - Use `flake8` and `mypy`:  
     ```bash
     flake8 module.py && mypy module.py
     ```  
   - Profile with `pyinstrument`:  
     ```bash
     pyinstrument script.py --include-all
     ```

3. **C Code**
   - Compile with `-O2 -march=native -g` and run `cppcheck`:  
     ```bash
     gcc -O2 -march=native -o prog prog.c  
     cppcheck --enable=performance prog.c
     ```  
   - Use `clang-tidy` for modern C idioms.

### 2.3 Dynamic Profiling

1. **Sampling Profiler**  
   - `perf record -g ./prog` → `perf report`  
   - Identify hot functions (>10% CPU).

2. **Instrumentation Profiler**  
   - Use `gprof`:
     ```bash
     gcc -pg -O2 -o prog prog.c  
     ./prog && gprof prog gmon.out > prof.txt
     ```  
   - Analyze call graphs.

3. **Memory Profiling**  
   - `valgrind --tool=massif ./prog` → `ms_print massif.out.*`  
   - Detect heap peaks.

### 2.4 Automated Tuning Loop

1. **Parameter Sweep**  
   - For scripts: vary batch sizes, concurrency flags.  
   - For C: tune buffer sizes, unrolling factors in code.  

2. **Bash Wrapper**  
   ```bash
   for bs in 16 32 64 128; do
     /usr/bin/time -f "%e,%M" ./myprog -b $bs input > /dev/null 2>> metrics/tune.csv
   done
````

3. **Analysis**

   * Load `metrics/tune.csv` into pandas/matplotlib (Python) for visualization.

### 2.5 Regression & CI Integration

1. **GitHub Actions Workflow**

   ```yaml
   jobs:
     benchmark:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - run: sudo apt-get install -y build-essential time valgrind
         - run: bash benchmarks/run_all.sh
         - run: python3 benchmarks/compare.py metrics/baseline.csv metrics/current.csv
   ```

2. **Threshold Alerts**

   * Fail build if latency > baseline ×1.10 or mem > baseline ×1.20.

---

## 3. Advanced Topics

### 3.1 JIT Compilation & Bytecode Caching

* **Python:** Use `__pycache__`, `pyinstaller` for AOT.
* **Shell:** Precompile via `shc` (optional).

### 3.2 Parallelism & Concurrency

1. **GNU Parallel**

   ```bash
   parallel -j "$(nproc)" ./worker.sh {} :::: tasks.txt
   ```
2. **POSIX xargs**

   ```bash
   cat tasks.txt | xargs -P4 -I{} ./worker.sh {}
   ```

### 3.3 File I/O Optimization

* Prefer `read -r` over `cat file | while read`.
* Use `dd bs=1M` for bulk transfers.

### 3.4 Asynchronous Execution

* Use background jobs with `&` and `wait`.

---

## 4. Best Practices & Pitfalls

* Avoid Useless Use of `cat`.
* Beware of globbing with large directories.
* Always quote variables: `"$var"`.
* Use `set -o nounset` to catch unset variables.

---

## 5. Common Patterns

| Pattern          | Before                        | After                           |                               |
| ---------------- | ----------------------------- | ------------------------------- | ----------------------------- |
| Grep + Awk       | \`grep foo file               | awk '{print \$2}'\`             | `awk '/foo/ {print $2}' file` |
| Subshell in Loop | `for f; do cmd; done < <(ls)` | `for f in *; do cmd "$f"; done` |                               |
| Counting Lines   | `wc -l file`                  | `awk 'END{print NR}' file`      |                               |

---

## 6. Resources & References

* **Perf Wiki:** [https://perf.wiki.kernel.org](https://perf.wiki.kernel.org)
* **ShellCheck:** [https://www.shellcheck.net](https://www.shellcheck.net)
* **Valgrind:** [http://valgrind.org](http://valgrind.org)

---

## 7. Extensibility

* Add new benchmarks in `benchmarks/` folder with naming convention `bench_*.sh`.
* Use `optimize-tools.toml` to configure custom metrics and thresholds.

---

## 8. Glossary

* **O(n):** Linear time.
* **Cache Miss:** CPU stall due to absent cache line.
* **Heap Profiling:** Tracking memory allocations.

---

*End of optimize-v2.md*
