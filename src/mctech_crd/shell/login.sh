#!/bin/sh

# export CREDENTIALS_DIR=$COSMIC_HOME/credentials
# # export CREDENTIALS_DIR=/boot/mct_credentials

# export COSMIC_PYTHON_VERSION=3.11.0
# export COSMIC_VIRTUALENV=cosmic-3.10

# export RELEASE="$COSMIC_HOME/tmp/cosmic-latest-release"

# # export COSMIC_CONFIG=~/.cosmic/config/default.json

# if [[ $OSTYPE == "darwin"* ]]; then
#     # homebrew pyenv versions seem to be behind
#     export COSMIC_PYTHON_VERSION=3.11.0rc2
#     export COSMIC_VIRTUALENV=cosmic-3.10
# fi

# # export COSMIC_DEV_PACKAGE_URL=git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git

# # DIR=$(dirname "$0")
# DIR=$(dirname -- $0)


# cosmic

LOG_FILE=bashrc.log

export COSMIC_HOME=~/cosmic
export COSMIC_ROOT=$COSMIC_HOME/.cosmic
export COSMIC_CREDS=$COSMIC_ROOT/credentials
export GH_REPO=MC-Technology/mctech-crd

export PYENV_ROOT="$COSMIC_HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

# add pyenv to path
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# activate pyenv venv
export PYENV_VERSION=$(cat $COSMIC_ROOT/.python-version)

python -V > $COSMIC_ROOT/log/bashrc.log
pyenv version >> $COSMIC_ROOT/log/bashrc.log
whoami >> $COSMIC_ROOT/log/bashrc.log
cosmic version >> $COSMIC_ROOT/log/bashrc.log

# end cosmic

echo "boot" && cat rc.log && echo "bash" && cat bash.log
