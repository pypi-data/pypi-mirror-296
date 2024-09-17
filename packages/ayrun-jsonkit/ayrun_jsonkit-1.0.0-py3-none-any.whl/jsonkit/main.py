import json
import os
from typing import Dict, Any, TypeAlias
from datetime import datetime
import uuid

import aiofiles

JSONData: TypeAlias = Dict[
    str, str | int | bool | datetime | uuid.UUID
]


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
    def __init__(self, filepath: str) -> None:
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
        with open(self.filepath, 'r') as file:
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
        with open(self.filepath, 'w') as file:
            json.dump(data, file, cls=CustomJSONEncoder, **kwargs)
            
        return self.load()
 

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
    def __init__(self, filepath: str) -> None:
        """
        Initializes the AsyncJSONFile instance and creates the file if it does not exist.

        Args:
            filepath (str): Path to the JSON file.
        """       
        self.filepath = filepath

        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as file:
                json.dump({}, file)

    async def load(self, **kwargs) -> JSONData:
        """
        Asynchronously loads JSON data from the file.

        Args:
            **kwargs: Additional keyword arguments to pass to json.loads.

        Returns:
            JSONData: The JSON data loaded from the file.
        """
        async with aiofiles.open(self.filepath, 'r') as file:
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
        async with aiofiles.open(self.filepath, 'w') as file:
            await file.write(json.dumps(data, cls=CustomJSONEncoder, **kwargs))

        return await self.load()


class CustomJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for serializing datetime and UUID objects.

    Methods:
        default(obj):
            Converts datetime and UUID objects to a serializable format.
    """
    def default(self, obj: Any):
        """
        Converts objects to a serializable format.

        Args:
            obj (Any): The object to convert.

        Returns:
            dict | Any: A dictionary representation of datetime and UUID objects
            and the default serialization of other objects.
        """
        if isinstance(obj, datetime):
            return {"__type__": "datetime", "__value__": obj.isoformat()}

        elif isinstance(obj, uuid.UUID):
            return {"__type__": "uuid", "__value__": str(obj)}

        return super().default(obj)


class CustomJSONDecoder(json.JSONDecoder):
    """
    A custom JSON decoder for deserializing datetime and UUID objects.

    Methods:
        custom_object_hook(dct):
            Converts dictionaries with special type markers back into datetime and UUID objects.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the CustomJSONDecoder with a custom object hook.

        Args:
            *args: Positional arguments to pass to json.JSONDecoder.
            **kwargs: Keyword arguments to pass to json.JSONDecoder.
        """
        super().__init__(object_hook=self.custom_object_hook, *args, **kwargs)

    def custom_object_hook(self, dct: dict) -> datetime | uuid.UUID | dict:
        """
        Converts dictionaries with special type markers back into datetime and UUID objects.

        Args:
            dct (dict): The dictionary to convert.

        Returns:
            datetime | uuid.UUID | dict: The converted object or the original dictionary.
        """
        if "__type__" in dct:
            if dct["__type__"] == "datetime":
                return datetime.fromisoformat(dct["__value__"])

            elif dct["__type__"] == "uuid":
                return uuid.UUID(dct["__value__"])

        return dct
