#!/bin/sh

git fetch

UPSTREAM="origin/master"
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse $UPSTREAM)
BASE=$(git merge-base @ $UPSTREAM)

if [ $LOCAL = $REMOTE ]; then
    echo Up-to-date
    exit 0
elif [ $LOCAL = $BASE ]; then
    echo Need to pull
    git pull origin master && exit 0
elif [ $REMOTE = $BASE ]; then
    echo Need to push
    echo Necessário verificar as modificações feitas localmente
    exit 1
else
    echo Git Repo Diverged
    echo Provavel Conflito
    exit 1
fi
