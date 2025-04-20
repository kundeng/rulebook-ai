#!/usr/bin/env python3

import os
import shutil
import errno
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

# --- Main Processing Functions ---

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


# --- Main Execution Logic ---

print(f"Using TEMPLATE_DIR: {os.path.join(ROOT_DIR, TEMPLATE_DIR)}")
print(f"Using ROOT_DIR: {ROOT_DIR}\n")

template_path = os.path.join(ROOT_DIR, TEMPLATE_DIR)
separator_line = "-" * 40 # Define a separator for console output

# Cursor: Flatten, Number, Add .mdc extension
print(separator_line)
print("--- Processing Cursor rules ---")
cursor_dir = os.path.join(ROOT_DIR, ".cursor", "rules")
copy_and_number_files(template_path, cursor_dir, extension_mode='add_mdc')
print(separator_line)


# CLINE: Flatten, Number, Remove extensions
print("--- Processing CLINE rules ---")
cline_dir = os.path.join(ROOT_DIR, ".clinerules")
copy_and_number_files(template_path, cline_dir, extension_mode='remove')
print(separator_line)

# RooCode: Preserve Structure, Rename Dirs, Remove extensions from files
print("--- Processing RooCode rules ---")
roo_rules_dir = os.path.join(ROOT_DIR, ".roo")
copy_and_restructure_roocode(template_path, roo_rules_dir)
print(separator_line)

# Windsurf: Concatenate ordered files into one
print("--- Processing Windsurf rules ---")
# Destination file is directly in the ROOT_DIR
windsurf_file_path = os.path.join(ROOT_DIR, ".windsurfrules")
concatenate_ordered_files(template_path, windsurf_file_path)
print(separator_line)


print("\nRule files processing complete!")
