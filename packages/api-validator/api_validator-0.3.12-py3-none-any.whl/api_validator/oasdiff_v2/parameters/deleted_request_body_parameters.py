from typing import Union
from abc import ABC
from loguru import logger

from api_validator.oasdiff_v2.parameters.parameter_data import ParameterType


class DeletedRequestBodyParameters(ParameterType, ABC):
    """
    Store and analyze DELETED request body parameter data
    """
    def __init__(self):
        self.data: dict = {}
        self.parameter_type: Union[str, None] = None
        self.name: Union[str, None] = None
        self.http_method: Union[str, None] = None
        self.path: Union[str, None] = None
        self.media_type: Union[str, None] = None
        super().__init__()
        # Have to set this default after calling super().__init__(), otherwise it will be overwritten
        self.parameter_type: str = "requestBody"

    def load_from_modified_media_type(self, data: dict, path: str, http_method: str, name: str, media_type: str):
        """
        Load the request body data.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.requestBody.content.{media_type}.schema.properties.deleted

        Example:
            paths.modified.["/hello/{name}"].operations.modified.["GET"].requestBody.content.["application/json"].schema.properties.deleted
        """
        self.data = data
        self.path = path
        self.http_method = http_method
        self.name = name
        self.media_type = media_type

    def changed_requirement_status(self) -> bool:
        """
        Did the parameter change from required to not required, or vice versa?

        Technically yes, because it was deleted, but we don't need to flag that as a separate error, so we can just return False.
        """
        return False

    def old_requirement_status(self) -> Union[bool, None]:
        """
        Return the old requirement status.

        It doesn't really matter because the parameter was deleted, so we can just return None.
        """
        return None

    def new_requirement_status(self) -> Union[bool, None]:
        """
        Return the new requirement status.

        It was deleted, so it's not required, but it's not valid anymore and doesn't really apply in this case, so we can just return False.
        """
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

        We can't tell what the old variable type is because of the way the data is structured.
        But it's not necessary anyway because changed_variable_type is False.
        So we can just return none.
        """
        return None

    def new_variable_type(self) -> Union[str, None]:
        """
        Doesn't apply here, so we can just return None.
        """
        return None

    def changed_default_value(self) -> bool:
        """
        Did the default value change?

        Technically it did change because it was deleted, but we don't need to flag that as an error, so we can just return False.
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

        It was deleted, so technically yes, but we don't need to flag that as an error, so we can just return None.
        """
        return False
