#!/bin/bash

DIR=$(dirname "$0")

# Set required environment variables
source $DIR/constants

init_python_environment() {
    export PYENV_VERSION=$PYENV_VERSION
}

init_python_environment
