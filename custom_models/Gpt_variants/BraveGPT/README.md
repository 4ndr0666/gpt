# BraveGPT Package

BraveGPT is a canonical, production-grade reference for Brave Browser flags with Arch Linux–centric workflows.

## Components
- **INIT_PROMPT.md** — Final initialization prompt referencing the unified starters file.
- **bravegpt-starters.json** — Unified conversation starters (dual-schema for backward compatibility).
- **ui-buttons-primary.json** — Hardcoded 5-button init set for Custom GPT UI.
- **quick-start_menu.md** — Human-friendly quick-start menu board.
- **brave_flags_refference.md** — Canonical flags reference (preserved as uploaded).
- **schemas/** — JSON schema for starters.
- **scripts/** — Validation, rendering, and idempotent flag management.

## Workflow (Idempotent)
1. Validate starters: `scripts/validate_starters.sh`
2. Render menu from starters (optional): `scripts/render_menu.sh > quick-start_menu.md`
3. Use `INIT_PROMPT.md` inside your Custom GPT.
4. Manage Arch flags with `scripts/ensure_flag.sh` (safe to re-run).

## Backward Compatibility
- Unified file keeps both legacy (`title`+`prompt`) and new (`name`+`description`+`prompt`) keys.
- Primary buttons also exposed in dedicated `ui-buttons-primary.json`.
