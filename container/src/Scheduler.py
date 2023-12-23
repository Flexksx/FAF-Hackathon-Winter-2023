import pandas as pd
from utils import apply_subject_round, Database, get_needed_dfs



subjects_df, teachers_df, student_group = get_needed_dfs()
# print(subjects_df)
# print(teachers_df)
# print(student_group)



days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
times = [f'{day}{i}' for day in days for i in range(1, 8)]
periods = range(1, 8)


# Create an empty DataFrame
empty_schedule_df = pd.DataFrame(index=periods, columns=days)

# Optionally, fill the DataFrame with some initial values (e.g., placeholders or NaN)
empty_schedule_df = empty_schedule_df.fillna('')

print(empty_schedule_df)