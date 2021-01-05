from tier1.tickerlist import read as read_tickerlist
from tier1.selection_plot import read as read_selection_plot



def get_todays_data():

    try:
        tickerlist = read_tickerlist()
        for ticker, companyTicker in tickerlist.items():
            for plottype in ['scatter', 'returns', 'histogram']:
                read_selection_plot(ticker, plottype)

        return 'get_todays_data succeeded'

    except Exception as e:

        return f'get_todays_data failed at ticker {ticker} of company {companyTicker} with exception {str(e)}'


if __name__ == "__main__":
    get_todays_data()
