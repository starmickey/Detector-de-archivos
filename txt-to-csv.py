# Text to Excel conversor

# Used to convert the .txt output from `detector-py-v2.py` to an excel file

import pandas as pd
import re

# Define the input and output file paths
input_file = "data.txt"  # Change to your actual file path
output_file = "output.xlsx"

# Read the text file
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Initialize a list to store parsed data
data = []

# Define regex pattern to extract required information
pattern = re.compile(r"^(.+?)\s+\|\s+(.+?)\s+\|\s+(\d+)\s+\|\s+(.+)$")

# Process each line after the header
for line in lines[2:]:  # Skip the first two lines (headers and separator)
    match = pattern.match(line.strip())
    if match:
        full_path, file_name, line_number, code_line = match.groups()
        data.append([full_path.strip(), file_name.strip(), int(line_number.strip()), code_line.strip()])

# Create a DataFrame
columns = ["Path", "File", "Line Number", "Code Line"]
df = pd.DataFrame(data, columns=columns)

# Export to Excel
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"Data successfully exported to {output_file}")