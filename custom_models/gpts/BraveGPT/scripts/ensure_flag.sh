#!/usr/bin/env bash
# Idempotently add one or more Brave flags to ~/.config/brave-flags.conf
# Usage: scripts/ensure_flag.sh --incognito "--rewards=staging=true"
# ShellCheck clean
set -euo pipefail
IFS=$'\n\t'

CONF="${XDG_CONFIG_HOME:-$HOME/.config}/brave-flags.conf"
mkdir -p "$(dirname "$CONF")"
touch "$CONF"

for FLAG in "$@"; do
  grep -qxF "$FLAG" "$CONF" || echo "$FLAG" >> "$CONF"
done

echo "Flags ensured in $CONF"
