import d6tflow
from d6tflow.tasks import TaskJson
from subs.getTickers import getTickers


class Task_getTickers(TaskJson):

    runDate = d6tflow.DateParameter()

    def run(self):
        tickers = getTickers()
        self.save(tickers)


if __name__ == "__main__":
    from datetime import date

    runDate = date.today()
    d6tflow.run(Task_getTickers(runDate=runDate))

    print(Task_getTickers(runDate).output().load())
