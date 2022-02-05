#!/usr/bin/env bash

main() {

    beautysh **/*.sh
    shellcheck **/*.sh

}

main "$@"
