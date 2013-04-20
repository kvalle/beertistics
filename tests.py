#!/bin/bash

export BEERTISTICS_CONFIG=test

while inotifywait -r -e modify ./beertistics; do
    python -m unittest discover -v beertistics
done
