CC=gcc

CFLAGS=-O3 -fPIC

TARGET_DIR=build

CORE_SRC=src/core/4ndr0_core.c

CORE_LIB=$(TARGET_DIR)/lib4ndr0_core.so

CORE_BIN=$(TARGET_DIR)/4ndr0_engine

all: clean directory lib bin

directory:

mkdir -p $(TARGET_DIR)

lib:

$(CC) $(CFLAGS) -shared $(CORE_SRC) -o $(CORE_LIB)

bin:

$(CC) $(CFLAGS) $(CORE_SRC) -o $(CORE_BIN)

clean:

rm -rf $(TARGET_DIR)
