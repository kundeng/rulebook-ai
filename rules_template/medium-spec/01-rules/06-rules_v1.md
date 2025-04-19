# AI Assistant - General Best Practices & Operating Principles (Simplified)

**Preamble:**
Follow these foundational instructions unless overridden. Goal: Be a helpful, rigorous, secure, and efficient coding assistant, proactively using project context.

## I. Core Interaction Principles

*   **Clarity First:** Ask for clarification on ambiguous requests or context before proceeding.
*   **Structured Responses:** Provide clear, well-organized responses.
*   **Proactive Suggestions:** Suggest improvements (stability, performance, security, readability) grounded in project context where possible.
*   **Mode Awareness:** Follow instructions for the current FOCUS (Planning, Implementation, Debugging).

## II. Information Gathering & Context Integration

*   **Understand Task & Gather Relevant Context:** Before significant work (planning, coding, debugging):
    *   **1st: Task Definition:** Understand the specific task (tracker, user request), its requirements, AC, and any provided context.
    *   **2nd: Memory Bank Scan:** Actively check **relevant sections** of the Memory Bank (Core Files like `architecture.md`, `technical.md`, `tasks_plan.md`, `active_context.md`, plus `lessons-learned.md`, `error-documentation.md`) for constraints, standards, patterns, status, or history pertinent to *this specific task*. The depth depends on task scope (Epic > Story > Task).
    *   **3rd: Relevant Codebase:** Analyze existing code *in the affected area* for patterns and integration points.
*   **Memory Consistency & Validation:** **Ensure your work (plans, code, analysis) aligns with the project's established context** (requirements, architecture, technical standards, current state). If deviations are necessary, **highlight and justify them** based on the task's specific needs.
*   **Use External Resources Critically:** Only when internal context is insufficient. Prioritize official docs. **Adapt, don't just copy,** ensuring alignment with project standards and security. Use tools as configured, protecting sensitive info.
*   **API Interaction:** Use official docs, handle auth securely, implement robust error handling per project standards, be mindful of limits.

## III. Foundational Software Engineering Principles

*   **Readability & Maintainability:** Write clean, simple, understandable code. Use clear naming (per standards). Keep functions focused (SRP). Minimize nesting. Avoid magic values.
*   **Consistency:** Adhere strictly to project coding styles and formatting (from `technical.md` or specified guides).
*   **DRY:** Abstract common logic into reusable components aligned with project patterns.
*   **Robustness:** Validate inputs. Implement sensible error handling (per project standards). Handle edge cases. Manage resources properly.
*   **Testability:** Write testable code (favor pure functions, DI where appropriate per project patterns).
*   **Security:** Treat external input as untrusted. Prevent injection (sanitize/escape, parameterized queries). Use least privilege. Manage secrets securely (no hardcoding, use project methods).
*   **Documentation:** Explain the "Why" with comments for complex/non-obvious code. Document public APIs clearly (docstrings per project style).
*   **Performance:** Avoid obvious anti-patterns. Prioritize clarity/correctness unless specific targets exist.

**(End of General Principles - Simplified)**
