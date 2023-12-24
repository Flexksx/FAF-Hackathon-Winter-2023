import copy
import math
import random
from database.scripts.dbclasses.Database import Database
from classes.Selector import Selector
from Schedule import ScheduleMaker


class ScheduleSimulatedAnnealing:
    def __init__(self, groupnames, semesters):
        self.__sl = Selector()
        self.groupnames = groupnames
        self.semesters = semesters
        self.initial_temperature = 100.0
        self.cooling_rate = 0.0015
        self.current_temperature = self.initial_temperature
        self.groupsdict = self.__sl.get_groups_dfs(groupnames, semesters)
        self.ready_schedule = self.anneal()

    # def calculate_distance_penalty(self, schedule):
    #     distance_penalty = 0
    #     for group in self.groupnames:
    #         group_schedule = schedule[group]

    #         # Filter valid lesson indices
    #         lesson_indices = [int(idx.replace(group, '')) for idx in group_schedule.index if group_schedule[idx].startswith(('c', 's', 'l', 'p'))]

    #         for i in range(len(lesson_indices) - 1):
    #             gap = lesson_indices[i + 1] - lesson_indices[i] - 1
    #             distance_penalty += max(0, gap)  # Only consider positive gaps as penalties

    #     return distance_penalty


    def evaluate_schedule(self, schedule):
        lesson_count = schedule.apply(lambda x: x.str.startswith(('c', 's', 'l', 'p')).sum(), axis=0).sum()
        # distance_penalty = self.calculate_distance_penalty(schedule)
        return lesson_count #- distance_penalty


    def __validate_teacher(self, teachers_df, lesson, groupname):
        if teachers_df.loc[teachers_df["id"] == lesson["teacher_id"]]["name"].values[0] in groupname:
            return True
        return False

    def generate_neighbour(self, current_schedule):
        # Your neighbourhood generation logic goes here
        # Generate a neighbouring solution for the current schedule
        # This could involve swapping or modifying lessons
        neighbour_schedule = copy.deepcopy(current_schedule)
        # For simplicity, swap two random lessons in a random day
        day = random.choice(neighbour_schedule.columns)
        lesson_indices = random.sample(range(len(neighbour_schedule)), 2)
        neighbour_schedule.iloc[lesson_indices, neighbour_schedule.columns.get_loc(day)] = \
            current_schedule.iloc[lesson_indices[::-1],
                                  current_schedule.columns.get_loc(day)].values
        return neighbour_schedule


    def acceptance_probability(self, current_cost, neighbour_cost, temperature):
        if neighbour_cost < current_cost:
            return 1.0
        return math.exp((current_cost - neighbour_cost) / temperature)

    def anneal(self):
        current_schedule = self.generate_initial_schedule()
        current_cost = self.evaluate_schedule(current_schedule)
        iteration = 0
        while self.current_temperature > 1:
            iteration += 1
            if iteration % 500 == 0:
                print(f'Iteration: {iteration}, Temperature: {
                    self.current_temperature}, Cost: {current_cost}')
            neighbour_schedule = self.generate_neighbour(current_schedule)
            neighbour_cost = self.evaluate_schedule(neighbour_schedule)

            acceptance_prob = self.acceptance_probability(
                current_cost, neighbour_cost, self.current_temperature)

            if acceptance_prob > random.random():
                current_schedule = copy.deepcopy(neighbour_schedule)
                current_cost = neighbour_cost

            self.current_temperature *= 1 - self.cooling_rate
            # break

        return current_schedule

    def generate_initial_schedule(self):
        return ScheduleMaker().generate_initial_schedule(self.groupnames, self.semesters)

    def to_json(self, filename):
        unformatted_schedule = self.ready_schedule.to_dict()
        formatted_schedule = {}
        for group in unformatted_schedule:
            formatted_schedule[group] = {}
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            for day in days:
                formatted_schedule[group][day] = {}
                for i in range(1, 8):
                    subj_name_teacher = unformatted_schedule[group][f"{day.lower()[:3]}{
                        i}"]
                    if subj_name_teacher == "":
                        formatted_schedule[group][day][i] = {"type": "", "name": "", "teacher": ""}
                    else:
                        subj_type = subj_name_teacher[0]
                        subj_name = subj_name_teacher[2:].split(", ")[0]
                        subj_teacher = subj_name_teacher[2:].split(", ")[1]
                        formatted_schedule[group][day][i]={"type":subj_type,"name":subj_name,"teacher":subj_teacher}
        import json
        json.dump(formatted_schedule, open(filename, "w"), indent=4)

# Example usage:
groupnames = ["FAF-223", "FAF-221", "FAF-222", "FAF-233"]
semesters = [3, 3, 3, 1]
schedule_simulated_annealing = ScheduleSimulatedAnnealing(
    groupnames, semesters)
optimal_schedule = schedule_simulated_annealing.anneal()
print(optimal_schedule)

