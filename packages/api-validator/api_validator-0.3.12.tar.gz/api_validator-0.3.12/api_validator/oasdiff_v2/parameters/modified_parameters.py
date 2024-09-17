from typing import Union
from abc import ABC
from loguru import logger

from api_validator.oasdiff_v2.parameters.parameter_data import ParameterType


class ModifiedParameterData(ParameterType, ABC):
    """
    Store and analyze MODIFIED parameter data.
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

        Specifically:
            paths.modified.{path}.operations.modified.{method}.parameters.modified.{param_type}.{param_name}

        Example:
            paths.modified.["/hello/{name}"].operations.modified.["GET"].parameters.modified.["path"].name
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

        Example values:
            - a-flaskrestful-api.json

        Example:
            "required": {
                "from": true,
                "to": false
            },
            "schema": {
                "type": {
                    "added": [
                        "string"
                    ]
                }
            }
        """
        if "required" in self.data:
            # If "from" and "to" are present, we can determine if the requirement status changed
            if "from" in self.data["required"] and "to" in self.data["required"]:
                # If the requirement status changed, return True
                return self.data["required"]["from"] != self.data["required"]["to"]
        # Otherwise, return false
        return False

    def old_requirement_status(self) -> Union[bool, None]:
        """
        If the requirement status changed, return the old status.
        """
        if "required" in self.data:
            # If "from" and "to" are present, we can determine if the requirement status changed
            if "from" in self.data["required"]:
                # If the requirement status changed, return True
                return self.data["required"]["from"]
        return None

    def new_requirement_status(self) -> Union[bool, None]:
        """
        If the requirement status changed, return the new status.
        """
        if "required" in self.data:
            # If "from" and "to" are present, we can determine if the requirement status changed
            if "to" in self.data["required"]:
                # If the requirement status changed, return True
                return self.data["required"]["to"]
        return

    def changed_default_value(self) -> bool:
        """
        Did the parameter change the default value?

        Example values:
            - a-flaskrestful-api.json

        Example values:
            "schema": {
                "default": {
                    "from": "World",
                    "to": null
                }
            }
        """
        if "schema" in self.data:
            # If "default" is present, we can determine if the default value changed
            if "default" in self.data["schema"]:
                # If the default value changed, return True
                return self.data["schema"]["default"]["from"] != self.data["schema"]["default"]["to"]
        # Otherwise, return false
        return False

    def old_default_value(self) -> Union[str, None]:
        """
        If the default value changed, return the old value.
        """
        if "schema" in self.data:
            # If "default" is present, we can determine if the default value changed
            if "default" in self.data["schema"]:
                # If the default value changed, return True
                return self.data["schema"]["default"]["from"]
        return None

    def new_default_value(self) -> Union[str, None]:
        """
        If the default value changed, return the new value.
        """
        if "schema" in self.data:
            # If "default" is present, we can determine if the default value changed
            if "default" in self.data["schema"]:
                # If the default value changed, return True
                return self.data["schema"]["default"]["to"]
        return None

    def changed_variable_type(self) -> bool:
        """
        Did the parameter change the type?

        Example values:
            - a-flaskrestful-api.json: This has one item with schema.type.added["string"]
            - argus-eye-django.json: This has one item with schema.type.from["string"] and schema.type.to["integer"]

        Example data:
            "schema": {
                "type": {
                    "from": "string",
                    "to": "integer"
                }
            }
        """
        if "schema" in self.data:
            # If "type" is present, we can determine if the type changed
            if "type" in self.data["schema"]:
                # If the type changed, return True
                # Sometimes it looks like this
                if "from" in self.data["schema"]["type"] and "to" in self.data["schema"]["type"]:
                    return self.data["schema"]["type"]["from"] != self.data["schema"]["type"]["to"]
                elif "format" in self.data["schema"]["type"]:
                    if self.data["schema"]["type"]["format"]["from"] != self.data["schema"]["type"]["format"]["to"]:
                        return True
                elif "added" in self.data["schema"]["type"] and "deleted" in self.data["schema"]["type"]:
                    if self.data["schema"]["type"]["added"] != self.data["schema"]["type"]["deleted"]:
                        return True
                elif "added" in self.data["schema"]["type"] and "deleted" not in self.data["schema"]["type"]:
                    # example: a weird case from the jellyfin app - [type][added] = ["object"]
                    if self.data["schema"]["type"]["added"]:
                        return True
                else:
                    logger.debug(f"Handle this schema case: {self.data['schema']}")
        # Otherwise, return false
        return False

    def old_variable_type(self) -> Union[str, None]:
        """
        If the variable type changed, return the old type.
        """
        if "schema" in self.data:
            # If "type" is present, we can determine if the type changed
            if "type" in self.data["schema"]:
                if "from" in self.data["schema"]["type"]:
                    return self.data["schema"]["type"]["from"]
                elif "format" in self.data["schema"]["type"]:
                    if self.data["schema"]["type"]["format"]["from"]:
                        return self.data["schema"]["type"]["format"]["from"]
                elif "deleted" in self.data["schema"]["type"]:
                    if self.data["schema"]["type"]["deleted"]:
                        return self.data["schema"]["type"]["deleted"]
                elif "added" in self.data["schema"]["type"] and "deleted" not in self.data["schema"]["type"]:
                    # example: a weird case from the jellyfin app - [type][added] = ["object"]
                    if self.data["schema"]["type"]["added"]:
                        return True
                else:
                    logger.debug(f"Handle this schema case: {self.data['schema']}")
        return None

    def new_variable_type(self) -> Union[str, None]:
        """
        If the variable type changed, return the new type.
        """
        if "schema" in self.data:
            # If "type" is present, we can determine if the type changed
            if "type" in self.data["schema"]:
                if "to" in self.data["schema"]["type"]:
                    return self.data["schema"]["type"]["to"]
                elif "format" in self.data["schema"]["type"]:
                    if self.data["schema"]["type"]["format"]["to"]:
                        return self.data["schema"]["type"]["format"]["to"]
                elif "added" in self.data["schema"]["type"]:
                    if self.data["schema"]["type"]["added"]:
                        return self.data["schema"]["type"]["added"]
                else:
                    logger.debug(f"Handle this schema case: {self.data['schema']}")
        return None

    def changed_schema(self) -> bool:
        """
        Did the parameter change the schema?

        Example values:
            - a-flaskrestful-api.json

        Example values:
            "schema": {
                "schemaAdded": True
            }
        """
        if "schema" in self.data:
            # If "schemaAdded" is present, we can determine if the schema changed
            if "schemaAdded" in self.data["schema"]:
                # If the schema changed, return True
                return self.data["schema"]["schemaAdded"]
        # Otherwise, return false
        return False
