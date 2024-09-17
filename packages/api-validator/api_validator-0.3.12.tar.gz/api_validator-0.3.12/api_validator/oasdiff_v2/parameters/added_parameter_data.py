from typing import Union
from abc import ABC
from loguru import logger

from api_validator.oasdiff_v2.parameters.parameter_data import ParameterType


class AddedParameterData(ParameterType, ABC):
    """
    Store and analyze ADDED parameter data.

    Unlike the Modified Parameter or Request Data parameter type, this one is pretty simple.

    Example:
        "/identity/api/auth/forget-password": {
            "operations": {
                "modified": {
                    "POST": {
                        "parameters": {
                            "added": {
                                "query": [
                                    "_csrf"
                                ]
                            }
                        },
                    }
                }
            }
        }
    """

    def __init__(self):
        self.data: dict = {}
        self.parameter_type: Union[str, None] = None
        self.name: Union[str, None] = None
        self.http_method: Union[str, None] = None
        self.path: Union[str, None] = None
        super().__init__()

    def load_from_modified(self, data: dict, parameter_type: str, path: str, http_method: str, name: str):
        """
        Load the parameter data.

        Because of how it is structured, the arguments to this method have to be pulled out explicitly from the JSON.
        We can't just pass in the JSON object and have it parse it for us.

        Specifically:
            paths.modified.{path}.operations.modified.{method}.parameters.added.{param_type}.{param_name}

        Example:
            paths.modified.["/hello/{name}"].operations.modified.["GET"].parameters.added.["query"].name
        """
        if parameter_type not in ["path", "query", "header", "cookie", "body"]:
            raise ValueError(f"Invalid parameter type: {parameter_type}")
        self.data = data
        self.parameter_type = parameter_type
        self.path = path
        self.http_method = http_method
        self.name = name

    def changed_requirement_status(self) -> bool:
        """
        Did the parameter change from required to not required, or vice versa?

        That doesn't apply here, so we can just return False.
        """
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
        return None

    def changed_variable_type(self) -> bool:
        """
        Did the variable type change?

        That doesn't apply here, so we can just return False.
        """
        return False

    def old_variable_type(self) -> Union[str, None]:
        """
        Return the old variable type.

        That doesn't apply here, so we can just return None.
        """
        return None

    def new_variable_type(self) -> Union[str, None]:
        """
        We can't tell what the new variable type is because of the way the data is structured.
        But it's not necessary anyway because changed_variable_type is False.
        So we can just return none.
        """
        return None

    def changed_default_value(self) -> bool:
        """
        Did the default value change?

        That doesn't apply here, so we can just return False.
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

        That doesn't apply here, so we can just return False.
        """
        return False
