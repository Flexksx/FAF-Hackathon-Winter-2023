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

    def __get_table(self, table) -> pd.DataFrame:
        return pd.read_sql_query(f"SELECT * FROM {table}", self.__conn)

    def __get_table_json(self, table):
        return self.__get_table(table).to_json(orient="records")

    def group_subjects_maptable(self):
        return self.__get_table("groups_subjects")

    def rooms(self):
        return self.__get_table("rooms")

    def subjects(self):
        return self.__get_table("subjects")

    def groups(self):
        return self.__get_table("studentgroups")

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

    def join(self, table1, table2, on):
        return pd.read_sql_query(f"SELECT * FROM {table1} JOIN {table2} ON {on}", self.__conn)

    def groups_subjects_joined(self):
        query = """
        SELECT sg.name AS groupname,
        sg.language AS language,
        sg.students AS students,
        s.name AS subjectname,
        s.theory AS theory,
        s.seminar AS seminar,
        s.lab AS lab,
        s.project AS project,
        s.year AS year,
        s.semester AS semester
        FROM studentgroups AS sg
        INNER JOIN groups_subjects AS gs
        ON sg.id = gs.group_id
        INNER JOIN subjects AS s
        ON gs.subject_id = s.id
        """
        return pd.read_sql_query(query, self.__conn)
