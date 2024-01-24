# import all libraries from requirements.txt
import yfinance as yf
import pandas as pd
import json

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
        limiter=Limiter(RequestRate(2, Duration.SECOND * 5)),  # max 2 requests per 5 seconds
        bucket_class=MemoryQueueBucket,
        backend=SQLiteCache("yfinance.cache"),
    )
    return session


def get_stock_data(ticker, period):
    """
    This function retrieves stock data for the given tickers and period.
    
    Parameters:
    tickers (str): The stock tickers.
    period (str): The period for which to retrieve the stock data.
    
    Returns:
    stock_price_dict (dict): Dictionary containing the stock data.
    """

    # Get the custom requests session
    session = create_custom_session()

    # Get the stock data
    stock_info = yf.Ticker(ticker, session=session)
    stock_price = stock_info.history(period=period)

    # Clean the data
    stock_price_clean = stock_price.loc[:, ["Close"]]
    stock_price_clean["closing_price"] = stock_price_clean["Close"]
    stock_price_clean["date"] = stock_price_clean.index.strftime("%Y-%m-%d %H:%M:%S%z")
    stock_price_clean["returns"] = stock_price_clean["Close"].pct_change()
    stock_price_clean["holding_period_yield"] = stock_price_clean["Close"] / stock_price_clean["Close"].shift(1) - 1
    stock_price_clean["holding_period_return"] = stock_price_clean["Close"] / stock_price_clean["Close"].shift(1)
    stock_price_clean["portfolio_of_1000"] = 1000 * stock_price_clean['holding_period_return'].cumprod()

    # Convert the index to string
    stock_price_clean.index = stock_price_clean.index.strftime("%Y-%m-%d %H:%M:%S%z")

    # Convert the DataFrame to a dictionary
    stock_price_dict = stock_price_clean.to_dict('records')

    # Return the dictionary in the specified format
    return {
        "ticker": ticker,
        "stock_price_data": stock_price_dict
    }


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
    df = pd.read_csv(file_path)

    # Extract the ticker symbols
    ticker_symbols = df[ticker_column].tolist()

    return ticker_symbols


if __name__ == '__main__':
    # Read the ticker symbols from the CSV file
    # path = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
    path = 'data/test.csv'
    ticker_symbols = read_ticker_symbols(file_path=path, ticker_column='Symbol')
    print(ticker_symbols)

    stock_ticker_list = []

    for ticker in ticker_symbols:
        data = get_stock_data(ticker=ticker, period='1mo')
        # Append the data to the stock_ticker_list
        stock_ticker_list.append(data)

    json_formatted_str = json.dumps(stock_ticker_list, indent=2)  # Dump stock_ticker_list, not data
    print(json_formatted_str)
