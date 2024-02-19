from typing import Literal, cast

from decouple import config

from src.main.data_models.stock_price_data import ProviderEnum

DATA_PROVIDER: Literal[
    ProviderEnum.FMP, ProviderEnum.INTRINIO, ProviderEnum.POLYGON, ProviderEnum.TIINGO, ProviderEnum.YFINANCE] = cast(
    Literal[ProviderEnum.FMP, ProviderEnum.INTRINIO, ProviderEnum.POLYGON, ProviderEnum.TIINGO, ProviderEnum.YFINANCE],
    config('DATA_PROVIDER', default='yfinance'))
TICKER_SYMBOLS_LIST: str = str(config('TICKER_SYMBOLS_LIST', default="../../data/test.csv"))
FIRESTORE_SERVICE_ACCOUNT: str = str(config('FIRESTORE_SERVICE_ACCOUNT', default=None))
