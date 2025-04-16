#!/usr/bin/env python3

import os
import shutil

# Project root directory
ROOT_DIR = "/Users/wangbo-ting/git/rules_template"

def remove_directory(directory):
    """Removes a directory and its contents."""
    path = os.path.join(ROOT_DIR, directory)
    if os.path.exists(path):
        print(f"Removing directory: {path}")
        shutil.rmtree(path)
    else:
        print(f"Directory not found: {path}")

# Remove rule directories
print("Removing rule directories...")
remove_directory(".cursor")
remove_directory(".clinerules")
remove_directory(".roo")

print("Rule directories removed successfully!")
