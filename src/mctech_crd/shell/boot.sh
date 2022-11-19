#!/bin/sh

# if [[ $OSTYPE == "darwin"* ]]; then
#     # homebrew pyenv versions seem to be behind
#     export COSMIC_PYTHON_VERSION=3.11.0rc2
#     export COSMIC_VIRTUALENV=cosmic-3.10
# fi

# Override tokens etc
# for f in $CREDENTIALS_DIR/*.sh; do source $f; done

# export COSMIC_DEV_PACKAGE_URL=git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git

# DIR=$(dirname "$0")
# DIR=$(dirname -- $0)

#cosmic start

# setup shell

export COSMIC_HOME=/home/cosmic
export COSMIC_ROOT=$COSMIC_HOME/.cosmic
export COSMIC_CREDS=$COSMIC_ROOT/credentials
export GH_REPO=MC-Technology/mctech-crd

export PYENV_ROOT="$COSMIC_HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

if [ -d /boot/mct_credentials ]; then
    mv /boot/mct_credentials/* $COSMIC_CREDS 2>/dev/null)
fi
for f in $COSMIC_CREDS/*.sh; do source $f; done

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# setup pyenv
export PYENV_VERSION=$(cat $COSMIC_ROOT/.python-version)

cosmic update # python library
cosmic update --pyenv

pyenv shell $PYENV_VERSION
python -V > /home/cosmic/boot.log
whoami >> /home/cosmic/boot.log

sudo -u cosmic cosmic listen
