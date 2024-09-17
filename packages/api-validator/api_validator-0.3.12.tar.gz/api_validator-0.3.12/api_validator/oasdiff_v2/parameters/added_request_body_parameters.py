from typing import Union
from abc import ABC
from loguru import logger

from api_validator.oasdiff_v2.parameters.parameter_data import ParameterType


class AddedRequestBodyParameters(ParameterType, ABC):
    """
    Store and analyze ADDED request body parameter data
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
        self.requirements_added: Union[set, None] = set()
        super().__init__()
        # Have to set this default after calling super().__init__(), otherwise it will be overwritten
        self.parameter_type: str = "requestBody"

    def load_from_modified_media_type(self, data: dict, path: str, http_method: str, name: str, media_type: str):
        """
        Load the request body data.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.requestBody.content.{media_type}.schema.properties.added

        Example:
            paths.modified.["/hello/{name}"].operations.modified.["GET"].requestBody.content.["application/json"].schema.properties.added
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
        self.requirements_added = set(data.get("added", []))
        # It can't be in requirements_deleted because it wasn't there before. So we don't need to store that.

    def changed_requirement_status(self) -> bool:
        """
        Did the parameter change from required to not required, or vice versa?
        """
        if self.name in self.requirements_added:
            return True
        return False

    def old_requirement_status(self) -> Union[bool, None]:
        """
        Return the old requirement status.

        That doesn't apply here, so we can just return None.
        """
        return None

    def new_requirement_status(self) -> Union[bool, None]:
        """
        Return the new requirement status.

        That doesn't apply here, so we can just return None.
        """
        if self.name in self.requirements_added:
            return True
        return False

    def changed_variable_type(self) -> bool:
        """
        Did the variable type change?

        It's new, so technically yes, but we don't need to flag that as an error, so we can just return None.
        """
        return False

    def old_variable_type(self) -> Union[str, None]:
        """
        Return the old variable type.

        We can't tell what the new variable type is because of the way the data is structured.
        But it's not necessary anyway because changed_variable_type is False.
        So we can just return none.
        """
        return None

    def new_variable_type(self) -> Union[str, None]:
        """
        It's new, so technically yes, but we don't need to flag that as an error, so we can just return None.
        """
        return None

    def changed_default_value(self) -> bool:
        """
        Did the default value change?

        We can't tell what the new variable type is because of the way the data is structured.
        But it's not necessary anyway because changed_variable_type is False.
        So we can just return False.
        """
        return False

    def old_default_value(self) -> Union[str, None]:
        """
        Return the old default value.

        That doesn't apply here, so we can just return None.
        """
        return None

    def new_default_value(self) -> Union[str, None]:
        """
        Return the new default value.

        That doesn't apply here, so we can just return None.
        """
        return None

    def changed_schema(self) -> bool:
        """
        Did the schema change?

        It's new, so technically yes, but we don't need to flag that as an error, so we can just return None.
        """
        return False
