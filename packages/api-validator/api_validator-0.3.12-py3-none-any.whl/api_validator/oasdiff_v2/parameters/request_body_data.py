from typing import Union, List


class RequestBodyData:
    """Store and analyze ALL request body data (NOT just modified)."""
    def __init__(self, data: dict):
        self.data = data

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        return self.data

    def __repr__(self):
        return "RequestBodyData({})".format(self.data)

    def load(self, data: dict):
        """
        Load the request body data.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.requestBody
        """
        self.data = data

    def changed_default_value(self) -> bool:
        """
        Did the request body change the default value?

        NOTE: The request body does not have a default value.
        """
        return False

    def changed_requirement_status(self) -> bool:
        """
        Did the request body change from required to not required, or vice versa?
        """
        if "required" in self.data:
            if self.data["required"].get("from") != self.data["required"].get("to"):
                return True
        return False

    def changed_variable_type(self) -> bool:
        """
        Did the request body change the type?
        """

    def new_variable_type(self) -> Union[str, None]:
        """
        If the variable type changed, return the new type.
        """
        if "schema" in self.data:
            if "type" in self.data["schema"]:
                if "added" in self.data["schema"]["type"]:
                    return self.data["schema"]["type"]["added"]
        return None

    def changed_request_body(self) -> bool:
        """
        Did the request body change?
        """
        return bool(self.added_request_body() or self.deleted_request_body())

    def added_request_body(self) -> bool:
        """
        Was the request body added?
        """
        if "content" in self.data:
            if "mediaTypeAdded" in self.data["content"]:
                return True
            elif "mediaTypeModified" in self.data["content"]:
                for media_type in self.data["content"]["mediaTypeModified"]:
                    if "schemaAdded" in self.data["content"]["mediaTypeModified"][media_type]:
                        if self.data["content"]["mediaTypeModified"][media_type]["schemaAdded"]:
                            return True
        return False

    def media_type_deleted(self) -> List[str]:
        """
        Was the media type deleted?
        """
        if "content" in self.data:
            if "mediaTypeDeleted" in self.data["content"]:
                return self.data["content"]["mediaTypeDeleted"]
        return []

    def deleted_request_body(self) -> bool:
        """
        Was the request body deleted?
        """
        return "deleted" in self.data and self.data["deleted"]
