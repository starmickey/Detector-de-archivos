import os
import re
import pandas as pd

def get_files(directory, file_pattern):
    files_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(file_pattern):
                files_list.append(os.path.join(root, file))
    return files_list

def is_in_phrase(flag, text):
    """Checks if a flag word appears as a whole word in the given text."""
    flag_pattern = rf'(?<!\w){re.escape(flag)}(?!\w)'
    return bool(re.search(flag_pattern, text, re.IGNORECASE))

def filter_files_by_pattern(files, pattern, excluded_words, start_flag=None):
    """
    Searches for a regex pattern in files but only after the start_flag has been found.
    
    Parameters:
    - files (list): List of file paths to search in.
    - pattern (str): Regex pattern to search for.
    - excluded_words (list): Words to exclude from matches.
    - start_flag (str, optional): If provided, search starts after this flag appears.
    
    Returns:
    - DataFrame: Matching results with file name, line number, and code line.
    """
    results = []
    compiled_pattern = re.compile(pattern, re.IGNORECASE)

    for file_path in files:
        try:
            flag_found = start_flag is None  # If no start_flag, search starts immediately
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_number, line in enumerate(f, start=1):
                    if not flag_found:
                        flag_found = is_in_phrase(start_flag, line)
                        if not flag_found:
                            continue  # Skip lines until start_flag is found
                    

                    # Search for pattern in the line
                    matches = compiled_pattern.findall(line)
                    # match = compiled_pattern.search(line)
                    for match in matches:
                        if not any(excluded in match for excluded in excluded_words):
                            results.append([os.path.basename(file_path), line_number, line.strip(), match])
        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    # Convert results to a DataFrame if not empty
    results_df = pd.DataFrame(results, columns=["File", "Line Number", "Code Line", "Match"])
    return results_df

def export_results_to_excel(results, output_file):
    results.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")
