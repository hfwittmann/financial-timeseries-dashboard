import d6tflow
from d6tflow.tasks import TaskCSVGZPandas, TaskCSVPandas, TaskJson
import pandas as pd

from subs.getData import getData
from tasks.task_getTickers import Task_getTickers

from environs import Env
env = Env()
env.read_env()


@d6tflow.requires(Task_getTickers)
class Task_getData(TaskJson):

    runDate = d6tflow.DateParameter()
    stockticker = d6tflow.Parameter()

    def run(self):

        tickers = self.input().load()
        #assert self.stockticker in tickers.keys(), 'Symbol should be in ticker list'

        out = getData(stockticker=self.stockticker)
        self.save(out)


if __name__ == "__main__":
    from datetime import date

    runDate = date.today()
    d6tflow.run(Task_getData(runDate=runDate, stockticker='FSE?ADS.DE_X'))

    print(
        Task_getData(runDate=runDate,
                     stockticker='FSE?ADS.DE_X').output().load())

    # produce failure:
    d6tflow.run(Task_getData(runDate=runDate, stockticker='Blubber'))

    print(Task_getData(runDate=runDate, stockticker='Blubber').output().load())
