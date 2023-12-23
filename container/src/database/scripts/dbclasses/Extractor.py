import sqlite3
import pandas as pd
import numpy as np
from .Env import Env


class DatabaseTableExtractor:
    def __init__(self):
        paths = Env().get_paths()
        self.__dbpath = paths["db"]
        self.__conn = self.__create_connection()

    def __create_connection(self):
        return sqlite3.connect(self.__dbpath)

    def __get_table(self, table):
        return pd.read_sql_query(f"SELECT * FROM {table}", self.__conn)

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

    def teachers_json(self) -> pd.DataFrame:
        return self.__get_table_json("teachers")

    # def __get_joined(self):