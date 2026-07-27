#!/bin/sh

# Fail fast on errors or unbound variables
set -eu

SOURCE_ARCHIVE="Anthropic-Cybersecurity-Skills-1.3.0.zip"
PREFIX="anthropic-bulk"
ORIG_DIR="$(pwd)"
MAX_FILES=850 

# ==========================================
# IDEMPOTENCY: Clean slate for any previous runs
# ==========================================
rm -f "${PREFIX}-part"*.skill
WORKSPACE="$(mktemp -d)"
trap 'rm -rf "$WORKSPACE"' EXIT

# ==========================================
# PREPARATION & FILTERING
# ==========================================
unzip -q "$SOURCE_ARCHIVE" -d "$WORKSPACE/source"

# PURGE RESTRICTED FILES: Remove all .ps1 files immediately
find "$WORKSPACE/source" -type f -name "*.ps1" -exec rm -f {} +

ROOT_DIR=$(find "$WORKSPACE/source" -type d -name "skills" | head -n 1 | sed 's|/skills$||')
mkdir -p "$WORKSPACE/template"

# 1. Copy the base configuration files, ignoring any existing root SKILL.md
for item in "$ROOT_DIR/"*; do
    [ -e "$item" ] || continue
    if [ "${item##*/}" != "skills" ] && [ "${item##*/}" != "SKILL.md" ]; then
        cp -r "$item" "$WORKSPACE/template/"
    fi
done

BASE_COUNT=$(find "$WORKSPACE/template" | wc -l)

# ==========================================
# REUSABLE FUNCTION: Initialize a compliant chunk
# ==========================================
init_part() {
    part_num="$1"
    mkdir -p "$WORKSPACE/Part${part_num}/skills"
    
    # Copy base files
    if [ "$(ls -A "$WORKSPACE/template")" ]; then
        cp -r "$WORKSPACE/template/"* "$WORKSPACE/Part${part_num}/"
    fi
    
    # Inject the mandatory YAML frontmatter exactly as specified
    cat <<EOF > "$WORKSPACE/Part${part_num}/SKILL.md"
---
name: ${PREFIX}-part-${part_num}
description: A chunked subset of the Anthropic Cybersecurity Skills library containing structured agent workflows.
domain: cybersecurity
subdomain: security-operations
tags: [cybersecurity, ai-agents, chunked-archive, agentskills]
version: "1.3.0"
author: mukul975
license: Apache-2.0
---

# Anthropic Cybersecurity Skills - Part ${part_num}

This bulk package contains a chunked subset of the master repository to accommodate file limits. 
It follows the agentskills.io standard.
EOF
}

# ==========================================
# DYNAMIC CHUNKING (Under 1000 files)
# ==========================================
current_part=1
current_count=$BASE_COUNT
init_part "$current_part"

for skill_dir in "$ROOT_DIR/skills/"*; do
    [ -e "$skill_dir" ] || continue
    
    skill_count=$(find "$skill_dir" | wc -l)
    
    if [ $((current_count + skill_count)) -ge "$MAX_FILES" ]; then
        current_part=$((current_part + 1))
        current_count=$BASE_COUNT
        init_part "$current_part"
    fi
    
    cp -r "$skill_dir" "$WORKSPACE/Part${current_part}/skills/"
    current_count=$((current_count + skill_count))
done

# ==========================================
# BUILD ARCHIVES (Root-aligned)
# ==========================================
i=1
while [ "$i" -le "$current_part" ]; do
    (
        cd "$WORKSPACE/Part$i"
        zip -r9q "$ORIG_DIR/${PREFIX}-part-${i}.skill" .
    )
    i=$((i + 1))
done

echo "Success! Packages built. All .ps1 files have been safely removed."
ls -lh "${PREFIX}-part-"*.skill
