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
        self.cooling_rate = 0.001
        self.current_temperature = self.initial_temperature
        self.groupsdict = self.__sl.get_groups_dfs(groupnames, semesters)
        self.ready_schedule = self.anneal()

    def evaluate_schedule(self, schedule):
        return schedule.apply(lambda x: x.str.startswith(('c', 's', 'l', 'p')).sum(), axis=0).sum()


    # def generate_neighbour(self, current_schedule):
    #     neighbour_schedule = copy.deepcopy(current_schedule)

    #     for group in self.groupnames:
    #         # Filter empty and non-empty slots only for the current group
    #         empty_slots = neighbour_schedule.loc[neighbour_schedule[group] == ''].index.tolist(
    #         )
    #         non_empty_slots = neighbour_schedule.loc[neighbour_schedule[group] != ''].index.tolist(
    #         )

    #         # Randomly choose an empty and a non-empty slot for the current group
    #         random_empty_slot = random.choice(empty_slots)
    #         random_non_empty_slot = random.choice(non_empty_slots)

    #         # Swap the values between the empty and non-empty slots for the current group
    #         neighbour_schedule.at[random_empty_slot,
    #                               group] = neighbour_schedule.at[random_non_empty_slot, group]
    #         neighbour_schedule.at[random_non_empty_slot, group] = ''

    #     return neighbour_schedule

    def generate_neighbour(self, current_schedule):
        # Your neighbourhood generation logic goes here
        # Generate a neighbouring solution for the current schedule
        # This could involve swapping or modifying lessons
        neighbour_schedule = copy.deepcopy(current_schedule)
        # For simplicity, swap two random lessons in a random day
        day = random.choice(neighbour_schedule.columns)
        lesson_indices = random.sample(range(len(neighbour_schedule)), 2)
        neighbour_schedule.iloc[lesson_indices, neighbour_schedule.columns.get_loc(day)] = \
            current_schedule.iloc[lesson_indices[::-1], current_schedule.columns.get_loc(day)].values
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
        return json.dumps(formatted_schedule)

# Example usage:
groupnames = ["FAF-223", "FAF-221", "FAF-222", "FAF-233"]
semesters = [3, 3, 3, 1]
schedule_simulated_annealing = ScheduleSimulatedAnnealing(
    groupnames, semesters)
optimal_schedule = schedule_simulated_annealing.anneal()
print(optimal_schedule)
