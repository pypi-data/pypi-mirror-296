"""
Utility functions to support getting missing parameters from oasdiff data.
"""


def get_raw_modified_endpoint_tree(data: dict) -> dict:
    """
    Get the modified endpoint tree from the OASDiff data.

    This is the raw data structure. We will need to process it further to get the missing parameters.

    Using the below as an example, it will give us everything under /another

    {
        "paths": {
            "modified": {
                "/another": {
                    ... give me this data...
                }
            }
    }
    """
    modified_endpoints = {}
    if "paths" in data:
        if "modified" in data["paths"]:
            for path, path_data in data["paths"]["modified"].items():
                modified_endpoints[path] = path_data
    return modified_endpoints


def get_raw_parameter_data_for_modified_method():
    """
    Get the raw parameter data for a modified method.

    After running get_raw_modified_endpoint_tree, we can use this to get the data for a specific method.

    Let's say I have the below as an example.
    {
    "paths": {
        "modified": {
            "/another": {
                "operations": {
                    "modified": {
                        "GET": {
                            "parameters": {
                                "modified": {
                                    "query": {
                                        "age": {
                                        ... give me this data...
                                        }

    endpoint_data = get_raw_modified_endpoint_tree(data)
    method_data = get_raw_parameter_data_for_modified_method(endpoint_data, "/another", "GET")
    """
