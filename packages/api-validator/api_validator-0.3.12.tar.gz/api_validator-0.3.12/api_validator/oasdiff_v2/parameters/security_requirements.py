class SecurityRequirements:
    """
    Security requirements are the types of authentication required for a given endpoint.
    """
    def __init__(self):
        self.data: dict = {}
        raise NotImplementedError("Have not implemented this yet. I just created the scaffolding for the class so we can add it later.")

    def __eq__(self, other):
        return self.data == other.data

    def __str__(self):
        return self.data

    def __repr__(self):
        return "SecurityRequirements({})".format(self.data)

    def load(self, data: dict):
        """
        Load the security requirements data.

        Specifically:
            paths.modified.{path}.operations.modified.{http_method}.securityRequirements
        """
        self.data = data

    def changed_security_requirements(self) -> bool:
        """
        Did the security requirements change?

        Example values:
            - argus-eye-django.json

        Example:
            "added": [
                "basicAuth",
                "cookieAuth",
                "tokenAuth",
                "jwtAuth",
                ""
            }
        """
        return bool(self.added_security_requirements)

    def deleted_security_requirements(self) -> list:
        """
        Did the security requirements change?

        This file has good example values: argus-eye-django.json

        Example data:
            "deleted": [
                "basicAuth",
                "cookieAuth",
                "tokenAuth",
                "jwtAuth",
                ""
            ]
        """
        if "deleted" in self.data:
            return self.data["deleted"]
        return []

    def added_security_requirements(self) -> list:
        """
        Did the security requirements change?

        This file has good example values: argus-eye-django.json

        Example data:
            "added": [
                "basicAuth",
                "cookieAuth",
                "tokenAuth",
                "jwtAuth",
                ""
            ]
        """
        if "added" in self.data:
            return self.data["added"]
        return []
