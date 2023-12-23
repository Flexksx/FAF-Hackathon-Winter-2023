import pandas as pd
from database.scripts.dbclasses.Database import Database

# teachers_df = Database().extract.teachers()
subjects_df = Database().extract.subjects()
subjects_df = subjects_df.where(subjects_df["semester"]>1).dropna()
print(subjects_df)