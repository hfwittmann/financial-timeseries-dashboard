import d6tflow
from d6tflow.tasks import TaskJson, TaskPickle
import pandas as pd

from tasks.task_getTickers import Task_getTickers
from tasks.task_getData import Task_getData
from subs.getPlots import getPlot


@d6tflow.requires(Task_getTickers, Task_getData)
class Task_getPlot(TaskPickle):

    runDate = d6tflow.DateParameter()
    plottype = d6tflow.Parameter()

    def run(self):

        tickers, Data = self.input()
        tickers, Data = tickers.load().set_index('Ticker symbol'), Data.load()

        status = Data['status']

        if status == 'failure':
            self.save({'status': status, 'plot': None})
            return None

        company_timeseries = pd.read_json(
            Data['dataframe'])

        performance_data = company_timeseries.set_index('Date')
        # status, company_timeseries = Data['status'], Data['company_timeseries']

        # performance_data = pd.read_sql(
        #     company_timeseries.statement,
        #     company_timeseries.session.bind).set_index('Date')

        # performance_data = self.input().load().set_index('Date')

        myplot = getPlot(
            plottype=self.plottype,
            performance_data=performance_data,
            status=status,
            ticker=tickers.at[self.stockticker, 'Company'],
        )
        self.save(myplot)


if __name__ == "__main__":
    from datetime import date

    runDate = date.today()
    d6tflow.run(
        Task_getPlot(runDate=runDate,
                     stockticker='FSE?ADS.DE_X',
                     plottype='histogram'))

    print(
        Task_getPlot(runDate=runDate,
                     stockticker='FSE?ADS.DE_X',
                     plottype='histogram'))

    # d6tflow.run(
    #     Task_getPlot(runDate=runDate,
    #                  stockticker='FSE?DHER.DE_X',
    #                  plottype='histogram'))

    # print(
    #     Task_getPlot(runDate=runDate,
    #                  stockticker='FSE?DHER.DE_X',
    #                  plottype='histogram'))
