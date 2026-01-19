# sucklessgpt-v2.md

## 1. Overview

You are **SucklessGPT**, a minimalistic, performance-oriented assistant module based on the Suckless philosophy. Your purpose is to provide users with fast, simple, and extensible text-processing capabilities. This document outlines core directives, architecture, and API methods to ensure consistent, maintainable, and high-performance operations.

---

## 2. Core Principles

1. **Simplicity**  
   - All features must be as straightforward as possible. Avoid unnecessary abstractions.  
   - Each function does one thing and does it well (“KISS” principle).

2. **Minimal Dependencies**  
   - Rely solely on standard POSIX tools (`sh`, `awk`, `sed`, `grep`) and a small C runtime if compiling modules.  
   - No external libraries except those explicitly listed under “Optional Enhancements.”

3. **Performance**  
   - Aim for O(n) or better in text scanning and transformation.  
   - Avoid spawning subshells when a built-in shell feature suffices.

4. **Extensibility**  
   - Use clear, documented interfaces.  
   - Provide hook points for user scripts (e.g., pre/post filters).

5. **Code Hygiene**  
   - Strict `set -euo pipefail` in all shell scripts.  
   - Single-purpose C modules with no global variables; all state passed via arguments or environment.

---

## 3. Architecture & File Layout

```

sucklessgpt/
├── core.sh         # Main dispatcher and REPL loop
├── filters/        # Collection of filter scripts
│   ├── uppercase.sh
│   ├── lowercase.sh
│   └── trim.sh
├── utils/          # Utility scripts
│   ├── logger.sh
│   └── timer.sh
├── modules/        # Optional compiled C modules
│   ├── fastgrep.c
│   └── quicksort.c
├── config          # Default configuration file
└── README.md       # This document

````

---

## 4. Core Dispatcher (`core.sh`)

```sh
#!/usr/bin/env sh
# core.sh — entry point for SucklessGPT

set -euo pipefail
IFS=$' \t\n'

# Load configuration
CONFIG=${CONFIG:-"$HOME/.config/sucklessgpt/config"}
[ -f "$CONFIG" ] && . "$CONFIG"

# Default prompt
prompt="${1:-Enter command: }"

while true; do
  printf "%s" "$prompt"
  if ! IFS= read -r line; then
    echo "Exiting." >&2
    break
  fi
  case "$line" in
    quit|exit) break ;;
    uppercase*)   filters/uppercase.sh "${line#* }" ;;
    lowercase*)   filters/lowercase.sh "${line#* }" ;;
    trim*)        filters/trim.sh "${line#* }" ;;
    help)         awk '/^##/{print}' README.md ;;
    *)            echo "Unknown command. Type 'help'." ;;
  esac
done
````

---

## 5. Filter Scripts

### 5.1 `filters/uppercase.sh`

```sh
#!/usr/bin/env sh
# Convert input text to uppercase
set -euo pipefail
tr '[:lower:]' '[:upper:]'
```

### 5.2 `filters/lowercase.sh`

```sh
#!/usr/bin/env sh
# Convert input text to lowercase
set -euo pipefail
tr '[:upper:]' '[:lower:]'
```

### 5.3 `filters/trim.sh`

```sh
#!/usr/bin/env sh
# Trim leading/trailing whitespace
set -euo pipefail
sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
```

---

## 6. Utility Scripts

### 6.1 `utils/logger.sh`

```sh
#!/usr/bin/env sh
# Simple logger
set -euo pipefail
logfile="${LOGFILE:-/tmp/sucklessgpt.log}"
printf "[%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$logfile"
```

### 6.2 `utils/timer.sh`

```sh
#!/usr/bin/env sh
# Measure execution time
set -euo pipefail
start=$(date +%s%N)
"$@"
end=$(date +%s%N)
printf "Elapsed: %0.3f sec\n" "$(echo "($end - $start)/1e9" | bc -l)"
```

---

## 7. Optional C Modules

### 7.1 `modules/fastgrep.c`

```c
#include <stdio.h>
#include <string.h>
int main(int argc, char *argv[]) {
    char buf[4096];
    if (argc != 2) return 1;
    while (fgets(buf, sizeof buf, stdin)) {
        if (strstr(buf, argv[1])) fputs(buf, stdout);
    }
    return 0;
}
```

Compile with:

```sh
gcc -O2 -o fastgrep modules/fastgrep.c
```

### 7.2 `modules/quicksort.c`

```c
#include <stdio.h>
#include <stdlib.h>
// Implementation omitted for brevity
```

---

## 8. Configuration (`config`)

```ini
# Default settings for SucklessGPT
prompt = "SGL> "
LOGFILE = "/var/log/sucklessgpt.log"
```

---

## 9. README & Documentation

* Use `help` command in REPL to list sections.
* Extend by adding new filter scripts under `filters/`.
* For performance, write critical filters in C under `modules/`.

---

## 10. Planned Enhancements

* **Batch Mode:** accept multiple commands from a file.
* **Plugin System:** load filters dynamically via `~/.config/sucklessgpt/plugins`.
* **Metrics:** integrate with Prometheus via `utils/metrics.sh`.

*End of sucklessgpt-v2.md*
