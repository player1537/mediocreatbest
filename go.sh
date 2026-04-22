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

go-New-Environment() {
    pexec uv venv --seed \
    ##
}

go-Initialize-Environment() {
    pexec uv pip install \
        -e "${root:?}[dev]" \
        build \
        twine \
    ##
}

go-Test() {
    prun "${self:?}" Test-Py \
    ##
}

go-Test-Me() {
    pexec uv run \
        --with=requests \
        --with=mediocreatbest \
        --with=pytest==6.2.4 \
        -- \
    pytest "${root:?}/test.py" \
    ##
}

go-Test-Py() {
    pexec pytest "${root:?}/test.py" \
    ##
}

go-Build-PyPackage() {
    cd "${root:?}" \
    || die "Failed to change directory to ${root:?}"

    prun rm -rv \
        "${root:?}/dist" \
        "${root:?}/build" \
    ##

    pexec uv run --with=build --with=twine python -m build \
        --sdist \
        --wheel \
        --outdir "${root:?}/dist" \
    ##
}

go-Deploy-TestDistribution() {
    pexec uv run --with=twine twine upload \
        --repository testpypi \
        --repository-url https://test.pypi.org/legacy/ \
        "${root:?}/dist"/* \
    ##
}

go-Deploy-PyPackage() {
    pexec uv run --with=twine twine upload \
        "${root:?}/dist"/* \
    ##
}


#---
test -f "${root:?}/env.sh" && source "${_:?}"
"go-$@"
