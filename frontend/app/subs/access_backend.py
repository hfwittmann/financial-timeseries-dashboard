# from subs.orderdict import orderByValue
import requests
import json
import streamlit as st
import pandas as pd

from environs import Env

env = Env()
env.read_env()

# @st.cache
def get_tickerlist():

    response = requests.get(
        f"http://{env('HOST')}/Tickerlist_provider?datatype=tickerlist"
    )

    response_json = response.json()

    companyTicker = pd.read_json(response_json["myData"])

    return companyTicker


# @st.cache
def get_plot(selection: str, plottype: str):

    assert plottype in ["scatter", "returns", "histogram"]

    response = requests.get(
        f"http://{env('HOST')}/Stockticker_provider?plottype={plottype}&selection={selection}"
    )

    blub = response.json()

    fig = json.loads(blub["plot"])

    return fig


if __name__ == "__main__":
    print(get_tickerlist())

    print(get_plot("ADS.DE", "scatter"))
