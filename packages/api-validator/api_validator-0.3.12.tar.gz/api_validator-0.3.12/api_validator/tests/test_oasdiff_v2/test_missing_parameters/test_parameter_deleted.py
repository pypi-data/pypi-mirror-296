import unittest
from api_validator.oasdiff_v2.diff_data import DiffData
from api_validator.oasdiff_v2.parameters.modified_parameters import ModifiedParameterData
from api_validator.oasdiff_v2.parameters.parameter_data import ParameterDataJSONEncoder
from api_validator.oasdiff_v2.missing_parameters_utils import (
    get_raw_modified_endpoint_tree,
    get_raw_parameter_data_for_modified_method
)


class ParameterTypeChangedTestCase(unittest.TestCase):
    def setUp(self):
        self.diff_data = DiffData()
        self.parameter_data = ModifiedParameterData()

    def test_query_parameter_deleted(self):
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

    def test_path_parameter_deleted(self):
        pass

    def test_header_parameter_deleted(self):
        pass

    def test_cookie_parameter_deleted(self):
        pass

