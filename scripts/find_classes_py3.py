from datetime import datetime
import sys
import os

# Import files from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.detector_py3 import get_files, filter_files_by_pattern, export_results_to_excel

if __name__ == "__main__":
    directory = "test/input"
    output_file = f"test/output/classes-{datetime.today().strftime('%Y-%m-%dT%H-%M-%S')}.xlsx"
    file_pattern = ".asp"
    search_pattern = r'\bclass\s*=\s*["\']([^"\'>]+)["\']'
    excluded_words = {}
    
    asp_files = get_files(directory, file_pattern)

    print("ASP files found", asp_files)
    
    results = filter_files_by_pattern(asp_files, search_pattern, excluded_words, start_flag="html")

    export_results_to_excel(results, output_file)


