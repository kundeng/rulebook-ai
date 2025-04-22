#!/usr/bin/env python3

import os
import shutil
import argparse
import re

# --- Constants ---
# Source template for rules
TEMPLATE_DIR = "rules_template/light-spec"
# Source directory for memory templates (relative to ROOT_DIR)
MEMORY_TEMPLATE_SOURCE_DIR = "memory_template"
# Name of the directory to store memory templates within the target repo
MEMORY_TEMPLATE_TARGET_DIR_NAME = "memory_template"
# Source directory for tools (relative to ROOT_DIR) - NEW
TOOLS_SOURCE_DIR = "tools"
# Name of the directory to store tools within the target repo - NEW
TOOLS_TARGET_DIR_NAME = "tools"
# Project root of this rules_template repository
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --- Helper Functions ---
# ... (copy_file, get_ordered_source_files, copy_and_number_files, copy_and_restructure_roocode, concatenate_ordered_files remain unchanged) ...
def copy_file(source, destination):
    """Copies a file from source to destination, creating parent dirs."""
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    print(f"Copying {source} -> {destination}")
    try:
        shutil.copy2(source, destination) # copy2 preserves metadata
    except Exception as e:
        print(f"Error copying {source} to {destination}: {e}")

def get_ordered_source_files(source_dir):
    """
    Walks the source directory and returns a sorted list of full file paths,
    respecting numerical prefixes on directories and files.
    """
    all_source_files = []
    print(f"Scanning source directory for ordered files: {source_dir}")
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' not found or is not a directory.")
        return []

    for root, dirs, files in os.walk(source_dir, topdown=True):
        # Sort directories and files numerically/alphabetically to guide walk
        # and ensure consistent order within directories.
        dirs.sort()
        files.sort()
        for filename in files:
            if filename.startswith('.'): # Ignore hidden files
                continue
            source_path = os.path.join(root, filename)
            if os.path.isfile(source_path):
                 all_source_files.append(source_path)

    # Global sort based on full path respects the NN- prefixes
    all_source_files.sort()
    print(f"Found {len(all_source_files)} files in specified order.")
    # for fpath in all_source_files: print(f"  - {fpath}") # Debug print
    return all_source_files

def copy_and_number_files(source_dir, dest_dir, extension_mode='keep'):
    """
    Flattens, orders, numbers, and copies files, handling extensions.
    (See previous version for full docstring)
    """
    if not os.path.exists(dest_dir):
        print(f"Creating destination directory: {dest_dir}")
        os.makedirs(dest_dir)
    else:
        print(f"Destination directory exists: {dest_dir}")
        # Optional: Clear destination directory?

    all_source_files = get_ordered_source_files(source_dir)
    if not all_source_files:
        print("No source files found to process.")
        return

    existing_files_count = 0
    if os.path.exists(dest_dir):
        for f in os.listdir(dest_dir):
            if os.path.isfile(os.path.join(dest_dir, f)) and re.match(r"^\d+-", f):
                 existing_files_count += 1
    next_num = existing_files_count + 1

    print(f"\nStarting numbering at: {next_num:02d} for flattened files.")
    print(f"Extension mode: '{extension_mode}'")

    for source_path in all_source_files:
        base_filename = os.path.basename(source_path)
        filename_no_prefix = re.sub(r"^\d+-", "", base_filename)
        filename_stem, _ = os.path.splitext(filename_no_prefix)

        if extension_mode == 'remove':
            processed_filename = filename_stem
        elif extension_mode == 'add_mdc':
            processed_filename = filename_stem + ".mdc"
        else: # 'keep' or default
             processed_filename = filename_no_prefix

        new_filename = "{:02d}-{}".format(next_num, processed_filename)
        dest_path = os.path.join(dest_dir, new_filename)
        copy_file(source_path, dest_path)
        next_num += 1

