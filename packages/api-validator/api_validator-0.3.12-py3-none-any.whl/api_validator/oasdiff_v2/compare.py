#! /usr/bin/env python3
"""
Invoke the OASDiff tool to compare two OpenAPI specifications.
"""
from os.path import exists, basename, relpath
from os import remove
from invoke import run
import json
from loguru import logger


def run_oasdiff(old_file: str, new_file: str):
    """
    Run the OASDiff tool to compare two OpenAPI specifications
    """
    command = f"oasdiff diff {old_file} {new_file}"
    flags = [
        "--exclude-elements",
        "description,examples,summary,title",
        "--format json",
        # case-insensitive header name comparison
        "--case-insensitive-headers",
        # include path parameter names in endpoint matching
        "--include-path-params"
    ]
    command += " " + " ".join(flags)
    logger.info(f"Running OASDiff command: {command}")
    process = run(command, warn=True, hide=True, in_stream=False)
    try:
        oasdiff_data = json.loads(process.stdout)
    except json.JSONDecodeError as e:
        if "expecting ref to schema object" in process.stderr:
            logger.error(f"OASDiff failed due to a reference to a schema object. It expects valid OpenAPI specs. Please correct the issue in the specified spec to evaluate it. stderr: {process.stderr}")
            return
        logger.error(f"Failed to parse the OASDiff output: {e.__class__.__name__}: {e}")
        logger.error(f"Error: {process.stderr}")
        return
    return oasdiff_data


def trim_output_old(data: dict):
    """
    Trim the output of the OASDiff tool by removing unnecessary keys under modified paths.
    """

    # Helper function to remove extensions and clean empty schema/items/enum/additionalProperties recursively
    def clean_schema(schema_data):
        if "extensions" in schema_data:
            del schema_data["extensions"]

        if "enum" in schema_data and not schema_data["enum"]:
            del schema_data["enum"]

        if "items" in schema_data:
            # Recursively clean items schema as well
            clean_schema(schema_data["items"])
            if not schema_data["items"]:
                del schema_data["items"]

        if "properties" in schema_data and "modified" in schema_data["properties"]:
            # Recursively clean each property
            for prop_name, prop_data in schema_data["properties"]["modified"].items():
                clean_schema(prop_data)

            # Remove the "properties" field if it becomes empty
            if not schema_data["properties"]["modified"]:
                del schema_data["properties"]["modified"]

        if "additionalProperties" in schema_data:
            # Recursively clean additionalProperties
            clean_schema(schema_data["additionalProperties"])

            # Remove additionalProperties if it becomes empty
            if not schema_data["additionalProperties"]:
                del schema_data["additionalProperties"]

        # Remove empty schema objects
        if not schema_data:
            return None

        return schema_data

    # Remove certain top-level keys
    for key in ["extensions", "openAPI", "info", "servers", "tags", "components", "security", "externalDocs"]:
        data.pop(key, None)

    # Process only the "modified" paths
    if "modified" in data["paths"]:
        paths_to_delete = []  # Track paths to remove if they become empty
        for path, path_data in data["paths"]["modified"].items():
            # Remove "extensions" at the path level
            path_data.pop("extensions", None)

            # Check if "operations" and "modified" exist under the path
            if "operations" in path_data and "modified" in path_data["operations"]:
                methods_to_delete = []

                for http_method, details in path_data["operations"]["modified"].items():
                    # Remove unnecessary fields under each HTTP method
                    for key in ["description", "summary", "extensions", "tags", "examples", "responses", "operationID"]:
                        details.pop(key, None)

                    # Process "parameters" if they exist
                    if "parameters" in details:
                        details["parameters"].pop("extensions", None)

                        if "modified" in details["parameters"]:
                            for param_type in ["path", "query", "header", "cookie"]:
                                if param_type in details["parameters"]["modified"]:
                                    for param_name, param_data in details["parameters"]["modified"][param_type].items():
                                        param_data.pop("extensions", None)

                                        if "schema" in param_data:
                                            cleaned_schema = clean_schema(param_data["schema"])
                                            if cleaned_schema is None:
                                                del param_data["schema"]
                                            else:
                                                param_data["schema"] = cleaned_schema

                    # Process "requestBody" if it exists
                    if "requestBody" in details:
                        details["requestBody"].pop("extensions", None)

                        # Process "content" if it exists
                        if "content" in details["requestBody"]:
                            if "mediaTypeModified" in details["requestBody"]["content"]:
                                for content_type, content_data in details["requestBody"]["content"][
                                    "mediaTypeModified"].items():
                                    content_data.pop("extensions", None)

                                    # Clean schema in the content
                                    if "schema" in content_data:
                                        cleaned_schema = clean_schema(content_data["schema"])
                                        if cleaned_schema is None:
                                            del content_data["schema"]
                                        else:
                                            content_data["schema"] = cleaned_schema

                    # If an HTTP method has no remaining fields, mark it for deletion
                    if not details:
                        methods_to_delete.append(http_method)

                # Delete empty HTTP methods
                for method in methods_to_delete:
                    del path_data["operations"]["modified"][method]

                # If "modified" in "operations" is now empty, delete it
                if not path_data["operations"]["modified"]:
                    path_data["operations"].pop("modified")

                # If "operations" is empty, mark the path for deletion
                if not path_data["operations"]:
                    paths_to_delete.append(path)

        # Remove empty paths
        for path in paths_to_delete:
            del data["paths"]["modified"][path]

    # If "modified" in paths is now empty, remove it
    if "modified" in data["paths"] and not data["paths"]["modified"]:
        data["paths"].pop("modified")

    return data


