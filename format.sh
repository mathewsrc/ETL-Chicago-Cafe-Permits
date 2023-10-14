#!/usr/bin/env bash

for DIR in */; do
    DIRNAME=$(basename "$DIR")
    echo "==> $DIRNAME <=="
    (cd $DIR && black *.py)
done

echo "Format complete."