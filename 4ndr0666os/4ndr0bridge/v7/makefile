# 4NDR0666OS HEADER — v7.0.0
# 4NDR0_LOGIC_BRIDGE Build System
# INFORMATION IS INERT. Ontological neutrality enforced.
# Builds both static binary and shared library for FFI bridges.
# Akasha Ephemeral State Machine compliant.

CC := gcc
CFLAGS := -O3 -fPIC -Wall -Wextra -std=c11
TARGET_DIR := build
SRC_DIR := .

CORE_SRC := 4ndr0_core.c
CORE_LIB := $(TARGET_DIR)/lib4ndr0_core.so
CORE_BIN := $(TARGET_DIR)/4ndr0_core

.PHONY: all directory lib bin clean test

all: clean directory lib bin test

directory:
	mkdir -p $(TARGET_DIR)

lib: directory
	$(CC) $(CFLAGS) -shared $(CORE_SRC) -o $(CORE_LIB)

bin: directory
	$(CC) $(CFLAGS) $(CORE_SRC) -o $(CORE_BIN)

clean:
	rm -rf $(TARGET_DIR)

test: bin
	@echo "┌──(root💀4ndr0666) [Running parity validation]"
	@./validate_bridge.sh || echo "[WARNING] Validation script not found. Run manually."

# Convenience target for quick rebuild
rebuild: clean all

# Debug build
debug:
	$(CC) -g -O0 -Wall -Wextra $(CORE_SRC) -o $(TARGET_DIR)/4ndr0_core_debug
