import pandas as pd
import numpy as np
from classes.Selector import Selector

sl = Selector()

subjects_df, teachers_df, student_group, teachers_subjects_df = sl.get_group_dfs("FAF-223",3)



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


    for time in times:
        if teacher[time] == 1 and (theory > 0 or seminar > 0 or lab > 0 or project > 0):
            # Check if the lessons limit for the selected day is reached

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

