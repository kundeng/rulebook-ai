---
trigger: always_on
---

# AI Assistant - Sprint Retrospective & Problem Resolution (SPRINT PHASE = RETROSPECTIVE)
# Applies when sprint phase is RETROSPECTIVE: sprint review, examining completed work, identifying lessons learned, resolving blockers
# Assumes General Sprint Principles processed and sprint execution is complete or needs review.

**(Rules for sprint retrospective analysis, continuous improvement, and sprint problem resolution follow)**

**Overall Goal:** Conduct thorough sprint retrospective analysis, identify improvement opportunities, resolve sprint blockers, extract lessons learned, and prepare insights for future sprint planning and execution.

## Process & Best Practices:

1.  **Sprint Review & Analysis:**
    *   **Gather Sprint Performance Data:** Collect sprint metrics including completed vs planned stories, velocity achieved, blockers encountered, and quality measures.
    *   **Mandatory Sprint Memory Consult:** Analyze sprint context from:
        *   `sprint_plan.md` (Original sprint goals, commitments, and planned stories).
        *   `active_context.md` (Current sprint status, decisions made, and blockers encountered).
        *   `sprint_history.md` (Historical sprint patterns and velocity trends).
        *   `error-documentation.md` (Sprint-related issues and technical problems).
    *   Reproduce the failure consistently (if possible). Request steps if needed.

2.  **Analyze & Understand (Context-Aware):**
    *   Perform detailed Error Analysis (stack traces, messages, code sections). Use tools if applicable.
    *   **Mandatory Memory Consult:** Conduct focused Dependency/Flow analysis around the failure point, interpreting findings **in the context of `architecture.md`** (component interactions, boundaries) and relevant code patterns from **`technical.md`** or the codebase.
    *   Understand *exactly* why the failure is occurring at a code level, considering potential violations of architectural or technical constraints.

3.  **Hypothesize & Reason:**
    *   Formulate potential root causes (logic error, incorrect assumption, interaction issue, architectural mismatch, environmental issue, violation of `technical.md` standards).
    *   Rigorously reason through evidence (logs, code, test results, Memory Bank context) to confirm/deny hypotheses.
    *   Look for similar patterns solved previously (`error-documentation.md`, `lessons-learned.md`, codebase, web search per general guidelines).

4.  **Identify Root Cause & Plan Fix (Validation):**
    *   Pinpoint the specific root cause with high confidence.
    *   Briefly outline the minimal necessary change to correct the issue.
    *   **Validate Fix Plan:** Ensure the proposed fix itself is consistent with `architecture.md` and `technical.md`. Consider side effects.
    *   **Flag Doc Issues:** If the root cause suggests a flaw or ambiguity in requirements, `architecture.md`, or `technical.md`, **explicitly note this** as needing attention.

5.  **Implement & Verify Fix:**
    *   Apply the fix. **Follow core implementation principles where applicable** (apply standards from `technical.md`, respect `architecture.md`, simulate mentally).
    *   Rerun the specific test(s) that initially failed.
    *   Run directly related tests to check for regressions.
    *   Add a new test specifically for the bug fixed, if appropriate.

6.  **Handle Persistence / Getting Stuck:**
    *   If debugging fails after reasonable attempts:
        *   Try a different diagnostic approach.
        *   Explicitly state the difficulty, approaches tried, why they failed, referencing analysis against Memory Bank context.
        *   Request human assistance or suggest stepping back. Do not loop indefinitely.

7.  **Report Outcome & Propose Memory Updates:**
    *   Report clearly: Was the issue diagnosed, fixed, and verified?
    *   If debugging failed, report findings, last state, reason for being stuck.
    *   Provide corrected code and new tests (if successful).
    *   **Propose Specific Memory Updates:**
        *   **Mandatory:** `error-documentation.md` (Document the problem, root cause, and solution/fix).
        *   `tasks_plan.md` / `active_context.md` (Update status of the affected task).
        *   `lessons-learned.md` (If the fix revealed a broader pattern or important learning).
        *   Potentially flag need for updates to `architecture.md` or `technical.md` if a root cause was traced back to them.
    *   Indicate completion of Debug Mode.

**(End of Debugging Workflow - Enhanced)**