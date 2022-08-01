#!/usr/bin/env bash

format() {
    autopep8 --in-place --aggressive "$1"
    autoflake --in-place --remove-unused-variables --remove-all-unused-imports --expand-star-imports "$1"
    isort "$1"
    black "$1"
}

main() {


    if [ $# -eq 0 ]; then
        echo "Must provide a path!"
        exit 1
    fi

    if [ "$1" == '.' ] || [ -d "${1}" ]; then
        for file in $(find "$1" -maxdepth 10 -type f -name "*.py")
        do
            format "$file"
        done
    elif [ -f "${1}" ]; then
        format "$1"
    else
        echo "$1 is not a valid path!"
    fi


}

main "$@"
