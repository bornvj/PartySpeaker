CC = gcc
LDFLAGS =
CFLAGS = -O0 -g -fsanitize=address

SRC_FILES = server/server.c
BIN_FILE = server.bin

all: server.bin

$(BIN_FILE): $(SRC_FILES)
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm -f $(BIN_FILE) ./soundQueue/*

.PHONY: clean