def copy_and_restructure_roocode(source_dir, dest_dir):
    """
    Copies structure, renames dirs, removes file extensions for RooCode.
    (See previous version for full docstring)
    """
    print(f"Copying tree structure from {source_dir} to {dest_dir}")
    os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
    if os.path.exists(dest_dir):
        print(f"Removing existing destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    try:
        shutil.copytree(source_dir, dest_dir)
        print("Initial tree copy complete.")
    except Exception as e:
        print(f"Error during initial copytree for RooCode: {e}")
        return

    # Rename directories (remove NN- prefix)
    print("Renaming numbered directories in destination...")
    dirs_to_rename = []
    for root, dirs, _ in os.walk(dest_dir, topdown=False):
         for dir_name in dirs:
             if re.match(r"^\d+-", dir_name):
                 dirs_to_rename.append(os.path.join(root, dir_name))
    dirs_to_rename.sort(key=len, reverse=True)
    renamed_dir_count = 0
    for old_dir_path in dirs_to_rename:
        # ... (directory renaming logic as before) ...
        if not os.path.isdir(old_dir_path): continue
        dir_name = os.path.basename(old_dir_path)
        parent_dir = os.path.dirname(old_dir_path)
        new_dir_name = re.sub(r"^\d+-", "", dir_name)
        new_dir_path = os.path.join(parent_dir, new_dir_name)
        if os.path.exists(new_dir_path):
             print(f"Warning: Target directory '{new_dir_path}' already exists. Skipping rename for '{old_dir_path}'.")
             continue
        try:
            # print(f"Renaming Dir: {old_dir_path} -> {new_dir_path}") # Less verbose option
            os.rename(old_dir_path, new_dir_path)
            renamed_dir_count += 1
        except OSError as e:
            print(f"Error renaming directory {old_dir_path} to {new_dir_path}: {e}")
    print(f"Directory renaming complete. Renamed {renamed_dir_count} directories.")


    # Remove extensions from files
    print("Removing extensions from files in destination...")
    renamed_file_count = 0
    for root, _, files in os.walk(dest_dir):
        for filename in files:
            # ... (file extension removal logic as before) ...
            if filename.startswith('.'): continue
            base_name, ext = os.path.splitext(filename)
            if ext:
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, base_name)
                if os.path.exists(new_file_path):
                    print(f"Warning: Target file '{new_file_path}' already exists. Skipping rename for '{old_file_path}'.")
                    continue
                try:
                    # print(f"Renaming File: {old_file_path} -> {new_file_path}") # Less verbose option
                    os.rename(old_file_path, new_file_path)
                    renamed_file_count += 1
                except OSError as e:
                     print(f"Error renaming file {old_file_path} to {new_file_path}: {e}")
    print(f"File extension removal complete. Renamed {renamed_file_count} files.")

# NEW function for Windsurf
def concatenate_ordered_files(source_dir, dest_file_path):
    """
    Finds all files in source_dir in the correct order, concatenates
    their content, and writes it to a single destination file.
    """
    all_source_files = get_ordered_source_files(source_dir)
    if not all_source_files:
        print("No source files found to concatenate.")
        return

    print(f"\nConcatenating {len(all_source_files)} files into: {dest_file_path}")
    # Ensure parent directory for the destination file exists
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

    try:
        with open(dest_file_path, 'w', encoding='utf-8') as dest_f:
            for i, source_path in enumerate(all_source_files):
                print(f"Appending content from: {source_path}")
                try:
                    with open(source_path, 'r', encoding='utf-8') as source_f:
                        content = source_f.read()
                        dest_f.write(content)
                        # Add a separator (e.g., two newlines) between files,
                        # but only if it's not the very last file.
                        # Or, simpler: always add it, and ensure content ends with newline.
                        # Let's add a clear separator comment and newlines
                        if i < len(all_source_files) - 1:
                             separator = f"\n\n# --- Appended from: {os.path.basename(source_path)} ---\n\n"
                             dest_f.write(separator)
                        else:
                             # Ensure the very last file ends with a newline if it doesn't
                             if not content.endswith('\n'):
                                 dest_f.write('\n')

                except Exception as e:
                    print(f"Error reading file {source_path}: {e}")
                    # Decide if you want to stop or continue on error
                    # raise # Stop execution
                    continue # Skip this file and continue

        print(f"Successfully created concatenated file: {dest_file_path}")

    except Exception as e:
        print(f"Error writing to destination file {dest_file_path}: {e}")


