import pandas as pd


def relative_strength_index(
    data: pd.DataFrame,
    *,
    close_key: str = "closePrice",
    order_key: str = "startTime",
) -> float:
    """Function count relative_strength_index

    Args:
        data (pd.DataFrame): Data frame with chronological and close data.
        close_key (str, optional): Name of column with close prices.
            Defaults to "closePrice".
        order_key (str, optional): Name of column with time.
            This key is for sorting closing prices chronologically.
            Defaults to "startTime".

    Returns:
        float: RSI of the given data.
    """
    _delta = data.sort_values(order_key)[close_key].diff()
    delta = _delta[~_delta.isna()]
    up_days = delta.copy()
    up_days[delta <= 0] = 0.0
    down_days = delta.copy()
    down_days[delta >= 0] = 0.0
    RS_up = up_days.mean()
    RS_down = -down_days.mean()
    return 100 - 100 / (1 + RS_up / RS_down)
