from typing import Literal, cast
from decouple import config

DATA_PROVIDER: Literal['fmp', 'intrinio', 'polygon', 'tiingo', 'yfinance'] \
    = cast(Literal['fmp', 'intrinio', 'polygon', 'tiingo', 'yfinance'], config('DATA_PROVIDER', default='yfinance'))
TICKER_SYMBOLS_LIST: str = str(config('TICKER_SYMBOLS_LIST', default="../../data/test.csv"))
FIRESTORE_SERVICE_ACCOUNT: str = str(config('FIRESTORE_SERVICE_ACCOUNT', default=None))
