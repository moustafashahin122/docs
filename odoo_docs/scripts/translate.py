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
module_path = input("Enter the path of the module: ")
# copy the file in the module path /i18n/ *.pot   to file po
i18n_folder = module_path + "/i18n/"

# for filename in os.listdir(i18n_folder):
#     # ask if user if he wants to translate each



#     if filename.endswith(".pot"):
#         pot_file_path = os.path.join(i18n_folder, filename)
#         po_file_path = os.path.join(i18n_folder, filename.replace(".pot", ".po"))
        
#         # Copy the .pot file to .po
#         shutil.copyfile(pot_file_path, po_file_path)
#         print(f"Copied {pot_file_path} to {po_file_path}")

# print("All .pot files have been copied and renamed to .po files.")

# def run_awaited(fro, to, src, dest):
#     return await run(fro=fro, to=to, src=src, dest=dest)

asyncio.run(run(fro="en", to="ar" ,src=i18n_folder, dest=i18n_folder))