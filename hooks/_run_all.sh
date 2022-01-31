#!/usr/bin/env bash

paths=(src)
for path in "${paths[@]}"; do
    for script in $(find hooks -type f -name "[^_]*.sh"); do
        $script $path
done

