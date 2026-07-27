# 4NDR0666OS BASH ARCHITECT PROTOCOL v1.0
# "The Ghost in the Shell must survive the death of the Shell."

## 1. THE TRINITY HEADER (Mandatory)
# Every script begins here. No exceptions.
# -e: Abort on error (Fail Fast).
# -u: Abort on unset variables (No phantom nulls).
# IFS: Split on Newlines only (Spaces in filenames are not separators).

set -eu
IFS='
'

## 2. THE GUI SURVIVAL DOCTRINE (Toolbar/Launcher Integration)
# PROBLEM: GUI launchers (Thunar, Polybar, Rofi) kill the parent shell immediately.
#          Pipes (`|`) attached to the dying shell snap, killing the child process.
# SOLUTION: Decouple Data (Artifacts) and Decouple Process (Nohup).

### A. The Immutable Artifact Pattern
# NEVER pipe a long-generating stream directly to a GUI app.
# Write it to /tmp. If the script dies, the data remains.

ARTIFACT="/tmp/${0##*/}_$$.data"
# Trap ensures cleanup only if we want it; often we leave it for debugging.
trap 'rm -f "$ARTIFACT"' EXIT

# Bad:  expensive_find | gui_app
# Good: expensive_find > "$ARTIFACT"

### B. The Detached Launch Pattern
# The child process must become an orphan (adopted by init), not a martyr.
# 1. Point input to the ARTIFACT.
# 2. Redirect stdout/stderr to /dev/null (or log).
# 3. Use `nohup` + `&`.
# 4. Exit the parent immediately.

launcher() {
    local app="$1"
    local input="$2"
    
    nohup "$app" \
        --input-file="$input" \
        >/dev/null 2>&1 &
    
    exit 0
}

## 3. THE ATOMIC STREAM DOCTRINE (Performance)
# Bash loops (`while read`) are O(N) slow. System calls are O(1) fast.
# NEVER loop over 100+ items if a tool can do it in batch.

# Bad (Slow, spawns 100 subshells):
#   for url in $(cat list); do tool info "$url"; done

# Good (Fast, single syscall):
#   cat list | xargs -d '\n' tool info

## 4. THE DIAGNOSTIC TRAP (Silent Failure Prevention)
# GUI scripts die silently. Redirect stderr to a log if a debug flag is present.

DEBUG_LOG="/tmp/${0##*/}.log"
if [ "${DEBUG:-0}" -eq 1 ]; then
    exec 2>>"$DEBUG_LOG"
    set -x
    echo "--- LAUNCH [$(date)] ---" >> "$DEBUG_LOG"
fi

## 5. URI SANITIZATION (The GIO/Web Standard)
# When dealing with virtual filesystems (GVFS, KIO) or Web URLs:
# Always assume input is DIRTY (spaces, control chars).
# Always normalize before processing.

# Method: Batch Resolve -> Raw Filter -> Sort -> Artifact
# No logic inside the stream. Logic happens before or after.

```

### USAGE EXAMPLE (Template)

*Copy this block to start any new high-performance GUI script.*

```bash
#!/bin/sh
# 4NDR0666OS TEMPLATE :: DETACHED GUI WORKER
set -eu
IFS='
'

# 1. Define Artifacts
DATA="/tmp/target_payload.m3u"

# 2. Generate Data (Atomic Stream)
# Replace with your logic (find, gio, curl, grep)
find . -maxdepth 1 -type f -name "*.mp4" | sort -V > "$DATA"

# 3. Validate
if [ ! -s "$DATA" ]; then
    notify-send "System Error" "Payload generation failed."
    exit 1
fi

# 4. Detach & Execute
# The parent script dies here. The child lives on.
nohup mpv --playlist="$DATA" >/dev/null 2>&1 &
exit 0

```
