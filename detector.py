import os
import re
import pandas as pd
from datetime import datetime

def get_files(directory, file_pattern):
    files_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(file_pattern):
                files_list.append(os.path.join(root, file))
    return files_list

def filter_files_by_pattern(files, pattern, excluded_words):
    results = []
    compiled_pattern = re.compile(pattern, re.IGNORECASE)
    
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                for line_number, line in enumerate(lines, start=1):
                    match = compiled_pattern.search(line)
                    if match:
                        object_name = match.group(1).lower()
                        if not any(excluded in object_name for excluded in excluded_words):
                            results.append([os.path.basename(file_path), line_number, line.strip()])
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return results

def export_results_to_excel(results, output_file):
    df = pd.DataFrame(results, columns=["File", "Line Number", "Code Line"])
    df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    directory = "ejemplos"
    output_file = f"store-proc-list-{datetime.today().strftime('%Y-%m-%dT%H-%M-%S')}.xlsx"
    file_pattern = ".asp"
    search_pattern = r'Server\.CreateObject\([\'"]([^\'"]+)[\'"]\)'
    excluded_words = {"datacompbd", "datacompgeneral", "abcupload4", "aspsmartupload", "control_licencia"}
    
    asp_files = get_files(directory, file_pattern)
    results = filter_files_by_pattern(asp_files, search_pattern, excluded_words)

    if results:
        export_results_to_excel(results, output_file)
    else:
        print("No matching lines found.")
