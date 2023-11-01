#!/usr/bin/env bash

for DIR in */; do
    DIRNAME=$(basename "$DIR")
    echo "==> $DIRNAME <=="
    (cd $DIR && ruff check *.py --ignore E902 --ignore E501)
done

echo "Format complete."