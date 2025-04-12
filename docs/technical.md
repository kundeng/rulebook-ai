# Technical Specifications Document

## Target Platforms:
Cursor, CLINE, RooCode, Windsurf.

## Rule File Formats:
- `.mdc` (Cursor)
- `.clinerules` (CLINE/RooCode)
- `@.clinerules-{mode}` (RooCode)
- `@clinerules/` directory content (CLINE - via manual copy)
- `.windsurfrules` (Windsurf - TBD)

## Memory File Formats:
- `.md` (Core Docs)
- `.mdc` (Error/Lessons Learned)
- `.tex` (Optional Context - Literature/RFCs)

## Known Technical Issues:
1.  **Inconsistent Documentation:** The `README.md` had inconsistencies regarding CLINE/RooCode rule loading (now partially addressed).
2.  **CLINE Manual Rule Loading:** CLINE requires manual copy-pasting of mode-specific rules into settings due to lack of native support.
3.  **CLINE UI Bug:** A known UI bug in Cline can cause custom instructions pasted for one mode (e.g., Plan) to overwrite the instructions for another mode (e.g., Act), making the manual copy-paste workaround unreliable.
4.  **RooCode `.cursor/rules` Incompatibility:** The `README.md` states RooCode cannot read the `.cursor/rules` directory (needs investigation - Task 6).
