from subs.orderdict import orderByValue
import requests
import json
import streamlit as st

from environs import Env
env = Env()
env.read_env()

@st.cache
def get_tickerlist():

    response = requests.get(f'http://{env("HOST")}:5000/api/tickerlist')
    companyTicker = response.json()
    companyTicker = orderByValue(companyTicker)

    ticker = list(companyTicker.keys())
    return ticker, companyTicker

@st.cache
def get_plot(selection:str, plottype:str):

    assert plottype in ['scatter', 'returns', 'histogram']

    _ = requests.get(
        f'http://{env("HOST")}:5000/api/plot/{selection}/{plottype}')
    fig = json.loads(_.json())

    return fig