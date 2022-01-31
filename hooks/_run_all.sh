#!/usr/bin/env bash

paths=(src)  # If you wish to check more directories, you may add them to this list.

for path in "${paths[@]}"; do
    for script in $(find hooks -type f -name "[^_]*.sh"); do
      $("$script" "$path")
      echo "Executing "$script""
    done
done
