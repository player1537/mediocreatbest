#!/usr/bin/env bash
# vim :set ts=4 sw=4 sts=4 et:
die() { printf $'Error: %s\n' "$*" >&2; exit 1; }
root=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
self=${BASH_SOURCE[0]:?}
project=${root##*/}
pexec() { >&2 printf exec; >&2 printf ' %q' "$@"; >&2 printf '\n'; exec "$@"; }
prun() { >&2 printf run; >&2 printf ' %q' "$@"; >&2 printf '\n'; "$@"; }
go() { "go-$@"; }
next() { "${FUNCNAME[1]:?}-$@"; }
#---

environment_dir=${root:?}/venv

go-New-Environment() {
    pexec python3 -m venv \
        "${environment_dir:?}" \
    ##
}

go-Initialize-Environment() {
    pexec "${environment_dir:?}/bin/pip" install \
        --editable "${root:?}" \
        build \
        twine \
    ##
}

go-Invoke-Environment() {
    source "${environment_dir:?}/bin/activate" \
    && \
    pexec "$@" \
    ##
}

go-Build-Distribution() {
    pexec "${environment_dir:?}/bin/python" -m build \
        --sdist \
        --wheel \
        --outdir "${root:?}/dist" \
    ##
}

go-Deploy-TestDistribution() {
    pexec "${environment_dir:?}/bin/twine" upload \
        --repository testpypi \
        --repository-url https://test.pypi.org/legacy/ \
        "${root:?}/dist"/* \
    ##
}

go-Deploy-Distribution() {
    pexec "${environment_dir:?}/bin/twine" upload \
        "${root:?}/dist"/* \
    ##
}

#---
test -f "${root:?}/env.sh" && source "${_:?}"
"go-$@"
