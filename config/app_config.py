from typing import Literal, cast

from decouple import config

from src.main.data_models.stock_price_data import ProviderEnum

DATA_PROVIDER: Literal[ProviderEnum.FMP: ProviderEnum, ProviderEnum.INTRINIO: ProviderEnum,
                       ProviderEnum.POLYGON: ProviderEnum, ProviderEnum.TIINGO: ProviderEnum,
                       ProviderEnum.YFINANCE: ProviderEnum] = cast(
    Literal[ProviderEnum.FMP: ProviderEnum, ProviderEnum.INTRINIO: ProviderEnum, ProviderEnum.POLYGON: ProviderEnum,
            ProviderEnum.TIINGO: ProviderEnum, ProviderEnum.YFINANCE: ProviderEnum],
    config('DATA_PROVIDER', default='yfinance'))
TICKER_SYMBOLS_LIST: str = str(config('TICKER_SYMBOLS_LIST', default="../../data/test.csv"))
FIRESTORE_SERVICE_ACCOUNT: str = str(config('FIRESTORE_SERVICE_ACCOUNT', default=None))
