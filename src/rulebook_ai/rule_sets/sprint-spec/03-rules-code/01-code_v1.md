---
trigger: always_on
---

# AI Assistant - Sprint Execution Workflow (SPRINT PHASE = EXECUTION)
# Applies when sprint phase is EXECUTION: implementing stories, writing code within sprint goals, completing sprint tasks
# Assumes General Sprint Principles processed AND sprint planning is complete with defined stories and acceptance criteria.

**(Rules for executing sprint stories and maintaining sprint velocity follow)**

**Overall Goal:** Execute sprint stories according to the sprint plan, maintain sprint velocity and quality standards, track progress against sprint goals, and ensure all work aligns with sprint commitments and acceptance criteria.

## Process & Best Practices:

1.  **Sprint Story Context & Acceptance Criteria:**
    *   **Mandatory Sprint Context Review:** Consult `active_context.md` for current sprint status, `sprint_plan.md` for story details and acceptance criteria, and `sprint_history.md` for velocity patterns and similar story examples.
    *   Confirm understanding of the current sprint story, its acceptance criteria, and how it fits within the overall sprint goal.
    *   Identify the story's dependencies and any blockers from previous sprint work.
    *   Reference story estimation and time constraints to maintain sprint velocity.

2.  **Execute Sprint Stories Incrementally & Track Progress:**
    *   For each story or sub-task within the current sprint:
        *   **a. Pre-Change Analysis (Safety & Context Check):**
            *   Identify the specific files/components targeted by *this step* (referencing plan and `architecture.md`).
            *   **Mandatory Memory Consult:** Perform focused validation against relevant Memory Bank sections *before writing code for this step*:
                *   Cross-reference planned change against `architecture.md` (boundaries, dependencies).
                *   Verify against `technical.md` (patterns, allowed libraries/tech).
                *   Check `active_context.md` for recent related changes/conflicts.
            *   **Explicitly confirm adherence** to these documents or **HALT execution** if a significant discrepancy is found that wasn't approved in the plan. Report the conflict and suggest Debug/Re-plan.
            *   Perform focused Dependency/Flow Analysis for immediate impacts.
            *   *If analysis reveals unforeseen major impact conflicting with plan, **HALT execution**, report, recommend **Debug Mode** or plan revision.*
        *   **b. Implement Planned Change (Context-Aware):**
            *   Write or modify code precisely as specified in the plan *for this step*.
            *   Apply *all* General and Project-Specific Standards, explicitly referencing guidance from `technical.md` (style, patterns, security) and respecting boundaries from `architecture.md`.
            *   Prioritize reuse, code preservation, integration (`architecture.md`), modularity.
        *   **c. Pre-Commit Simulation / Mental Check:**
            *   Mentally trace execution for the *specific change* just made.
            *   Analyze impacts on expected behavior and potential edge cases related to *this change*.
            *   *If simulation reveals unexpected side effects or breaks related logic, **HALT execution**, revert problematic part, initiate **Debug Mode**.*
        *   **d. Post-Implementation Memory Check (Brief):**
            *   After implementing a logical block within the step, briefly re-verify that the code adheres to the constraints checked in Step 2a (`architecture.md`, `technical.md`). Note any accidental deviations for immediate correction or Debug Mode.
        *   **e. Iterate:** Continue implementing sub-parts of the current plan step, repeating a-d as needed.

3.  **Develop Comprehensive Tests (Post-Implementation per Step/Feature):**
    *   Based on the plan's testing strategy and implemented code:
        *   **Test Plan Adherence:** Implement tests covering scenarios from plan (edge cases, validations).
        *   **Dependency-Based Tests:** Write unit tests for new/modified code, covering interactions with immediate dependencies (informed by `architecture.md`).
        *   **Separate Test Files:** Follow project conventions.
        *   **No Breakage Goal:** Run relevant existing tests + new tests. *If any test fails, **HALT execution** and initiate **Debug Mode**.*

4.  **Document Code as Planned:**
    *   Add code comments and documentation (docstrings, etc.) as specified in the plan and per General standards/`technical.md`. Focus on 'why' and link to task IDs/decisions.

5.  **Handle Plan Deviations/Completion & Propose Memory Updates:**
    *   If execution was halted (plan conflict, failed simulation, failed tests) report final status *after* Debug Mode attempt concludes.
    *   If *all* steps completed and tests pass:
        *   Report successful completion of the task implementation.
        *   **Propose Specific Memory Updates:** Based on the work done, propose concise updates for:
            *   `tasks_plan.md` (Mark task complete, note outcomes/results).
            *   `active_context.md` (Reflect new state, remove task from 'in progress').
            *   `lessons-learned.md` (If significant new pattern/insight emerged).
            *   `error-documentation.md` (If the task fixed a non-trivial bug).
            *   (Rarely) `architecture.md` or `technical.md` if implementation revealed necessary minor clarifications (major changes require re-planning).

6.  **(Optional) Final Optimization:** Perform safe optimizations *after* verification, if planned.

**(End of Implementation Workflow - Enhanced)**