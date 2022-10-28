#!/bin/sh

export LOG_FILE=$HOME/mctech-crd.log
export NEW_RELEASE=/tmp/cosmic-release

export GH_REPO=MC-Technology/mctech-crd
export CREDENTIALS_DIR=/boot/mct_credentials
export GH_CREDENTIALS=$CREDENTIALS_DIR/gh_token.sh

# export COSMIC_DEV_PACKAGE_URL=git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git

if [[ $OSTYPE == "darwin"* ]]; then
    # homebrew pyenv versions seem to be behind
    export COSMIC_PYTHON_VERSION=3.11.0rc2
    export COSMIC_VIRTUALENV=cosmic-3.11
else
    export COSMIC_PYTHON_VERSION=3.11.0
    export COSMIC_VIRTUALENV=cosmic-3.11
fi