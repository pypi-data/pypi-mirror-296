import json
import os

from rich.console import Console
import aiofiles

from jsonkit.custom_types import JSONData
from jsonkit.codec import CustomJSONDecoder, CustomJSONEncoder

console = Console()


class AsyncJSONFile:
    """
    A class for handling JSON file operations asynchronously.

    Attributes:
        filepath (str): Path to the JSON file.

    Methods:
        load(**kwargs) -> JSONData:
            Asynchronously loads the JSON data from the file.

        write(data: JSONData, **kwargs) -> None:
            Asynchronously writes JSON data to the file and returns the loaded data.
    """

    def __init__(self, filepath: str):
        """
        Initializes the AsyncJSONFile instance and creates the file if it does not exist.

        Args:
            filepath (str): Path to the JSON file.
        """
        self.filepath = filepath

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as file:
                json.dump({}, file)

    async def load(self, **kwargs) -> JSONData:
        """
        Asynchronously loads JSON data from the file.

        Args:
            **kwargs: Additional keyword arguments to pass to json.loads.

        Returns:
            JSONData: The JSON data loaded from the file.
        """
        async with aiofiles.open(self.filepath, "r") as file:
            contents = await file.read()
            return json.loads(contents, cls=CustomJSONDecoder, **kwargs)

    async def write(self, data: JSONData, **kwargs) -> JSONData:
        """
        Asynchronously writes JSON data to the file and returns the loaded data.

        Args:
            data (JSONData): The JSON data to write to the file.
            **kwargs: Additional keyword arguments to pass to json.dumps.

        Returns:
            JSONData: The JSON data loaded from the file.
        """
        async with aiofiles.open(self.filepath, "w") as file:
            await file.write(json.dumps(data, cls=CustomJSONEncoder, **kwargs))

        return await self.load()

    async def print_data(self, **kwargs):
        data = await self.load()
        console.print_json(data=data, **kwargs)
