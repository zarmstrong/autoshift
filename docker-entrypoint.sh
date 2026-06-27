#!/bin/sh
set -eu

if [ -n "${SHIFT_REDEEM:-}" ]; then
    # Preserve SHIFT_ARGS word splitting while ensuring Python becomes PID 1.
    # shellcheck disable=SC2086
    set -- ${SHIFT_ARGS:-}
    exec python ./autoshift/auto.py --user "${SHIFT_USER:-}" --pass "${SHIFT_PASS:-}" --redeem "${SHIFT_REDEEM}" "$@"
fi

# shellcheck disable=SC2086
set -- ${SHIFT_ARGS:-}
exec python ./autoshift/auto.py --user "${SHIFT_USER:-}" --pass "${SHIFT_PASS:-}" --games "${SHIFT_GAMES}" --platforms "${SHIFT_PLATFORMS}" "$@"