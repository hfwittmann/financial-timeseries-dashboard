from datetime import date
import json
import plotly
from re import sub
from plotly import graph_objects as go

import streamlit as st
st.set_page_config(layout='wide')

from subs.access_backend import get_tickerlist
from subs.access_backend import get_plot

ticker, companyTicker = get_tickerlist()
# part = st.selectbox(label='Part', options=[1, 2, 3])

# default = {
#     '1': ticker[0:10],
#     '2': ticker[10:20],
#     '3': ticker[20:30]
# }[str(part)]

default = [ticker[i] for i in [2, 3, 6, 12]]

selections = st.multiselect(label='Dax Constituents',
                            options=ticker,
                            format_func=lambda x: companyTicker[x],
                            default=default)

for selection in selections:

    try:

        fig_scatter = get_plot(selection, 'scatter')
        fig_returns = get_plot(selection, 'returns')
        fig_histogram = get_plot(selection, 'histogram')


        st.header(companyTicker[selection])
        c1, _, c2, _, c3 = st.beta_columns((10, 1, 10, 1, 10))

        # widgets = {
        #     'success':'plotly_chart',
        #     'failure':'text'
        # }

        
        # getattr(c1, widgets[fig_scatter['status']])(fig_scatter['plot'], use_container_width=True)
        # getattr(c2, widgets[fig_returns['status']])(fig_scatter['plot'], use_container_width=True)
        # getattr(c3, widgets[fig_histogram['status']])(fig_scatter['plot'], use_container_width=True)

        c1.plotly_chart(fig_scatter['plot'], use_container_width=True)
        c2.plotly_chart(fig_returns['plot'], use_container_width=True)
        c3.plotly_chart(fig_histogram['plot'], use_container_width=True)

    except Exception as e:
        st.header(companyTicker[selection])
        st.markdown(f'Data for {companyTicker[selection]} not available', unsafe_allow_html=False)
        print(selection)
        print(e)
