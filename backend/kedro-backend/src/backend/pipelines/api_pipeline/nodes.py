import pandas as pd
import subprocess
from src.backend.pipelines.api_pipeline.utils.getPlots import getPlot


class Tickerlist_provider:
    def __init__(self):
        pass
        # self.model = model

    def predict(self, args_API: pd.DataFrame, context):
        df_args = args_API
        print(df_args)

        try:

            myData = pd.read_csv(f"data/01_raw/tickers.csv")
            myData = myData.to_json()
            # prediction = self.model.predict(df_args)

        except Exception as e:
            return {"status": "failure", "Exception": str(e)}

        return {"myData": myData}


def save_tickerlist_provider():
    provider = Tickerlist_provider()
    return provider


class Stockticker_provider:
    def __init__(self):
        pass
        # self.model = model

    def predict(self, args_API: pd.DataFrame, context):
        df_args = args_API
        print(df_args)

        try:
            # plottype selection
            # 0  Stockticker_providerplottype.scatter    BEI.DE

            selection = df_args.loc[0, "selection"]
            plottype = df_args.loc[0, "plottype"].split(".")[-1]

            myData = pd.read_json(
                f"data/01_raw/{selection}.json", orient="index"
            ).T.loc[0]
            assert myData["status"] == "success"

            tickers = pd.read_csv(f"data/01_raw/tickers.csv").set_index("Ticker")

            company_timeseries = pd.read_json(myData["dataframe"])
            performance_data = company_timeseries.set_index("Date")

            myplot = getPlot(
                plottype=plottype,
                performance_data=performance_data,
                status=myData["status"],
                ticker=tickers.at[selection, "Company"],
            )
        except Exception as e:
            self.save({"status": "failure", "plot": None})
            pass

            # prediction = self.model.predict(df_args)

        myplot = pd.Series(myplot)

        return myplot  # {"status": "blub"}


def save_stockticker_provider():
    provider = Stockticker_provider()
    return provider


class Cron_provider:
    def __init__(self):
        pass
        # self.model = model

    def predict(self, args_API: pd.DataFrame, context):
        df_args = args_API
        # print(df_args)

        try:

            result = subprocess.run(
                ["echo 9"], shell=True, capture_output=True, text=True
            )
            print(result.stdout)
            result = subprocess.run(
                ["kedro run --pipeline getPrepared"],
                shell=True,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
            return {"status": "success"}

        except Exception as e:
            return {"status": "failure", "Exception": str(e)}

        return {"status": "success", "myData": "Data of Dax constituents collected"}


def save_cron_provider():
    provider = Cron_provider()
    return provider


if __name__ == "__main__":
    # provider = Tickerlist_provider()

    # input = [{"datatype": "tickerlist"}]

    # args_API = pd.DataFrame.from_dict((input))
    # out = provider.predict(args_API, context="blub")
    # print(out)

    # ###################################################
    provider = Stockticker_provider()

    input = [
        {
            "plottype": "Stockticker_providerplottype.scatter",
            "selection": "BAS.DE",
        }
    ]
    args_API = pd.DataFrame.from_dict((input))
    out = provider.predict(args_API, context="blub")
    print(out)

    print("success")
    ####################################################
    # provider = Cron_provider()

    # input = [{"datatype": "cron"}]

    # args_API = pd.DataFrame.from_dict((input))
    # out = provider.predict(args_API, context="blub")
    # print(out)

    # print("success")
    ###################################################
