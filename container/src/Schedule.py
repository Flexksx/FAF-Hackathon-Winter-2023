import numpy as np
import pandas as pd
from database.scripts.dbclasses.Database import Database
from classes.Selector import Selector


class ScheduleMaker:
    def __init__(self):
        self.__sl = Selector()

    def empty_schedule(self):
        days = ["mon", "tue", "wed", "thu", "fri"]
        periods = range(1, 8)
        schedule_df = pd.DataFrame(index=periods, columns=days)
        schedule_df = schedule_df.fillna('')
        return schedule_df

    def empty_schedule_by_groups(self, groupnames: list):
        days = ["mon", "tue", "wed", "thu", "fri"]
        lessons = range(1, 8)
        index = pd.MultiIndex.from_product(
            [days, lessons], names=['day', 'lesson'])
        schedule_df = pd.DataFrame(index=index, columns=groupnames)
        schedule_df = schedule_df.fillna('')
        return schedule_df

    def __lessons_number_constraint(self, schedule_df, n):
        lessons_per_day = schedule_df.apply(
            lambda x: x.str.startswith(('c', 's', 'l', 'p')).sum(), axis=0)
        return not any(lessons_per_day > n)

    def generate_initial_schedule(self, groupnames: list, semesters: list):
        schedule = self.empty_schedule_by_groups(groupnames)
        groupdict = self.__sl.get_groups_dfs(groupnames, semesters)
        rooms = self.__sl.get_rooms_df()
        days = ["mon", "tue", "wed", "thu", "fri"]
        # lessons = [f'{day}{i}' for day in days for i in range(1, 8)]
        lessons = range(1, 8)
        for groupentry in groupdict:
            teachers = groupdict[groupentry]["map"]
            for index, t in teachers.iterrows():
                for day in days:
                    for lesson in lessons:
                        if schedule.loc[(day, lesson), groupentry] != '':
                            continue
                        if t.get(day+str(lesson)) == 1:
                            if t.get("theoryhrs") > 0:
                                schedule.loc[(day, lesson), groupentry] = "c," + \
                                    t.get("subject_name") + "," + \
                                    t.get("teacher_name")
                                t["theoryhrs"] -= 1
                            elif t.get("seminarhrs") > 0:
                                schedule.loc[(day, lesson), groupentry] = "s," + \
                                    t.get("subject_name") + "," + \
                                    t.get("teacher_name")
                                t["seminarhrs"] -= 1
                            elif t.get("labhrs") > 0:
                                schedule.loc[(day, lesson), groupentry] = "l," + \
                                    t.get("subject_name") + "," + \
                                    t.get("teacher_name")
                                t["labhrs"] -= 1
                            elif t.get("projecthrs") > 0:
                                schedule.loc[(day, lesson), groupentry] = "p," + \
                                    t.get("subject_name") + "," + \
                                    t.get("teacher_name")
                                t["projecthrs"] -= 1
                            else:
                                continue
            print()
        return schedule

# s = ScheduleMaker()
# # sch = s.empty_schedule_by_groups(["FAF-223", "FAF-221", "FAF-222"])
# sch = s.generate_initial_schedule(["FAF-223", "FAF-221", "FAF-222"], [3, 3, 3])
# print(sch)
