#!/bin/sh

export LOG_FILE=$HOME/mctech-crd.log
export NEW_RELEASE=/tmp/cosmic-release

export GH_REPO=MC-Technology/mctech-crd

DIR=$(dirname "$0")
cd $DIR

if [ -f "/boot/DEBUG.txt" ]; then
    echo "launcher.sh ran" >> $LOG_FILE
fi

# If .python-version specifies invalid version, use system
python -V || export PYENV_VERSION=system

# find and download most recent github release/tag
# TODO: check if already most recent
# TODO: move update process to another script
gh release download -A tar.gz -D $NEW_RELEASE && \
tar -xvzf $NEW_RELEASE/mctech-crd-*.tar.gz -C $NEW_RELEASE && \
rm -rf $HOME/mctech-crd/*
mv $NEW_RELEASE/mctech-crd*/* $HOME/mctech-crd && \
rm $NEW_RELEASE/*.tar.gz

cosmic listen
# python3 src/cosmic.py

exit 0