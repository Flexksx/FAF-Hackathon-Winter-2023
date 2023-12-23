import sqlite3
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from os import getenv
from .DatabaseTableCreator import DatabaseTableCreator
from .DatabaseTableExtractor import DatabaseTableExtractor

class Database:
    def __init__(self):
        self.creator = DatabaseTableCreator()
        self.extract = DatabaseTableExtractor()