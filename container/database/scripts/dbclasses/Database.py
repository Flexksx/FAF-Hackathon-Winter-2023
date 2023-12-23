import sqlite3
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from os import getenv
from .Creator import DatabaseTableCreator
from .Extractor import DatabaseTableExtractor

class Database:
    def __init__(self):
        self.create = DatabaseTableCreator()
        self.extract = DatabaseTableExtractor()