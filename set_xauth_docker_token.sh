#!/bin/bash
DISPLAY_NUMBER=$(echo $DISPLAY | cut -d. -f1 | cut -d: -f2)

# Extract auth cookie
#AUTH_COOKIE=$(xauth list | grep "^$(hostname)/unix:${DISPLAY_NUMBER} " | awk '{print $3}')
AUTH_COOKIE=$(xauth list | grep "^$(hostname)/unix: " | awk '{print $3}')
# Add the xauth cookie to xauth
export XAUTH_DOCKER_TOKEN="$(hostname)/unix:${DISPLAY_NUMBER} MIT-MAGIC-COOKIE-1 ${AUTH_COOKIE}"
echo $XAUTH_DOCKER_TOKEN
