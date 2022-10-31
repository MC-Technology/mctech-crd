#!/bin/bash

export NEW_RELEASE=/tmp/cosmic-release

export GH_REPO=MC-Technology/mctech-crd

export RELEASE=~/.cosmic/tmp/cosmic-latest-release

# export COSMIC_DEV_PACKAGE_URL=git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git

update_python_environment() {
    # Should pass through if already installed
    pyenv update

    # This should match mctech-crd/.python-version
    pyenv install $COSMIC_PYTHON_VERSION -s
    pyenv virtualenv $COSMIC_PYTHON_VERSION $COSMIC_VIRTUALENV
    PYENV_VERSION=$COSMIC_VIRTUALENV

    # If now invalid version, use system (3.9.2)
    VER=`python -V`
    if [[ -z "${VER}" ]]; then
        PYENV_VERSION=system
    fi

    # When run from shell this will activate pyenv virtualenv
    export PYENV_VERSION=$PYENV_VERSION

    # On boot, this will inform PYENV_VERSION set in bashrc
    # this makes the 'cosmic' command available from the virtual environment
    echo $PYENV_VERSION > $COSMIC_HOME/.python-version
}

download_latest_release() {
    mkdir -p $RELEASE
    rm -rf $RELEASE/*;
    gh release download -A tar.gz -D $RELEASE && \
    tar -xzf $RELEASE/mctech-crd*.tar.gz -C $RELEASE && \
    rm $RELEASE/*.tar.gz && \
    echo $(ls $RELEASE)
}

install_latest_release(){
    # find and download most recent github release/tag
    if [[ -z "$COSMIC_DEV_PACKAGE_URL" ]]; then
        download_latest_release
        pip install --upgrade $RELEASE/mctech-crd*
    else
        echo "Downloading development version mctech-crd"
        pip install --force-reinstall $COSMIC_DEV_PACKAGE_URL
    fi
}

update_python_environment
install_latest_release
