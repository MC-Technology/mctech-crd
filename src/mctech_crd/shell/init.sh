#!/bin/bash

DIR=$(dirname "$0")
source $DIR/constants

init_python_environment() {
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

    # When run as a shell script this will activate pyenv virtualenv
    export PYENV_VERSION=$PYENV_VERSION
}

init_python_environment
