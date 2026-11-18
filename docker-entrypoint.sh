#!/bin/sh
# Word-split SHIFT_ARGS, SHIFT_REDEEM, SHIFT_GAMES and SHIFT_PLATFORMS while
# ensuring Python becomes PID 1. Pathname expansion is disabled (-f) so the
# unquoted expansions only split on whitespace and never match files.
# shellcheck disable=SC2086
set -euf

set -- ${SHIFT_ARGS:-}

if [ -n "${SHIFT_REDEEM:-}" ]; then
    exec python ./autoshift/auto.py --user "${SHIFT_USER:-}" --pass "${SHIFT_PASS:-}" --redeem ${SHIFT_REDEEM} "$@"
fi

exec python ./autoshift/auto.py --user "${SHIFT_USER:-}" --pass "${SHIFT_PASS:-}" --games ${SHIFT_GAMES} --platforms ${SHIFT_PLATFORMS} "$@"
