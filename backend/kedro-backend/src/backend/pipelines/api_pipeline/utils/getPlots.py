from plotly import graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import pandas as pd
import json


def __scatter_plot(performance_data: pd.DataFrame, ticker: str):

    # performance_data = performance_data.tail(10)

    trace_open = go.Scatter(
        x=performance_data.index,
        y=performance_data["Open"],
        mode="lines",
        marker={"colorscale": "Viridis"},
        name="Open",
    )

    trace_close = go.Scatter(
        x=performance_data.index,
        y=performance_data["Close"],
        mode="lines",
        marker={"colorscale": "Viridis"},
        name="Close",
    )

    data = [trace_open, trace_close]  # , trace_close]

    layout = {"title": f"{ticker} Performance", "yaxis": {"type": "log"}}

    fig_performance = dict(data=data, layout=layout)

    return fig_performance


def __returns_plot(performance_data, ticker):
    returns = performance_data.diff(axis=0) / performance_data

    trace_open = go.Scatter(
        x=returns.index,
        y=returns["Open"],
        mode="lines",
        marker={"colorscale": "Viridis"},
        name="Open",
    )

    trace_close = go.Scatter(
        x=returns.index,
        y=returns["Close"],
        mode="lines",
        marker={"colorscale": "Viridis"},
        name="Close",
    )

    data = [trace_open, trace_close]

    layout = {
        "title": f"{ticker} Returns"
        # 'yaxis':{'type': 'lin'}
    }

    fig_returns = dict(data=data, layout=layout)

    return fig_returns


def __histogram_plot(performance_data, ticker):
    returns = performance_data.diff(axis=0) / performance_data

    returns = performance_data.diff(axis=0) / performance_data

    trace_open = go.Histogram(
        x=returns["Open"], marker={"colorscale": "Viridis"}, name="Open"
    )

    trace_close = go.Histogram(
        x=returns["Open"], marker={"colorscale": "Viridis"}, name="Close"
    )

    data = [trace_open, trace_close]

    layout = {
        "title": f"{ticker} Histogram"
        # 'yaxis':{'type': 'lin'}
    }

    fig_histogram = dict(data=data, layout=layout)

    return fig_histogram


def getPlot(plottype, performance_data, status, ticker):

    plots = {
        "scatter": __scatter_plot,
        "returns": __returns_plot,
        "histogram": __histogram_plot,
    }

    fig = plots[plottype](performance_data, ticker)

    fig_serialised = json.dumps(fig, cls=PlotlyJSONEncoder)

    return {"status": status, "plot": fig_serialised}
