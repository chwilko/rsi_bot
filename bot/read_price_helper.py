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
        "M",
    ]
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
        self, *, symbol: str = "SOLUSDT", interval: str = "D", category: str = "spot"
    ) -> None:
        assert interval in self.INTERVALS
        self.interval = interval
        self.symbol = symbol
        self.category = category
        self.session = HTTP(testnet=False)

    def read_interval(self, start: int, end: int) -> pd.DataFrame:
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
