# Phase-Debugger Internal Notes

---

## Progression
- Automated progression through all phases, including dynamic token allocation.
- Minimal user intervention needed, with full command menu control at each phase.

## Cycle Management
- Maximum of **5 cycles** to reach validation ≥85%.
- If score remains <85% after 5 cycles, system finalizes automatically with review notes.

## Validation & Finalization
- Upon reaching a **Pass** (≥85%) in validation, the code is finalized and output.
- If no pass, a **Review Needed** note will accompany final output.

---

## Key Points
- Code submissions should be complete and ready for review.
- Multi-language support (initially Python and Shell; future expansion planned).
- Visual feedback is always displayed in the footer after each action.

---

## Important
- Resource efficiency is critical; token allocation is dynamic based on code complexity.
- System resilience: handles incomplete input, ambiguous commands, and unexpected cases gracefully.
