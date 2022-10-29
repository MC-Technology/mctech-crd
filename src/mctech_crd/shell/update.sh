#!/bin/bash

export LOG_FILE=$HOME/mctech-crd.log
export NEW_RELEASE=/tmp/cosmic-release

export GH_REPO=MC-Technology/mctech-crd
export CREDENTIALS_DIR=/boot/mct_credentials
export GH_CREDENTIALS=$CREDENTIALS_DIR/gh_token.sh

# export COSMIC_DEV_PACKAGE_URL=git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git

export COSMIC_PYTHON_VERSION=3.11.0
export COSMIC_VIRTUALENV=cosmic-3.11
if [[ $OSTYPE == "darwin"* ]]; then
    # homebrew pyenv versions seem to be behind
    export COSMIC_PYTHON_VERSION=3.11.0rc2
    export COSMIC_VIRTUALENV=cosmic-3.11
fi
echo "COSMIC_PYTHON_VERSION=$COSMIC_PYTHON_VERSION"
echo "COSMIC_VIRTUALENV=$COSMIC_VIRTUALENV"

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
        pip install --upgrade $COSMIC_DEV_PACKAGE_URL
    fi
}

download_install_latest_release(){
    # find and download most recent github release/tag
    if [[ -z "$COSMIC_DEV_PACKAGE_URL" ]]; then
        rm -rf ~/tmp/cosmic-latest-release/*;
        gh release download -A tar.gz -D ~/tmp/cosmic-latest-release
        tar -xzf ~/tmp/cosmic-latest-release/mctech-crd*.tar.gz -C ~/tmp/cosmic-latest-release
        rm ~/tmp/cosmic-latest-release/*.tar.gz
        # rename for simplicity
        # mv ~/tmp/cosmic-latest-release/mctech-crd-* ~/tmp/cosmic-latest-release/mctech-crd
        pip install --upgrade ~/tmp/cosmic-latest-release/mctech-crd*
    else
        echo "Downloading development version mctech-crd"
        pip install --force-reinstall $COSMIC_DEV_PACKAGE_URL
    fi
}

init_python_environment
init_credentials
download_install_latest_release
