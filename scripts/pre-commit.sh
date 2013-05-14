#!/bin/bash
#
# Script intended for running as git pre-commit hook.
# Setup hook using
# 
#   ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit
# 
# from the projects root directory

# Only verify staged code
git stash -q --keep-index

cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../.."

# Remove all .pyc files in project
find beertistics | grep ".pyc$" | xargs rm

# Run tests
export BEERTISTICS_CONFIG=test
python -m unittest discover --failfast -s beertistics/tests/ -p '*.py'
CODE=$?

if [[ $CODE -ne 0 ]]; then
    echo -e "\n\033[31mAborting commit: there are failing tests\033[0m"
fi

# Put back un-staged code
git stash pop -q

# exit with status code from tests
exit $CODE