#!/bin/sh

echo `gh api "/repos/$GH_REPO/releases/latest"`
