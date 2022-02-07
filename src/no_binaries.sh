#!/usr/bin/env bash

check_for_binaries() {
    local path="$1"

    # check if there are binaries in the path and subdirectories
    if [ -n "$(grep -rIL "${path}")" ]; then
        echo "Found binaries in ${path}!"
        exit 1
    fi

}

main() {

    if [ $# -eq 0 ]; then
        echo "Must provide a path!"
        exit 1
    else [ $# -gt 1 ]
        echo "Only one path is supported!"
        exit 1
    fi

    path="$1"
    check_for_binaries "${path}"

    echo "No binaries found in ${path}!"

}

main "$@"

