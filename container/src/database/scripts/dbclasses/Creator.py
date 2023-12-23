import sqlite3
import pandas as pd
import numpy as np
from .Env import Env


class DatabaseTableCreator:
    def __init__(self):
        self.tables = ["rooms", "subjects", "groups", "teachers"]
        paths = Env().get_paths()
        self.__dbpath = paths["db"]
        self.__rooms_path = paths["rooms"]
        self.__subjects__path = paths["subjects"]
        self.__groups_path = paths["groups"]
        self.__teachers_path = paths["teachers"]
        self.__conn = self.__create_connection()

    def __create_connection(self) -> sqlite3.Connection:
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.__dbpath)
            # print("Connected to SQLite version: ", sqlite3.version)
            return conn
        except sqlite3.Error as e:
            print(e)
        return conn

    def __create_rooms_table(self, conn: sqlite3.Connection) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS rooms (
            id TEXT PRIMARY KEY,
            is_lab BOOLEAN,
            capacity INT
        )
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            print("Created rooms table")
        except sqlite3.Error as e:
            print(e)
        cursor.close()

    def __insert_rooms(self) -> None:
        roomsdf = pd.read_csv(self.__rooms_path)
        roomsdf.rename(columns={
                       "id ": "id", "nr_persons": "capacity", "is_lab_cab": "is_lab"}, inplace=True)
        roomsdf["is_lab"] = roomsdf["is_lab"].astype(bool)
        roomsdf["id"] = roomsdf["id"].astype(str)
        roomsdf["capacity"] = roomsdf["capacity"].astype(int)
        print(roomsdf.columns)
        try:
            roomsdf.to_sql("rooms", self.__conn,
                           if_exists="append", index=False)
            print("Inserted data into rooms table")
        except sqlite3.Error as e:
            print(e)

    def __create_teachers_table(self):
        query = """CREATE TABLE IF NOT EXISTS teachers (
            id INT PRIMARY KEY,
            name TEXT NOT NULL,
            subject INT NOT NULL,
            theory BOOLEAN,
            seminar BOOLEAN,
            lab BOOLEAN,
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
            fri7 BOOLEAN NOT NULL,
            sat1 BOOLEAN NOT NULL,
            sat2 BOOLEAN NOT NULL,
            sat3 BOOLEAN NOT NULL,
            sat4 BOOLEAN NOT NULL,
            sat5 BOOLEAN NOT NULL,
            sat6 BOOLEAN NOT NULL,
            sat7 BOOLEAN NOT NULL,
            FOREIGN KEY (subject) REFERENCES subjects(id)
        )"""
        cursor = self.__conn.cursor()
        try:
            cursor.execute(query)
            print("Created teachers table")
        except sqlite3.Error as e:
            print(e)

    def __create_subjects_table(self):
        query = """CREATE TABLE IF NOT EXISTS subjects (
            id INT PRIMARY KEY,
            name TEXT,
            theory INT,
            seminar INT,
            lab INT,
            project INT,
            year INT,
            semester INT
        )"""
        cursor = self.__conn.cursor()
        try:
            cursor.execute(query)
            print("Created subjects table")
        except sqlite3.Error as e:
            print(e)

    def __create_groups_table(self):
        query = """CREATE TABLE IF NOT EXISTS studentgroups (
            id INT PRIMARY KEY,
            name TEXT,
            language TEXT,
            students INT
        )"""
        cursor = self.__conn.cursor()
        try:
            cursor.execute(query)
            print("Created groups table")
        except sqlite3.Error as e:
            print(e)

    def __create_groups_subjects_joint_table(self):
        query = """CREATE TABLE IF NOT EXISTS groups_subjects (
            group_id INT,
            subject_id INT,
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )"""
        cursor = self.__conn.cursor()
        try:
            cursor.execute(query)
            print("Created groups_subjects table")
        except sqlite3.Error as e:
            print(e)

    def __insert_groups_subjects(self):
        groups_df = pd.read_csv(self.__groups_path)
        groups_subjects_df = pd.DataFrame(columns=["group_id", "subject_id"])
        print(groups_df.columns)
        for group in groups_df.iterrows():
            subject_ids = group[1]["subject_ids"].split(",")
            group_id = group[1]["id"]
            for subject_id in subject_ids:
                if subject_id == 39:
                    groups_subjects_df = pd.concat([groups_subjects_df, pd.DataFrame(
                        {"group_id": [group_id], "subject_id": 118})])
                if subject_id == 40:
                    groups_subjects_df = pd.concat([groups_subjects_df, pd.DataFrame(
                        {"group_id": [group_id], "subject_id": 119})])
                else:
                    groups_subjects_df = pd.concat([groups_subjects_df, pd.DataFrame(
                        {"group_id": [group_id], "subject_id": subject_id})])
        try:
            groups_subjects_df.to_sql(
                "groups_subjects", self.__conn, if_exists="append", index=False)
            print("Inserted data into groups_subjects table")
        except sqlite3.Error as e:
            print(e)

    def __insert_groups(self):
        groups_df = pd.read_csv(self.__groups_path)
        groups_df.drop(columns=["subject_ids"], inplace=True)
        try:
            groups_df.to_sql("studentgroups", self.__conn,
                             if_exists="append", index=False)
            print("Inserted data into groups table")
        except sqlite3.Error as e:
            print(e)

    def __insert_subjects(self):
        subjects_df = pd.read_csv(self.__subjects__path)
        subjects_df
        try:
            subjects_df.to_sql("subjects", self.__conn,
                               if_exists="append", index=False)
            print("Inserted data into subjects table")
        except sqlite3.Error as e:
            print(e)

    def __insert_teachers(self):
        teachers_df = pd.read_csv(self.__teachers_path)
        for index, teacher in teachers_df.iterrows():
            if teacher["type"] == "TEOR,PRACT":
                teachers_df.at[index, "theory"] = 1
                teachers_df.at[index, "seminar"] = 1
                teachers_df.at[index, "lab"] = 0
            else:
                teachers_df.at[index, "theory"] = 0
                teachers_df.at[index, "seminar"] = 0
                teachers_df.at[index, "lab"] = 1
        teachers_df.drop(columns=["type"], inplace=True)
        teachers_df.rename(columns={
            "id": "id",
            "name": "name",
            "subject": "subject",
            "mon_per_1": "mon1",
            "mon_per_2": "mon2",
            "mon_per_3": "mon3",
            "mon_per_4": "mon4",
            "mon_per_5": "mon5",
            "mon_per_6": "mon6",
            "mon_per_7": "mon7",
            "tue_per_1": "tue1",
            "tue_per_2": "tue2",
            "tue_per_3": "tue3",
            "tue_per_4": "tue4",
            "tue_per_5": "tue5",
            "tue_per_6": "tue6",
            "tue_per_7": "tue7",
            "wed_per_1": "wed1",
            "wed_per_2": "wed2",
            "wed_per_3": "wed3",
            "wed_per_4": "wed4",
            "wed_per_5": "wed5",
            "wed_per_6": "wed6",
            "wed_per_7": "wed7",
            "thu_per_1": "thu1",
            "thu_per_2": "thu2",
            "thu_per_3": "thu3",
            "thu_per_4": "thu4",
            "thu_per_5": "thu5",
            "thu_per_6": "thu6",
            "thu_per_7": "thu7",
            "fri_per_1": "fri1",
            "fri_per_2": "fri2",
            "fri_per_3": "fri3",
            "fri_per_4": "fri4",
            "fri_per_5": "fri5",
            "fri_per_6": "fri6",
            "fri_per_7": "fri7",
            "sat_per_1": "sat1",
            "sat_per_2": "sat2",
            "sat_per_3": "sat3",
            "sat_per_4": "sat4",
            "sat_per_5": "sat5",
            "sat_per_6": "sat6",
            "sat_per_7": "sat7"
        }, inplace=True)
        try:
            teachers_df.to_sql("teachers", self.__conn,
                               if_exists="append", index=False)
            print("Inserted data into teachers table")
        except sqlite3.Error as e:
            print(e)

    def drop_all_tables(self):
        cursor = self.__conn.cursor()
        for table in self.tables:
            try:
                cursor.execute(f"DROP TABLE {table}")
                print(f"Dropped table {table}")
            except sqlite3.Error as e:
                print(e)
        cursor.close()

    def create_all_tables(self):
        self.__create_rooms_table(self.__conn)
        self.__create_teachers_table()
        self.__create_subjects_table()
        self.__create_groups_table()
        self.__create_groups_subjects_joint_table()

    def insert_all_data(self):
        self.__insert_rooms()
        self.__insert_groups()
        self.__insert_subjects()
        self.__insert_teachers()
        self.__insert_groups_subjects()

    def reload_tables(self):
        self.drop_all_tables()
        self.create_all_tables()
        self.insert_all_data()
