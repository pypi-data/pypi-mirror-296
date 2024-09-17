import json
import unittest
from api_validator.oasdiff_v2.diff_data import DiffData
from api_validator.oasdiff_v2.parameters.modified_parameters import ModifiedParameterData
from api_validator.oasdiff_v2.parameters.parameter_data import ParameterDataJSONEncoder


class ParameterNotRequiredAnymore(unittest.TestCase):
    """
    Test cases:
    - Query parameter not required anymore
    - Path parameter not required anymore
    - Header parameter not required anymore
    - Cookie parameter not required anymore
    - Request body parameter not required anymore
    """
    def setUp(self):
        self.diff_data = DiffData()
        self.parameter_data = ModifiedParameterData()

    def test_required_status_changed_query_parameter(self):
        data = {
            "/workshop/api/mechanic/mechanic_report": {
                "operations": {
                    "modified": {
                        "GET": {
                            "parameters": {
                                "modified": {
                                    "query": {
                                        "report_id": {
                                            "style": {
                                                "from": "form",
                                                "to": ""
                                            },
                                            "explode": {
                                                "from": True,
                                                "to": None
                                            },
                                            "required": {
                                                "from": True,
                                                "to": False
                                            },
                                            "schema": {
                                                "type": {
                                                    "added": [
                                                        "string"
                                                    ],
                                                    "deleted": [
                                                        "integer"
                                                    ]
                                                },
                                                "format": {
                                                    "from": "int32",
                                                    "to": ""
                                                },
                                                "example": {
                                                    "from": 2,
                                                    "to": None
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "securityRequirements": {
                                "deleted": [
                                    "bearerAuth"
                                ]
                            }
                        }
                    }
                }
            },
        }
        self.diff_data.load_path_data(data)
        changed = self.diff_data.parameters_with_changed_requirements()
        # print(json.dumps(changed, indent=4, cls=ParameterDataEncoder))
        self.assertEqual(changed[0].name, "report_id", "The parameter name should be 'report_id'")
        self.assertEqual(changed[0].parameter_type, "query", "The parameter type should be 'query'")
        self.assertEqual(changed[0].http_method, "GET", "The HTTP method should be 'GET'")
        self.assertEqual(changed[0].path, "/workshop/api/mechanic/mechanic_report", "The path should be '/workshop/api/mechanic/mechanic_report'")
        self.assertEqual(len(changed), 1)

    # def test_required_status_changed_path_parameter(self):
    #     pass

    def test_required_status_changed_header_parameter(self):
        # Case: eshop-ordering-api.json
        data = {
            "/api/v1/orders": {
                "operations": {
                    "modified": {
                        "GET": {
                            "securityRequirements": {
                                "deleted": [
                                    "oauth2"
                                ]
                            }
                        },
                        "POST": {
                            "parameters": {
                                "modified": {
                                    "header": {
                                        "x-requestid": {
                                            "style": {
                                                "from": "simple",
                                                "to": ""
                                            },
                                            "required": {
                                                "from": True,
                                                "to": False
                                            },
                                            "schema": {
                                                "format": {
                                                    "from": "uuid",
                                                    "to": ""
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "requestBody": {
                                "content": {
                                    "mediaTypeModified": {
                                        "application/json": {
                                            "schema": {
                                                "schemaAdded": True
                                            }
                                        }
                                    }
                                }
                            },
                            "securityRequirements": {
                                "deleted": [
                                    "oauth2"
                                ]
                            }
                        }
                    }
                }
            },
        }

    def test_required_status_changed_request_body_parameter(self):
        data = {
            "/api/v4/markdown": {
                "operations": {
                    "modified": {
                        "POST": {
                            "requestBody": {
                                "required": {
                                    "from": True,
                                    "to": False
                                },
                                "content": {
                                    "mediaTypeModified": {
                                        "application/json": {
                                            "schema": {
                                                "schemaAdded": True
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
        }
