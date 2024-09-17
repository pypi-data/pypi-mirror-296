from typing import Union, List
from abc import ABC
from loguru import logger

from api_validator.oasdiff_v2.parameters.parameter_data import ParameterType


class ModifiedRequestBodyParameters(ParameterType, ABC):
    """
    Store and analyze MODIFIED request body parameter data.
    """
    def __init__(self):
        self.data: dict = {}
        self.parameter_type: Union[str, None] = None
        self.name: Union[str, None] = None
        self.http_method: Union[str, None] = None
        self.path: Union[str, None] = None
        self.media_type: Union[str, None] = None
        # This is something we have to do specifically for request data because it's stored in a separate list
        self.requirement_data: dict = {}
        self.requirements_deleted: Union[set, None] = set()
        self.requirements_added: Union[set, None] = set()
        super().__init__()
        # Have to set this default after calling super().__init__(), otherwise it will be overwritten
        self.parameter_type: str = "requestBody"

    def load_from_modified_media_type(self, data: dict, path: str, http_method: str, name: str, media_type: str):
        """
        Load the request body data.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.requestBody.content.{media_type}.schema.properties.modified

        Example:
            paths.modified.["/hello/{name}"].operations.modified.["GET"].requestBody.content.["application/json"]
        """
        self.data = data
        self.path = path
        self.http_method = http_method
        self.name = name
        self.media_type = media_type

    def load_requirement_data(self, data: dict):
        """
        Load the requirement data.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.requestBody.content.mediaTypeModified.{media_type}.schema.required
        """
        self.requirement_data = data
        self.requirements_deleted = set(data.get("deleted", []))
        self.requirements_added = set(data.get("added", []))

    def changed_requirement_status(self) -> bool:
        """
        Did the request body change from required to not required, or vice versa?

        Note for oasdiff searching: You can use this regex expression in Pycharm to find it: required":\s*\{\n[\t ]*"deleted":\s*\[
        """
        if self.name in self.requirements_deleted or self.name in self.requirements_added:
            return True
        return False

    def old_requirement_status(self) -> Union[bool, None]:
        """
        Return the old requirement status.
        """
        # If the parameter was deleted, it was required.
        if self.name in self.requirements_deleted:
            return True
        # was_not_required = self.name in self.requirements_added
        # We don't know the current status of the parameter if it's not modified,
        # so if it's not in either, we will just say it wasn't required
        return False

    def new_requirement_status(self) -> Union[bool, None]:
        """
        Return the new requirement status.
        """
        if self.name in self.requirements_added:
            return True
        return False

    def changed_default_value(self) -> bool:
        """
        Did the request body change the default value?

        NOTE: The request body does not have a default value.
        """
        return False

    def changed_variable_type(self) -> bool:
        """
        Did the request body change the type?
        """
        if "type" in self.data:
            if "added" in self.data["type"]:
                return True
        return False

    def new_variable_type(self) -> Union[List[str], None]:
        """
        If the variable type changed, return the new type.
        """
        if "type" in self.data:
            if "added" in self.data["type"]:
                return self.data["type"]["added"]
        return None

    def old_variable_type(self) -> Union[List[str], None]:
        """
        If the variable type changed, return the old type.
        """
        if "type" in self.data:
            if "deleted" in self.data["type"]:
                return self.data["type"]["deleted"]
        return None

    def changed_schema(self) -> bool:
        """
        Did the schema change?
        """
        if "schema" in self.data:
            if "added" in self.data["schema"]:
                return True
        return False
