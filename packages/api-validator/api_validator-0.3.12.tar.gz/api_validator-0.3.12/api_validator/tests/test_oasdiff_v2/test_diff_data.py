import unittest
from api_validator.oasdiff_v2.diff_data import DiffData
from api_validator.oasdiff_v2.missing_parameters_utils import (
    get_raw_modified_endpoint_tree,
    get_raw_parameter_data_for_modified_method
)


class TestDiffData(unittest.TestCase):
    """Test the DiffData class to make sure it is behaving properly"""
    def setUp(self):
        self.diff_data = DiffData()

    def test_load_endpoint_data_item_no_operations(self):
        """Test that we raise an error if the endpoint data does not contain an 'operations' key"""
        data = {
            "/api/v4/deploy_keys": {
                "description": "This is a description"
            }
        }
        with self.assertRaises(ValueError):
            self.diff_data.load_endpoint_data_item(data, "/api/v4/deploy_keys")

    def test_load_endpoint_data_item_no_modified(self):
        """Test that we raise an error if the endpoint data does not contain a 'modified' key in 'operations'"""
        data = {
            "/api/v4/deploy_keys": {
                "operations": {
                    "added": {
                        "GET": {
                            "parameters": {
                                "deleted": {
                                    "query": [
                                        "page",
                                        "per_page",
                                        "public"
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(ValueError):
            self.diff_data.load_endpoint_data_item(data, "/api/v4/deploy_keys")

    def test_load_endpoint_data_item(self):
        """Test that we can load an endpoint item when the data is supplied properly"""
        data = {
            "operations": {
                "modified": {
                    "GET": {
                        "parameters": {
                            "deleted": {
                                "query": [
                                    "page",
                                    "per_page",
                                    "public"
                                ]
                            }
                        }
                    }
                }
            }
        }
        path = "/api/v4/deploy_keys"
        self.diff_data.load_endpoint_data_item(data, path)
        self.assertEqual(self.diff_data.data["paths"]["modified"][path], data)
        self.assertEqual(self.diff_data.modified_paths, {path})

    def test_load_path_data(self):
        """We have a separate method that makes understanding test data easier."""
        data = {
            "/api/v4/deploy_keys": {
                "operations": {
                    "modified": {
                        "GET": {
                            "parameters": {
                                "deleted": {
                                    "query": [
                                        "page",
                                        "per_page",
                                        "public"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
        }
        self.diff_data.load_path_data(data)
        self.assertEqual(self.diff_data.data["paths"]["modified"], data)
        self.assertEqual(self.diff_data.modified_paths, {"/api/v4/deploy_keys"})

