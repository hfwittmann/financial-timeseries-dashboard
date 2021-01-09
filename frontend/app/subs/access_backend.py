from subs.orderdict import orderByValue
import requests
import json
import streamlit as st
import pandas as pd

from environs import Env
env = Env()
env.read_env()

# @st.cache
def get_tickerlist():

    response = requests.get(f'http://{env("HOST")}:5000/api/tickerlist')
    response_json = response.json()

    companyTicker = pd.read_json(response_json)
    # companyTicker = orderByValue(companyTicker)

    # ticker = list(companyTicker.keys())
    return companyTicker

# @st.cache
def get_plot(selection:str, plottype:str):

    assert plottype in ['scatter', 'returns', 'histogram']
    _ = requests.get(
        f'http://{env("HOST")}:5000/api/plot/{selection}/{plottype}')

    fig = json.loads(_.json())

    return fig

if __name__ == "__main__":
    print(get_tickerlist())