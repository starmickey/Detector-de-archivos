# -*- coding: utf-8 -*-

# Detector adaptado para Python 2

import os
import re
import io
import csv
from datetime import datetime

def get_files(directory, file_pattern):
    files_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(file_pattern):
                files_list.append(os.path.join(root, file))
    return files_list

def filter_files_and_export_txt(files, pattern, excluded_words, output_file):
    compiled_pattern = re.compile(pattern, re.IGNORECASE)
    
    with io.open(output_file, "w", encoding="utf-8") as f:
        f.write(u"Full Path | File | Line Number | Code Line\n")
        f.write(u"-" * 80 + "\n")
        
        for file_path in files:
            try:
                with io.open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    lines = file.readlines()
                    for line_number, line in enumerate(lines, start=1):
                        match = compiled_pattern.search(line)
                        if match:
                            object_name = match.group(1).lower()
                            if not any(excluded in object_name for excluded in excluded_words):
                                f.write(u"{} | {} | {} | {}\n".format(
                                    file_path.decode("utf-8"), 
                                    os.path.basename(file_path).decode("utf-8"), 
                                    line_number, 
                                    line.strip().decode("utf-8")
                                ))
            except Exception as e:
                print("Error reading {}: {}".format(file_path, e))
    
    print("Results saved to {}".format(output_file))

if __name__ == "__main__":
    directory = "../trilay"
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
