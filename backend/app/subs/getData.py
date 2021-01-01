import pandas as pd
import quandl

from environs import Env
env = Env()
env.read_env()

api = env('quandl_api_key')
quandl.ApiConfig.api_key = api


def getData(stockticker: str):
    stockticker = stockticker.replace('.DE', '').replace(env('CHARACTER'), '/')

    try:
        mydata = quandl.get(stockticker)
        performance_data = mydata.loc['2007':].filter(items=['Open', 'Close'])
        performance_data.reset_index(inplace=True)

        return {'dataframe': performance_data.to_json(), 'status': 'success'}

    except Exception as e:
        print(e)

        return {'dataframe': None, 'status': 'failure'}
