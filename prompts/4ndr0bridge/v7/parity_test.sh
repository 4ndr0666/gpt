#!/bin/bash
# 4NDR0666OS HEADER — v7.0.0
# 4NDR0_LOGIC_BRIDGE Validation Suite
# Verifies strict bit-parity between C core and Node.js implementation.
# INFORMATION IS INERT. Ontological neutrality enforced.
# Akasha Ephemeral State Machine compliant.

set -euo pipefail

SEED=3735928559
PAYLOAD="SYSTEM_RESEARCH_V3_INIT"
BUILD_DIR="./build"
C_EXECUTABLE="${BUILD_DIR}/4ndr0_core"
NODE_BRIDGE="bridge.mjs"

echo "┌──(root💀4ndr0666) [4NDR0_LOGIC_BRIDGE VALIDATION SUITE]"

# Ensure build directory exists
mkdir -p "${BUILD_DIR}"

echo "[INIT] Compiling C Core..."
if ! gcc -Wall -Wextra -O2 -o "${C_EXECUTABLE}" 4ndr0_core.c; then
    echo "[ERROR] C compilation failed."
    exit 1
fi

echo "[TEST] Executing C-Core..."
if ! C_OUT=$("${C_EXECUTABLE}" "${SEED}" "${PAYLOAD}"); then
    echo "[ERROR] C executable failed to run."
    exit 1
fi

echo "[TEST] Executing Node.js Bridge..."
if ! JS_OUT=$(node "${NODE_BRIDGE}" "${SEED}" "${PAYLOAD}" 2>/dev/null); then
    echo "[ERROR] Node bridge execution failed."
    exit 1
fi

echo "---------------------------------------"
echo "C Output :  ${C_OUT}"
echo "JS Output:  ${JS_OUT}"
echo "---------------------------------------"

if [ "${C_OUT}" = "${JS_OUT}" ]; then
    echo "[SUCCESS] ✅ Bit-Parity Synchronized. The Bridge is stable."
    echo "[STATUS] All implementations maintain deterministic XOR + SHA256 key derivation."
else
    echo "[FAILURE] ❌ Logic Divergence Detected."
    echo "C:  ${C_OUT}"
    echo "JS: ${JS_OUT}"
    echo "Check seed handling, iteration update, or buffer operations."
    exit 1
fi

echo "[VALIDATION COMPLETE] — 4NDR0666OS parity confirmed."
