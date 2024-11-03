#!/bin/sh

./server.bin &
python3 ./player/player.py &