def remove_empty_dicts(d):
    # If it's a dictionary, process each key-value pair
    if isinstance(d, dict):
        # Recursively call the function for each value
        return {k: remove_empty_dicts(v) for k, v in d.items() if remove_empty_dicts(v) != {}}
    # If it's not a dictionary, return the value as is
    return d


def trim_output(data: dict):
    """
    Trim the output of the OASDiff tool by removing unnecessary keys under modified paths.
    """

    # Helper function to remove extensions and clean empty schema/items/enum/additionalProperties recursively
    def clean_schema(schema_data):
        if "extensions" in schema_data:
            del schema_data["extensions"]

        if "enum" in schema_data and not schema_data["enum"]:
            del schema_data["enum"]

        if "items" in schema_data:
            # Recursively clean items schema as well
            clean_schema(schema_data["items"])
            if not schema_data["items"]:
                del schema_data["items"]

        if "properties" in schema_data and "modified" in schema_data["properties"]:
            # Recursively clean each property
            for prop_name, prop_data in schema_data["properties"]["modified"].items():
                clean_schema(prop_data)

            # Remove the "properties" field if it becomes empty
            if not schema_data["properties"]["modified"]:
                del schema_data["properties"]["modified"]

        if "additionalProperties" in schema_data:
            # Recursively clean additionalProperties
            clean_schema(schema_data["additionalProperties"])

            # Remove additionalProperties if it becomes empty
            if not schema_data["additionalProperties"]:
                del schema_data["additionalProperties"]

        # Remove empty schema objects
        if not schema_data:
            return None

        return schema_data

    # Helper function to remove empty query/path/header/cookie parameters and modified blocks
    def clean_parameters(parameters_data):
        if "modified" in parameters_data:
            for param_type in ["path", "query", "header", "cookie"]:
                if param_type in parameters_data["modified"]:
                    # Remove empty parameters in modified blocks
                    empty_params = [param for param, param_data in parameters_data["modified"][param_type].items() if
                                    not param_data]
                    for param in empty_params:
                        del parameters_data["modified"][param_type][param]

                    # Recursively clean the schema of each parameter
                    for param_name, param_data in parameters_data["modified"][param_type].items():
                        if "schema" in param_data:
                            cleaned_schema = clean_schema(param_data["schema"])
                            if cleaned_schema is None:
                                del param_data["schema"]
                            else:
                                param_data["schema"] = cleaned_schema

                        # Clean extensions directly in the parameter level
                        if "extensions" in param_data:
                            del param_data["extensions"]

                    # Remove the modified block if it becomes empty
                    if not parameters_data["modified"][param_type]:
                        del parameters_data["modified"][param_type]

            # Remove the modified field if it's empty
            if not parameters_data["modified"]:
                del parameters_data["modified"]

    # Remove certain top-level keys
    for key in ["extensions", "openAPI", "info", "servers", "tags", "security", "externalDocs"]:
        data.pop(key, None)

    # Process only the "modified" paths
    if "modified" in data["paths"]:
        paths_to_delete = []  # Track paths to remove if they become empty
        for path, path_data in data["paths"]["modified"].items():
            # Remove "extensions" at the path level
            path_data.pop("extensions", None)

            # Check if "operations" and "modified" exist under the path
            if "operations" in path_data and "modified" in path_data["operations"]:
                methods_to_delete = []

                for http_method, details in path_data["operations"]["modified"].items():
                    # Remove unnecessary fields under each HTTP method
                    for key in ["description", "summary", "extensions", "tags", "examples", "responses", "operationID"]:
                        details.pop(key, None)

                    # Process "parameters" if they exist
                    if "parameters" in details:
                        details["parameters"].pop("extensions", None)

                        # Clean empty query/path/header/cookie parameters in the "modified" section
                        clean_parameters(details["parameters"])

                    # Process "requestBody" if it exists
                    if "requestBody" in details:
                        details["requestBody"].pop("extensions", None)

                        # Process "content" if it exists
                        if "content" in details["requestBody"]:
                            if "mediaTypeModified" in details["requestBody"]["content"]:
                                for content_type, content_data in details["requestBody"]["content"][
                                    "mediaTypeModified"].items():
                                    content_data.pop("extensions", None)

                                    # Clean schema in the content
                                    if "schema" in content_data:
                                        cleaned_schema = clean_schema(content_data["schema"])
                                        if cleaned_schema is None:
                                            del content_data["schema"]
                                        else:
                                            content_data["schema"] = cleaned_schema

                    # If an HTTP method has no remaining fields, mark it for deletion
                    if not details:
                        methods_to_delete.append(http_method)

                # Delete empty HTTP methods
                for method in methods_to_delete:
                    del path_data["operations"]["modified"][method]

                # If "modified" in "operations" is now empty, delete it
                if not path_data["operations"]["modified"]:
                    path_data["operations"].pop("modified")

                # If "operations" is empty, mark the path for deletion
                if not path_data["operations"]:
                    paths_to_delete.append(path)

        # Remove empty paths
        for path in paths_to_delete:
            del data["paths"]["modified"][path]

    # If "modified" in paths is now empty, remove it
    if "modified" in data["paths"] and not data["paths"]["modified"]:
        data["paths"].pop("modified")

    data = remove_empty_dicts(data)
    return data


