# ask for the source and destination paths from user input


# import json
# import re

# def remove_comments(json_like_str):
#     """Remove comments from VS Code config (// style)."""
#     # Remove single-line comments
#     json_like_str = re.sub(r'//.*?\n', '\n', json_like_str)
#     # Remove multi-line comments
#     json_like_str = re.sub(r'/\*.*?\*/', '', json_like_str, flags=re.S)
    
#     # Remove trailing commas before closing braces or brackets
#     json_like_str = re.sub(r',\s*([\]}])', r'\1', json_like_str)
    
#     # Remove trailing commas in lists (new)
#     json_like_str = re.sub(r',\s*([}\]])', r'\1', json_like_str)

#     return json_like_str

# def load_vscode_config(file_path):
#     """Load a VS Code configuration file by removing comments."""
#     with open(file_path, 'r') as file:
#         content = file.read()
    
#     # Remove the comments before parsing the content
#     cleaned_content = remove_comments(content)
    
#     # Now parse the cleaned JSON-like string
#     print(cleaned_content)
#     config = json.loads(cleaned_content)
#     return config





# import subprocess

# # Define the path to your odoo-bin file
# odoo_bin_path = '/path/to/odoo/odoo-bin'

# # Define the parameters and options for running Odoo
# args = [
#     odoo_bin_path,             # Path to odoo-bin
#     '-c', '/path/to/odoo.conf'  # Path to your Odoo configuration file
# ]

# # Start Odoo using subprocess
# process = subprocess.Popen(args)

# # Optional: Wait for the process to complete
# process.wait()









# # Example usage
# config_path = '/opt/work_code/odoo_15/.vscode/launch.json'  # Replace with the actual path
# config = load_vscode_config(config_path)

# # Access parts of the configuration
# print(config["version"])  # Example to print the version
# print(config["configurations"][0]["name"])  # Example to print the configuration name







import asyncio





import os
import shutil
from translate_po.main import run

# Ask user for translation mode
mode = input("Choose mode (1: Translate entire module, 2: Translate single file): ")

if mode == "1":
    # Translate entire module
    module_path = input("Enter the path of the module: ")
    i18n_folder = module_path + "/i18n/"
    asyncio.run(run(fro="en", to="ar", src=i18n_folder, dest=i18n_folder))
elif mode == "2":
    # Translate single file
    file_path = input("Enter the path of the .po/.pot file: ")
    if os.path.isfile(file_path):
        # Create temporary directory
        temp_dir = "temp123"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # Copy file to temp directory
        file_name = os.path.basename(file_path)
        temp_file_path = os.path.join(temp_dir, file_name)
        shutil.copy2(file_path, temp_file_path)
        
        # Run translation on temp directory
        asyncio.run(run(fro="en", to="ar", src=temp_dir, dest=temp_dir))
        
        # Copy translated file back to original location
        translated_file = temp_file_path.replace('.pot', '.po') if temp_file_path.endswith('.pot') else temp_file_path
        if os.path.exists(translated_file):
            original_translated_path = file_path.replace('.pot', '.po') if file_path.endswith('.pot') else file_path
            shutil.copy2(translated_file, original_translated_path)
        
        # Remove temp directory
        shutil.rmtree(temp_dir)
    else:
        print("Error: File not found!")
else:
    print("Invalid mode selected!")