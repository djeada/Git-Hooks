#!/usr/bin/env bash

assert_last_line_empty() {
    local file="$1"

    echo "Checking if the last line of ${file} is empty..."

    local last_line
    last_line=$(tail -n 1 "${file}")

    if [ -z "${last_line}" ]; then
        echo "Last line is empty!"
        # remove all empty lines at the end of the file
        # this way we make sure that there is one empty line
        # at the end of the file
        while [[ -z "${last_line}" ]]; do
            tail -n 1 "${file}" > "${file}.tmp"
            mv "${file}.tmp" "${file}"
            last_line=$(tail -n 1 "${file}")
        done
    else
        echo "Last line is not empty!"
    fi

    #append an empty line to the end of the file
    echo >> "${file}"

}

main() {

    if [ $# -eq 0 ]; then
        echo "Must provide a path!"
        exit 1
    elif [ $# -gt 1 ]; then
        echo "Only one path is supported!"
        exit 1
    fi

    if [ "$1" == '.' ] || [ -d "${1}" ]; then
        for file in $(find "$1" -maxdepth 10 -type f)
        do
            assert_last_line_empty "$file"
        done
    elif [ -f "${1}" ]; then
        assert_last_line_empty "$1"
    else
        echo "$1 is not a valid path!"
    fi

}

main "$@"
