#!/bin/sh
DIR=$(dirname "$0")
cd $DIR

# If .python-version specifies invalid version, use system
python -V || export PYENV_VERSION=system

# find and download most recent github release/tag

python3 src/cosmic.py
exit 0
