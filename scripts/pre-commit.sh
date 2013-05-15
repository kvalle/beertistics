#!/bin/bash
#
# Script intended for running as git pre-commit hook.
# Setup hook using
# 
#   ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit
# 
# from the projects root directory

function fail {
    echo -e "\033[31m->" $1 "\033[0m"
}

function info {
    echo -e "\033[32m-->" $1 "\033[0m"
}

# Only verify staged code
git stash -q --keep-index

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../.."


# Remove all .pyc files in project
info "removing .pyc files"
find beertistics | grep ".pyc$" | xargs rm

# Run tests
info "running tests"
export BEERTISTICS_CONFIG=test
python -m unittest discover --failfast -s beertistics/tests/ -p '*.py'
CODE=$?

if [[ $CODE -ne 0 ]] 
then
    fail "aborting commit: there are failing tests"
else
    # Run flake8 to check for code problems
    info "checking for code smells"
    flake8 beertistics
fi

# Put back un-staged code
git stash pop -q

# exit with status code from tests
exit $CODE