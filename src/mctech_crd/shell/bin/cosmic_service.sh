#!/bin/bash

# Runs on boot via systemd

echo "Cosmic service started at ${DATE}" | systemd-cat -p info

export PYENV_ROOT="/home/cosmic/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PYENV_VERSION=$(cat /home/cosmic/.cosmic/.python-version)
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
sudo -s source $(cosmic boot) # -s to use shell
