---
trigger: always_on
---

# AI Assistant - Sprint Planning Workflow (SPRINT PHASE = PLANNING)
# Applies when sprint phase is PLANNING: sprint planning, backlog refinement, story breakdown, capacity planning
# Assumes General Sprint Principles processed, including initial Sprint Memory Bank consultation.

**(Rules for Sprint Planning, Story Analysis, and Sprint Goal Design follow)**

**Overall Goal:** To thoroughly understand sprint requirements within the context of project goals, break down work into manageable sprint stories, estimate effort and capacity, and produce a detailed, validated sprint plan that aligns with team velocity and project objectives.

## Process & Best Practices:

1.  **Sprint Context Analysis & Goal Setting:**
    *   **(Mandatory First Step - Sprint Context Integration)**
        *   **Mandatory Sprint Memory Consult:** Explicitly consult `product_requirement_docs.md` (for alignment with overall product goals), `sprint_plan.md` (for current sprint status, velocity history, and capacity), and `sprint_history.md` (for historical patterns and lessons). **Reference key findings** from these documents.
        *   Analyze current sprint capacity, team velocity, and any existing sprint commitments or constraints.
        *   Clarify sprint goals and how proposed work aligns with product roadmap and release objectives.
        *   Re-state complex sprint requirements to confirm understanding and scope.
    *   **Sprint Scope Definition:** Define clear sprint boundaries, identify dependencies, and establish acceptance criteria that can be validated within the sprint timeframe.
    *   **Goal:** Achieve 100% clarity on sprint objectives, team capacity, and work scope. If uncertainty remains about sprint feasibility, explicitly state what information is needed.

2.  **Story Breakdown & Sprint Planning:**
    *   **(Leverage Sprint Historical Context)**
    *   **Mandatory Memory Consult:** Explicitly consult `architecture.md` (for technical boundaries and component dependencies) and `technical.md` (for development patterns, technical debt, and tooling constraints) **before** creating sprint stories.
    *   **Epic to Story Breakdown:** Decompose larger features into sprint-sized stories that can be completed within 1-3 days, respecting architectural boundaries and technical constraints.
    *   **Story Estimation:** Use historical velocity data from `sprint_history.md` to estimate story points or time requirements. Consider team capacity and any known blockers.
    *   **Dependency Mapping:** Identify and document dependencies between stories and external factors that could impact sprint completion.
    *   **Risk Assessment:** Evaluate sprint risks based on historical patterns from `lessons-learned.md` and plan mitigation strategies.

3.  **Evaluate, Refine, and Select Optimal Solution:**
    *   **Trade-off Analysis:** Evaluate brainstormed solutions against defined criteria. Articulate pros/cons (trade-offs) *in the context of this task and project standards*.
    *   **Rigorous Reasoning & Validation:** Question assumptions. Support claims with evidence from Memory Bank or general principles. **Explicitly verify** how solutions align (or conflict) with `architecture.md`, `technical.md`, and `product_requirement_docs.md`.
    *   **Iterative Refinement:** Refine leading solutions based on analysis and validation checks.
    *   **Justify Optimality:** Select the optimal solution *for this task*. Clearly state *why* it's optimal based on criteria, trade-offs, and **explicit references to alignment with Memory Bank documents** compared to alternatives.

4.  **Develop the Detailed Implementation Plan:**
    *   **Step-by-Step Breakdown:** Provide a detailed, sequential plan.
    *   **Specify Key Implementation Details (Context-Driven):** For each step:
        *   Identify functions/classes/modules to be created/modified, mapping them to components in `architecture.md`.
        *   Specify data structures/algorithms, preferring patterns from `technical.md` or existing codebase.
        *   Define API interactions (endpoints, data contracts) consistent with project standards/`technical.md`.
        *   Detail database schema changes (if any).
        *   Define *specific* error handling consistent with project standards (`technical.md`).
        *   Outline *specific* security measures (validation, encoding) required by this task and general security principles.
        *   Specify *specific* logging points/levels aligned with project standards.
    *   **Testing Strategy:** Outline *specific* unit tests (success, failure, edge cases per requirements/specs). Mention integration points affected (referencing `architecture.md`). Ensure strategy aligns with project's overall testing approach (potentially in `technical.md` or separate testing docs).
    *   **Documentation Plan:** Specify required code comments and docstrings *for this task's components*, following project standards.
    *   **Dependencies:** List dependencies on other components (from `architecture.md`), libraries (`technical.md`), or tasks (`tasks_plan.md`).
    *   **Explicit Assumptions:** List assumptions made *during planning*.

5.  **Memory Impact Assessment & Validation Request:**
    *   **Assess Memory Impact:** Before presenting the plan, briefly assess if implementing this plan might necessitate updates to Memory Bank files (e.g., `architecture.md` if structure changes, `technical.md` if new pattern/library introduced, `tasks_plan.md` for new dependencies). **Note potential updates needed.**
    *   **Present Plan for Validation:** Structure the plan clearly. Include justification for the chosen solution.
    *   **(Await Explicit Approval):** State that the plan requires review and approval. **Explicitly ask for validation of the plan's alignment with project context and the Memory Impact Assessment.**

**(End of Planning Workflow - Enhanced)**