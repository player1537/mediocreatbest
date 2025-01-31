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

go-Build-Package() {
    cd "${root:?}" \
    || die "cd ${root:?}"

    pexec npx vite build \
    ##
}

go-Deploy-Package() {
    cd "${root:?}" \
    || die "cd ${root:?}"

    pexec npm publish \
    ##
}

unset VAINL_API_KEY

go-Test-Package() {
    cd "${root:?}" \
    || die "cd ${root:?}"

    VAINL_API_KEY=${VAINL_API_KEY:?} \
    pexec npm test \
    ##
}

#---
test -f "${root:?}/env.sh" && source "${_:?}"
"go-$@"
