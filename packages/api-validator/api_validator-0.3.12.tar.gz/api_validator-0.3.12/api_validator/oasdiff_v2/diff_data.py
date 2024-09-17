"""
Load oasdiff JSON data and provide methods to access the data
"""
import json
from typing import Union, List
from api_validator.oasdiff_v2.parameters.modified_parameters import ModifiedParameterData
from api_validator.oasdiff_v2.parameters.deleted_parameter_data import DeletedParameterData
from api_validator.oasdiff_v2.parameters.added_parameter_data import AddedParameterData
from api_validator.oasdiff_v2.parameters.modified_request_body_parameters import ModifiedRequestBodyParameters
from api_validator.oasdiff_v2.parameters.deleted_request_body_parameters import DeletedRequestBodyParameters
from api_validator.oasdiff_v2.parameters.added_request_body_parameters import AddedRequestBodyParameters
from loguru import logger


class DiffData:
    """
    All the data about missing or added parameters, request bodies, and security requirements.

    This is found under paths.modified in the oasdiff data.

    You might be wondering if paths.added or paths.deleted is useful to us. It's not, because it
    doesn't store HTTP methods or parameters - just a list of paths.
    """
    def __init__(self):
        self.data: dict = {"paths": {"modified": {}, "added": [], "deleted": []}}
        self.modified_paths: set = set()
        # We will load requestBody AND parameters into these sets
        self.modified_parameters: set = set()
        self.added_parameters: set = set()
        self.deleted_parameters: set = set()
        # We will only load requestBody into this set
        self.modified_request_data: set = set()
        self.added_request_data: set = set()
        self.deleted_request_data: set = set()

    def __str__(self):
        return self.data

    def __repr__(self):
        return f"DiffData(paths={len(self.modified_paths)}, parameters={len(self.modified_parameters)})"

    def load(self, data: dict):
        """Load the raw oasdiff data, from the root level."""
        if not data:
            logger.warning("The data is empty. Perhaps there are no modifications to existing endpoints in the spec - not a bad thing!.")
            return
        self.data = data
        # self.modified_paths = {path for path in self.data.get("paths", {}).get("modified", {}).keys()}
        if "paths" not in self.data:
            raise ValueError("The data does not contain a 'paths' key")
        if "modified" not in self.data["paths"]:
            logger.warning("The data does not contain a 'modified' key in 'paths'. This means there are no modifications to existing endpoints in the spec - not a bad thing!.")
            return
        for path, path_data in self.data["paths"]["modified"].items():
            self.load_path_data({path: path_data})

    def load_from_file(self, file_path: str):
        """Load the raw oasdiff data from a file."""
        with open(file_path, "r") as file:
            data = json.loads(file.read())
        self.load(data)

    def load_endpoint_data_item(self, endpoint_data: dict, path: str):
        """
        Load a single item of raw oasdiff data. This is useful for testing.

        Example usage with raw oasdiff_data:
            endpoint_data = get_raw_modified_endpoint_tree(oasdiff_data)
            diff_data = DiffData()
            diff_data.load_endpoint_data_item(endpoint_data, "/another", "GET")
        """
        if "operations" not in endpoint_data:
            raise ValueError("The endpoint data does not contain an 'operations' key")
        elif "modified" not in endpoint_data["operations"]:
            if "paths" not in self.data:
                self.data["paths"] = {"modified": {}}
            elif "modified" not in self.data["paths"]:
                self.data["paths"]["modified"] = {}
            return
        else:
            self.data["paths"]["modified"][path] = endpoint_data
            self.modified_paths.add(path)
            self.hydrate_parameter_data()

    def load_path_data(self, path_data: dict):
        """
        As an alternative to load_endpoint_data_item, load a path directly.
        This makes our tests easier to understand.
        """
        for path, path_data in path_data.items():
            self.load_endpoint_data_item(path_data, path)

    # I know the format is crazy, but it would be harder to reason about the nested nature if it was stretched out.
    # fmt: off
    def hydrate_parameter_data(self):
        """After loading the data, hydrate the parameter data."""
        for path, path_data in self.data["paths"]["modified"].items():
            if "operations" in path_data:
                if "modified" in path_data["operations"]:
                    for http_method, method_data in path_data["operations"]["modified"].items():
                        if "parameters" in method_data:
                            if "modified" in method_data["parameters"]:
                                for parameter_type, parameters in method_data["parameters"]["modified"].items():
                                    for name, parameter_data in parameters.items():
                                        this_parameter_data = ModifiedParameterData()
                                        this_parameter_data.load_from_modified(
                                            data=parameter_data,
                                            parameter_type=parameter_type,
                                            path=path,
                                            http_method=http_method,
                                            name=name
                                        )
                                        self.modified_parameters.add(this_parameter_data)
                            if "deleted" in method_data["parameters"]:
                                for parameter_type, parameter_list in method_data["parameters"]["deleted"].items():
                                    for parameter in parameter_list:
                                        this_parameter_data = DeletedParameterData()
                                        this_parameter_data.load_from_modified(
                                            data=method_data["parameters"]["deleted"],
                                            parameter_type=parameter_type,
                                            path=path,
                                            http_method=http_method,
                                            name=parameter
                                        )
                                        self.deleted_parameters.add(this_parameter_data)
                            if "added" in method_data["parameters"]:
                                for parameter_type, parameter_list in method_data["parameters"]["added"].items():
                                    for parameter in parameter_list:
                                        this_parameter_data = AddedParameterData()
                                        this_parameter_data.load_from_modified(
                                            data=method_data["parameters"]["added"],
                                            parameter_type=parameter_type,
                                            path=path,
                                            http_method=http_method,
                                            name=parameter
                                        )
                                        self.added_parameters.add(this_parameter_data)
                            # If something other than moddified, deleted, or added is there, log it:
                            if set(method_data["parameters"].keys()) - {"modified", "deleted", "added"}:
                                logger.debug(f"A parameter type other than modified, added, or deleted was found for {path} {http_method}")
                        if "requestBody" in method_data:
                            if "content" in method_data["requestBody"]:
                                if "mediaTypeModified" in method_data["requestBody"]["content"]:
                                    for media_type, media_type_data in method_data["requestBody"]["content"]["mediaTypeModified"].items():
                                        if "schema" in media_type_data:
                                            requirement_data = media_type_data["schema"].get("required", {})
                                            if "properties" in media_type_data["schema"]:
                                                if "modified" in media_type_data["schema"]["properties"]:
                                                    # Modified requestBody parameters
                                                    for name, schema_data in media_type_data["schema"]["properties"]["modified"].items():
                                                        this_parameter_data = ModifiedRequestBodyParameters()
                                                        this_parameter_data.load_from_modified_media_type(
                                                            data=schema_data,
                                                            path=path,
                                                            http_method=http_method,
                                                            name=name,
                                                            media_type=media_type
                                                        )
                                                        this_parameter_data.load_requirement_data(requirement_data)
                                                        self.modified_parameters.add(this_parameter_data)
                                                        self.modified_request_data.add(this_parameter_data)
                                                if "added" in media_type_data["schema"]["properties"]:
                                                    # Added requestBody parameters
                                                    for name in media_type_data["schema"]["properties"]["added"]:
                                                        this_parameter_data = AddedRequestBodyParameters()
                                                        this_parameter_data.load_from_modified_media_type(
                                                            data=media_type_data["schema"]["properties"]["added"],
                                                            path=path,
                                                            http_method=http_method,
                                                            name=name,
                                                            media_type=media_type
                                                        )
                                                        this_parameter_data.load_requirement_data(requirement_data)
                                                        self.added_parameters.add(this_parameter_data)
                                                        self.added_request_data.add(this_parameter_data)
                                                if "deleted" in media_type_data["schema"]["properties"]:
                                                    # Deleted requestBody parameters
                                                    for name in media_type_data["schema"]["properties"]["deleted"]:
                                                        this_parameter_data = DeletedRequestBodyParameters()
                                                        this_parameter_data.load_from_modified_media_type(
                                                            data=media_type_data["schema"]["properties"]["deleted"],
                                                            path=path,
                                                            http_method=http_method,
                                                            name=name,
                                                            media_type=media_type
                                                        )
                                                        self.deleted_parameters.add(this_parameter_data)
                                                        self.deleted_request_data.add(this_parameter_data)

                                                if set(media_type_data["schema"]["properties"].keys()) - {"modified", "deleted", "added"}:
                                                    logger.debug(f"A parameter type other than modified, added, or deleted was found for the requestBody data under {path} {http_method}")
    # fmt: on

    def hydrate_security_requirements_data(self):
        """After loading the data, hydrate the security requirements data."""
        # TODO: Do the same for security requirements data
        raise NotImplementedError

    def removed_parameters(self) -> Union[List[Union[DeletedParameterData, DeletedRequestBodyParameters]], None]:
        """
        Return parameters that were removed under a modified endpoint.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.parameters.deleted
        """
        parameters = [parameter for parameter in self.deleted_parameters]
        parameters.sort()
        return parameters

    def removed_request_data(self) -> Union[List[Union[DeletedRequestBodyParameters]], None]:
        """
        Return request data that was removed under a modified endpoint.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.requestBody.content.mediaTypeModified.{media_type}.schema.properties.deleted
        """
        parameters = [parameter for parameter in self.deleted_request_data]
        parameters.sort()
        return parameters

    def added_parameters(self) -> Union[List[Union[AddedParameterData, AddedRequestBodyParameters]], None]:
        """
        Return parameters that were added under a modified endpoint.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.parameters.added
        """
        parameters = [parameter for parameter in self.added_parameters]
        parameters.sort()
        return parameters

    def parameters_with_changed_variable_types(self) -> Union[List[Union[ModifiedParameterData, ModifiedRequestBodyParameters]], None]:
        """
        Return parameters under the modified key.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.parameters.modified
        """
        parameters = [parameter for parameter in self.modified_parameters if parameter.changed_variable_type()]
        parameters.sort()
        return parameters

    def parameters_with_changed_requirements(self) -> Union[List[Union[ModifiedParameterData, ModifiedRequestBodyParameters]], None]:
        """
        Return parameters under the modified key.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.parameters.modified
        """
        parameters = [parameter for parameter in self.modified_parameters if parameter.changed_requirement_status()]
        parameters.sort()
        return parameters

    def parameters_with_changed_schema(self) -> Union[List[Union[ModifiedParameterData, ModifiedRequestBodyParameters]], None]:
        """
        Return parameters under the modified key.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.parameters.modified
        """
        parameters = [parameter for parameter in self.modified_parameters if parameter.changed_schema()]
        # TODO: It will help to have requestData in here so we can reflect mediaTypeModified
        parameters.sort()
        return parameters

    def parameters_with_changed_default_values(self) -> Union[List[Union[ModifiedParameterData, ModifiedRequestBodyParameters]], None]:
        """
        Return parameters under the modified key.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.parameters.modified
        """
        parameters = [parameter for parameter in self.modified_parameters if parameter.changed_default_value()]
        parameters.sort()
        return parameters
