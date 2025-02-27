# Text to Excel conversor

# Used to convert the .txt output from `detector-py-v2.py` to an excel file

import pandas as pd
import re

# Define the input and output file paths
input_file = "resultados-reales/store-proc-list-2025-01-30T12-25-50.txt"  # Change to your actual file path
output_file = "output.xlsx"

# Read the text file
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize a list to store parsed data
data = []

# Define regex pattern to extract the table columns
col_pattern = re.compile(r"^(.+?)\s+\|\s+(.+?)\s+\|\s+(\d+)\s+\|\s+(.+)$")

# Define regex pattern to extract the argument of the createobject function
func_pattern = r'server\.CreateObject\(["\']([^"\']+)["\']\)'

# Define regex pattern to extract the module name
mod_pattern = r"^(?:\.\./|/)?([^/]+)/([^/]+)/"

# Process each line after the header
for line in lines[2:]:  # Skip the first two lines (headers and separator)
    cols = col_pattern.match(line.strip())
    if cols:
        full_path, file_name, line_number, code_line = cols.groups()

        # Get argument of createObject function
        func_match = re.search(func_pattern, code_line, re.IGNORECASE)
        func = func_match.group(1) if func_match else ""

        # Get module name
        normalized_path = full_path.replace("\\", "/")
        mod_match = re.search(mod_pattern, normalized_path)

        root_folder = mod_match.group(1) 
        second_folder = mod_match.group(2) 

        module = second_folder if root_folder.lower() == "trilay" else "root"

        # Create the data entry
        data.append([
            full_path.strip(),
            file_name.strip(),
            int(line_number.strip()),
            code_line.strip(),
            func,
            module,
        ])

# Create a DataFrame
columns = ["Path", "File", "Line Number", "Code Line", "Function", "Module"]
df = pd.DataFrame(data, columns=columns)

# Export to Excel
try:
    df.to_excel(output_file, index=False, engine="openpyxl")
except Exception as e:
    print(f"An error occured, did you close {output_file}?")
    raise e
finally:
    print(f"Data successfully exported to {output_file}")