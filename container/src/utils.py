import numpy as np
from database.scripts.dbclasses.Database import Database


def custom_round(value):
    if np.isnan(value):
        return 0
    elif value == 0.9375:
        return 1.0
    elif value == 0.46875:
        return 0.5
    elif value == 1.40625:
        return 1.5
    elif value == 1.875:
        return 2
    elif value == 1.125:
        # Handle the case of 1.125 according to your requirements
        # For example, you can round it to 1 or 1.5 based on your preference
        return 1.5
    else:
        # For other values, you can use the default rounding behavior
        return round(value)

def apply_subject_round(df):
    df["theory"] = (df["theory"]/32).apply(custom_round)
    df["seminar"] = (df["seminar"]/32).apply(custom_round)
    df["lab"] = (df["lab"]/32).apply(custom_round)
    df["project"] = (df["project"]/32).apply(custom_round)
    return df


def get_needed_dfs():
    db = Database()

    """Extract data from database"""
    teachers_df = db.extract.teachers()
    groups_df = db.extract.groups()
    subjects_df = db.extract.subjects()

    subjects_df = apply_subject_round(subjects_df)

    student_group = groups_df.loc[groups_df["name"]=="FAF-223"]

    gr_sub_map_df = db.extract.group_subjects_maptable()
    gr_sub_map_df = gr_sub_map_df.loc[gr_sub_map_df["group_id"]
                                    == student_group["id"].values[0]]

    subject_ids = gr_sub_map_df["subject_id"]
    subjects_df = subjects_df.loc[(subjects_df["id"].isin(
        subject_ids)) & (subjects_df["semester"] == 3)]

    teachers_df = teachers_df.loc[teachers_df["id"].isin(
        subjects_df["id"].values)]

    return subjects_df, teachers_df, student_group