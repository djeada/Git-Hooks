#!/usr/bin/env bash

paths=(src)  # If you wish to check more directories, you may add them to this list.

for path in "${paths[@]}"; do
  for script in $(find "$path" -type f -name "[^_]*.sh"); do
      eval ""$script" "$path""
      echo -e "\nExecuting "$script""
    done
done

