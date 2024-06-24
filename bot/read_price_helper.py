import pandas as pd
from pybit.unified_trading import HTTP


class ReadPriceHelper:
    INTERVALS = [
        "1",
        "3",
        "5",
        "15",
        "30",
        "60",
        "120",
        "240",
        "360",
        "720",
        "D",
        "W",
    ]
    INTERVALS_IN_MILLISECONDS = {
        "1": 60000,
        "3": 180000,
        "5": 300000,
        "15": 900000,
        "30": 1800000,
        "60": 3600000,
        "120": 7200000,
        "240": 14400000,
        "360": 21600000,
        "720": 43200000,
        "D": 86400000,
        "W": 604800000,
    }
    COLUMNS = [
        "startTime",
        "openPrice",
        "highPrice",
        "lowPrice",
        "closePrice",
        "volume",
        "turnover",
    ]

    COLUMNS_TYPES = [
        int,
        float,
        float,
        float,
        float,
        float,
        float,
    ]

    def __init__(
        self,
        *,
        symbol: str = "SOLUSDT",
        interval: str = "D",
        category: str = "spot",
    ) -> None:
        assert interval in self.INTERVALS
        self.interval = interval
        self.symbol = symbol
        self.category = category
        self.session = HTTP(testnet=False)

    def get_intervals_by_periods(self, now: int, periods: int) -> pd.DataFrame:
        start = now - periods * self.INTERVALS_IN_MILLISECONDS[self.interval]
        return self.get_intervals_by_range(start, now)

    def get_intervals_by_range(self, start: int, end: int) -> pd.DataFrame:
        """Method use API to get data from bybit market.
        Method get kline data.

        Args:
            start (int): start of the time range in milliseconds.
            end (int): end of the time range in milliseconds.

        Returns:
            pd.DataFrame: kline data.
        """
        response = self.session.get_kline(
            category=self.category,
            symbol=self.symbol,
            interval=self.interval,
            start=start,
            end=end,
        )
        data = map(
            lambda x: [new_type(val) for val, new_type in zip(x, self.COLUMNS_TYPES)],
            response["result"]["list"],
        )
        return pd.DataFrame(data, columns=self.COLUMNS)
