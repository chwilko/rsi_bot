from bot.bybit_kline_data_fetcher import BybitKlineDataFetcher
import pytest

@pytest.mark.parametrize("interval", ("2", "M", "2D"))
def test_catch_bad_interval(interval: str):
    with pytest.raises(AttributeError):
        BybitKlineDataFetcher(interval=interval)

