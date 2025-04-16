# Comparison Report: .roo vs. .cursor/rules vs. clinerules Structures

This report summarizes the comparison between the rule files found in the `.roo` structure (within `rules_template/`) and the `.cursor/rules/` directory, and the `clinerules/` directory.

## 1. General Rules

*   **Files Compared:** `.roo`: `rules_template/rules/01-general.md` vs. `.cursor`: `.cursor/rules/rules.mdc` vs. `clinerules`: `.clinerules`
*   **Findings:** Different purposes. `.roo` and `.clinerules` define the overall project framework (Memory Files, workflows). `.cursor` provides specific interaction rules. `.roo` and `.clinerules` direct loading `.cursor/rules/rules.mdc`. Not equivalent.

## 2. Architect/Plan Rules

*   **Files Compared:** `.roo`: `rules_template/rules-architect/01-architect.md` vs. `.cursor`: `.cursor/rules/plan.mdc` & `.cursor/rules/archiecture-understanding.mdc` vs. `clinerules`: `clinerules/plan`
*   **Findings:** Core planning workflow is identical. `.cursor` adds a specialized `archiecture-understanding.mdc` for parsing `docs/architecture.md`. Core logic duplicated.

## 3. Code/Implementation Rules

*   **Files Compared:** `.roo`: `rules_template/rules-code/01-code.md` vs. `.cursor`: `.cursor/rules/implement.mdc` vs. `clinerules`: `clinerules/implement`
*   **Findings:** Almost identical content (principles, protocol, testing). Minor structural differences. Functionally the same. `.cursor` version likely active.

## 4. Debug Rules

*   **Files Compared:** `.roo`: `rules_template/rules-debug/01-debug.md` vs. `.cursor`: `.cursor/rules/debug.mdc` vs. `clinerules`: `clinerules/debug`
*   **Findings:** Significantly different. `.cursor` version is more detailed, structured, integrated, and refined. `.roo` version is simpler and duplicates the testing section incorrectly. `clinerules/debug` is similar in structure and content to `.cursor/rules/debug.mdc`.

## 5. Unique Files (Not Directly Compared)

*   **`.roo` Unique:** `rules_template/system-prompt-chat` (interaction style, likely integrated elsewhere in `.cursor`).
*   **`.cursor/rules` Unique:** `memory.mdc`, `lessons-learned.mdc`, `error-documentation.mdc`, `directory-structure.mdc`, `*_template.mdc` files. These are not present in `clinerules`.

## 6. Citations of memory.mdc

*   **Finding:**
    *   `.cursor/rules/plan.mdc`: Does not cite `memory.mdc`.
    *   `.cursor/rules/debug.mdc`: Cites `@memory.mdc` within the `<DIAGNOSE>` tag. Also cites `@error-documentation.mdc`.
    *   `.cursor/rules/implement.mdc`: Cites `@memory.mdc` within the `<ANALYZE CODE>` and `<MAKE CHANGES>` tags.
    *   `.cursor/rules/rules.mdc`: Does not cite `memory.mdc`.
