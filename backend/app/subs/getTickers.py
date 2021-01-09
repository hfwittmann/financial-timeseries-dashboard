import pandas as pd


def getTickers():
    # Start : Global configuration
    # Get Table
    url = "https://en.wikipedia.org/wiki/DAX"
    tables = pd.read_html(url)

    for constituents in tables:
        if 'Ticker symbol' in constituents.columns: break

    constituents = constituents.loc[:, ~constituents.columns.str.contains('^Unnamed')]

    return constituents


if __name__ == "__main__":
    print(getTickers())