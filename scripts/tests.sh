#!/bin/bash

# Script for running the test suite once, and then re-run once every 
# time a file is changed within the `beertistics` folder.

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

function run_tests() {
    python -m unittest discover -v -s beertistics/tests/ -p '*.py'
}

export BEERTISTICS_CONFIG=test

run_tests

while inotifywait -r -e modify ./beertistics; do
    run_tests
done
