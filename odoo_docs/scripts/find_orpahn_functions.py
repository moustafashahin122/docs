"""
Orphan Function Finder

This script identifies orphan functions in Python files - functions that are defined
but never called anywhere in the codebase. It helps maintain clean code by finding
unused functions that can potentially be removed or refactored.

Features:
    - Analyzes single Python files or all files in a directory (non-recursive)
    - Extracts all function definitions from target Python file(s)
    - Searches the entire codebase for function usage
    - Identifies functions that are never called (orphan functions)
    - Single file mode: Generates detailed Markdown and JSON reports
    - Directory mode: Prints results to terminal with per-file and overall summary

Usage:
    Single File Mode:
        python find_orpahn_functions.py -p <file_path> -c <codebase_path>
        
    Directory Mode:
        python find_orpahn_functions.py -d <directory_path> -c <codebase_path>
    
    Interactive Mode:
        python find_orpahn_functions.py
        
        The script will prompt for:
        1. Target Python file path to analyze
        2. Codebase root path to search for function usage

Examples:
    # Single file mode with CLI arguments
    $ python find_orpahn_functions.py -p /path/to/my_module.py -c /path/to/project/
    
    Analyzing functions...
    
    Found 5 function(s) in the target file.
    Found 2 orphan function(s):
      - unused_helper (line 45)
      - old_function (line 89)
    
    Generating analysis reports...
    
    ✓ Markdown report saved: /path/to/my_module_orphan_analysis.md
    ✓ JSON report saved: /path/to/my_module_orphan_analysis.json
    
    Analysis complete.
    
    # Directory mode with CLI arguments
    $ python find_orpahn_functions.py -d /path/to/modules/ -c /path/to/project/
    
    Found 3 Python file(s) in directory.
    
    Analyzing: module1.py
      Found 5 function(s)
      Orphan function(s): 1
        - old_helper (line 23)
      Summary for module1.py: 5 total, 1 orphans
    ---
    
    Analyzing: module2.py
      Found 8 function(s)
      Orphan function(s): 0
      Summary for module2.py: 8 total, 0 orphans
    ---
    
    ============================================================
    OVERALL SUMMARY
    ============================================================
    Files analyzed: 2
    Total functions: 13
    Total orphans: 1

Author: Generated for Odoo Documentation Project
License: MIT
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime


def extract_functions_from_file(file_path):
    """
    Extract all function definitions from a Python file.
    
    This function scans a Python file line by line and uses regex to identify
    function definitions (lines starting with 'def'). It captures both the
    function name and its line number for later reference.
    
    Args:
        file_path (str): Path to the Python file to analyze
        
    Returns:
        list: List of tuples containing (function_name, line_number)
              Empty list if file cannot be read or has no functions
              
    Examples:
        >>> extract_functions_from_file('my_module.py')
        [('calculate_total', 15), ('process_data', 32), ('validate_input', 48)]
        
    Notes:
        - Only captures top-level and class method definitions
        - Line numbers are 1-indexed
        - Handles UTF-8 encoded files
        - Silently returns empty list on errors
    """
    functions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, start=1):
                # Match function definitions using regex pattern: def function_name(
                # Pattern explanation:
                # - def\s+ : 'def' keyword followed by one or more whitespace
                # - (\w+)  : capture group for function name (alphanumeric + underscore)
                # - \s*\(  : optional whitespace followed by opening parenthesis
                match = re.search(r'def\s+(\w+)\s*\(', line)
                if match:
                    func_name = match.group(1)  # Extract the function name from capture group
                    functions.append((func_name, i))
    except (IOError, OSError, UnicodeDecodeError) as e:
        print(f"Error reading file {file_path}: {e}")
        return []
    
    return functions


def search_function_usage(func_name, codebase_path, exclude_file):
    """
    Search for function usage across the entire codebase.
    
    This function recursively searches all Python and XML files in the codebase directory
    to find any occurrence of the specified function being called. It uses different
    search strategies based on file type:
    - Analyzed file: Searches for function calls but excludes the definition line
    - Python files: Searches for "function_name(" pattern
    - XML files: Searches for the function name (common in Odoo views/actions)
    
    Args:
        func_name (str): Name of the function to search for
        codebase_path (str): Root path of the codebase to search in
        exclude_file (str): Path to the file containing the function definition
                           (will be searched but definition line excluded)
    
    Returns:
        bool: True if the function is called somewhere in the codebase
              False if the function is never called (orphan function)
    
    Examples:
        >>> search_function_usage('calculate_total', '/project/src', '/project/src/utils.py')
        True  # Function is used somewhere
        
        >>> search_function_usage('old_helper', '/project/src', '/project/src/helpers.py')
        False  # Function is orphaned
    
    Notes:
        - Python files: Searches for "function_name(" to identify function calls
        - XML files: Searches for the function name (e.g., in button name attributes)
        - Analyzed file: Uses regex to exclude "def function_name(" but find "function_name("
        - Recursively searches all .py and .xml files in the codebase
        - Skips files that cannot be read (permission errors, encoding issues)
        - Case-sensitive search
        - May have false negatives if function is called dynamically (getattr, eval, etc.)
    """
    # Build search pattern: function_name followed by opening parenthesis
    search_pattern = f"{func_name}"
    
    # Regex pattern to find function calls but exclude definitions
    # Negative lookbehind ensures "def " is not before the function name
    call_pattern = re.compile(rf'(?<!def\s)\b{re.escape(func_name)}\s*')
    
    # Convert exclude_file to absolute path for accurate comparison
    exclude_file_abs = os.path.abspath(exclude_file)
    
    codebase_path = Path(codebase_path)
    
    # Search all Python files in the codebase recursively
    for py_file in codebase_path.rglob('*.py'):
        py_file_abs = os.path.abspath(py_file)
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Special handling for the analyzed file itself
                if py_file_abs == exclude_file_abs:
                    # Use regex to find function calls but exclude definition lines
                    if call_pattern.search(content):
                        return True  # Function is called within its own file
                else:
                    # For other Python files, use simple string search
                    if search_pattern in content:
                        return True  # Function is used in another Python file
        except (IOError, OSError, UnicodeDecodeError):
            # Skip files that can't be read (permissions, encoding issues, etc.)
            continue
    
    # Search all XML files in the codebase recursively
    for xml_file in codebase_path.rglob('*.xml'):
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # In XML files, search for the function name without requiring parenthesis
                # Common in Odoo: <button name="func_name"/> or <field name="func_name"/>
                if func_name in content:
                    return True  # Function name found in XML file
        except (IOError, OSError, UnicodeDecodeError):
            # Skip files that can't be read (permissions, encoding issues, etc.)
            continue
    for xml_file in codebase_path.rglob('*.js'):
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # In XML files, search for the function name without requiring parenthesis
                # Common in Odoo: <button name="func_name"/> or <field name="func_name"/>
                if func_name in content:
                    return True  # Function name found in XML file
        except (IOError, OSError, UnicodeDecodeError):
            # Skip files that can't be read (permissions, encoding issues, etc.)
            continue
    
    # Function was not found in any file - it's an orphan
    return False


def add_todo_to_orphans(file_path, orphan_lines):
    """
    Add TODO comments above orphan function definitions in the source file.
    
    This function modifies the source file by inserting TODO comments directly
    above each orphan function definition. The comments are properly indented to
    match the indentation of the function they annotate.
    
    Args:
        file_path (str): Path to the Python file to modify
        orphan_lines (set): Set of line numbers where orphan functions are defined
                           (1-indexed line numbers)
    
    Returns:
        bool: True if modification was successful
              False if an error occurred during file modification
    
    Examples:
        >>> orphan_lines = {15, 32, 48}
        >>> add_todo_to_orphans('/path/to/module.py', orphan_lines)
        True
        
        # Before:
        # def calculate_total():
        #     return sum(items)
        
        # After:
        # # TODO: Orphan function - not used in codebase
        # def calculate_total():
        #     return sum(items)
    
    Notes:
        - Processes lines in reverse order to maintain correct line numbers
        - Preserves original indentation (spaces/tabs)
        - Modifies the file in-place (overwrites original)
        - Comment format: "# TODO: Orphan function - not used in codebase"
        - No backup is created - ensure version control is in place
    
    Raises:
        Prints error message to console but doesn't raise exceptions
    """
    try:
        # Read the entire file into memory
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Insert TODO comments in reverse order to maintain correct line numbers
        # Processing from bottom to top ensures that adding a line doesn't shift
        # the positions of functions we haven't processed yet
        for line_num in sorted(orphan_lines, reverse=True):
            # Get the indentation level of the function definition
            func_line = lines[line_num - 1]  # Convert to 0-indexed
            indent = len(func_line) - len(func_line.lstrip())
            indent_str = ' ' * indent
            
            # Create TODO comment with matching indentation
            todo_comment = f"{indent_str}# TODO: Orphan function - not used in codebase\n"
            
            # Insert comment above the function (at line_num - 1 position)
            lines.insert(line_num - 1, todo_comment)
        
        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return True
    except (IOError, OSError, IndexError, UnicodeDecodeError) as e:
        print(f"Error modifying file: {e}")
        return False


def generate_markdown_report(target_file, codebase_path, all_functions, orphan_functions, output_dir=None):
    """
    Generate a detailed Markdown report of the orphan function analysis.
    
    Creates a comprehensive markdown-formatted report containing analysis summary,
    statistics, detailed function tables, and recommendations. The report is saved
    in the specified directory or the same directory as the analyzed file.
    
    Args:
        target_file (str): Path to the analyzed Python file
        codebase_path (str): Root path of the codebase that was searched
        all_functions (list): List of all (function_name, line_number) tuples
        orphan_functions (list): List of orphan (function_name, line_number) tuples
        output_dir (str, optional): Directory to save the report. Defaults to analyzed file's directory
    
    Returns:
        str: Path to the generated markdown report file
        None: If report generation failed
    
    Report Contents:
        - Header with analysis metadata (timestamp, file paths)
        - Summary statistics (total functions, orphan count, usage rate)
        - Orphan Functions table (name and line number)
        - All Functions table (name, line, and status)
        - Recommendations section based on findings
    
    Examples:
        >>> generate_markdown_report('utils.py', '/project', functions, orphans)
        '/path/to/utils_orphan_analysis.md'
    """
    try:
        # Generate report filename
        base_name = os.path.splitext(os.path.basename(target_file))[0]
        report_dir = output_dir if output_dir else os.path.dirname(os.path.abspath(target_file))
        report_path = os.path.join(report_dir, f"{base_name}_orphan_analysis.md")
        
        # Calculate statistics
        total_functions = len(all_functions)
        orphan_count = len(orphan_functions)
        used_count = total_functions - orphan_count
        usage_rate = (used_count / total_functions * 100) if total_functions > 0 else 0
        
        # Create orphan set for quick lookup
        orphan_set = {func_name for func_name, _ in orphan_functions}
        
        # Generate markdown content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        markdown_content = f"""# Orphan Function Analysis Report

