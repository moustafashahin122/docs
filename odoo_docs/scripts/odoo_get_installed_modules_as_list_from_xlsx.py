import pandas as pd

# Read the Excel files
# get the path from the user input for live environment
live_path = input("Enter the path of the Live Excel file: ")
live_df = pd.read_excel(live_path)

# get the path from the user input for stage environment
stage_path = input("Enter the path of the Stage Excel file: ")
stage_df = pd.read_excel(stage_path)

# Convert the "Technical Name" column to lists
live_modules = live_df["Technical Name"].tolist()
stage_modules = stage_df["Technical Name"].tolist()

# Merge the module names and remove duplicates
all_modules = list(set(live_modules + stage_modules))

# Sort the list for better readability
all_modules.sort()

# Format and print the list in the requested format
formatted_list = "(" + " ".join(f'"{item}"' for item in all_modules) + ")"
print(formatted_list)
