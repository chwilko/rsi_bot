import pandas as pd


def relative_strength_index(
    data: pd.DataFrame, window: int = 15, *, close_key: str = "Close"
) -> float:
    _delta = data[close_key].diff()
    delta = _delta[~_delta.isna()]
    up_days = delta.copy()
    up_days[delta <= 0] = 0.0
    down_days = delta.copy()
    down_days[delta >= 0] = 0.0
    RS_up = up_days.mean()
    RS_down = -down_days.mean()
    return 100 - 100 / (1 + RS_up / RS_down)
