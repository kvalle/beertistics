#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
"$DIR/../elasticsearch-0.90.0/bin/elasticsearch" -f
