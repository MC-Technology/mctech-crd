# export GH_REPO=MC-Technology/mctech-crd
# export GH_TOKEN=123abc

RELEASE_DIR=$COSMIC_ROOT/tmp/cosmic-latest-release

download_latest_release() {
    mkdir -p $RELEASE_DIR
    rm -rf $RELEASE_DIR/*;
    gh release download -A tar.gz -D $RELEASE_DIR && \
    tar -xzf $RELEASE_DIR/mctech-crd*.tar.gz -C $RELEASE_DIR && \
    rm $RELEASE_DIR/*.tar.gz && \
    echo $(ls $RELEASE_DIR)
}

install_latest_release(){
    # install most recent github release/tag
    if [[ -z "$COSMIC_DEV_PACKAGE_URL" ]]; then
        download_latest_release
        LATEST_RELEASE=$(ls $RELEASE_DIR | tail -1)
        pip install --upgrade $RELEASE_DIR/$LATEST_RELEASE
    else
        echo "Downloading development version mctech-crd"
        pip install --force-reinstall $COSMIC_DEV_PACKAGE_URL
    fi
    echo $(cosmic env --target) > $COSMIC_ROOT/.python-version
}

install_latest_release