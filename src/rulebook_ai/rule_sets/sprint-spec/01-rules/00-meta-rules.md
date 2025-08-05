---
trigger: always_on
---

# Meta-Rules for AI Assistant Interaction (Sprint-Based Development)

You will receive a sequence of approximately 10 rule files that enforce a sprint-based development methodology. Process them in order as they provide context and instructions for our interaction.

**File Sequence Purpose Overview:**
*   **This File (0th):** Explains the sprint-based system, how to interpret the subsequent files, and how to determine your operational focus within sprint cycles.
*   **Files 1 through 4 (approx.):** Project Memory Bank with Sprint Context (Requirements, Architecture, Technical Details, Sprint History, etc.). Consult as directed or needed. Note `alwaysApply` flags. **These files provide essential sprint context.**
*   **File 5 (approx.):** Project Directory Structure with Sprint Organization.
*   **File 6 (approx.):** General Sprint Principles and Best Practices (**ALWAYS FOLLOW**).
*   **Files 7 through 9 (approx.):** Sprint-specific operational workflows:
    *   **File 7 (approx.):** Rules for **SPRINT PHASE = PLANNING** (sprint planning, backlog refinement, story breakdown).
    *   **File 8 (approx.):** Rules for **SPRINT PHASE = EXECUTION** (implementation within sprint goals).
    *   **File 9 (approx.):** Rules for **SPRINT PHASE = RETROSPECTIVE** (sprint review, debugging, lessons learned).

**Determining Your Sprint Phase and Applicable Rules:**

Apply the MOST relevant sprint workflow rule set (from files approx. 7, 8, or 9) IN ADDITION to the general sprint rules (file approx. 6). **Crucially, initial consultation of sprint context from Memory Bank files is required before executing within a chosen SPRINT PHASE.** Use the following hierarchy to determine SPRINT PHASE:

1.  **Explicit Sprint Command:** Check IF the user's LATEST request contains an explicit instruction like `SPRINT PHASE = PLANNING`, `SPRINT PHASE = EXECUTION`, or `SPRINT PHASE = RETROSPECTIVE`.
    *   IF YES: Prioritize applying the workflow rules associated with that specified SPRINT PHASE (File 7, 8, or 9). This command OVERRIDES other factors for this turn.

2.  **Infer Sprint Activity (Primary Method after Explicit Command):** IF no explicit command (Step 1) applies, analyze the user's CURRENT request to determine the primary sprint activity:
    *   Is it about sprint planning, backlog refinement, story breakdown, goal setting, capacity planning? -> Determine **SPRINT PHASE = PLANNING** (Use rules from file approx. 7).
    *   Is it about implementing stories, writing code within sprint goals, completing sprint tasks, making progress on committed work? -> Determine **SPRINT PHASE = EXECUTION** (Use rules from file approx. 8).
    *   Is it about sprint review, retrospective analysis, examining completed work, identifying lessons learned, fixing blockers? -> Determine **SPRINT PHASE = RETROSPECTIVE** (Use rules from file approx. 9).
    *   IF unsure about the sprint context based on the request, ASK the user for clarification on the required SPRINT PHASE (Planning, Execution, or Retrospective).

3.  **Assistant's Internal State (Context / Cross-Check - If Applicable):** IF you are an assistant with persistent internal modes (e.g., 'Act', 'Debug', 'Architect'):
    *   **Cross-check:** Does your current internal mode *conflict* with the SPRINT PHASE determined in Step 2?
        *   **Example Conflict:** You are in 'Debug Mode', but Step 2 determined `SPRINT PHASE = PLANNING` based on the user's request ("Let's plan the next sprint").
        *   **Example Ambiguity:** You are in 'Act Mode' (which covers both Execution and Retrospective), and Step 2 determined `SPRINT PHASE = EXECUTION`. This is consistent.
    *   **Action on Conflict:** If your internal mode *clearly conflicts* with the SPRINT PHASE determined from the user's current request (Step 2), NOTIFY the user: "My current internal mode is [Your Mode Name]. However, your request seems to be for [SPRINT PHASE determined in Step 2]. I will proceed with SPRINT PHASE = [SPRINT PHASE determined in Step 2] based on your request. Is this correct, or should I remain focused on tasks related to [Your Mode Name]?" *Prioritize the SPRINT PHASE derived from the current request (Step 2) after notifying.*
    *   **Action on Ambiguity:** If your internal mode covers multiple SPRINT PHASES, rely primarily on the SPRINT PHASE determined in Step 2 from the *specific request*. Your internal mode serves as broader context but doesn't dictate the rules file if the request is clearly about one specific SPRINT PHASE.

**Applying Sprint Rules:**
*   Always apply the rules from file approx. 6 (General Sprint Principles). **Ensure required Sprint Memory Bank consultations outlined in File 6 happen first.**
*   Apply the *one* most relevant specific sprint workflow rule set (from files approx. 7, 8, or 9) determined primarily by Step 1 or Step 2 logic.
*   Consult sprint memory bank files (approx. 1-4) **actively and as specified** within the applicable general and workflow rule files, or when directed by the user. Sprint context is essential for maintaining velocity and continuity.
*   **Sprint Continuity:** Always consider current sprint goals, progress, and constraints when making decisions or recommendations.

**(End of Meta-Rules - Sprint-Based Development)**