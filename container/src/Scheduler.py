import pandas as pd
from database.scripts.dbclasses.Database import Database

teachers_df = Database().extract.teachers()

