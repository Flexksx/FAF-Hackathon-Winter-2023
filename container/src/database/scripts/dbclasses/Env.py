from typing import Any
from dotenv import load_dotenv
from os import getenv

class Env:
    def __init__(self):
        self.paths = self.get_paths()

    def get_paths(self) -> dict:
        paths = {
            "db": "",
            "groups": "",
            "rooms": "",
            "subjects": "",
            "teachers": ""
        }
        load_dotenv()
        paths["db"] = getenv("DBPATH")
        paths["groups"] = getenv("GROUPS")
        paths["rooms"] = getenv("ROOMS")
        paths["subjects"] = getenv("SUBJECTS")
        paths["teachers"] = getenv("TEACHERS")
        return paths