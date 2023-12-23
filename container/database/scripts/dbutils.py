import sqlite3
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from os import getenv


class Database:
    def __init__(self):
        self.tables = ["rooms", "subjects", "groups", "teachers"]
        paths = self.get_paths()
        self.dbpath = paths["db"]
        self.rooms_path = paths["rooms"]
        self.subjects_path = paths["subjects"]
        self.groups_path = paths["groups"]
        self.teachers_path = paths["teachers"]
        self.conn = self.__create_connection()

    def get_paths(self):
        paths = {
            "db": "",
            "rooms": "",
            "subjects": "",
            "groups": "",
            "teachers": ""
        }
        load_dotenv()
        paths["db"] = getenv("DBPATH")
        paths["groups"] = getenv("GROUPS")
        paths["rooms"] = getenv("ROOMS")
        paths["subjects"] = getenv("SUBJECTS")
        paths["teachers"] = getenv("TEACHERS")
        return paths

    def __create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.dbpath)
            print("Connected to SQLite version: ", sqlite3.version)
            return conn
        except sqlite3.Error as e:
            print(e)
        return conn

    def create_rooms_table(self, conn: sqlite3.Connection):
        query = """
        CREATE TABLE IF NOT EXISTS rooms (
            id TEXT PRIMARY KEY,
            is_lab BOOLEAN NOT NULL,
            capacity INTEGER
        )
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            print("Created rooms table")
        except sqlite3.Error as e:
            print(e)
        cursor.close()

    def insert_rooms(self):
        roomsdf = pd.read_csv(self.rooms_path)
        roomsdf.rename(columns={
                       "id ": "id", "nr_persons": "capacity", "is_lab_cab": "is_lab"}, inplace=True)
        roomsdf["is_lab"] = roomsdf["is_lab"].astype(bool)
        roomsdf["id"] = roomsdf["id"].astype(str)
        roomsdf["capacity"] = roomsdf["capacity"].astype(int)
        print(roomsdf.columns)
        try:
            roomsdf.to_sql("rooms", self.conn, if_exists="append", index=False)
            print("Inserted data into rooms table")
        except sqlite3.Error as e:
            print(e)

    def create_teachers_table(self):
        query = """CREATE TABLE IF NOT EXISTS teachers (
            id INT PRIMARY KEY,
            name TEXT NOT NULL,
            subject TEXT NOT NULL,
            mon1 BOOLEAN NOT NULL,
            mon2 BOOLEAN NOT NULL,
            mon3 BOOLEAN NOT NULL,
            mon4 BOOLEAN NOT NULL,
            mon5 BOOLEAN NOT NULL,
            mon6 BOOLEAN NOT NULL,
            mon7 BOOLEAN NOT NULL,
            tue1 BOOLEAN NOT NULL,
            tue2 BOOLEAN NOT NULL,
            tue3 BOOLEAN NOT NULL,
            tue4 BOOLEAN NOT NULL,
            tue5 BOOLEAN NOT NULL,
            tue6 BOOLEAN NOT NULL,
            tue7 BOOLEAN NOT NULL,
            wed1 BOOLEAN NOT NULL,
            wed2 BOOLEAN NOT NULL,
            wed3 BOOLEAN NOT NULL,
            wed4 BOOLEAN NOT NULL,
            wed5 BOOLEAN NOT NULL,
            wed6 BOOLEAN NOT NULL,
            wed7 BOOLEAN NOT NULL,
            thu1 BOOLEAN NOT NULL,
            thu2 BOOLEAN NOT NULL,
            thu3 BOOLEAN NOT NULL,
            thu4 BOOLEAN NOT NULL,
            thu5 BOOLEAN NOT NULL,
            thu6 BOOLEAN NOT NULL,
            thu7 BOOLEAN NOT NULL,
            fri1 BOOLEAN NOT NULL,
            fri2 BOOLEAN NOT NULL,
            fri3 BOOLEAN NOT NULL,
            fri4 BOOLEAN NOT NULL,
            fri5 BOOLEAN NOT NULL,
            fri6 BOOLEAN NOT NULL,
            fri7 BOOLEAN NOT NULL
        )"""
        cursor = self.conn.cursor()


    def insert_teachers(self):
        teachersdf = pd.read_csv(get_paths()["teachers"])
        print(teachersdf)

    def create_subjects_table(conn: sqlite3.Connection):
        subjectsdf = pd.read_csv(get_paths()["subjects"])
        print(subjectsdf)

    def create_groups_table(conn: sqlite3.Connection):
        groupsdf = pd.read_csv(get_paths()["groups"])
        print(groupsdf)
