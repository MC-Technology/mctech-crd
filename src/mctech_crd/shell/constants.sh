#!/bin/sh

export LOG_FILE=$HOME/mctech-crd.log
export COSMIC_HOME=~/.cosmic
export RELEASE="$COSMIC_HOME/tmp/cosmic-latest-release"

# export CREDENTIALS_DIR=/boot/mct_credentials
export CREDENTIALS_DIR=$COSMIC_HOME/credentials

export GH_REPO=MC-Technology/mctech-crd

export COSMIC_PYTHON_VERSION=3.11.0
export COSMIC_VIRTUALENV=cosmic-3.11
# export COSMIC_CONFIG=~/.cosmic/config/default.json

if [[ $OSTYPE == "darwin"* ]]; then
    # homebrew pyenv versions seem to be behind
    export COSMIC_PYTHON_VERSION=3.11.0rc2
    export COSMIC_VIRTUALENV=cosmic-3.11
fi

# Override tokens etc
for f in $CREDENTIALS_DIR/*.sh; do source $f; done

# export COSMIC_DEV_PACKAGE_URL=git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git
