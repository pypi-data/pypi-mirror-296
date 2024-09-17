from typing import Union
from abc import ABC

from api_validator.oasdiff_v2.parameters.parameter_data import ParameterType


class RequestBodyParameterData(ParameterType, ABC):
    """Store and analyze REQUEST BODY parameter data."""

    def __init__(self):
        self.data: dict = {}
        self.parameter_type: Union[str, None] = None
        self.name: Union[str, None] = None
        self.http_method: Union[str, None] = None
        self.path: Union[str, None] = None
        super().__init__()

    def load(self, data: dict):
        """
        Load the request body data.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.requestBody
        """
        self.data = data

    def changed_default_value(self) -> bool:
        pass

    def changed_variable_type(self) -> bool:
        pass

    def changed_requirement_status(self) -> bool:
        """
        Did the request body change from required to not required, or vice versa?

        Example values:
            - argus-eye-django.json
        """
        if "required" in self.data:
            # If "from" and "to" are present, we can determine if the requirement status changed
            if "from" in self.data["required"] and "to" in self.data["required"]:
                # If the requirement status changed, return True
                return self.data["required"]["from"] != self.data["required"]["to"]
        return False

    def changed_media_type(self) -> bool:
        """
        Did the media type change?

        Example values:
            - argus-eye-django.json
        """
        if "mediaTypeModified" in self.data.get("content", {}):
            return bool(self.data["content"]["mediaTypeModified"])
        return False

    def deleted_media_type(self) -> list:
        """
        Did the media type change?

        Example values:
            - argus-eye-django.json
        """
        if "mediaTypeDeleted" in self.data.get("content", {}):
            return self.data["content"]["mediaTypeDeleted"]
        return []

    def to_dict(self) -> dict:
        pass

