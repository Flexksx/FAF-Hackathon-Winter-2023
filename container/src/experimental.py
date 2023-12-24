import pandas as pd
import numpy as np
from utils import get_needed_dfs
from classes.Selector import Selector

sl = Selector()

subjects_df, teachers_df, student_group = sl.get_group_dfs("FAF-233")

teachers_subjects_df = pd.merge(teachers_df, subjects_df, left_on="subject", right_on="id").rename(columns={
    "name_x": "teacher_name", "name_y": "subject_name", "id_x": "teacher_id", "id_y": "subject_id", "theory_y": "theoryhrs", "seminar_y": "seminarhrs", "lab_y": "labhrs", "project": "projecthrs", "theory_x": "theory", "seminar_x": "seminar", "lab_x": "lab"})

# print(subjects_df)
# print(teachers_df)
# print(student_group)
# print(teachers_subjects_df.columns)

days = ["mon", "tue", "wed", "thu", "fri", "sat"]
times = [f'{day}{i}' for day in days for i in range(1, 8)]
periods = range(1, 8)


# Create an empty DataFrame
schedule_df = pd.DataFrame(index=periods, columns=days)

# Optionally, fill the DataFrame with some initial values (e.g., placeholders or NaN)
schedule_df = schedule_df.fillna('')
for index, teacher in teachers_subjects_df.iterrows():
    theory = teacher["theoryhrs"]
    seminar = teacher["seminarhrs"]
    lab = teacher["labhrs"]
    project = teacher["projecthrs"]
    days_dict = {day: 0 for day in days}
    lessons_per_day = {day: 0 for day in days}

    # Count the available times for each day
    for day in days:
        for teacher_day in teacher.keys().values:
            if day in teacher_day and teacher[teacher_day] == 1:
                days_dict[day] += 1

    # Select the day with the most available times
    selected_day = max(days_dict, key=days_dict.get)

    for time in times:
        if selected_day in time:
            if schedule_df.loc[int(time[3:]), selected_day] != '':
                continue
            if teacher[time] == 1 and (theory > 0 or seminar > 0 or lab > 0 or project > 0):
                # Check if the lessons limit for the selected day is reached
                if lessons_per_day[selected_day] >= 5:
                    continue

                schedule_df.loc[int(time[3:]), selected_day] = teacher["subject_name"]
                lessons_per_day[selected_day] += 1

                if theory > 0:
                    teacher["theoryhrs"] -= 1
                    theory -= 1
                elif seminar > 0:
                    teacher["seminarhrs"] -= 1
                    seminar -= 1
                elif lab > 0:
                    teacher["labhrs"] -= 1
                    lab -= 1
                elif project > 0:
                    teacher["projecthrs"] -= 1
                    project -= 1

print(schedule_df)

