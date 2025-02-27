from datetime import datetime
import sys
import os

# Import files from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.detector_py3 import get_files, filter_files_by_pattern, export_results_to_excel

if __name__ == "__main__":
    directory = "ejemplos"
    output_file = f"store-proc-list-{datetime.today().strftime('%Y-%m-%dT%H-%M-%S')}.xlsx"
    file_pattern = ".asp"
    search_pattern = r'Server\.CreateObject\([\'"]([^\'"]+)[\'"]\)'
    excluded_words = {"datacompbd", "datacompgeneral", "abcupload4", "aspsmartupload", "control_licencia"}
    
    asp_files = get_files(directory, file_pattern)

    print("ASP files", asp_files)
    
    results = filter_files_by_pattern(asp_files, search_pattern, excluded_words)

    if results:
        export_results_to_excel(results, output_file)
    else:
        print("No matching lines found.")
