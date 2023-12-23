import sqlite3
import pandas as pd
import numpy as np
from .Env import Env


class DatabaseTableExtractor:
    def __init__(self):
        self.tables = ["rooms", "subjects", "groups", "teachers"]
        paths = Env().get_paths()
        self.dbpath = paths["db"]
        self.rooms_path = paths["rooms"]
        self.subjects_path = paths["subjects"]
        self.groups_path = paths["groups"]
        self.teachers_path = paths["teachers"]
        self.conn = self.__create_connection()

    def __create_connection(self):
        return sqlite3.connect(self.dbpath)

    def __get_table(self, table):
        return pd.read_sql_query(f"SELECT * FROM {table}", self.conn)

    def __get_table_json(self, table):
        return self.__get_table(table).to_json(orient="records")


    def rooms(self):
        return self.__get_table("rooms")

    def subjects(self):
        return self.__get_table("subjects")

    def groups(self):
        return self.__get_table("groups")

    def teachers(self):
        return self.__get_table("teachers")

    def rooms_json(self):
        return self.__get_table_json("rooms")

    def subjects_json(self):
        return self.__get_table_json("subjects")

    def groups_json(self):
        return self.__get_table_json("groups")

    def teachers_json(self):
        return self.__get_table_json("teachers")


