"""
This is a boilerplate pipeline 'getTickers'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import getTickers, get_Data_AllTickers


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(getTickers, inputs=None, outputs="tickers", name="getTickers"),
            node(
                get_Data_AllTickers,
                inputs="tickers",
                outputs="data_message",
                name="get_Data_AllTickers",
            ),
        ]
    )
