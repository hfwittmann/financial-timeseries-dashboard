"""
This is a boilerplate pipeline 'getTickers'
generated using Kedro 0.18.4
"""
import pandas as pd
import json

import os
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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Try without the class filter to get ALL tables
    tables = pd.read_html(url, storage_options={'User-Agent': headers['User-Agent']})

    # Look for the constituents table (should be the largest with company data)
    constituents = None
    ticker_col = None

    # Find table with "Company" column (that's usually the constituents table)
    for i, table in enumerate(tables):
        if 'Company' in table.columns:
            constituents = table
            # Now find the ticker column in this table
            for col in table.columns:
                if any(keyword in col.lower() for keyword in ['tick', 'symbol']):
                    ticker_col = col
                    break
            break

    if constituents is None or ticker_col is None:
        raise ValueError("No constituents table found")

    # Clean up the dataframe
    constituents = constituents.loc[:, ~constituents.columns.str.contains("^Unnamed")]
    constituents.ticker_column = ticker_col
    return constituents


def _get_one_stock(stockticker: str):
      log.info(f"Fetching data for: {stockticker}")

      try:
          # Try different ticker formats for German stocks
          ticker_variants = [
              stockticker,  # Original format (e.g., 'ADS.DE')
              stockticker.replace('.DE', '.F'),  # Frankfurt format (e.g., 'ADS.F')
          ]

          mydata = None
          successful_ticker = None

          for ticker in ticker_variants:
              try:
                  log.info(f"Trying ticker format: {ticker}")
                  mydata = yf.Ticker(ticker).history(period="max", auto_adjust=False)
                  if mydata.empty:
                      raise ValueError(f"No data returned from Yahoo for {ticker}")
                  # Yahoo returns a tz-aware index; strip it to match the old format
                  mydata.index = mydata.index.tz_localize(None)
                  mydata.index.name = "Date"
                  successful_ticker = ticker
                  log.info(f"Successfully fetched data with ticker: {ticker}")
                  break
              except Exception as e:
                  log.info(f"Failed with ticker {ticker}: {e}")
                  continue

          if mydata is None:
              raise Exception(f"All ticker formats failed for {stockticker}")

          # Sort the index to make it monotonic
          mydata = mydata.sort_index()

          # Filter data from 2007 onwards more safely
          try:
              # Try the original approach first
              performance_data = mydata.loc["2007":].filter(items=["Open", "Close"])
          except:
              # Fallback: filter by datetime comparison
              start_date = pd.Timestamp('2007-01-01')
              performance_data = mydata[mydata.index >= start_date].filter(items=["Open", "Close"])

          # If still no data, just take all available data
          if performance_data.empty:
              performance_data = mydata.filter(items=["Open", "Close"])

          performance_data.reset_index(inplace=True)

          out = {
              "stockticker": successful_ticker,
              "original_ticker": stockticker,
              "status": "success",
              "dataframe": performance_data.to_json(),
              "rows": len(performance_data)
          }

      except Exception as e:
          log.error(f"Error fetching data for {stockticker}: {e}")
          out = {"stockticker": stockticker, "status": "failure", "dataframe": None, "error": str(e)}

      return out


def get_Data_AllTickers(constituents):
    try:
        # Use the stored ticker column name dynamically
        ticker_col = getattr(constituents, 'ticker_column', 'Ticker')

        for ticker_symbol in constituents[ticker_col]:
            ticker_data = _get_one_stock(ticker_symbol)

            # Clean the ticker symbol for filename (remove dots and special chars)
            clean_ticker = ticker_symbol.replace('.', '_').replace('/', '_')
            filepath = f"data/01_raw/{clean_ticker}.json"

            # Don't overwrite previously fetched data with a failed fetch
            if ticker_data["status"] != "success" and os.path.exists(filepath):
                with open(filepath) as f:
                    if json.load(f).get("status") == "success":
                        log.warning(f"Keeping existing data for {ticker_symbol}")
                        continue

            with open(filepath, "w") as f:
                json.dump(ticker_data, f)

        out = {"status": "success"}

    except Exception as e:
        out = {"status": "failure", "Exception": str(e)}

    return out

if __name__ == "__main__":
    constituents = getTickers()
    # Use the stored ticker column name
    blub = _get_one_stock(constituents[constituents.ticker_column].iloc[0])
    print(blub)
    print("success")