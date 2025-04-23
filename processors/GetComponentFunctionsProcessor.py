import os
import re
from fs.File import File
from processors.CodeProcessor import CodeProcessor

class GetComponentFunctionsProcessor(CodeProcessor):
    """
    This class processes files in a directory to extract information about components and their methods.
    It looks for patterns in the code (e.g., server.CreateObject), extracts the relevant details, and
    exports the results to an Excel file, appending new results if the file already exists.
    """
    def __init__(self, directory_path, excluded_words=None, omit_directories=[]):
        """
        Initialize the processor with directory_path and optional excluded_words.
        """
        if excluded_words is None:
            excluded_words = []
        # Call the parent constructor with appropriate arguments
        super().__init__(
            directory_path,
            allowed_extensions=['asp'],
            excluded_words=excluded_words,
            omit_directories=omit_directories
        )


    def _process_file(self, file_name):
        """
        Process a single file to extract variable declarations, class names, and function calls.
        
        Args:
            file_name (str): The name of the file to process.

        Returns:
            list: A list of dictionaries with file path, file name, line number, line content,
                  class/component name, and function name.
        """
        variables = []  # List to store variable names
        classes = []    # List to store class names
        results = []    # List to store results for the current file

        # Regex pattern to match server.CreateObject declarations
        declare_pattern = r"^(?!\s*'+).*\b(\w+)\s*=\s*server\.CreateObject\s*\(\s*\"([^\"]+)\"\s*\)"
        declare_regex = re.compile(declare_pattern, re.IGNORECASE)

        # Get the ASP code lines from the file
        lines = CodeProcessor.extract_asp_code(file_name)

        # Process each line in the file
        for line in lines:
            match = declare_regex.search(line)
            if match:
                variable_name = match.group(1)  # The name of the variable (e.g., "varName")
                class_name = match.group(2)     # The class name used in CreateObject (e.g., "DataCompGeneral.clasegeneral")
                
                variables.append(variable_name)
                classes.append(class_name)

            # Check if any declared variables are used in method calls
            for i, variable in enumerate(variables):
                function_pattern = rf"(?<=\b{variable}\.)\w+"
                function_regex = re.compile(function_pattern, re.IGNORECASE)
                
                function_match = function_regex.search(line) 

                if function_match:
                    function_name = function_match.group(0) # The name of the method called

                    # Check if the function is not in the excluded words list (case insensitive)
                    if not any(excluded.lower() in function_name.lower() for excluded in self.excluded_words):
                        results.append({
                            "File path": file_name,
                            "File name": File.get_file_name(file_name),  # Extract only the file name
                            "Module": File.get_last_subdirectory(file_name),
                            "Line": line, 
                            "Component": classes[i],
                            "Function": function_name
                        })

        print(f"File name: {file_name} processed.")
        return results

