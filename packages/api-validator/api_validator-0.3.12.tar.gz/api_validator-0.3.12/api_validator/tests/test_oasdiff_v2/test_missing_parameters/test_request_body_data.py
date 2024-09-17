import json
import unittest

import api_validator.oasdiff_v2.parameters.parameter_data
from api_validator.oasdiff_v2.parameters.modified_request_body_parameters import ModifiedRequestBodyParameters
from api_validator.oasdiff_v2.diff_data import DiffData
from api_validator.oasdiff_v2.parameters.parameter_data import ParameterDataJSONEncoder


class TestModifiedRequestBodyParameters(unittest.TestCase):
    def setUp(self):
        self.kubero_data = {
            "/api/cli/apps": {
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
                                                "required": {
                                                    "deleted": [
                                                        "name",
                                                        "pipeline",
                                                        "buildpack",
                                                        "ssl",
                                                        "podsize",
                                                        "branch",
                                                        "phase",
                                                        "autodeploy",
                                                        "domain"
                                                    ]
                                                },
                                                "properties": {
                                                    "added": [
                                                        "security",
                                                        "appname",
                                                        "web",
                                                        "ingress",
                                                        "buildstrategy",
                                                        "cronjobs",
                                                        "envvars",
                                                        "extraVolumes",
                                                        "worker"
                                                    ],
                                                    "deleted": [
                                                        "name",
                                                        "envVars"
                                                    ],
                                                    "modified": {
                                                        "addons": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "array"
                                                                ]
                                                            },
                                                            "items": {
                                                                "schemaDeleted": True
                                                            }
                                                        },
                                                        "autodeploy": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "boolean"
                                                                ]
                                                            }
                                                        },
                                                        "autoscale": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "boolean"
                                                                ]
                                                            }
                                                        },
                                                        "branch": {
                                                            "example": {
                                                                "from": "main",
                                                                "to": None
                                                            }
                                                        },
                                                        "buildpack": {
                                                            "example": {
                                                                "from": "NodeJS",
                                                                "to": None
                                                            }
                                                        },
                                                        "domain": {
                                                            "example": {
                                                                "from": "myapp.lacolhost.com",
                                                                "to": None
                                                            }
                                                        },
                                                        "gitrepo": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "object"
                                                                ]
                                                            }
                                                        },
                                                        "image": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "object"
                                                                ]
                                                            },
                                                            "properties": {
                                                                "deleted": [
                                                                    "tag",
                                                                    "build",
                                                                    "containerPort",
                                                                    "fetch",
                                                                    "repository",
                                                                    "run"
                                                                ]
                                                            }
                                                        },
                                                        "phase": {
                                                            "example": {
                                                                "from": "Test",
                                                                "to": None
                                                            }
                                                        },
                                                        "pipeline": {
                                                            "example": {
                                                                "from": "example",
                                                                "to": None
                                                            }
                                                        },
                                                        "podsize": {
                                                            "example": {
                                                                "from": "small",
                                                                "to": None
                                                            }
                                                        },
                                                        "ssl": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "boolean"
                                                                ]
                                                            }
                                                        }
                                                    }
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
        self.valetudo_data = {
            "/api/v2/timers/": {
                "operations": {
                    "modified": {
                        "POST": {
                            "requestBody": {
                                "content": {
                                    "mediaTypeModified": {
                                        "application/json": {
                                            "schema": {
                                                "description": {
                                                    "from": "Everything time-related is in UTC",
                                                    "to": ""
                                                },
                                                "required": {
                                                    "deleted": [
                                                        "dow",
                                                        "hour",
                                                        "minute",
                                                        "action",
                                                        "enabled"
                                                    ]
                                                },
                                                "properties": {
                                                    "deleted": [
                                                        "id"
                                                    ],
                                                    "modified": {
                                                        "action": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "object"
                                                                ]
                                                            },
                                                            "additionalPropertiesAllowed": {
                                                                "from": False,
                                                                "to": None
                                                            },
                                                            "properties": {
                                                                "deleted": [
                                                                    "params",
                                                                    "type"
                                                                ]
                                                            }
                                                        },
                                                        "dow": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "array"
                                                                ]
                                                            },
                                                            "description": {
                                                                "from": "Day of Week\nSunday = 0, Monday = 1, ... Saturday = 6",
                                                                "to": ""
                                                            },
                                                            "items": {
                                                                "schemaDeleted": True
                                                            }
                                                        },
                                                        "enabled": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "boolean"
                                                                ]
                                                            }
                                                        },
                                                        "hour": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "number"
                                                                ]
                                                            },
                                                            "min": {
                                                                "from": 0,
                                                                "to": None
                                                            },
                                                            "max": {
                                                                "from": 23,
                                                                "to": None
                                                            }
                                                        },
                                                        "label": {
                                                            "description": {
                                                                "from": "An optional user-defined label for the timer",
                                                                "to": ""
                                                            },
                                                            "pattern": {
                                                                "from": "^.{0,24}$",
                                                                "to": ""
                                                            }
                                                        },
                                                        "minute": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "number"
                                                                ]
                                                            },
                                                            "min": {
                                                                "from": 0,
                                                                "to": None
                                                            },
                                                            "max": {
                                                                "from": 59,
                                                                "to": None
                                                            }
                                                        },
                                                        "pre_actions": {
                                                            "type": {
                                                                "added": [
                                                                    "string"
                                                                ],
                                                                "deleted": [
                                                                    "array"
                                                                ]
                                                            },
                                                            "description": {
                                                                "from": "Actions to run before the main action (e.g. set fan speed to x)",
                                                                "to": ""
                                                            },
                                                            "items": {
                                                                "schemaDeleted": True
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            "examples": {
                                                "deleted": [
                                                    "full_cleanup",
                                                    "segment_cleanup"
                                                ]
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

    def test_kubero_request_body_data(self):
        http_method = "POST"
        path = "/api/cli/apps"
        media_type = "application/json"
        parameter_type = "requestBody"
        modified_properties = self.kubero_data[path]["operations"]["modified"][http_method][parameter_type]["content"]["mediaTypeModified"][media_type]["schema"]["properties"]["modified"]
        requirement_data = self.kubero_data[path]["operations"]["modified"][http_method][parameter_type]["content"]["mediaTypeModified"][media_type]["schema"]["required"]
        # TODO: Handle deleted properties and added properties
        deleted_properties = self.kubero_data[path]["operations"]["modified"][http_method][parameter_type]["content"]["mediaTypeModified"][media_type]["schema"]["properties"]["deleted"]
        added_properties = self.kubero_data[path]["operations"]["modified"][http_method][parameter_type]["content"]["mediaTypeModified"][media_type]["schema"]["properties"]["added"]

        # addons looks like this:
        # {'items': {'schemaDeleted': True}, 'type': {'added': ['string'], 'deleted': ['array']}}
        add_ons = modified_properties["addons"]
        parameter_data = ModifiedRequestBodyParameters()
        parameter_data.load_from_modified_media_type(
            data=add_ons, name="addons", path=path, http_method=http_method, media_type=media_type
        )
        self.assertTrue(parameter_data.changed_variable_type())

        # Create a new instance of ModifiedRequestBodyParameters
        parameter_data = ModifiedRequestBodyParameters()
        autodeploy = modified_properties["autodeploy"]
        parameter_data.load_from_modified_media_type(
            data=autodeploy, name="autodeploy", path=path, http_method=http_method, media_type=media_type
        )
        parameter_data.load_requirement_data(
            data=self.kubero_data[path]["operations"]["modified"][http_method][parameter_type]["content"]["mediaTypeModified"][media_type]["schema"]["required"]
        )
        # Assertions on the variable type
        self.assertTrue(parameter_data.changed_variable_type(), "The variable type has changed")
        self.assertListEqual(parameter_data.new_variable_type(), ["string"], "The new variable type is string")
        self.assertListEqual(parameter_data.old_variable_type(), ["boolean"], "The old variable type is boolean")
        # Assertions on the requirement status
        self.assertTrue(parameter_data.changed_requirement_status(), "The requirement status has changed")
        self.assertTrue(parameter_data.old_requirement_status(), "The old requirement status is True")
        self.assertFalse(parameter_data.new_requirement_status(), "The new requirement status is False")

    def test_diff_data(self):
        diff_data = DiffData()
        diff_data.load_path_data(self.kubero_data)
        params = diff_data.removed_parameters()
        removed = json.loads(json.dumps(params, indent=4, cls=ParameterDataJSONEncoder))
        # print(json.dumps(removed, indent=4))
        expected = [
            {
                "data": [
                    "name",
                    "envVars"
                ],
                "parameter_type": "requestBody",
                "name": "envVars",
                "http_method": "POST",
                "path": "/api/cli/apps"
            },
            {
                "data": [
                    "name",
                    "envVars"
                ],
                "parameter_type": "requestBody",
                "name": "name",
                "http_method": "POST",
                "path": "/api/cli/apps"
            }
        ]
        self.assertListEqual(removed, expected, "Parameters from requestBody should be in the list of removed parameters")

        params = diff_data.removed_request_data()
        removed = json.loads(json.dumps(params, indent=4, cls=ParameterDataJSONEncoder))
        print(json.dumps(removed, indent=4))
        self.assertListEqual(removed, expected, "Parameters from requestBody should be in the removed request data")

        # Parameters with changed variable types should include those in requestBody
        params = diff_data.parameters_with_changed_variable_types()
        names = [param.name for param in params]
        names.sort()
        expected = [
            "addons",
            "autodeploy",
            "autoscale",
            "gitrepo",
            "image",
            "ssl"
        ]
        self.assertListEqual(names, expected, "Parameters from requestBody should be included in the list of parameters with changed variables")
