#!/bin/bash

SEED=3735928559

PAYLOAD="SYSTEM_RESEARCH_V3"

echo "[TEST] Running C-Core..."

C_OUT=$(./build/4ndr0_engine $SEED "$PAYLOAD")

echo "[TEST] Running Node-Bridge..."

JS_OUT=$(node src/node/bridge.mjs $SEED "$PAYLOAD")

echo "C Output: $C_OUT"

echo "JS Output: $JS_OUT"

if [ "$C_OUT" == "$JS_OUT" ]; then

echo "[SUCCESS] Parity Synchronized."

else

echo "[FAILURE] Logic Divergence Detected."

exit 1

fi
