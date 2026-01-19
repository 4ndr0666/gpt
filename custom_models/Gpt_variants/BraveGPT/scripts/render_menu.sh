#!/usr/bin/env bash
# Render quick-start_menu.md from bravegpt-starters.json (full) or ui-buttons-primary.json (primary).
# Usage:
#   scripts/render_menu.sh                # full set
#   scripts/render_menu.sh primary        # primary 5 from ui-buttons-primary.json
# ShellCheck clean
set -euo pipefail
IFS=$'\n\t'

MODE="${1:-full}"
STARTERS_JSON="bravegpt-starters.json"
PRIMARY_JSON="ui-buttons-primary.json"

echo "# ⚡ BraveGPT Quick-Start Menu"
echo
echo "| Category | Starter Prompt |"
echo "|---|---|"

if [ "$MODE" = "primary" ]; then
  jq -r '.conversation_starters[] | [.name, .prompt] | @tsv' "$PRIMARY_JSON" |
    while IFS=$'\t' read -r name prompt; do
      echo "| ${name} | “${prompt}” |"
    done
else
  jq -r '
    .conversation_starters[]
    | [ (if has("name") then .name else .title end), .prompt ]
    | @tsv
  ' "$STARTERS_JSON" | while IFS=$'\t' read -r label prompt; do
      echo "| ${label} | “${prompt}” |"
    done
fi
