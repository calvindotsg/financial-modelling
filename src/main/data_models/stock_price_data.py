import json
from enum import Enum
from typing import Optional, Literal

import pandas as pd
from openbb import obb
from pydantic import BaseModel

from config.app_config import DATA_PROVIDER


class ProviderEnum(Enum):
    """
    Enumeration of data providers.
    """
    FMP: str = 'fmp'
    INTRINIO: str = 'intrinio'
    POLYGON: str = 'polygon'
    TIINGO: str = 'tiingo'
    YFINANCE: str = 'yfinance'


# Define a Pydantic model for the stock price data
class StockPriceData(BaseModel):
    """
    Pydantic model for representing stock price data.
    """
    date: str
    closing_price: float
    returns: Optional[float]
    holding_period_yield: Optional[float]
    holding_period_return: Optional[float]
    portfolio_of_1000: Optional[float]

    def validation(self):
        """
        TODO: Validate the data types and formats.
        
        Raises
        ------
        ValueError
            If any validation fails.
        """
        pass

    def convert(self):
        """
        TODO:Convert the data types and formats as needed.

        This method is responsible for converting the data types and formats of the StockPriceData object as needed.
        For example, it can be used to convert the date string to a datetime object.
        """
        pass

    def to_dict(self):
        """
        Return a dictionary representation of the object.
        """
        return vars(self)


# Define a Pydantic model for the stock data
class StockData(BaseModel):
    """
    Pydantic model for representing stock data.

    Notes
    -----
    1. Rationale
        This Pydantic model defines the structure for representing stock data,
        consisting of a stock ticker symbol and a list of associated stock price data.

    """
    symbol: str
    stock_price_data: list[StockPriceData]


def get_stock_data(symbol: str, provider: Literal[
    ProviderEnum.FMP, ProviderEnum.INTRINIO, ProviderEnum.POLYGON, ProviderEnum.TIINGO, ProviderEnum.YFINANCE],
                   start_date: str, end_date: str, interval: str) -> StockData:
    """
    Retrieves and processes stock data for a given symbol, provider, start date, and interval.

    Parameters
    ----------
    symbol: str
        The stock ticker symbol, e.g. "AAPL" for Apple Inc.
    provider: Literal[ProviderEnum.FMP, ProviderEnum.INTRINIO, ProviderEnum.POLYGON, ProviderEnum.TIINGO,
    ProviderEnum.YFINANCE]
        The data provider.
    start_date: str
        The start date for the data retrieval in 'YYYY-MM-DD' format.
    end_date: str
        The end date for the data retrieval in 'YYYY-MM-DD' format.
    interval: str
        The interval for the stock data (e.g., '1d' = One day, '1W' = One week, '1M' = One month).

    Returns
    -------
    StockData
        A Pydantic model instance containing the stock ticker symbol and a list of cleaned stock price data.

    Notes
    -----
    1. Implementation Details
        - Retrieves historical stock price data from the specified provider for given symbol, start date, and interval.
        - The raw stock price data is cleaned and additional metrics are calculated.
        - The cleaned data is structured into a StockData Pydantic model.

    """
    stock_price: pd.DataFrame = obb.equity.price.historical(symbol=symbol, provider=provider, start_date=start_date,
                                                            end_date=end_date, interval=interval).to_df()
    stock_price_clean: pd.DataFrame = clean_stock_price(stock_price)
    stock_price_data_dict: list[StockPriceData] = [StockPriceData(**{str(k): v for k, v in data.items()}) for data in
                                                   stock_price_clean.to_dict("records")]
    stock_data: StockData = StockData(symbol=symbol, stock_price_data=stock_price_data_dict)
    return stock_data


def clean_stock_price(stock_price: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw stock price data and enhance it with additional calculated metrics.

    Parameters
    ----------
    stock_price: pd.DataFrame
        The raw stock price data.

    Returns
    -------
    pd.DataFrame
        The cleaned stock price data with additional calculated metrics.

    Notes
    -----
    1. Rationale
        This function takes raw stock price data and performs data cleaning operations,
        including selecting relevant columns, calculating returns, and deriving additional
        metrics such as holding period yield, holding period return, and portfolio value based on
        a hypothetical initial investment of $1000.

    """
    stock_price_clean: pd.DataFrame = stock_price.loc[:, ["close"]]
    stock_price_clean["closing_price"] = stock_price_clean["close"]
    stock_price_clean["date"] = pd.to_datetime(stock_price_clean.index).strftime("%Y-%m-%d %H:%M:%S%z")
    stock_price_clean["returns"] = stock_price_clean["close"].pct_change()
    stock_price_clean["holding_period_yield"] = (stock_price_clean["close"] / stock_price_clean["close"].shift(1) - 1)
    stock_price_clean["holding_period_return"] = stock_price_clean["close"] / stock_price_clean["close"].shift(1)
    stock_price_clean["portfolio_of_1000"] = (1000 * stock_price_clean["holding_period_return"].cumprod())
    stock_price_clean.index = pd.to_datetime(stock_price_clean.index).strftime("%Y-%m-%d %H:%M:%S%z")
    return stock_price_clean


def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> StockData:
    """
    Fetch stock data for given symbols.

    Parameters
    ----------
    symbol : str
        Ticker symbol to fetch stock data for.
    start_date: str
        The start date for the data retrieval in 'YYYY-MM-DD' format.
    end_date: str
        The end date for the data retrieval in 'YYYY-MM-DD' format.

    Returns
    -------
    StockData
        Stock data for each ticker symbol, as StockData object
    """
    data: StockData = get_stock_data(symbol=symbol, provider=DATA_PROVIDER, start_date=start_date, end_date=end_date,
                                     interval="1d")
    return data


def log_stock_data(stock_data) -> None:
    """
    Print to console stock data for given symbol list.

    Parameters
    ----------
    stock_data : StockData
        stock data to log.

    Returns
    -------
    None
    """
    # Log stock_ticker_list as a prettified JSON
    stock_data_json = json.dumps(stock_data.dict(), indent=2)
    print(stock_data_json)
