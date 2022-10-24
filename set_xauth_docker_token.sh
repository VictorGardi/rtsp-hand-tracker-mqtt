#!/bin/bash
DISPLAY_NUMBER=$(echo $DISPLAY | cut -d. -f1 | cut -d: -f2)

# Extract auth cookie
AUTH_COOKIE=$(xauth list | grep "^$(hostname)/unix:${DISPLAY_NUMBER} " | awk '{print $3}')
if [[ ! $AUTH_COOKIE ]]; then
    AUTH_COOKIE=$(xauth list | grep "^$(hostname)/unix: " | awk '{print $3}')
fi
if [[ ! $AUTH_COOKIE ]]; then
    printf '%s\n' "It seems like the current device doesn't have a display! Debug mode is not possible." >&2
    exit 1
fi
# Add the xauth cookie to xauth
export XAUTH_DOCKER_TOKEN="$(hostname)/unix:${DISPLAY_NUMBER} MIT-MAGIC-COOKIE-1 ${AUTH_COOKIE}"
info="XAUTH_DOCKER_TOKEN is set to: "
info+=${XAUTH_DOCKER_TOKEN}
echo ${info}
