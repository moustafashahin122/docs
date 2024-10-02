# ask for the source and destination paths from user input
import os
import shutil
from translate_po.main import run
module_path = input("Enter the path of the module: ")
# copy the file in the module path /i18n/ *.pot   to file po
i18n_folder = module_path + "/i18n/"

for filename in os.listdir(i18n_folder):
    if filename.endswith(".pot"):
        pot_file_path = os.path.join(i18n_folder, filename)
        po_file_path = os.path.join(i18n_folder, filename.replace(".pot", ".po"))
        
        # Copy the .pot file to .po
        shutil.copyfile(pot_file_path, po_file_path)
        print(f"Copied {pot_file_path} to {po_file_path}")

print("All .pot files have been copied and renamed to .po files.")

run(fro="en", to="ar" ,src=i18n_folder, dest=i18n_folder)