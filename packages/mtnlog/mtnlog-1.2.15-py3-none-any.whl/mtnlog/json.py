"""
JSONLogger Module
=================
This module provides the `JSONLogger` class for serializing Python objects to JSON format and logging them to files.

The `JSONLogger` class allows for flexible serialization of various Python objects, including handling non-serializable 
types by converting them into string representations. It can be used to log data into a specified directory, ensuring 
the data is stored in a readable JSON format.

Classes:
--------
- JSONLogger: A class for logging Python objects into JSON files, with support for custom serialization of 
              non-serializable types.

Dependencies:
-------------
- `json`: For handling JSON serialization.
- `os`: For file and directory management.
- `typing`: For type annotations.
"""

import json
import os
from typing import Any, Union, Dict, List, TypeVar

# Define generic type variables
K = TypeVar('K')
V = TypeVar('V')


class JSONLogger:
    """
    JSONLogger
    ==========
    A logger class that serializes Python objects into JSON format and saves them to a specified directory.

    This class provides functionality to log any Python object into a JSON file. It includes custom serialization 
    methods to handle non-serializable objects, converting them into a string representation to ensure they can 
    be saved in JSON format.

    Attributes:
    -----------
    - log_dir (str): The directory where log files will be saved. If it doesn't exist, it will be created.
    """

    def __init__(self, log_dir: str) -> None:
        """
        Initializes the JSONLogger with a directory to store log files.

        Parameters:
        -----------
        - log_dir (str): The directory where JSON log files will be saved. If the directory 
                         does not exist, it will be created.
        """
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir: str = log_dir

    def serialize(
        self, obj: Any
    ) -> Union[Dict[str, Any], List[Any], int, float, str, bool, None]:
        """
        Recursively serializes Python objects into a format compatible with JSON.

        This method converts complex or non-serializable objects into a form that can be easily serialized to JSON. 
        For example, it converts dictionaries and lists containing non-serializable types into a string representation.

        Parameters:
        -----------
        - obj (Any): The Python object to be serialized.

        Returns:
        --------
        - Union[Dict[str, Any], List[Any], int, float, str, bool, None]: A JSON-compatible representation of the 
                                                                         input object, with non-serializable elements 
                                                                         converted to strings.
        """
        if isinstance(obj, dict):
            return {k: self.serialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.serialize(v) for v in obj]
        if isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        # Convert non-serializable objects to their string representation
        return str(obj)

    def log(self, obj: Any, filename: str = "log") -> None:
        """
        Logs the given Python object into a JSON file.

        This method takes any Python object, serializes it into JSON format using the `serialize` method, 
        and writes it to a file in the specified log directory.

        Parameters:
        -----------
        - obj (Any): The Python object to be logged.
        - filename (str): The name of the file (without extension) where the log will be saved. Defaults to "log".

        Raises:
        -------
        - IOError: If the file cannot be written to the specified directory.
        """
        with open(f"{self.log_dir}/{filename}.json", "w", encoding='utf-8') as f:
            json.dump(self.serialize(obj), f, ensure_ascii=False, indent=4)