## Analysis Summary

- **Generated:** {timestamp}
- **Target File:** `{target_file}`
- **Codebase Path:** `{codebase_path}`

## Statistics

| Metric | Value |
|--------|-------|
| Total Functions | {total_functions} |
| Orphan Functions | {orphan_count} |
| Used Functions | {used_count} |
| Usage Rate | {usage_rate:.1f}% |

## Orphan Functions

"""
        
        if orphan_functions:
            markdown_content += "The following functions are defined but never called in the codebase:\n\n"
            markdown_content += "| Function Name | Line Number |\n"
            markdown_content += "|---------------|-------------|\n"
            for func_name, line_num in orphan_functions:
                markdown_content += f"| `{func_name}` | {line_num} |\n"
        else:
            markdown_content += "*No orphan functions found. All functions are used in the codebase.*\n"
        
        markdown_content += "\n## All Functions\n\n"
        markdown_content += "Complete list of all functions with their usage status:\n\n"
        markdown_content += "| Function Name | Line Number | Status |\n"
        markdown_content += "|---------------|-------------|--------|\n"
        
        for func_name, line_num in all_functions:
            status = "❌ Orphan" if func_name in orphan_set else "✅ Used"
            markdown_content += f"| `{func_name}` | {line_num} | {status} |\n"
        
        markdown_content += "\n## Recommendations\n\n"
        
        if orphan_functions:
            markdown_content += f"""Based on the analysis, {orphan_count} orphan function(s) were identified. Consider the following actions:

