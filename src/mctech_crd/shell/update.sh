#!/bin/bash

export NEW_RELEASE=/tmp/cosmic-release

export GH_REPO=MC-Technology/mctech-crd

export RELEASE=~/.cosmic/tmp/cosmic-latest-release

# export COSMIC_DEV_PACKAGE_URL=git+https://$GH_TOKEN@github.com/MC-Technology/mctech-crd.git

download_latest_release() {
        mkdir -p $RELEASE
        rm -rf $RELEASE/*;
        gh release download -A tar.gz -D $RELEASE
        tar -xzf $RELEASE/mctech-crd*.tar.gz -C $RELEASE
        rm $RELEASE/*.tar.gz
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

install_latest_release
