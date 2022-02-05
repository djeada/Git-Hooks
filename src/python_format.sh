#!/usr/bin/env bash

main() {

    black **/*.py
    autopep8 **/*.py

}

main "$@"
