#!/bin/bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

export BEERTISTICS_CONFIG=test

python -m unittest discover -v beertistics

while inotifywait -r -e modify ./beertistics; do
    python -m unittest discover -v beertistics
done