def handle_install(args):
    """Handles the install command."""
    target_repo_path = os.path.abspath(args.target_repo_path)
    # Source and target for RULES
    source_of_truth_rules_dir_target = os.path.join(target_repo_path, args.source_of_truth_dir_name)
    template_source_rules = os.path.join(ROOT_DIR, TEMPLATE_DIR)
    # Source and target for MEMORY TEMPLATES
    memory_template_source_path = os.path.join(ROOT_DIR, MEMORY_TEMPLATE_SOURCE_DIR)
    memory_template_target_path = os.path.join(target_repo_path, MEMORY_TEMPLATE_TARGET_DIR_NAME)
    # Source and target for TOOLS - NEW
    tools_source_path = os.path.join(ROOT_DIR, TOOLS_SOURCE_DIR)
    tools_target_path = os.path.join(target_repo_path, TOOLS_TARGET_DIR_NAME)

    print(f"--- Installing rules, memory templates, and tools to {target_repo_path} ---")
    print(f"Using rule template: {args.template_name}")
    print(f"Target Rule Source of Truth: {source_of_truth_rules_dir_target}")
    print(f"Target Memory Templates Dir: {memory_template_target_path}")
    print(f"Target Tools Dir: {tools_target_path}") # NEW

    # 1. Install RULE templates into the source of truth directory
    print(f"\nStep 1: Copying RULE templates ({args.source_of_truth_dir_name}/)...")
    if os.path.exists(source_of_truth_rules_dir_target):
        print(f"Warning: Rule source of truth directory already exists: {source_of_truth_rules_dir_target}. Skipping rule template copy.")
    else:
        try:
            shutil.copytree(template_source_rules, source_of_truth_rules_dir_target)
            print(f"Successfully copied rule templates to {source_of_truth_rules_dir_target}")
        except Exception as e:
            print(f"Error copying rule templates: {e}")
            return # Stop if rule copy fails

    # 2. Install MEMORY template directory
    print(f"\nStep 2: Copying MEMORY template directory ({MEMORY_TEMPLATE_TARGET_DIR_NAME}/)...")
    if not os.path.exists(memory_template_source_path):
         print(f"Warning: Source memory template directory not found: {memory_template_source_path}. Skipping memory template copy.") # Changed Error to Warning
    elif os.path.exists(memory_template_target_path):
        print(f"Warning: Target memory template directory already exists: {memory_template_target_path}. Skipping memory template copy.")
    else:
        try:
            shutil.copytree(memory_template_source_path, memory_template_target_path)
            print(f"Successfully copied memory templates to {memory_template_target_path}")
        except Exception as e:
            print(f"Error copying memory templates: {e}")

    # 3. Install TOOLS directory - NEW
    print(f"\nStep 3: Copying TOOLS directory ({TOOLS_TARGET_DIR_NAME}/)...")
    if not os.path.exists(tools_source_path):
        print(f"Warning: Source tools directory not found: {tools_source_path}. Skipping tools copy.")
    elif os.path.exists(tools_target_path):
        print(f"Warning: Target tools directory already exists: {tools_target_path}. Skipping tools copy.")
    else:
        try:
            shutil.copytree(tools_source_path, tools_target_path)
            print(f"Successfully copied tools to {tools_target_path}")
        except Exception as e:
            print(f"Error copying tools directory: {e}")

    # 4. Run initial SYNC to generate platform-specific rules (Renumbered step)
    print(f"\nStep 4: Running initial sync...")
    handle_sync(args) # Pass args to use correct target path and rule SoT dir name

    # 5. Remind user about .gitignore and committing new directories (Renumbered step)
    print(f"\n--- Installation Complete ---")
    print(f"\nIMPORTANT:")
    print(f"1. Add the following lines to .gitignore in {target_repo_path}:")
    print(f"   .cursor/rules/")
    print(f"   .clinerules")
    print(f"   .roo/")
    print(f"   .windsurfrules")
    print(f"   # Add other generated rule directories if applicable")
    print(f"\n2. Commit the NEW directories added to your project:")
    print(f"   {args.source_of_truth_dir_name}/")
    print(f"   {MEMORY_TEMPLATE_TARGET_DIR_NAME}/")
    print(f"   {TOOLS_TARGET_DIR_NAME}/") # NEW
    print(f"\n3. REMINDER: Ensure your rule files (in {args.source_of_truth_dir_name}/) reference memory files")
    print(f"   using paths relative to the project root, starting with '{MEMORY_TEMPLATE_TARGET_DIR_NAME}/',")
    print(f"   e.g., '{MEMORY_TEMPLATE_TARGET_DIR_NAME}/docs/product_requirement_docs.md'")
    print(f"\n4. REMINDER: Ensure your rule files (in {args.source_of_truth_dir_name}/) reference tools") # NEW
    print(f"   using paths relative to the project root, starting with '{TOOLS_TARGET_DIR_NAME}/',") # NEW
    print(f"   e.g., 'python {TOOLS_TARGET_DIR_NAME}/my_script.py'") # NEW


