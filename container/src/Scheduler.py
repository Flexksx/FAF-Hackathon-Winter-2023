import pandas as pd
from database.scripts.dbclasses.Database import Database
from utils import apply_subject_round


db = Database()

# teachers_df = db.extract.teachers()
groups_df = db.extract.groups()
subjects_df = db.extract.subjects()
subjects_df = apply_subject_round(subjects_df)
student_group_id = groups_df[groups_df["name"] == "FAF-223"]
gr_sub_map_df = db.extract.group_subjects_maptable()
gr_sub_map_df = gr_sub_map_df.loc[gr_sub_map_df["group_id"]
                                  == student_group_id["id"].values[0]]
print(gr_sub_map_df)



# groups_subjects_joined_df = pd.merge(groups_df, gr_sub_map_df, left_on="id", right_on="group_id")
# groups_subjects_joined_df = pd.merge(groups_subjects_joined_df, subjects_df, left_on="subject_id", right_on="id")
# print(groups_subjects_joined_df)

days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
times = [f'{day}{i}' for day in days for i in range(1, 8)]


# print(subjects_df)