1. **Review Each Orphan Function:**
   - Determine if the function is truly unused or called dynamically
   - Check if it's part of a public API that external code might use
   - Verify it's not used via reflection or dynamic imports

2. **Possible Actions:**
   - **Remove:** Delete the function if it's confirmed to be unused
   - **Deprecate:** Mark for future removal if it's part of a public API
   - **Document:** Add comments explaining why it exists if it's intentionally unused
   - **Refactor:** Move to a utilities module if it might be useful later

3. **Code Maintenance:**
   - Consider setting up automated orphan detection in your CI/CD pipeline
   - Regularly review and clean up unused code to maintain codebase health
   - Update documentation to reflect removed functionality

### Orphan Functions to Review:

"""
            for func_name, line_num in orphan_functions:
                markdown_content += f"- `{func_name}` (line {line_num})\n"
        else:
            markdown_content += """Excellent! No orphan functions were found. Your codebase appears to be well-maintained with all functions in active use.

**Best Practices to Maintain:**
- Continue regular code reviews to catch unused code early
- Remove functions immediately when they're no longer needed
- Keep documentation up-to-date with actual code usage
"""
        
        markdown_content += "\n---\n\n*Report generated by Orphan Function Finder*\n"
        
        # Write report to file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return report_path
        
    except Exception as e:
        print(f"Error generating markdown report: {e}")
        return None


def generate_json_report(target_file, codebase_path, all_functions, orphan_functions, output_dir=None):
    """
    Generate a structured JSON report of the orphan function analysis.
    
    Creates a machine-readable JSON report containing all analysis data in a
    structured format. Useful for programmatic processing, integration with
    other tools, or automated workflows.
    
    Args:
        target_file (str): Path to the analyzed Python file
        codebase_path (str): Root path of the codebase that was searched
        all_functions (list): List of all (function_name, line_number) tuples
        orphan_functions (list): List of orphan (function_name, line_number) tuples
        output_dir (str, optional): Directory to save the report. Defaults to analyzed file's directory
    
    Returns:
        str: Path to the generated JSON report file
        None: If report generation failed
    
    JSON Structure:
        {
            "metadata": {
                "timestamp": "...",
                "analyzed_file": "...",
                "codebase_path": "..."
            },
            "statistics": {
                "total_functions": int,
                "orphan_count": int,
                "used_count": int,
                "usage_rate": float
            },
            "functions": [
                {
                    "name": "...",
                    "line_number": int,
                    "is_orphan": bool,
                    "is_used": bool
                }
            ],
            "orphan_functions": [
                {
                    "name": "...",
                    "line_number": int
                }
            ]
        }
    
    Examples:
        >>> generate_json_report('utils.py', '/project', functions, orphans)
        '/path/to/utils_orphan_analysis.json'
    """
    try:
        # Generate report filename
        base_name = os.path.splitext(os.path.basename(target_file))[0]
        report_dir = output_dir if output_dir else os.path.dirname(os.path.abspath(target_file))
        report_path = os.path.join(report_dir, f"{base_name}_orphan_analysis.json")
        
        # Calculate statistics
        total_functions = len(all_functions)
        orphan_count = len(orphan_functions)
        used_count = total_functions - orphan_count
        usage_rate = round((used_count / total_functions * 100), 2) if total_functions > 0 else 0
        
        # Create orphan set for quick lookup
        orphan_set = {func_name for func_name, _ in orphan_functions}
        
        # Build JSON structure
        report_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "analyzed_file": os.path.abspath(target_file),
                "codebase_path": os.path.abspath(codebase_path),
                "generator": "Orphan Function Finder v1.0"
            },
            "statistics": {
                "total_functions": total_functions,
                "orphan_count": orphan_count,
                "used_count": used_count,
                "usage_rate": usage_rate
            },
            "functions": [
                {
                    "name": func_name,
                    "line_number": line_num,
                    "is_orphan": func_name in orphan_set,
                    "is_used": func_name not in orphan_set
                }
                for func_name, line_num in all_functions
            ],
            "orphan_functions": [
                {
                    "name": func_name,
                    "line_number": line_num
                }
                for func_name, line_num in orphan_functions
            ],
            "summary": {
                "has_orphans": orphan_count > 0,
                "recommendation": "Review and remove unused functions" if orphan_count > 0 else "All functions are in use"
            }
        }
        
        # Write JSON to file with pretty formatting
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return report_path
        
    except Exception as e:
        print(f"Error generating JSON report: {e}")
        return None


def analyze_directory(directory_path, codebase_path):
    """
    Analyze all Python files in a directory for orphan functions.
    
    This function processes all Python files in the specified directory (non-recursive)
    and analyzes each file for orphan functions. Results are printed to the terminal
    instead of generating report files.
    
    Args:
        directory_path (str): Path to the directory containing Python files to analyze
        codebase_path (str): Root path of the codebase to search for function usage
    
    Returns:
        dict: Summary statistics containing:
            - files_analyzed (int): Number of Python files processed
            - total_functions (int): Total function count across all files
            - total_orphans (int): Total orphan function count across all files
    
    Examples:
        >>> analyze_directory('/path/to/modules/', '/path/to/project/')
        {'files_analyzed': 5, 'total_functions': 42, 'total_orphans': 3}
    
    Notes:
        - Only processes .py files in the specified directory (non-recursive)
        - Prints detailed results for each file to terminal
        - Skips files that cannot be read
        - Returns summary statistics for overall analysis
    """
    # Get all Python files in the directory (non-recursive)
    directory = Path(directory_path)
    py_files = [f for f in directory.iterdir() if f.is_file() and f.suffix == '.py']
    
    if not py_files:
        print(f"No Python files found in directory: {directory_path}")
        return {'files_analyzed': 0, 'total_functions': 0, 'total_orphans': 0}
    
    print(f"Found {len(py_files)} Python file(s) in directory.")
    print()
    
    # Track overall statistics
    total_files = 0
    total_functions_count = 0
    total_orphans_count = 0
    
    # Process each Python file
    for py_file in py_files:
        py_file_path = str(py_file)
        file_name = py_file.name
        
        print(f"Analyzing: {file_name}")
        
        # Extract functions from the file
        functions = extract_functions_from_file(py_file_path)
        
        if not functions:
            print("  No functions found")
            print("---")
            print()
            continue
        
        
        # Find orphan functions
        orphan_functions = []
        for func_name, line_num in functions:
            is_used = search_function_usage(func_name, codebase_path, py_file_path)
            if not is_used:
                orphan_functions.append((func_name, line_num))
        
        # Display orphan functions for this file
        if orphan_functions:
            print(f"  Orphan function(s): {len(orphan_functions)}")
            print(f"  Found {len(functions)} function(s)")
            print(f"  Summary for {file_name}: {len(functions)} total, {len(orphan_functions)} orphans")
            for func_name, line_num in orphan_functions:
                print(f"    - {func_name} (line {line_num})")

        
        print("---")
        print()
        
        # Update overall statistics
        total_files += 1
        total_functions_count += len(functions)
        total_orphans_count += len(orphan_functions)
    
    # Print overall summary
    print("=" * 60)
    print("OVERALL SUMMARY")
    print("=" * 60)
    print(f"Files analyzed: {total_files}")
    print(f"Total functions: {total_functions_count}")
    print(f"Total orphans: {total_orphans_count}")
    print()
    
    return {
        'files_analyzed': total_files,
        'total_functions': total_functions_count,
        'total_orphans': total_orphans_count
    }


def main():
    """
    Main entry point for the Orphan Function Finder script.
    
    This function orchestrates the entire workflow:
    1. Accepts command-line arguments or prompts user for input
    2. Validates the provided paths
    3. Processes either a single file or all Python files in a directory
    4. Searches for each function's usage in the codebase
    5. Identifies orphan functions
    6. Displays results (and optionally generates reports for single file mode)
    
    Command-Line Arguments:
        -p, --path: Path to Python file to check (single file mode)
        -d, --directory: Directory path to check all Python files (directory mode, non-recursive)
        -c, --codebase: Codebase path to search against
    
    Modes:
        Single File Mode (-p):
            - Analyzes one Python file
            - Offers to generate Markdown and JSON reports
            - Interactive prompts for file path and codebase (if not provided via args)
        
        Directory Mode (-d):
            - Analyzes all Python files in the specified directory (non-recursive)
            - Prints results to terminal only (no report generation)
            - Requires codebase path via -c or interactive prompt
            - Shows per-file results and overall summary
    
    Interactive Prompts:
        - Target Python file path: The file to analyze (if -p not provided in single file mode)
        - Codebase path: The root directory to search for function usage (if -c not provided)
        - Report generation: Ask if user wants to generate reports (single file mode only)
        - Output directory: Where to save the reports (single file mode only)
    
    Output:
        Single File Mode:
            - Prints analysis results
            - Optional Markdown and JSON reports
        
        Directory Mode:
            - Per-file results showing orphan functions
            - Overall summary with total statistics
    
    Returns:
        None
        
    Examples:
        >>> main()  # Interactive mode
        >>> python script.py -p utils.py -c /project/src  # Single file mode
        >>> python script.py -d /project/modules -c /project  # Directory mode
    
    Notes:
        - -p and -d are mutually exclusive
        - Exits early if inputs are invalid
        - Handles cases where no functions or no orphans are found
        - Provides clear feedback at each step
        - Does not modify the original source file
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Find orphan functions in Python files')
    parser.add_argument('-p', '--path', type=str, help='Path to Python file to check')
    parser.add_argument('-d', '--directory', type=str, help='Directory path to check all Python files (non-recursive)')
    parser.add_argument('-c', '--codebase', type=str, help='Codebase path to search against')
    args = parser.parse_args()
    
    print("=" * 60)
    print("Orphan Function Finder")
    print("=" * 60)
    print()
    
    # Step 1: Check for mutual exclusivity between -p and -d
    if args.path and args.directory:
        print("Error: Cannot use both -p/--path and -d/--directory options together.")
        print("Please use either -p for a single file or -d for a directory.")
        return
    
    # Step 2: Handle directory mode (-d flag)
    if args.directory:
        directory_path = args.directory
        
        # Validate directory exists
        if not os.path.isdir(directory_path):
            print(f"Error: Directory '{directory_path}' does not exist.")
            return
        
        # Get codebase path (required for directory mode)
        if args.codebase:
            codebase_path = args.codebase
        else:
            codebase_path = input("Enter the codebase path to search against: ").strip()
        
        # Validate codebase path
        if not os.path.isdir(codebase_path):
            print(f"Error: Codebase path '{codebase_path}' does not exist.")
            return
        
        print()
        # Analyze directory
        analyze_directory(directory_path, codebase_path)
        
        print("=" * 60)
        print("Analysis complete.")
        print("=" * 60)
        return
    
    # Step 3: Handle single file mode (existing logic)
    # Get user inputs (from CLI args or interactive prompts)
    if args.path:
        target_file = args.path
    else:
        target_file = input("Enter the Python file path to check: ").strip()
    
    if args.codebase:
        codebase_path = args.codebase
    else:
        codebase_path = input("Enter the codebase path to search against: ").strip()
    
    # Step 4: Validate inputs before proceeding
    if not os.path.isfile(target_file):
        print(f"Error: Target file '{target_file}' does not exist.")
        return
    
    if not os.path.isdir(codebase_path):
        print(f"Error: Codebase path '{codebase_path}' does not exist.")
        return
    
    print()
    print("Analyzing functions...")
    print()
    
    # Step 3: Extract all function definitions from the target file
    functions = extract_functions_from_file(target_file)
    
    if not functions:
        print("No functions found in the target file.")
        return
    
    print(f"Found {len(functions)} function(s) in the target file.")
    print()
    
    # Step 4: Check each function to see if it's used anywhere in the codebase
    orphan_functions = []  # List of (function_name, line_number) tuples
    orphan_lines = set()   # Set of line numbers for efficient lookup
    
    for func_name, line_num in functions:
        is_used = search_function_usage(func_name, codebase_path, target_file)
        if not is_used:
            # Function is not called anywhere - it's an orphan
            orphan_functions.append((func_name, line_num))
            orphan_lines.add(line_num)
    
    # Step 5: Display results
    if orphan_functions:
        print(f"Found {len(orphan_functions)} orphan function(s):")
        print()
        for func_name, line_num in orphan_functions:
            print(f"  - {func_name} (line {line_num})")
        print()
    else:
        print("No orphan functions found! All functions are used in the codebase.")
        print()
    
    # Step 6: Ask user if they want to generate reports
    generate_reports = input("Do you want to generate analysis reports? (y/n): ").strip().lower()
    
    if generate_reports in ['y', 'yes']:
        # Ask for output directory
        default_dir = os.path.dirname(os.path.abspath(target_file))
        print(f"\nDefault output directory: {default_dir}")
        output_dir = input("Enter the directory path to save reports (press Enter for default): ").strip()
        
        if not output_dir:
            output_dir = default_dir
        
        # Validate output directory
        if not os.path.isdir(output_dir):
            print(f"Warning: Directory '{output_dir}' does not exist. Attempting to create it...")
            try:
                os.makedirs(output_dir, exist_ok=True)
                print(f"✓ Directory created: {output_dir}")
            except Exception as e:
                print(f"✗ Failed to create directory: {e}")
                print(f"Using default directory: {default_dir}")
                output_dir = default_dir
        
        print()
        print("Generating analysis reports...")
        print()
        
        # Generate Markdown report
        md_report_path = generate_markdown_report(target_file, codebase_path, functions, orphan_functions, output_dir)
        if md_report_path:
            print(f"✓ Markdown report saved: {md_report_path}")
        else:
            print("✗ Failed to generate Markdown report")
        
        # Generate JSON report
        json_report_path = generate_json_report(target_file, codebase_path, functions, orphan_functions, output_dir)
        if json_report_path:
            print(f"✓ JSON report saved: {json_report_path}")
        else:
            print("✗ Failed to generate JSON report")
        
        print()
    else:
        print("\nSkipping report generation.")
        print()
    
    print("=" * 60)
    print("Analysis complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

