from api_validator.oasdiff_v2.parameters.modified_parameters import ModifiedParameterData
import unittest


class ModifiedParameterTestCase(unittest.TestCase):
    def setUp(self):
        self.parameter_data = ModifiedParameterData()

    def test_load_from_modified(self):
        data = {
            "required": {
                "from": True,
                "to": False
            },
            "schema": {
                "type": {
                    "added": [
                        "string"
                    ]
                }
            }
        }
        self.parameter_data.load_from_modified(data, "path", "/hello/{name}", "GET", "name")
        self.assertEqual(self.parameter_data.parameter_type, "path")
        self.assertEqual(self.parameter_data.path, "/hello/{name}")
        self.assertEqual(self.parameter_data.http_method, "GET")
        self.assertEqual(self.parameter_data.name, "name")
        self.assertEqual(self.parameter_data.data, data)
