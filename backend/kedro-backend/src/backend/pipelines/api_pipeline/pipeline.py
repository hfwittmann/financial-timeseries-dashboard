from kedro.pipeline import Pipeline, node

from .nodes import (
    save_tickerlist_provider,
    save_stockticker_provider,
    save_cron_provider,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=save_tickerlist_provider,
                name="save_tickerlist_provider",
                inputs=None,
                outputs="Tickerlist_provider",
            ),
            node(
                func=save_stockticker_provider,
                name="save_stockticker_provider",
                inputs=None,
                outputs="Stockticker_provider",
            ),
            node(
                func=save_cron_provider,
                name="save_cron_provider",
                inputs=None,
                outputs="Cron_provider",
            ),
        ]
    )
