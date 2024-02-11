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
    Create a custom requests session with caching and rate limiting.

    Returns
    -------
    CachedLimiterSession
        A custom requests session configured with a rate limiter allowing a maximum
        of 2 requests per 5 seconds. The session uses an in-memory queue bucket
        (MemoryQueueBucket) for efficient request tracking and a SQLite cache
        (SQLiteCache) named "yfinance.cache" for response caching.

    Notes
    -----
    1. Rationale
        The function initializes a CachedLimiterSession with a rate limiter
        allowing controlled access to external resources, preventing abuse and
        ensuring a smooth flow of requests. The choice of MemoryQueueBucket
        enhances performance by using an in-memory queue for tracking requests.
        Additionally, the use of an SQLite cache named "yfinance.cache" enables
        response caching, reducing redundant requests and improving overall
        efficiency.

    2. Implementation Details
        - The rate limiter is configured with a maximum of 2 requests per 5 seconds.
        - The bucket class is set to MemoryQueueBucket for efficient request tracking.
        - The cache backend is configured with an SQLiteCache named "yfinance.cache".

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
    """
    Pydantic model for representing stock data.

    Notes
    -----
    1. Rationale
        This Pydantic model defines the structure for representing stock data,
        consisting of a stock ticker symbol and a list of associated stock price data.

    """
    ticker: str
    stock_price_data: List[StockPriceData]


def fetch_stock_info(ticker: str, session: Session) -> yf.Ticker:
    """
    Fetch stock information for the given ticker using a custom requests session.

    Parameters
    ----------
    ticker: str
        The stock ticker symbol.
    session: Session
        The custom requests session configured for fetching stock information.

    Returns
    -------
    yf.Ticker:
        The stock information.

    Notes
    -----
    1. Rationale
        This function utilizes the Yahoo Finance API (yf.Ticker) to fetch detailed
        information for the specified stock ticker using the provided custom requests session.
        The use of a custom session allows for enhanced control over requests and efficient
        handling of stock-related data.

    """
    return yf.Ticker(ticker, session=session)


def get_stock_price(stock_info: yf.Ticker, period: str) -> pl.DataFrame:
    """
    Get stock price data for the given stock information and period.

    Parameters
    ----------
    stock_info: yf.Ticker
        The stock information.
    period: str
        The period for which to retrieve the stock data (e.g., '1d', '1mo', '1y').

    Returns
    -------
    pl.DataFrame
        The stock price data.

    Notes
    -----
    1. Rationale
        This function retrieves historical stock price data for the specified stock information
        and period, utilizing the Yahoo Finance API. The returned data is structured as a pandas
        DataFrame for further analysis and visualization.

    """
    return stock_info.history(period=period)


def clean_stock_price(stock_price: pl.DataFrame) -> pl.DataFrame:
    """
    Clean the raw stock price data and enhance it with additional calculated metrics.

    Parameters
    ----------
    stock_price: pl.DataFrame
        The raw stock price data.

    Returns
    -------
    pl.DataFrame
        The cleaned stock price data with additional calculated metrics.

    Notes
    -----
    1. Rationale
        This function takes raw stock price data and performs data cleaning operations,
        including selecting relevant columns, calculating returns, and deriving additional
        metrics such as holding period yield, holding period return, and portfolio value based on
        a hypothetical initial investment of $1000.

    """
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
    """
    Get stock data for the given ticker and period.

    Parameters
    ----------
    ticker: str
        The stock ticker symbol.
    period: str
        The period for which to retrieve the stock data (e.g., '1d', '1mo', '1y').

    Returns
    -------
    StockData
        The stock data containing the specified stock ticker symbol and associated
        cleaned stock price data.

    Notes
    -----
    1. Rationale
        This function orchestrates the retrieval and processing of stock data for the
        specified stock ticker and period. It utilizes a custom requests session,
        fetches stock information, obtains historical stock price data, cleans the data,
        and structures it using the StockData Pydantic model.

    2. Implementation Details
        - A custom requests session is created using create_custom_session().
        - Stock information is fetched using fetch_stock_info().
        - Historical stock price data is obtained using get_stock_price().
        - The raw stock price data is cleaned and additional metrics are calculated using clean_stock_price().
        - The cleaned data is structured into a StockData Pydantic model.

    """
    session = create_custom_session()
    stock_info = fetch_stock_info(ticker, session)
    stock_price = get_stock_price(stock_info, period)
    stock_price_clean = clean_stock_price(stock_price)
    stock_price_data_dict = [
        StockPriceData(**data) for data in stock_price_clean.to_dict("records")
    ]
    return StockData(ticker=ticker, stock_price_data=stock_price_data_dict)


def read_ticker_symbols(file_path, ticker_column):
    """
    Read ticker symbols from a CSV file.

    Parameters
    ----------
    file_path: str
        The path to the CSV file.
    ticker_column: str
        The header of the column containing the ticker symbols.

    Returns
    -------
    list
        A list of ticker symbols extracted from the specified column in the CSV file.

    Notes
    -----
    1. Rationale
        This function reads ticker symbols from a CSV file, providing flexibility in
        specifying the file path and the column header containing the ticker symbols.
        The function uses polars to efficiently handle large CSV files and extract
        the desired information.

    2. Implementation Details
        - The CSV file is read into a LazyFrame using pl.scan_csv().
        - The LazyFrame is materialized into a DataFrame using df.collect().
        - Ticker symbols are extracted from the specified column and returned as a list.

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
    path = "../../data/test.csv"
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
