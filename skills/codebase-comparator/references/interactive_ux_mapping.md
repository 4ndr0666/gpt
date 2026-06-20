# Interactive UX Mapping Reference

This document maps the intended graphical user interface states into text-based chat states for the `codebase-comparator` skill.

## 1. Feature Matrix (FeatureMatrix.tsx)
The UI presents features in an accordion list with specific source chips and decision buttons.
* **Visual Source Chips** -> Translated to Matrix Columns: `Unique to A`, `Unique to B`, `Common`.
* **Decision Buttons (Include, Remove, Discuss)** -> Translated to text commands: 
    * `[I]` (Include: Marked for Inclusion)
    * `[R]` (Remove: Marked for Removal)
    * `[D]` (Discuss: Triggers sub-loop explanation)

## 2. Review Output & Actions (ReviewOutput.tsx)
The UI presents the generated code alongside post-review action buttons.
* **Generate Commit** -> Triggered via `[1]`.
* **Show Diff** -> Triggered via `[2]`.
* **Analyze Root Cause** -> Triggered via `[3]`.
* **Debugger / Follow-up** -> Triggered via `[4]`.

**Constraint Check:** The UI strictly disables the "Finalize Revision" button until ALL features have a decision. The LLM must enforce this same constraint conversationally by refusing to output the final script until every feature in the matrix has been assigned `[I]` or `[R]`.
