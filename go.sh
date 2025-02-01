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
        -e "${root:?}/py" \
    ##
}

go-Test() {
    prun "${self:?}" Test-Py \
    ##

    pexec "${self:?}" Test-Js \
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
    pexec "${root:?}/py/go.sh" Test \
    ##
}

go-Test-Js() {
    pexec "${root:?}/js/go.sh" Test-Package \
    ##
}

go-Build-PyPackage() {
    pexec "${root:?}/py/go.sh" Build-Distribution \
    ##
}

go-Deploy-PyPackage() {
    pexec "${root:?}/py/go.sh" Deploy-Distribution \
    ##
}

go-Build-JsPackage() {
    pexec "${root:?}/js/go.sh" Build-Package \
    ##
}

go-Deploy-JsPackage() {
    pexec "${root:?}/js/go.sh" Deploy-Package \
    ##
}


#---
test -f "${root:?}/env.sh" && source "${_:?}"
"go-$@"
