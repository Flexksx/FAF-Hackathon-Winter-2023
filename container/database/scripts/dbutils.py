import sqlite3
import pandas as pd
from dotenv import load_dotenv
from os import getenv


def get_paths():
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


def create_connection(db_file = get_paths()["db"]):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to SQLite version: ", sqlite3.version)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_rooms_table(conn: sqlite3.Connection):
    """Creates a table containing the rooms.

    Args:
        conn (sqlite3.Connection): The connection to your database
    """
    roomsdf = pd.read_csv(get_paths()["rooms"])
    print(roomsdf)
