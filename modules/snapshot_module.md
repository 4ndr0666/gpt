# Snapshot Refactoring v3.0

**1. Initial Verification (Snapshot 1: The Anchor)**

* **Mandatory Feature-to-Function Matrix**: Map every function, its exact task, and its source.
* **Hard Count**: State the **Total Function Sum** and **Exact Line Count** in the header.
* **Drift-Source Identification**: Flag utility functions (fetchers/normalizers) as "UNTOUCHABLE CORE."
* **Variable Registry**: List every global and locally critical variable (e.g., `progressFill`, `imageUrls`) that must survive the refactor.

**2. Operational Hardening (Structural Constraint)**

* **Regression Penalty**: Any solution proposing the merging of two or more functions from Snapshot 1 is automatically disqualified unless the user provides an "Optimization Waiver."
* **Plug-in Architecture**: Enhancement logic (e.g., Hydra-Kill) must be inserted as distinct code blocks within existing function bodies. Rewriting the function's signature or core loop structure is a **Violation of Integrity**.
* **Contextual Lock-in**: Before any segment is parsed, the model must re-read the variable registry to ensure no specific identifier (like `logsContainer`) is renamed or omitted.

**3. Literal Integrity Protocol (The !P Mandate)**

* **Verbatim Emission**: No elisions (`...`), no placeholders (`// logic here`), and no summaries. Every line must be parsed literally.
* **Segmented Checksum**: Each 100-line segment must conclude with a count of functions and a list of variables contained within that block.
* **Orphan Audit**: A mandatory "Pre-Finalization Scan" to locate functions present in Snapshot 1 but absent in Snapshot 2.

**4. Validation & Persistence (Snapshot 2)**

* **Parity Comparison**: A direct, row-by-row comparison of Function Sums.
* **Name Integrity Check**: Confirm the primary extension name (**GDV-saver**) is the only one used. References to internal vessel IDs (e.g., 4ndr0666os) are permitted only in diagnostic logs, not UI headers.
* **Delta Justification**: Any mismatch in line counts must be explained by specific line numbers added for enhancements.
