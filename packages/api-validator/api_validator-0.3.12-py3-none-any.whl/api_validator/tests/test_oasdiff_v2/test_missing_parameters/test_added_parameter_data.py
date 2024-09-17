from api_validator.oasdiff_v2.parameters.added_parameter_data import AddedParameterData
import unittest


class AddedParameterTestCase(unittest.TestCase):
    def setUp(self):
        self.parameter_data = AddedParameterData()

    def test_basic(self):
        data = {
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
        }
