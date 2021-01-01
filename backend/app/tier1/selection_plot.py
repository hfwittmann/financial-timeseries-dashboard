'''
Handler for ticker_plot
'''
import json
import plotly

import d6tflow
from datetime import date
from tasks.task_getTickers import Task_getTickers
from tasks.task_plot import Task_getPlot


def get_runDate():
    return date.today()


def read(selection, plottype):
    # selection = 'Daimler'
    runDate = get_runDate()
    d6tflow.run(Task_getTickers(runDate=runDate))
    companyTicker = Task_getTickers(runDate=runDate).output().load()

    ticker = selection  # companyTicker[selection]
    plot_dict = dict(runDate=runDate, stockticker=ticker, plottype=plottype)

    d6tflow.run(Task_getPlot(**plot_dict))

    fig: dict = Task_getPlot(**plot_dict).output().load()

    fig_serialied = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return fig_serialied
