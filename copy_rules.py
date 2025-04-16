#!/usr/bin/env python3

import os
import shutil
import errno
import re

# Source and destination directories
TEMPLATE_DIR = "rules_template"
ROOT_DIR = "/Users/wangbo-ting/git/rules_template"  # Project root directory

def copy_file(source, destination):
    """Copies a file from source to destination."""
    print(f"Copying {source} to {destination}")
    os.makedirs(os.path.dirname(destination), exist_ok=True)  # Ensure destination directory exists
    shutil.copy2(source, destination)  # copy2 preserves metadata

def copy_and_number_files(source_dir, dest_dir, add_extension=False):
    """
    Copies files from source_dir to dest_dir, flattening the structure,
    respecting the numbered order of source directories/files, and adding
    sequential numbers to the destination files.
    """
    if not os.path.exists(dest_dir):
        print(f"Creating destination directory: {dest_dir}")
        os.makedirs(dest_dir)
    else:
        print(f"Destination directory exists: {dest_dir}")

    # --- Step 1: Collect all file paths ---
    all_source_files = []
    print(f"Scanning source directory: {source_dir}")
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' not found or is not a directory.")
        return

    for root, dirs, files in os.walk(source_dir, topdown=True):
        # Sort directories and files numerically/alphabetically *within* os.walk
        # This ensures consistent ordering for files within the same directory
        # and helps guide os.walk's traversal order (though global sort later is key)
        dirs.sort()
        files.sort()
        # print(f"Walking root: {root}")
        # print(f"  Sorted dirs: {dirs}")
        # print(f"  Sorted files: {files}")
        for filename in files:
            # Ignore hidden files like .DS_Store
            if filename.startswith('.'):
                continue
            source_path = os.path.join(root, filename)
            if os.path.isfile(source_path): # Ensure it's actually a file
                 all_source_files.append(source_path)

    # --- Step 2: Sort the collected paths globally ---
    # Sorting the full paths alphabetically should respect the 01-, 02- prefixes
    all_source_files.sort()
    print(f"\nFound {len(all_source_files)} files to copy. Sorted order:")
    # for fpath in all_source_files: # Optional: print sorted list for debugging
    #     print(f"  - {fpath}")

    # --- Step 3: Iterate through sorted list, copy, and number ---
    # Determine starting number based on existing files in dest_dir
    # Note: This only works well if dest_dir is initially empty or contains
    # files already following the ##- pattern. If mixing file types,
    # this numbering might be unpredictable. Consider clearing dest_dir first if needed.
    existing_files = [f for f in os.listdir(dest_dir) if os.path.isfile(os.path.join(dest_dir, f))]
    next_num = len(existing_files) + 1
    print(f"\nStarting numbering at: {next_num:02d}")

    for source_path in all_source_files:
        base_filename = os.path.basename(source_path)

        # Remove existing leading number (e.g., "01-") from the base filename if present
        filename_no_prefix = re.sub(r"^\d+-", "", base_filename)

        # Create the new numbered filename
        new_filename = "{:02d}-{}".format(next_num, filename_no_prefix)
        if add_extension:
            # Ensure we don't add .mdc if it already ends with it (just in case)
            if not new_filename.endswith(".mdc"):
                 new_filename = new_filename + ".mdc"

        dest_path = os.path.join(dest_dir, new_filename)
        copy_file(source_path, dest_path)
        next_num += 1

def copy_and_restructure_roocode(source_dir, dest_dir):
    """
    Copies the source directory tree to the destination, preserving structure,
    but removes leading 'NN-' prefixes from directory names in the destination.
    File names (including prefixes) are preserved.
    """
    print(f"Copying tree structure from {source_dir} to {dest_dir}")

    # Ensure the parent directory of the destination exists
    os.makedirs(os.path.dirname(dest_dir), exist_ok=True)

    # Clean destination directory first for a fresh copy
    if os.path.exists(dest_dir):
        print(f"Removing existing destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    try:
        # Copy the entire tree initially
        shutil.copytree(source_dir, dest_dir)
        print("Initial tree copy complete.")
    except Exception as e:
        print(f"Error during initial copytree for RooCode: {e}")
        return # Stop if copy fails

    # --- Rename directories in the destination ---
    print("Renaming numbered directories in destination...")
    dirs_to_rename = []
    # Walk the destination directory to find all subdirectories
    for root, dirs, files in os.walk(dest_dir, topdown=False): # topdown=False is crucial for renaming
         for dir_name in dirs:
             if re.match(r"^\d+-", dir_name):
                 dirs_to_rename.append(os.path.join(root, dir_name))

    # Sort directories by path depth (longest first) to rename children before parents
    dirs_to_rename.sort(key=len, reverse=True)

    renamed_count = 0
    for old_dir_path in dirs_to_rename:
        if not os.path.isdir(old_dir_path): # Check if it still exists (might have been renamed as part of parent)
            continue
        dir_name = os.path.basename(old_dir_path)
        parent_dir = os.path.dirname(old_dir_path)
        new_dir_name = re.sub(r"^\d+-", "", dir_name)
        new_dir_path = os.path.join(parent_dir, new_dir_name)

        # Avoid collision if a directory with the target name already exists (shouldn't happen with clean copy)
        if os.path.exists(new_dir_path):
             print(f"Warning: Target directory '{new_dir_path}' already exists. Skipping rename for '{old_dir_path}'.")
             continue

        try:
            print(f"Renaming: {old_dir_path} -> {new_dir_path}")
            os.rename(old_dir_path, new_dir_path)
            renamed_count += 1
        except OSError as e:
            print(f"Error renaming directory {old_dir_path} to {new_dir_path}: {e}")

    print(f"Directory renaming complete. Renamed {renamed_count} directories.")

# Cursor
print("Copying Cursor rules...")
cursor_dir = os.path.join(ROOT_DIR, ".cursor", "rules")
copy_and_number_files(TEMPLATE_DIR, cursor_dir, add_extension=True)

# CLINE
print("Copying CLINE rules...")
cline_dir = os.path.join(ROOT_DIR, ".clinerules")
copy_and_number_files(TEMPLATE_DIR, cline_dir)

# RooCode
print("--- Processing RooCode rules (Preserve Structure, Rename Dirs) ---")
roo_rules_dir = os.path.join(ROOT_DIR, ".roo", "rules")
copy_and_restructure_roocode(TEMPLATE_DIR, roo_rules_dir)
print("-" * 30)

print("Rule files copied successfully!")
