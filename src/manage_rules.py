#!/usr/bin/env python3

import os
import shutil
import argparse
import re

# Source and destination directories
TEMPLATE_DIR = "rules_template/light-spec"
# IMPORTANT: Adjust this path to your actual project root if necessary
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Project root is parent of script dir
# Or keep your original path if preferred:
# ROOT_DIR = "/Users/wangbo-ting/git/rules_template"

# --- Helper Functions ---

def copy_file(source, destination):
    """Copies a file from source to destination."""
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
    source_of_truth_dir = os.path.join(target_repo_path, args.source_of_truth_dir_name)
    template_source = os.path.join(ROOT_DIR, TEMPLATE_DIR)

    print(f"Installing rules to {target_repo_path}")
    print(f"Using template: {args.template_name}")
    print(f"Creating source of truth directory: {source_of_truth_dir}")

    if os.path.exists(source_of_truth_dir):
        print(f"Error: Source of truth directory already exists: {source_of_truth_dir}")
        return

    try:
        shutil.copytree(template_source, source_of_truth_dir)
        print(f"Successfully copied template to {source_of_truth_dir}")
    except Exception as e:
        print(f"Error copying template: {e}")
        return

    handle_sync(args)

    print(f"\nIMPORTANT: Add the following lines to .gitignore in {target_repo_path}:\n")
    print(f".cursor/rules\n.clinerules\n.roo\n.windsurfrules\n")


def handle_sync(args):
    """Handles the sync command."""
    target_repo_path = os.path.abspath(args.target_repo_path)
    source_of_truth_dir = os.path.join(target_repo_path, args.source_of_truth_dir_name)

    print(f"Syncing rules in {target_repo_path}")
    print(f"Using source of truth directory: {source_of_truth_dir}")

    if not os.path.exists(source_of_truth_dir):
        print(f"Error: Source of truth directory not found: {source_of_truth_dir}")
        return

    cursor_dir = os.path.join(target_repo_path, ".cursor")
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules")

    # Remove existing rules
    print("Removing existing rules directories...")
    if os.path.exists(cursor_dir):
        shutil.rmtree(cursor_dir)
    if os.path.exists(cline_dir):
        shutil.rmtree(cline_dir)
    if os.path.exists(roo_rules_dir):
        shutil.rmtree(roo_rules_dir)
    if os.path.exists(windsurf_file_path):
        os.remove(windsurf_file_path)

    # Generate new rules
    print("\nGenerating new rules...")
    print("--- Processing Cursor rules ---")
    copy_and_number_files(source_of_truth_dir, cursor_dir, extension_mode='add_mdc')
    print("--- Processing CLINE rules ---")
    copy_and_number_files(source_of_truth_dir, cline_dir, extension_mode='remove')
    print("--- Processing RooCode rules ---")
    copy_and_restructure_roocode(source_of_truth_dir, roo_rules_dir)
    print("--- Processing Windsurf rules ---")
    concatenate_ordered_files(source_of_truth_dir, windsurf_file_path)

    print("\nRule files processing complete!")


def handle_clean(args):
    """Handles the clean command."""
    target_repo_path = os.path.abspath(args.target_repo_path)
    source_of_truth_dir = os.path.join(target_repo_path, args.source_of_truth_dir_name)

    print(f"Cleaning rules in {target_repo_path}")
    print(f"Removing source of truth directory: {source_of_truth_dir}")

    cursor_dir = os.path.join(target_repo_path, ".cursor")
    cline_dir = os.path.join(target_repo_path, ".clinerules")
    roo_rules_dir = os.path.join(target_repo_path, ".roo")
    windsurf_file_path = os.path.join(target_repo_path, ".windsurfrules")

    # Remove existing rules
    print("Removing existing rules directories...")
    if os.path.exists(cursor_dir):
        shutil.rmtree(cursor_dir)
    if os.path.exists(cline_dir):
        shutil.rmtree(cline_dir)
    if os.path.exists(roo_rules_dir):
        shutil.rmtree(roo_rules_dir)
    if os.path.exists(windsurf_file_path):
        os.remove(windsurf_file_path)

    try:
        shutil.rmtree(source_of_truth_dir)
        print(f"Successfully removed source of truth directory: {source_of_truth_dir}")
    except Exception as e:
        print(f"Error removing source of truth directory: {e}")
        return


def main():
    parser = argparse.ArgumentParser(description="Manage AI assistant rule sets in target repositories.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install rule sets to a target repository")
    install_parser.add_argument("target_repo_path", help="Path to the target repository")
    install_parser.add_argument("--template-name", default="light-spec", help="Name of the template to use (default: light-spec)")
    install_parser.add_argument("--source-of-truth-dir-name", default="project_rules_template", help="Name of the source of truth directory (default: project_rules_template)")
    install_parser.set_defaults(func=handle_install)

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync rule sets in a target repository")
    sync_parser.add_argument("target_repo_path", help="Path to the target repository")
    sync_parser.add_argument("--source-of-truth-dir-name", default="project_rules_template", help="Name of the source of truth directory (default: project_rules_template)")
    sync_parser.set_defaults(func=handle_sync)

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean rule sets from a target repository")
    clean_parser.add_argument("target_repo_path", help="Path to the target repository")
    clean_parser.add_argument("--source-of-truth-dir-name", default="project_rules_template", help="Name of the source of truth directory (default: project_rules_template)")
    clean_parser.set_defaults(func=handle_clean)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
