#!/usr/bin/env bash

main() {

    find . -regex '.*\.\(cpp\|hpp\|cu\|c\|h\)' -exec clang-format -style=file -i {} \;
    clang-tidy -checks=* -fix '.*\.\(cpp\|hpp\|cu\|c\|h\)' -- -std=c++14

}

main "$@"

