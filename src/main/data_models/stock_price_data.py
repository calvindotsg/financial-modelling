from pydantic import BaseModel
from typing import Optional
from openbb import obb

import pandas as pd


# Define a Pydantic model for the stock price data
class StockPriceData(BaseModel):
    date: str
    closing_price: float
    returns: Optional[float]
    holding_period_yield: Optional[float]
    holding_period_return: Optional[float]
    portfolio_of_1000: Optional[float]

    def validation(self):
        # TODO: Validate the data types and formats
        # Raise an exception if any validation fails
        # For example, check if the date is a valid ISO 8601 string
        pass

    def convert(self):
        # TODO: Convert the data types and formats as needed
        # For example, convert the date string to a datetime object
        pass

    def to_dict(self):
        # Return a dictionary representation of the object
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
    ticker: str
    stock_price_data: list[StockPriceData]


def get_stock_data(symbol: str, provider: str, start_date: str, interval: str) -> StockData:
    """
    Retrieves and processes stock data for a given symbol, provider, start date, and interval.

    Parameters
    ----------
    symbol: str
        The stock ticker symbol.
    provider: str
        The data provider.
    start_date: str
        The start date for the data retrieval in 'YYYY-MM-DD' format.
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
    stock_price = obb.equity.price.historical(symbol=symbol, provider=provider, start_date=start_date,
                                              interval=interval).to_df()
    stock_price_clean = clean_stock_price(stock_price)
    stock_price_data_dict = [
        StockPriceData(**{str(k): v for k, v in data.items()}) for data in stock_price_clean.to_dict("records")
    ]
    return StockData(ticker=symbol, stock_price_data=stock_price_data_dict)


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
    stock_price_clean = stock_price.loc[:, ["close"]]
    stock_price_clean["closing_price"] = stock_price_clean["close"]
    stock_price_clean["date"] = pd.to_datetime(stock_price_clean.index).strftime("%Y-%m-%d %H:%M:%S%z")
    stock_price_clean["returns"] = stock_price_clean["close"].pct_change()
    stock_price_clean["holding_period_yield"] = (
            stock_price_clean["close"] / stock_price_clean["close"].shift(1) - 1
    )
    stock_price_clean["holding_period_return"] = stock_price_clean[
                                                     "close"
                                                 ] / stock_price_clean["close"].shift(1)
    stock_price_clean["portfolio_of_1000"] = (
            1000 * stock_price_clean["holding_period_return"].cumprod()
    )
    stock_price_clean.index = pd.to_datetime(stock_price_clean.index).strftime("%Y-%m-%d %H:%M:%S%z")
    return stock_price_clean
