#!/usr/bin/env python3

import os
import shutil
import errno
import re

# Source and destination directories
TEMPLATE_DIR = "rules_template"
# IMPORTANT: Adjust this path to your actual project root if necessary
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # More robust way to find project root
# Or keep your original path if preferred:
# ROOT_DIR = "/Users/wangbo-ting/git/rules_template"

def copy_file(source, destination):
    """Copies a file from source to destination."""
    # Ensure the destination directory exists before printing the copy message
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    print(f"Copying {source} to {destination}")
    try:
        shutil.copy2(source, destination) # copy2 preserves metadata
    except Exception as e:
        print(f"Error copying {source} to {destination}: {e}")

# Updated function signature and logic for extension handling
def copy_and_number_files(source_dir, dest_dir, extension_mode='keep'):
    """
    Copies files from source_dir to dest_dir, flattening the structure,
    respecting the numbered order of source directories/files, adding
    sequential numbers, and handling file extensions based on extension_mode.

    Args:
        source_dir (str): Path to the source directory.
        dest_dir (str): Path to the destination directory.
        extension_mode (str): Controls extension handling:
            'keep': Keep original extension (default).
            'remove': Remove any existing extension.
            'add_mdc': Ensure the file ends with '.mdc'.
    """
    if not os.path.exists(dest_dir):
        print(f"Creating destination directory: {dest_dir}")
        os.makedirs(dest_dir)
    else:
        print(f"Destination directory exists: {dest_dir}")
        # Optional: Clear destination directory
        # ... (clearing logic as before) ...

    all_source_files = []
    print(f"Scanning source directory: {source_dir}")
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' not found or is not a directory.")
        return

    for root, dirs, files in os.walk(source_dir, topdown=True):
        dirs.sort()
        files.sort()
        for filename in files:
            if filename.startswith('.'): # Ignore hidden files
                continue
            source_path = os.path.join(root, filename)
            if os.path.isfile(source_path):
                 all_source_files.append(source_path)

    all_source_files.sort()
    print(f"\nFound {len(all_source_files)} files to copy (flattened). Sorted order:")
    # for fpath in all_source_files: print(f"  - {fpath}") # Debug print

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
        # Remove existing leading number (e.g., "01-") from the base filename
        filename_no_prefix = re.sub(r"^\d+-", "", base_filename)

        # Separate filename stem and original extension
        filename_stem, _ = os.path.splitext(filename_no_prefix)

        # Apply extension logic
        if extension_mode == 'remove':
            processed_filename = filename_stem
        elif extension_mode == 'add_mdc':
            processed_filename = filename_stem + ".mdc"
        else: # 'keep' or default
             # Reconstruct with original extension if needed (though filename_no_prefix has it)
             processed_filename = filename_no_prefix # Keep as is after prefix removal

        # Create the new numbered filename
        new_filename = "{:02d}-{}".format(next_num, processed_filename)

        dest_path = os.path.join(dest_dir, new_filename)
        copy_file(source_path, dest_path)
        next_num += 1

def copy_and_restructure_roocode(source_dir, dest_dir):
    """
    Copies the source directory tree to the destination, preserving structure,
    removes leading 'NN-' prefixes from directory names, and removes extensions
    from all files in the destination.
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

    # --- Rename directories in the destination ---
    print("Renaming numbered directories in destination...")
    dirs_to_rename = []
    for root, dirs, _ in os.walk(dest_dir, topdown=False): # bottom-up
         for dir_name in dirs:
             if re.match(r"^\d+-", dir_name):
                 dirs_to_rename.append(os.path.join(root, dir_name))

    dirs_to_rename.sort(key=len, reverse=True) # Deepest first

    renamed_dir_count = 0
    for old_dir_path in dirs_to_rename:
        if not os.path.isdir(old_dir_path): continue
        dir_name = os.path.basename(old_dir_path)
        parent_dir = os.path.dirname(old_dir_path)
        new_dir_name = re.sub(r"^\d+-", "", dir_name)
        new_dir_path = os.path.join(parent_dir, new_dir_name)
        if os.path.exists(new_dir_path):
             print(f"Warning: Target directory '{new_dir_path}' already exists. Skipping rename for '{old_dir_path}'.")
             continue
        try:
            print(f"Renaming Dir: {old_dir_path} -> {new_dir_path}")
            os.rename(old_dir_path, new_dir_path)
            renamed_dir_count += 1
        except OSError as e:
            print(f"Error renaming directory {old_dir_path} to {new_dir_path}: {e}")
    print(f"Directory renaming complete. Renamed {renamed_dir_count} directories.")

    # --- Remove extensions from files in the destination ---
    print("Removing extensions from files in destination...")
    renamed_file_count = 0
    # Walk again, now that directories have correct names
    for root, _, files in os.walk(dest_dir):
        for filename in files:
            if filename.startswith('.'): # Ignore hidden files
                continue
            base_name, ext = os.path.splitext(filename)
            if ext: # Only rename if there is an extension
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, base_name)

                if os.path.exists(new_file_path):
                    print(f"Warning: Target file '{new_file_path}' already exists. Skipping rename for '{old_file_path}'.")
                    continue
                try:
                    print(f"Renaming File: {old_file_path} -> {new_file_path}")
                    os.rename(old_file_path, new_file_path)
                    renamed_file_count += 1
                except OSError as e:
                     print(f"Error renaming file {old_file_path} to {new_file_path}: {e}")

    print(f"File extension removal complete. Renamed {renamed_file_count} files.")


# --- Main Execution Logic ---

print(f"Using TEMPLATE_DIR: {os.path.join(ROOT_DIR, TEMPLATE_DIR)}")
print(f"Using ROOT_DIR: {ROOT_DIR}\n")

template_path = os.path.join(ROOT_DIR, TEMPLATE_DIR)

# Cursor: Flatten, Number, Add .mdc extension
print("--- Processing Cursor rules ---")
cursor_dir = os.path.join(ROOT_DIR, ".cursor", "rules")
# Use extension_mode='add_mdc'
copy_and_number_files(template_path, cursor_dir, extension_mode='add_mdc')
print("-" * 30)


# CLINE: Flatten, Number, Remove extensions
print("--- Processing CLINE rules ---")
cline_dir = os.path.join(ROOT_DIR, ".clinerules")
# Use extension_mode='remove'
copy_and_number_files(template_path, cline_dir, extension_mode='remove')
print("-" * 30)

# RooCode: Preserve Structure, Rename Dirs, Remove extensions from files
print("--- Processing RooCode rules ---")
roo_rules_dir = os.path.join(ROOT_DIR, ".roo", "rules")
copy_and_restructure_roocode(template_path, roo_rules_dir)
print("-" * 30)


print("Rule files processing complete!")
