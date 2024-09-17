import unittest

"""
Good test cases can be found by searching for "schemaDeleted": true or "enumDeleted": true in the oasdiff examples folder.
- kubero.json - /api/cli/apps
"""


class RequestBodyDeletedTestCase(unittest.TestCase):
    def test_request_body_deleted(self):
        data = {
            "/api/v4/features/{name}": {
                "operations": {
                    "modified": {
                        "POST": {
                            "parameters": {
                                "modified": {
                                    "path": {
                                        "name": {
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
                            },
                            "requestBody": {
                                "deleted": True
                            }
                        }
                    }
                }
            },
        }

    def test_media_type_deleted(self):
        """Case: mediaTypeDeleted. The test case is wallet-wasabi.json"""
        data = {
            "/WabiSabi/connection-confirmation": {
                "operations": {
                    "modified": {
                        "POST": {
                            "requestBody": {
                                "content": {
                                    "mediaTypeDeleted": [
                                        "application/*+json",
                                        "application/json-patch+json",
                                        "text/json"
                                    ],
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

    def test_media_type_added(self):
        """Case: mediaTypeAdded. The test case is Alibaba-Nacos.json"""
        data = {
            "/v1/cs/configs": {
                "operations": {
                    "added": [
                        "HEAD"
                    ],
                    "modified": {
                        "DELETE": {
                            "parameters": {
                                "modified": {
                                    "query": {
                                        "tenant": {
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
                        "GET": {
                            "parameters": {
                                "modified": {
                                    "query": {
                                        "dataId": {
                                            "required": {
                                                "from": True,
                                                "to": False
                                            }
                                        },
                                        "group": {
                                            "required": {
                                                "from": True,
                                                "to": False
                                            }
                                        },
                                        "tenant": {
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
                        "POST": {
                            "parameters": {
                                "added": {
                                    "query": [
                                        "_csrf"
                                    ]
                                },
                                "deleted": {
                                    "query": [
                                        "namespace",
                                        "file"
                                    ]
                                },
                                "modified": {
                                    "query": {
                                        "policy": {
                                            "schema": {
                                                "type": {
                                                    "added": [
                                                        "object"
                                                    ],
                                                    "deleted": [
                                                        "string"
                                                    ]
                                                },
                                                "enum": {
                                                    "enumDeleted": True,
                                                    "deleted": [
                                                        "ABORT",
                                                        "SKIP",
                                                        "OVERWRITE"
                                                    ]
                                                },
                                                "default": {
                                                    "from": "ABORT",
                                                    "to": None
                                                }
                                            }
                                        },
                                        "tenant": {
                                            "schema": {
                                                "default": {
                                                    "from": "",
                                                    "to": None
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "requestBody": {
                                "content": {
                                    "mediaTypeAdded": [
                                        "multipart/form-data"
                                    ],
                                    "mediaTypeDeleted": [
                                        "application/json"
                                    ]
                                }
                            }
                        }
                    }
                }
            },
        }

    def test_deleted_email_request_body_parameter(self):
        data = {
            "/identity/api/auth/forget-password": {
                "operations": {
                    "modified": {
                        "POST": {
                            "requestBody": {
                                "required": {
                                    "from": False,
                                    "to": True
                                },
                                "content": {
                                    "mediaTypeModified": {
                                        "application/json": {
                                            "schema": {
                                                "description": {
                                                    "from": "",
                                                    "to": "Class ForgetPassword"
                                                },
                                                "required": {
                                                    "deleted": [
                                                        "email"
                                                    ]
                                                },
                                                "properties": {
                                                    "modified": {
                                                        "email": {
                                                            "example": {
                                                                "from": "adam007@example.com",
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
                        }
                    }
                }
            }
        }

