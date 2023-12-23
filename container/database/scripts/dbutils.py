import sqlite3
import pandas as pd
from dotenv import load_dotenv




def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to SQLite version: ", sqlite3.version)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

