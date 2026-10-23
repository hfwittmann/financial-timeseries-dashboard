"""
This is a boilerplate pipeline 'getTickers'
generated using Kedro 0.18.4
"""
import pandas as pd
import json

import pandas_datareader.data as web
from pandas_datareader import data as pdr
import yfinance as yf

from environs import Env
import logging

log = logging.getLogger(__name__)

env = Env()
env.read_env()


def getTickers():
    # Start : Global configuration
    # Get Table
    url = "https://en.wikipedia.org/wiki/DAX"
    tables = pd.read_html(url)

    for constituents in tables:
        if "Ticker" in constituents.columns:
            break

    constituents = constituents.loc[:, ~constituents.columns.str.contains("^Unnamed")]

    return constituents


def _get_one_stock(stockticker: str):

    log.info(stockticker)

    try:
        yf.pdr_override()
        mydata = pdr.get_data_yahoo(stockticker)
        # mydata = web.DataReader(stockticker, 'yahoo')

        performance_data = mydata.loc["2007":].filter(items=["Open", "Close"])
        performance_data.reset_index(inplace=True)

        out = {
            "stockticker": stockticker,
            "status": "success",
            "dataframe": performance_data.to_json(),
        }

    except Exception as e:

        out = {"stockticker": stockticker, "status": "failure", "dataframe": None}

    return out


def get_Data_AllTickers(constituents):

    try:
        for ticker_symbol in constituents["Ticker"]:

            ticker_data = _get_one_stock(ticker_symbol)

            filepath = f"data/01_raw/{ticker_symbol}.json"
            with open(filepath, "w") as f:
                json.dump(ticker_data, f)

        out = {"status": "success"}

    except Exception as e:
        out = {"status": "failure", "Exception": str(e)}

    return out
