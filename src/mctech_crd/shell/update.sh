#!/bin/sh

export LOG_FILE=$HOME/mctech-crd.log
export NEW_RELEASE=/tmp/cosmic-release

export GH_REPO=MC-Technology/mctech-crd
export CREDENTIALS_DIR=/boot/mct_credentials
export GH_CREDENTIALS=$CREDENTIALS_DIR/gh_token.sh


if [[ $OSTYPE == "darwin"* ]]; then
    # homebrew pyenv versions seem to be behind
    export COSMIC_PYTHON_VERSION=3.11.0rc2
    export COSMIC_VIRTUALENV=cosmic-3.11
else
    export COSMIC_PYTHON_VERSION=3.11.0
    export COSMIC_VIRTUALENV=cosmic-3.11
fi

DIR=$(dirname "$0")
cd $DIR

# Should pass through if already installed
# This should match mctech-crd/.python-version
init_python_environment() {
    pyenv update
    pyenv install $COSMIC_PYTHON_VERSION -s
    # TODO: more accurate validation of venv
    pyenv virtualenv $COSMIC_PYTHON_VERSION $COSMIC_VIRTUALENV || echo "$COSMIC_VIRTUALENV virtual environment already exists"
    export PYENV_VERSION=$COSMIC_VIRTUALENV

    # If .python-version specifies invalid version, use system (3.9.2)
    python -V || export PYENV_VERSION=system
}

init_credentials() {
    if [ -f $GH_CREDENTIALS ]; then
        source $GH_CREDENTIALS
    else
        echo "No credentials file found"
    fi
}

update_crd_python_package() {
    if [[ -z "${GH_TOKEN}" ]]; then
        echo "Could not update cosmic client package (mctech-crd) - GH_TOKEN not available"
    else
        pip install --upgrade git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git
    fi
}

# download_release(){
    ## find and download most recent github release/tag
    ## TODO: check if already most recent
    ## TODO: move update process to another script
    # gh release download -A tar.gz -D $NEW_RELEASE && \
    # tar -xvzf $NEW_RELEASE/mctech-crd-*.tar.gz -C $NEW_RELEASE && \
    # rm -rf $HOME/mctech-crd/*
    # mv $NEW_RELEASE/mctech-crd*/* $HOME/mctech-crd && \
    # rm $NEW_RELEASE/*.tar.gz
    ## start listener
    # python3 src/cosmic.py
# }

if [ -f "/boot/DEBUG.txt" ]; then
    echo "launcher.sh ran" >> $LOG_FILE
fi

init_python_environment
init_credentials

pip install --upgrade mctech-crd

exit 0