def handle_sync(args):
    """Handles the sync command."""
    target_repo_path = os.path.abspath(args.target_repo_path)
    source_of_truth_rules_dir = os.path.join(target_repo_path, args.source_of_truth_dir_name)

    print(f"\n--- Syncing platform rules in {target_repo_path} ---")
    print(f"Using rule source of truth: {source_of_truth_rules_dir}")

    if not os.path.exists(source_of_truth_rules_dir):
        print(f"Error: Rule source of truth directory not found: {source_of_truth_rules_dir}")
        print("Cannot sync. Run the 'install' command first?")
        return

    cursor_dir = os.path.join(target_repo_path, ".cursor", "rules")
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules")

    # Ensure parent .cursor directory exists for cursor_dir
    if not os.path.exists(os.path.dirname(cursor_dir)):
         os.makedirs(os.path.dirname(cursor_dir))

    # Remove existing generated rules
    print("Removing existing generated platform rule files/directories...")
    # (Cleanup logic remains the same as previous version)
    if os.path.exists(cursor_dir):
        shutil.rmtree(cursor_dir)
        print(f"Removed: {cursor_dir}")
    if os.path.exists(cline_dir):
        if os.path.isfile(cline_dir): os.remove(cline_dir)
        elif os.path.isdir(cline_dir): shutil.rmtree(cline_dir)
        print(f"Cleared/Removed: {cline_dir}")
    if os.path.exists(roo_rules_dir):
        shutil.rmtree(roo_rules_dir)
        print(f"Removed: {roo_rules_dir}")
    if os.path.exists(windsurf_file_path):
        os.remove(windsurf_file_path)
        print(f"Removed: {windsurf_file_path}")

    # Generate new rules
    print("\nGenerating new platform rule files...")
    print("--- Processing Cursor rules ---")
    copy_and_number_files(source_of_truth_rules_dir, cursor_dir, extension_mode='add_mdc')
    print("--- Processing CLINE rules ---")
    copy_and_number_files(source_of_truth_rules_dir, cline_dir, extension_mode='remove')
    print("--- Processing RooCode rules ---")
    copy_and_restructure_roocode(source_of_truth_rules_dir, roo_rules_dir)
    print("--- Processing Windsurf rules ---")
    concatenate_ordered_files(source_of_truth_rules_dir, windsurf_file_path)

    print("\n--- Rule sync complete! ---")


def handle_clean(args):
    """Handles the clean command."""
    target_repo_path = os.path.abspath(args.target_repo_path)
    # Path to rule source of truth in target
    source_of_truth_rules_dir_target = os.path.join(target_repo_path, args.source_of_truth_dir_name)
    # Path to memory templates in target
    memory_template_target_path = os.path.join(target_repo_path, MEMORY_TEMPLATE_TARGET_DIR_NAME)
    # Path to tools in target - NEW
    tools_target_path = os.path.join(target_repo_path, TOOLS_TARGET_DIR_NAME)

    print(f"--- Cleaning rules framework from {target_repo_path} ---")

    # Define paths to generated rules
    cursor_dir = os.path.join(target_repo_path, ".cursor", "rules")
    cursor_parent_dir = os.path.dirname(cursor_dir) # .cursor
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules")

    # List of ALL items to remove (Generated rules + Installed templates/tools)
    items_to_remove = [
        cursor_parent_dir,
        cline_dir,
        roo_rules_dir,
        windsurf_file_path,
        source_of_truth_rules_dir_target, # Rule source of truth
        memory_template_target_path,      # Memory template dir
        tools_target_path                 # Tools dir - NEW
    ]

    print("Removing generated platform rules and installed template/tools directories...")
    removed_count = 0
    for item_path in items_to_remove:
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Removed file: {item_path}")
                removed_count += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")
                removed_count += 1
            # else: file/dir doesn't exist, skip silently
        except Exception as e:
            print(f"Error removing {item_path}: {e}")

    print(f"\n--- Clean operation complete. Removed {removed_count} items. ---")
    print(f"Removed items included generated rules and directories:")
    print(f"  '{args.source_of_truth_dir_name}/'")
    print(f"  '{MEMORY_TEMPLATE_TARGET_DIR_NAME}/'")
    print(f"  '{TOOLS_TARGET_DIR_NAME}/'") # NEW


def main():
    parser = argparse.ArgumentParser(description="Manage AI assistant rule sets, memory templates, and tools in target repositories.") # Updated description
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Install command
    install_parser = subparsers.add_parser("install", help="Install rule sets, memory templates, and tools to a target repository") # Updated help
    install_parser.add_argument("target_repo_path", help="Path to the target repository")
    install_parser.add_argument("--template-name", default="light-spec", help="Name of the rule template subdirectory in rules_template/ (default: light-spec)")
    install_parser.add_argument("--source-of-truth-dir-name", default="project_rules_template", help="Name of the directory to store rule templates within the target repo (default: project_rules_template)")
    install_parser.set_defaults(func=handle_install)

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync platform rules from the target repository's rule source of truth")
    sync_parser.add_argument("target_repo_path", help="Path to the target repository")
    sync_parser.add_argument("--source-of_truth-dir-name", default="project_rules_template", help="Name of the rule source of truth directory within the target repo (default: project_rules_template)")
    sync_parser.set_defaults(func=handle_sync)

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean generated rules and installed template/tools directories from a target repository") # Updated help
    clean_parser.add_argument("target_repo_path", help="Path to the target repository")
    clean_parser.add_argument("--source-of_truth-dir-name", default="project_rules_template", help="Name of the rule source of truth directory within the target repo (default: project_rules_template)")
    clean_parser.set_defaults(func=handle_clean)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
