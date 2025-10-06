#!/bin/bash

# Simple script to replace directories in target with matching directories from source
#
# USAGE INSTRUCTIONS:
# ===================
# 1. Make the script executable: chmod +x odoo_replace_dirs_in_target_from_source.sh
# 2. Run the script: ./odoo_replace_dirs_in_target_from_source.sh
# 3. Enter the TARGET directory path when prompted
# 4. Enter the SOURCE directory path when prompted
# 5. Confirm each replacement when asked
#
# WHAT THIS SCRIPT DOES:
# ======================
# - Scans all subdirectories in the TARGET directory
# - For each TARGET subdirectory, looks for a matching name in SOURCE directory
# - If a match is found, asks if you want to replace the TARGET subdirectory
# - If confirmed, removes the old subdirectory from TARGET and copies the matching one from SOURCE
# - If no match found in SOURCE, skips that TARGET subdirectory
#
# TARGET vs SOURCE EXPLANATION:
# ==============================
# TARGET DIRECTORY: The directory that will be MODIFIED (subdirectories will be replaced)
#   - This is where you want to update/replace existing subdirectories
#   - Example: Your current project directory with outdated modules
#
# SOURCE DIRECTORY: The directory containing the NEW/UPDATED subdirectories
#   - This is where the replacement subdirectories come from
#   - These subdirectories will be COPIED to replace matching ones in target
#   - Example: A directory with updated/newer versions of modules
#
# EXAMPLE SCENARIO:
# =================
# TARGET: /home/user/my_project/modules (has: module_a, module_b, module_c)
# SOURCE: /home/user/updated_modules (has: module_a, module_x, module_c)
# RESULT: module_a and module_c in TARGET will be replaced with versions from SOURCE
#         module_b stays unchanged (no match in SOURCE)
#         module_x is ignored (not in TARGET)

echo "Directory Replacement Script"
echo "============================"
echo
echo "This script will replace subdirectories in TARGET with matching ones from SOURCE"
echo

# Get target directory
echo -n "Enter target directory path: "
read TARGET_DIR

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist!"
    exit 1
fi

# Get source directory
echo -n "Enter source directory path: "
read SOURCE_DIR

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist!"
    exit 1
fi

# Check if directories are different
if [ "$TARGET_DIR" = "$SOURCE_DIR" ]; then
    echo "Error: Target and source directories cannot be the same!"
    exit 1
fi

echo
echo "Target: $TARGET_DIR"
echo "Source: $SOURCE_DIR"
echo

# Find and replace matching directories
echo "Scanning target subdirectories for matches in source..."

# Arrays to track replaced and skipped directories
replaced_dirs=()
skipped_dirs=()

for target_subdir in "$TARGET_DIR"/*; do
    # Skip if not a directory
    [ ! -d "$target_subdir" ] && continue
    
    dir_name=$(basename "$target_subdir")
    source_match="$SOURCE_DIR/$dir_name"
    
    # Check if matching directory exists in source
    if [ -d "$source_match" ]; then
        echo "Found match for: $dir_name - replacing automatically..."
        
        echo "Removing old directory..."
        rm -rf "$target_subdir"
        
        echo "Copying new directory..."
        cp -r "$source_match" "$target_subdir"
        
        echo "Replaced: $dir_name"
        # Add to replaced directories list
        replaced_dirs+=("$dir_name")
        echo
    else
        echo "No match found for: $dir_name (skipping)"
        # Add to skipped directories list (no match found)
        skipped_dirs+=("$dir_name")
    fi
done

echo "Done!"
echo
echo "===================="
echo "REPLACEMENT SUMMARY:"
echo "===================="

if [ ${#replaced_dirs[@]} -eq 0 ]; then
    echo "No directories were replaced."
else
    echo "The following directories were replaced:"
    for dir in "${replaced_dirs[@]}"; do
        echo "  - $dir"
    done
    echo
    echo "Total replaced: ${#replaced_dirs[@]} directories"
    fi
    
    echo
if [ ${#skipped_dirs[@]} -eq 0 ]; then
    echo "No directories were skipped."
else
    echo "The following directories were skipped:"
    for dir in "${skipped_dirs[@]}"; do
        echo "  - $dir"
    done
    echo
    echo "Total skipped: ${#skipped_dirs[@]} directories"
fi