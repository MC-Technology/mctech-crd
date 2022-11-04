#!/bin/bash

echo $COSMIC_VIRTUALENV
echo $COSMIC_PYTHON_VERSION

update_python_environment() {

    if [[ -z "$COSMIC_PYTHON_VERSION" ]]; then
        echo "COSMIC_PYTHON_VERSION environment var not set"
        exit 1
    fi

    if [[ -z "$COSMIC_VIRTUALENV" ]]; then
        echo "COSMIC_VIRTUALENV environment var not set"
        exit 1
    fi

    # Should pass through if already installed
    pyenv update

    # This should match mctech-crd/.python-version
    echo "pyenv install -s $COSMIC_PYTHON_VERSION"
    pyenv install -s $COSMIC_PYTHON_VERSION || echo "Could not install python version" && exit 1

    echo "pyenv virtualenv $COSMIC_PYTHON_VERSION $COSMIC_VIRTUALENV"
    pyenv virtualenv $COSMIC_PYTHON_VERSION $COSMIC_VIRTUALENV

    echo "PYENV_VERSION=$COSMIC_VIRTUALENV"
    PYENV_VERSION=$COSMIC_VIRTUALENV

    # If now invalid version, use system (3.9.2)
    VER=`python -V`
    if [[ -z "${VER}" ]]; then
        PYENV_VERSION=system
    fi

    export PYENV_VERSION=$PYENV_VERSION
}

update_python_environment