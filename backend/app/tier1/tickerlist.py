'''
Handler for tickerlist
'''
import d6tflow

import d6tflow
from datetime import date
from tasks.task_getTickers import Task_getTickers


def get_runDate():
    return date.today()


def read():
    runDate = get_runDate()
    d6tflow.run(Task_getTickers(runDate=runDate))
    out = Task_getTickers(runDate=runDate).output().load()

    return out
