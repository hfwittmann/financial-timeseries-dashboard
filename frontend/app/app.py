from datetime import date
import json
import plotly
from re import sub
from plotly import graph_objects as go

import streamlit as st

st.set_page_config(layout="wide")

from subs.access_backend import get_tickerlist
from subs.access_backend import get_plot

tickerTable = get_tickerlist().set_index("Ticker")

PrimeStandardSector = "Prime Standard Sector"
sectors = tickerTable[PrimeStandardSector].unique()
sectors.sort()
sector = st.selectbox(
    label="Select a Sector. Remark: This sets the default for the selected stocks",
    options=sectors,
)

default_index = tickerTable[PrimeStandardSector] == sector

default = tickerTable[default_index]

selections = st.multiselect(
    label="Dax Constituents",
    options=list(tickerTable.index),
    format_func=lambda x: tickerTable.at[x, "Company"],
    default=list(default.index),
)

for selection in selections:

    try:

        fig_scatter = get_plot(selection, "scatter")
        fig_returns = get_plot(selection, "returns")
        fig_histogram = get_plot(selection, "histogram")

        st.header(tickerTable.at[selection, "Company"])
        c1, _, c2, _, c3 = st.columns((10, 1, 10, 1, 10))

        c1.plotly_chart(fig_scatter, use_container_width=True)
        c2.plotly_chart(fig_returns, use_container_width=True)
        c3.plotly_chart(fig_histogram, use_container_width=True)

    except Exception as e:
        st.header(tickerTable.at[selection, "Company"])
        st.markdown(
            f"Data for {tickerTable.at[selection, 'Company']} not available",
            unsafe_allow_html=False,
        )
        # print(selection)
        # print(e)

if __name__ == "__main__":
    print(tickerTable)
    print(tickerTable.index[:3])

    print(sectors)
    print(tickerTable["Prime Standard Sector"] == sector)
    print(default)
