import json
import unittest
from api_validator.oasdiff_v2.diff_data import DiffData
from api_validator.oasdiff_v2.parameters.modified_parameters import ModifiedParameterData
from api_validator.oasdiff_v2.parameters.parameter_data import ParameterDataJSONEncoder


class ParameterDefaultValueChanged(unittest.TestCase):
    """
    Test cases:
    - Default value change for QUERY parameter
    - Default value change for PATH parameter
    - Default value change for REQUEST BODY parameter on a POST request
    - Default value change for REQUEST BODY parameter on a PUT request
    - Default value change for REQUEST BODY parameter on a PATCH request
    - Default value change for REQUEST BODY parameter on a DELETE request
    - Default value change for HEADER parameter
    - Default value change for COOKIE parameter
    """
    def setUp(self):
        self.diff_data = DiffData()
        self.parameter_data = ModifiedParameterData()

    def test_default_value_changed_query_parameter(self):
        """Case: Default value change for QUERY parameter"""
        data = {
            "/v1/auth/roles": {
                "operations": {
                    "added": [
                        "HEAD"
                    ],
                    "modified": {
                        "DELETE": {
                            "parameters": {
                                "modified": {
                                    "query": {
                                        "username": {
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    }
                }
            }
        }
        self.diff_data.load_path_data(data)
        changed = self.diff_data.parameters_with_changed_default_values()
        self.assertEqual(len(changed), 1)

    def test_default_value_changed_path_parameter(self):
        """Case: Default value change for PATH parameter. Example data: universalis.json"""
        data = {
            "/api/{worldDcRegion}/{itemIds}": {
                "operations": {
                    "modified": {
                        "GET": {
                            "parameters": {
                                "modified": {
                                    "header": {
                                        "user-agent": {
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
                                            }
                                        }
                                    },
                                    "path": {
                                        "itemIds": {
                                            "description": {
                                                "from": "The item ID or comma-separated item IDs to retrieve data for.",
                                                "to": ""
                                            }
                                        },
                                        "worldDcRegion": {
                                            "description": {
                                                "from": "The world, data center, or region to retrieve data for. This may be an ID or a name. Regions should be specified as Japan, Europe, North-America, Oceania, China, or \u4e2d\u56fd.",
                                                "to": ""
                                            }
                                        }
                                    },
                                    "query": {
                                        "entries": {
                                            "description": {
                                                "from": "The number of recent history entries to return per item. By default, a maximum of 5 entries will be returned.",
                                                "to": ""
                                            },
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
                                            }
                                        },
                                        "entriesWithin": {
                                            "description": {
                                                "from": "The amount of time before now to take entries within, in seconds. Negative values will be ignored.",
                                                "to": ""
                                            },
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
                                            }
                                        },
                                        "fields": {
                                            "description": {
                                                "from": "A comma separated list of fields that should be included in the response, if omitted will return all fields.\r\nFor example, if you're only interested in the listings price per unit you can set this to listings.pricePerUnit.\r\nNote that querying multiple items changes the response schema, which should be reflected in the value provided\r\nfor this field. In this case, querying the price per unit requires setting this field to\r\nitems.listings.pricePerUnit.",
                                                "to": ""
                                            },
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
                                            }
                                        },
                                        "hq": {
                                            "description": {
                                                "from": "Filter for HQ listings and entries. By default, both HQ and NQ listings and entries will be returned.",
                                                "to": ""
                                            },
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
                                            }
                                        },
                                        "listings": {
                                            "description": {
                                                "from": "The number of listings to return per item. By default, all listings will be returned.",
                                                "to": ""
                                            },
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
                                            }
                                        },
                                        "statsWithin": {
                                            "description": {
                                                "from": "The amount of time before now to calculate stats over, in milliseconds. By default, this is 7 days.",
                                                "to": ""
                                            },
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
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

    def test_default_value_changed_post_request_body_parameter(self):
        """Case: Default value change for REQUEST BODY parameter on a POST request"""

    def test_default_value_changed_put_request_body_parameter(self):
        """Case: Default value change for REQUEST BODY parameter on a PUT request"""

    def test_default_value_changed_patch_request_body_parameter(self):
        """Case: Default value change for REQUEST BODY parameter on a PATCH request"""

    def test_default_value_changed_delete_request_body_parameter(self):
        """Case: Default value change for REQUEST BODY parameter on a DELETE request"""

    def test_default_value_changed_header_parameter(self):
        """Case: Default value change for HEADER parameter"""

    def test_default_value_changed_cookie_parameter(self):
        """Case: Default value change for COOKIE parameter"""
