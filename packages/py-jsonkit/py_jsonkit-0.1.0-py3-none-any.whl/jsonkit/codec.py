from json import JSONEncoder, JSONDecoder
from typing import Dict, Any
from datetime import datetime
from uuid import UUID


class CustomJSONEncoder(JSONEncoder):
    """
    A custom JSON encoder for serializing datetime and UUID objects.

    Methods:
        default(obj):
            Converts datetime and UUID objects to a serializable format.
    """

    def default(self, obj: Any) -> Dict[str, str] | Any:
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

        elif isinstance(obj, UUID):
            return {"__type__": "uuid", "__value__": str(obj)}

        return super().default(obj)


class CustomJSONDecoder(JSONDecoder):
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

    def custom_object_hook(self, dct: dict) -> datetime | UUID | dict:
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
                return UUID(dct["__value__"])

        return dct
