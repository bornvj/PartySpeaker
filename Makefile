CC = gcc
LDFLAGS =
CFLAGS = -O0 -g -Wall -Wextra

SRC_FILES = server/server.c
BIN_FILE = server.bin

install: server.bin py_packages

run:
	./run.sh

$(BIN_FILE): $(SRC_FILES)
	$(CC) $(CFLAGS) $^ -o $@

py_packages:
	pip install -r player/requirements.txt --break-system-packages

clean:
	rm -f $(BIN_FILE) ./soundQueue/*

.PHONY: clean
