"""
Parse the Oasdiff results
"""
import json


def parse_oasdiff_results(data: dict) -> dict:
    """
    Parse the Oasdiff results
    """


class ModifiedPath:
    def __init__(self):
        self.path: str = ""
        self.deleted_operations: list = []
        self.added_operations: list = []
        self.modified_operations: dict = {}

    def load(self, data: dict):
        self.path = data.get("path", "")
        self.deleted_operations = data.get("operations", {}).get("deleted", [])
        self.added_operations = data.get("operations", {}).get("added", [])
        self.modified_operations = data.get("operations", {}).get("modified", {})


class OasdiffParser:
    def __init__(self):
        self.data: dict = {}
        self.deleted_paths: list = []
        self.added_paths: list = []
        self.modified_paths: dict = {}

    def load(self, data: dict):
        self.data = data
        self.deleted_paths = self.data.get("paths", {}).get("deleted", [])
        self.deleted_paths.sort()
        self.added_paths = self.data.get("paths", {}).get("added", [])
        self.added_paths.sort()
        self.modified_paths = self.data.get("paths", {}).get("modified", {})


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Parse the Oasdiff results file")
    parser.add_argument("file", help="The Oasdiff results file")
    args = parser.parse_args()
    with open(args.file, "r") as f:
        oasdiff_data = json.load(f)
    result = parse_oasdiff_results(oasdiff_data)
    print(result)
