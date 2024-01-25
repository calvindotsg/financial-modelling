# import all libraries from requirements.txt
import yfinance as yf
import polars as pl
import json

from pydantic import BaseModel
from typing import Optional, List
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


def create_custom_session() -> CachedLimiterSession:
    """
    This function creates a custom requests session with caching and rate limiting.

    Returns:
    CachedLimiterSession: A custom requests session.
    """
    session = CachedLimiterSession(
        limiter=Limiter(
            RequestRate(2, Duration.SECOND * 5)
        ),  # max 2 requests per 5 seconds
        bucket_class=MemoryQueueBucket,
        backend=SQLiteCache("yfinance.cache"),
    )
    return session

# Define a Pydantic model for the stock price data
class StockPriceData(BaseModel):
    date: str
    closing_price: float
    returns: Optional[float]
    holding_period_yield: Optional[float]
    holding_period_return: Optional[float]
    portfolio_of_1000: Optional[float]


# Define a Pydantic model for the stock data
class StockData(BaseModel):
    ticker: str
    stock_price_data: List[StockPriceData]


def fetch_stock_info(ticker: str, session: Session) -> yf.Ticker:
    return yf.Ticker(ticker, session=session)


def get_stock_price(stock_info: yf.Ticker, period: str) -> pl.DataFrame:
    return stock_info.history(period=period)


def clean_stock_price(stock_price: pl.DataFrame) -> pl.DataFrame:
    stock_price_clean = stock_price.loc[:, ["Close"]]
    stock_price_clean["closing_price"] = stock_price_clean["Close"]
    stock_price_clean["date"] = stock_price_clean.index.strftime("%Y-%m-%d %H:%M:%S%z")
    stock_price_clean["returns"] = stock_price_clean["Close"].pct_change()
    stock_price_clean["holding_period_yield"] = (
        stock_price_clean["Close"] / stock_price_clean["Close"].shift(1) - 1
    )
    stock_price_clean["holding_period_return"] = stock_price_clean[
        "Close"
    ] / stock_price_clean["Close"].shift(1)
    stock_price_clean["portfolio_of_1000"] = (
        1000 * stock_price_clean["holding_period_return"].cumprod()
    )
    stock_price_clean.index = stock_price_clean.index.strftime("%Y-%m-%d %H:%M:%S%z")
    return stock_price_clean


def get_stock_data(ticker: str, period: str) -> StockData:
    session = create_custom_session()
    stock_info = fetch_stock_info(ticker, session)
    stock_price = get_stock_price(stock_info, period)
    stock_price_clean = clean_stock_price(stock_price)
    stock_price_data = [
        StockPriceData(**data) for data in stock_price_clean.to_dict("records")
    ]
    return StockData(ticker=ticker, stock_price_data=stock_price_data)

def read_ticker_symbols(file_path, ticker_column):
    """
    This function reads the ticker symbols from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file.
    ticker_column (str): The header of the column containing the ticker symbols.

    Returns:
    list: A list of ticker symbols.
    """
    # Read the CSV file
    df = pl.scan_csv(file_path)

    # Materialize the LazyFrame to a DataFrame
    df = df.collect()

    # Extract the ticker symbols
    ticker_symbols = df[ticker_column].to_list()

    return ticker_symbols

if __name__ == "__main__":
    # Read the ticker symbols from the CSV file
    # path = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
    path = "data/test.csv"
    ticker_symbols = read_ticker_symbols(file_path=path, ticker_column="Symbol")
    print(ticker_symbols)

    stock_ticker_list = []

    for ticker in ticker_symbols:
        data = get_stock_data(ticker=ticker, period="1mo")
        # Append the data to the stock_ticker_list
        stock_ticker_list.append(data)

    # Log stock_ticker_list as a prettified JSON
    stock_ticker_list_json = json.dumps(
        [data.dict() for data in stock_ticker_list], indent=2
    )
    print(stock_ticker_list_json)
