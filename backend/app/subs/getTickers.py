import pandas as pd
from environs import Env
env = Env()
env.read_env()


def getTickers():
    # Start : Global configuration
    # Get Table
    url = "https://en.wikipedia.org/wiki/DAX"
    tables = pd.read_html(url)

    for constituents in tables:
        if 'Ticker symbol' in constituents.columns: break

    constituents = constituents.reset_index(drop=True)

    constituents['Yahoo Ticker symbol'] = constituents['Ticker symbol']

    companyTicker = {stockinfo['Yahoo Ticker symbol'] : stockinfo['Company'] \
            for i, stockinfo in constituents.iterrows() \
            if isinstance(stockinfo['Yahoo Ticker symbol'], str) }

    return companyTicker