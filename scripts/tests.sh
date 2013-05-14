#!/bin/bash

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

function run_tests() {
    python -m unittest discover -v -s beertistics/tests/ -p '*.py'
}

export BEERTISTICS_CONFIG=test

run_tests

while inotifywait -r -e modify ./beertistics; do
    run_tests
done
