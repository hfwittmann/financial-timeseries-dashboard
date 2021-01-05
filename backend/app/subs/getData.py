import pandas as pd
import pandas_datareader.data as web

from environs import Env
env = Env()
env.read_env()



def getData(stockticker: str):


    try:
        mydata = web.DataReader(stockticker, 'yahoo')
        performance_data = mydata.loc['2007':].filter(items=['Open', 'Close'])
        performance_data.reset_index(inplace=True)

        return {'dataframe': performance_data.to_json(), 'status': 'success'}

    except Exception as e:
        print(e)

        return {'dataframe': None, 'status': 'failure'}
