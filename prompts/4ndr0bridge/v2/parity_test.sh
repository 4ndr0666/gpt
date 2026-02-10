#!/bin/bash
# 4NDR0_LOGIC_BRIDGE Validation Suite
# Verifies bit-parity between Node.js and C implementations.

SEED=3735928559
PAYLOAD="SYSTEM_RESEARCH_V3_INIT"

echo "[INIT] Compiling Core..."
make > /dev/null

echo "[TEST] Executing C-Core..."
C_OUT=$(./build/4ndr0_engine $SEED "$PAYLOAD")

echo "[TEST] Executing Node-Bridge..."
JS_OUT=$(node src/node/bridge.mjs $SEED "$PAYLOAD")

echo "---------------------------------------"
echo "C Output: $C_OUT"
echo "JS Output: $JS_OUT"
echo "---------------------------------------"

if [ "$C_OUT" == "$JS_OUT" ]; then
	echo "[SUCCESS] Bit-Parity Synchronized. The Bridge is stable."
else
	echo "[FAILURE] Logic Divergence Detected. Check seed overflow logic."
	exit 1
fi
