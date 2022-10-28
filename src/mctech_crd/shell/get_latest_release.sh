#!/bin/bash

export GH_REPO=MC-Technology/mctech-crd
echo `gh api "/repos/$GH_REPO/releases/latest"`
