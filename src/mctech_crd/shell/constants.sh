#!/bin/sh

export LOG_FILE=$HOME/mctech-crd.log
export RELEASE="~/.cosmic/tmp/cosmic-latest-release"
export CREDENTIALS_DIR=/boot/mct_credentials

export GH_REPO=MC-Technology/mctech-crd

export COSMIC_PYTHON_VERSION=3.11.0
export COSMIC_VIRTUALENV=cosmic-3.11

if [[ $OSTYPE == "darwin"* ]]; then
    # homebrew pyenv versions seem to be behind
    export COSMIC_PYTHON_VERSION=3.11.0rc2
    export COSMIC_VIRTUALENV=cosmic-3.11
fi

# export COSMIC_DEV_PACKAGE_URL=git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git
