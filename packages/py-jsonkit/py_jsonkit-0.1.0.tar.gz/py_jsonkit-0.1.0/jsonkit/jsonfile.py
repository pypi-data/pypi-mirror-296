import json
import os

from rich.console import Console

from jsonkit.codec import CustomJSONDecoder, CustomJSONEncoder
from jsonkit.custom_types import JSONData

console = Console()


class JSONFile:
    """
    A class for handling JSON file operations synchronously.

    Attributes:
        filepath (str): Path to the JSON file.

    Methods:
        load(**kwargs) -> JSONData:
            Loads the JSON data from the file.

        write(data: JSONData, **kwargs) -> JSONData:
            Writes JSON data to the file and returns the loaded data.

    """

    def __init__(self, filepath: str):
        """
        Initializes the JSONFile instance and creates the file if it does not exist.

        Args:
            filepath (str): Path to the JSON file.

        """
        self.filepath = filepath

        if not os.path.exists(self.filepath):
            self.write({})

    def load(self, **kwargs) -> JSONData:
        """
        Loads JSON data from the file.

        Args:
            **kwargs: Additional keyword arguments to pass to json.load

        Returns:
            JSONData: The JSON data loaded from the file.
        """
        with open(self.filepath, "r") as file:
            return json.load(file, cls=CustomJSONDecoder, **kwargs)

    def write(self, data: JSONData, **kwargs) -> JSONData:
        """
        Writes JSON data to the file and returns the loaded data.

        Args:
            data (JSONData): The JSON data to write to the file.
            **kwargs: Additional keyword arguments to pass to json.dump

        Returns:
            JSONData: The JSON data loaded from the file.
        """
        with open(self.filepath, "w") as file:
            json.dump(data, file, cls=CustomJSONEncoder, **kwargs)

        return self.load()

    def print_data(self, **kwargs):
        console.print_json(data=self.load(), **kwargs)
