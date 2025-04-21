from abc import ABC, abstractmethod
import pandas as pd
import os
import re
from fs.Directory import Directory
from fs.File import File

class CodeProcessor(ABC):
    """
    Abstract base class for processing code files, extracting component functions, and exporting results.
    """

    def __init__(self, directory_path, allowed_extensions, excluded_words):
        """
        Initializes the CodeProcessor with the directory to process, allowed file extensions,
        and the excluded words for function names.
        """
        self.directory_path = directory_path
        self.allowed_extensions = allowed_extensions
        self.excluded_words = excluded_words
        self.results = None

    @abstractmethod
    def _process_file(self, file_name):
        """
        Abstract method to process a single file. Must be implemented by subclasses.
        """
        pass

    @staticmethod
    def extract_asp_code(file_path):
        """
        Extracts ASP code wrapped between `<%` and `%>` from a given file. This method reads the file line-by-line, 
        processes the content to capture all ASP code blocks, and returns a list of all ASP code found in the file.

        This method is particularly useful for extracting server-side ASP code that is embedded within HTML or script files.

        Args:
            file_path (str): The path to the file from which to extract ASP code.

        Returns:
            list: A list of strings where each string contains a segment of the ASP code 
                  found between `<%` and `%>`. Each ASP code block is stripped of extra whitespaces 
                  and empty lines, ensuring clean results.
        
        Example:
            Given a file containing:
                <%
                    var x = 10;
                    var y = 20;
                %>
                this isnt in the output
                <%
                    if (x > y) {
                        var z = 30;
                    }
                %>

            The method will return:
                ['var x = 10;', 'var y = 20;', 'if (x > y) {', 'var z = 30;', '}']

        Raises:
            FileNotFoundError: If the file at `file_path` does not exist.
            IOError: If an error occurs while reading the file.
        """

        # Create a regex pattern to match the ASP code delimited by <% and %>
        pattern = r"<%=?(.*?)%>"

        # Buffer to temporally store unchecked code
        asp_code_buffer = ""

        # Array that will keep the ASP lines of codes that were found
        asp_code = []
        
        file = File(file_path)

        # Read ASP file line by line
        for line in file.get_lines():
            # Add the current line to the buffer
            asp_code_buffer += " " + line
            
            # If we detect that the buffer contains a full ASP code block, process it
            if "%>" in asp_code_buffer:
                matches = re.findall(pattern, asp_code_buffer, re.DOTALL)

                for match in matches:
                    # Split the string into lines
                    asp_lines = match.split("\n")
                    # Remove empty lines
                    asp_lines = [asp_line.strip() for asp_line in asp_lines if asp_line.strip()]

                    asp_code += asp_lines
                
                # Clear the buffer after processing the match
                asp_code_buffer = ""

        return asp_code

 

    @staticmethod
    def export_to_excel(content, output_file, overwrite=True):
        """
        Export the results to an Excel file.

        Args:
            content (list): The results to export.
            output_file (str): The path to the output Excel file.
            overwrite (bool): If False, appends to the existing file. Defaults to True.
        """
        if output_file is None:
            raise ValueError("Output file is not defined")

        df = pd.DataFrame(content)

        if not overwrite and os.path.exists(output_file):
            # If the file exists, read the existing file
            existing_df = pd.read_excel(output_file)

            # Concatenate the new results with the existing ones
            updated_df = pd.concat([existing_df, df], ignore_index=True)

            # Write the updated DataFrame back to the Excel file
            updated_df.to_excel(output_file, index=False)
        else:
            # If the file doesn't exist, create a new file
            df.to_excel(output_file, index=False)


    def get_results(self):
        """
        Get the results from processing the files in the directory.

        Returns:
            list: All results processed across the files.
        """
        if self.results is not None:
            return self.results

        directory = Directory(self.directory_path)

        # List to accumulate all results
        all_results = []

        # Process files in the directory
        for file_name in directory.get_files_by_extensions(self.allowed_extensions):
            results = self._process_file(file_name)
            all_results.extend(results)  # Add results of the current file to the main results list

        self.results = all_results
        return self.results

    def process_and_export_results(self, output_file):
        """
        Process files and directly export the results to the Excel file without storing them in memory.

        This method is useful when processing a large number of files and we don't want to
        store them in memory, but only write them to the output file.
        """
        if output_file is None:
            raise ValueError("Output file is not defined")

        directory = Directory(self.directory_path)

        for file_name in directory.get_files_by_extensions(self.allowed_extensions):
            results = self._process_file(file_name)

            if len(results) > 0:
                self.export_to_excel(results, output_file, overwrite=False)
