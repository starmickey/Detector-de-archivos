from datetime import datetime
import sys
import os

# Import files from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.detector_py2 import get_files, filter_files_and_export_txt

if __name__ == "__main__":
    directory = "test"
    timestamp = datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
    txt_output_file = "store-proc-list-{}.txt".format(timestamp)
    file_pattern = ".asp"
    search_pattern = r"Server\.CreateObject\(['\"]([^'\"]+)['\"]\)"
    excluded_words = {"datacompbd", "datacompgeneral", "abcupload4", "aspsmartupload", "control_licencia"}
    
    asp_files = get_files(directory, file_pattern)
    print("ASP files", asp_files)
    
    if asp_files:
        filter_files_and_export_txt(asp_files, search_pattern, excluded_words, txt_output_file)
    else:
        print("No matching files found.")