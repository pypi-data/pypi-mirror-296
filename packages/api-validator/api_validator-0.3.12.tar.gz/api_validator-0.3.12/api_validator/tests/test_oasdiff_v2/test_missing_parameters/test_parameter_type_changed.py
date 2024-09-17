import unittest


class ParameterTypeChangedTestCase(unittest.TestCase):
    def test_path_parameter_type_changed(self):
        path_data = {
            "/api/v4/bulk_imports/{import_id}/entities/{entity_id}/failures": {
                "operations": {
                    "modified": {
                        "GET": {
                            "parameters": {
                                "modified": {
                                    "path": {
                                        "entity_id": {
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
                                                }
                                            }
                                        },
                                        "import_id": {
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

    def test_query_parameter_type_changed(self):
        data = {
            "/api/v4/projects/{id}/alert_management_alerts/{alert_iid}/metric_images": {
                "operations": {
                    "modified": {
                        "GET": {
                            "parameters": {
                                "added": {
                                    "query": [
                                        "alert_iid"
                                    ]
                                },
                                "modified": {
                                    "path": {
                                        "alert_iid": {
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
                                                }
                                            }
                                        },
                                        "id": {
                                            "schema": {}
                                        }
                                    }
                                }
                            }
                        },
                        "POST": {
                            "parameters": {
                                "modified": {
                                    "path": {
                                        "alert_iid": {
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
                                                }
                                            }
                                        },
                                        "id": {
                                            "schema": {}
                                        }
                                    }
                                }
                            },
                            "requestBody": {
                                "required": {
                                    "from": True,
                                    "to": False
                                },
                                "content": {
                                    "mediaTypeAdded": [
                                        "application/json"
                                    ],
                                    "mediaTypeDeleted": [
                                        "multipart/form-data"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
        }

    def test_header_parameter_type_changed(self):
        pass

    def test_cookie_parameter_type_changed(self):
        pass
