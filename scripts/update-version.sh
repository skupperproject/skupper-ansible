#!/bin/bash

export version=""
export old_version="v2-dev"
export image_version="v2-dev"

usage() {
    echo "Updates the skupper.v2 collection to the desired version"
    echo
    echo "Use: $0 version"
    echo
    echo "    version         Target version (required)"
    echo
    [ $# -gt 0 ] && echo ERROR: $*
    exit 1
}

parse_args() {
    [[ $# -ne 1 ]] && usage
    version="${1}"
    [[ ! -f galaxy.yml ]] && usage "galaxy.yml not found (run from project root)"
    old_version=$(grep -E '^version: ' galaxy.yml | sed -E 's/version: (.*)/\1/')
    if [[ "$version" == "$old_version" ]]; then
        echo "Version is already $version, nothing to update"
        exit 0
    fi
    if [[ "$version" != *"-preview" ]]; then
        image_version="${version}"
    fi
}

update_makefile() {
    sed -ri "s/^VERSION :=.*/VERSION := ${version}/" Makefile
}

update_galaxyyml() {
    sed -ri "s/^version: .*/version: ${version}/" galaxy.yml
}

update_cli() {
    grep -rl "quay.io/skupper/cli:${old_version}" plugins/modules/ tests/integration/ tests/unit/plugins/modules/ \
        | xargs -r sed -i "s#quay.io/skupper/cli:${old_version}#quay.io/skupper/cli:${image_version}#g"
}

update_controller() {
    grep -rl "quay.io/skupper/system-controller:${old_version}" plugins/modules/ tests/integration/ tests/unit/plugins/modules/ \
        | xargs -r sed -i "s#quay.io/skupper/system-controller:${old_version}#quay.io/skupper/system-controller:${image_version}#g"
}

main() {
    parse_args $*
    echo Updating version to: $version
    update_makefile
    update_galaxyyml
    update_cli
    update_controller
}

main $*