def create_diff_file(old_file: str, new_file: str, output_file: str, overwrite: bool = True):
    """
    Run the OASDiff tool to compare two OpenAPI specifications and write the results to a file
    """
    output = run_oasdiff(old_file, new_file)
    try:
        trimmed = trim_output(output)
        if exists(output_file):
            if overwrite:
                logger.info(f"Overwriting existing file: {relpath(output_file)}")
                remove(output_file)
            else:
                logger.info(f"Output file already exists: {relpath(output_file)}")
                return
        logger.info(f"Creating diff file for {basename(old_file)}: {relpath(old_file)} -> {relpath(new_file)} -> {relpath(output_file)}")
        with open(output_file, "w") as f:
            json.dump(trimmed, f, indent=4)
        logger.info("OASDiff comparison completed successfully.")
    except Exception as e:
        logger.error(f"Failed to create the diff file: {e.__class__.__name__}: {e}")
        logger.error(f"Oasdiff data (for reference): {output}")


def get_diff_data(old_file: str, new_file: str):
    """
    Run the OASDiff tool to compare two OpenAPI specifications and return the results
    """
    output = run_oasdiff(old_file, new_file)
    try:
        trimmed = trim_output(output)
        return trimmed
    except Exception as e:
        logger.error(f"Failed to get the diff: {e.__class__.__name__}: {e}")
        logger.error(f"Oasdiff data (for reference): {output}")
        logger.error(f"Files: {old_file} -> {new_file}")


if __name__ == '__main__':
    import argparse
    from os.path import exists
    from os import remove
    parser = argparse.ArgumentParser(description="Run OASDiff to compare two OpenAPI specifications")
    parser.add_argument("old_file", help="The base OpenAPI specification file")
    parser.add_argument("new_file", help="The new OpenAPI specification file")
    parser.add_argument("output_file", help="The output file to write the OASDiff results to")
    args = parser.parse_args()
    create_diff_file(args.old_file, args.new_file, args.output_file)
