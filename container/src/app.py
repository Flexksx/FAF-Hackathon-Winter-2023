from ScheduleAlgo import ScheduleSimulatedAnnealing
import pandas as pd
import numpy as np
from flask import Flask

app = Flask(__name__)

scheduler = ScheduleSimulatedAnnealing(
    ["FAF-223", "FAF-221", "FAF-222", "FAF-231", "FAF-232", "FAF-233", "CR-221", "CR-222", "CR-223", "AI-221","IBM-231"], [3, 3, 3, 1, 1, 1, 3, 3, 3, 3,1])


@app.route("/schedule")
def get_schedule():
    return scheduler.to_json()

