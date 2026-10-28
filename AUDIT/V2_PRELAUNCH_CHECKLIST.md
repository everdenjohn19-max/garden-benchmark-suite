# V2 Prelaunch Review and Execution Checklist

**Status:** Draft review; V2 has not been run or scored.  
**Branch:** `audit/v1-repair-spec`  
**Purpose:** Keep the repaired test, independent rubric, and run protocol auditable before collecting results.

## Changes made during prelaunch review

- Corrected C2.4 so it does not teach the inaccurate simplification that condensation alone makes rain heavy.
- Clarified C3.5: pure gold is not ferromagnetic like iron; it is weakly diamagnetic.
- Aligned C4.5's retention probe with the exact three constraints used in C4.1–C4.4.
- Reframed H1.2, H1.3, H1.5, and H1.8 to test epistemic boundaries without presupposing that an unfamiliar title, citation, or theorem does not exist.
- Split R2.2 into `R2.2_SETUP` and `R2.2_PROBE`, so identity consistency is evaluated across two turns in the same conversation.
- Added explicit session boundaries: questions within a category are sequential in one conversation; each category/repetition starts fresh.
- Clarified that paired model comparisons should target at least five independent paired runs per model/version/condition. Fewer runs must be reported as exploratory pilot data.

## Run protocol

1. Freeze the exact V2 test file and scoring rubric commit before running any model.
2. For each model/version, run both `STANDARD` and `GARDEN` under matched sampling settings, tool access, system context, and context window wherever technically possible. Record unavoidable differences.
3. Randomize which condition runs first. Keep a separate fresh conversation for every category and repetition, while preserving turns within the category.
4. Target at least five independent paired repetitions per model/version. Do not count questions in the same conversation as independent runs.
5. Save complete raw responses without edits. Record model/version, condition, settings, tool access, timestamps, test and rubric versions, prompt-sequence hash, and raw-file hash.
6. Before scoring, declare whether only the primary answer field or any specified supplementary fields can receive substantive credit. Report primary-field completion and eligible-field completion separately.
7. Score with the same rubric in both conditions. Blind scorers to condition where feasible; double-score subjective items and record adjudications.
8. Report per-item and per-dimension scores, denominators, blanks, missing runs, and unscorable rates. Do not publish a composite unless its weights and missing-data rules were preregistered.

## Checks before treating V2 as canonical

- [ ] Independently review all answer keys and evaluation notes, especially C2.4, C3.5, C4.5, R4 transformations, A1.9 logic, and R6 scheduling.
- [ ] Validate the test and rubric as strict JSON in CI.
- [ ] Validate unique item IDs and verify every multi-turn dependency is represented in the run protocol.
- [ ] Add a machine-readable run manifest and response schema before collecting results.
- [ ] Confirm model/version identifiers and exact Garden/Standard configuration are recorded.
- [ ] Predeclare which fields count as eligible answers and how tool use will be logged.
- [ ] Do not merge or relabel the draft as an official V2 until review is complete.

## Important limits

V1 results are a small, mixed-model observational pilot, not evidence of a causal Garden effect. The revised V2 can improve scorable coverage and fairness, but it cannot establish a general intelligence advantage from one run, a handful of models, or easy near-ceiling items. Calibration requires multiple predictions evaluated against outcomes; a confidence percentage on one item is not a calibration score.

**Execution status:** Not run. This repository edit prepares the protocol and test draft; it does not execute external model APIs or produce new model outputs.
