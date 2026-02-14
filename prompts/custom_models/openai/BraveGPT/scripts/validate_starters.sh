#!/usr/bin/env bash
# Validate bravegpt-starters.json against minimal constraints using jq.
# ShellCheck clean
set -euo pipefail
IFS=$'\n\t'

JSON="${1:-bravegpt-starters.json}"
jq -e '.' "$JSON" >/dev/null

# Require array exists and non-empty
jq -e '.conversation_starters | arrays and (length > 0)' "$JSON" >/dev/null

# Each item must have .prompt and at least one of .name or .title
jq -e '
  .conversation_starters[]
  | (.prompt | type=="string" and (length>=8))
  and ((has("name") and (.name|type=="string")) or (has("title") and (.title|type=="string")))
' "$JSON" >/dev/null

# Check uniqueness of prompts
PROMPT_COUNT="$(jq -r '.conversation_starters[].prompt' "$JSON" | wc -l | tr -d ' ')"
PROMPT_UNIQ="$(jq -r '.conversation_starters[].prompt' "$JSON" | sort -u | wc -l | tr -d ' ')"
if [ "$PROMPT_COUNT" -ne "$PROMPT_UNIQ" ]; then
  echo "Duplicate prompts detected in $JSON" >&2
  exit 1
fi

echo "OK: $JSON is valid."
