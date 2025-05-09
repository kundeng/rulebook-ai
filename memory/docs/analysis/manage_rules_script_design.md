# Design: `manage_rules.py` - Rule Management Script

**Status:** Proposed

**Related Feature Tasks:** 1.e (Develop Setup Scripts), 1.d (Create Setup Guides), 6.a (Document Customization Points)

## Overview

This document outlines the design for a new Python script, `src/manage_rules.py`, intended to replace the existing `src/copy_rules.py` and `src/clean_rules.py`. This script provides a unified command-line interface for installing, synchronizing, and cleaning AI assistant rule sets within target project repositories.

## Core Concepts

1.  **Source Template Repo:** The central repository (this one) containing master rule templates (e.g., `rules_template/light-spec/`) and the `manage_rules.py` script itself.
2.  **Target Repo:** Any project repository where the rules need to be installed and used (e.g., `~/git/another_project`).
3.  **Target Source of Truth:** A dedicated folder *created inside* the Target Repo during installation (e.g., `project_rules_template/`). This folder holds the specific rule files for that project, copied initially from a template in the Source Template Repo. **This folder should be version controlled within the Target Repo.**
4.  **Target Platform Rules:** The generated, platform-specific rule directories (e.g., `.clinerules/`, `.cursor/rules/`, `.roo/`, `.windsurfrules`) created *inside* the Target Repo by the `sync` command. **These folders should be added to the Target Repo's `.gitignore` file.**

## Features & Advantages

*   **Project-Specific Customization:** Enables each target repository to maintain its own tailored set of rules based on a common starting template.
*   **Decentralized Maintenance:** Developers manage and customize rules directly within their project's context (`Target Source of Truth` folder).
*   **Clear Source of Truth:** Simplifies the workflow by establishing the `Target Source of Truth` folder as the single place to edit rules within the target repo.
*   **Reusability:** The Source Template Repo acts as a factory for bootstrapping rule sets in multiple projects.
*   **Cleanliness:** Keeps generated platform-specific rules (`.clinerules`, etc.) out of the target repository's version control.
*   **Simplified Workflow:** Provides clear `install`, `sync`, and `clean` commands for managing the rule lifecycle in a target repo.

## Specification: `manage_rules.py` Commands

*   **`install <target_repo_path> [--template-name <name>] [--source-of-truth-dir-name <dir_name>]`**
    *   **Action:** Copies the specified rule template (default: `light-spec`) from the Source Template Repo into the `<target_repo_path>` under the specified `<source-of-truth-dir-name>` (default: `project_rules_template`). Then, immediately runs the `sync` logic to generate the initial platform rules.
    *   **Output:** Prints progress messages and suggests adding generated platform rule directories to the target repo's `.gitignore`.
*   **`sync <target_repo_path> [--source-of-truth-dir-name <dir_name>]`**
    *   **Action:** Reads rules from the `<source-of-truth-dir-name>` within the `<target_repo_path>`. Deletes any existing Target Platform Rules directories/files. Regenerates the Target Platform Rules based on the content of the Target Source of Truth, applying platform-specific formatting (flattening, numbering, extension changes, concatenation) adapted from the original `copy_rules.py` logic.
    *   **Use Case:** Run this command after modifying files within the `Target Source of Truth` folder to update the rules used by AI assistants.
    *   **Output:** Prints progress messages.
*   **`clean <target_repo_path> [--source-of-truth-dir-name <dir_name>]`**
    *   **Action:** Removes both the generated Target Platform Rules directories/files *and* the `Target Source of Truth` folder from the `<target_repo_path>`.
    *   **Use Case:** Completely uninstall the rules framework from the target repository.
    *   **Output:** Prints progress messages.

## Implementation Notes

*   Use Python's `argparse` library for command-line argument parsing.
*   Adapt core file processing logic from `copy_rules.py`.
*   Implement robust path handling and error checking.
*   Provide clear user feedback via print statements.

## Initial Documentation Approach (Task 6.a)

For the initial release:
1.  Document the usage of the `manage_rules.py` script itself (commands, arguments).
2.  Clearly explain the concept of the `Target Source of Truth` folder.
3.  State that customization is done by editing files *within* the `Target Source of Truth` folder in the target repository *after* running `install`.
4.  Recommend running `sync` after making customizations to update the platform-specific rules.
5.  Defer detailed guides on *how* to write effective custom rules until the core mechanism is validated and user feedback is gathered.
