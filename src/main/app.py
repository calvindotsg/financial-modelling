"""
This module fetches stock data for given ticker symbols and logs the data to a Firestore database. It uses helper
functions to read ticker symbols from a CSV file, update a Firestore database, and get stock data from a data
provider.
"""
import json

from config.app_config import DATA_PROVIDER, TICKER_SYMBOLS_LIST
from src.main.helpers.read_csv import read_ticker_symbols
from src.main.helpers.firestore_update import FirestoreDB, store_data
from src.main.data_models.stock_price_data import get_stock_data, StockData


def fetch_stock_data(symbols) -> list[StockData]:
    """
    Fetch stock data for given symbols.

    Parameters
    ----------
    symbols : list
        list of ticker symbols to fetch data for.

    Returns
    -------
    list
        list of stock data for each ticker symbol.
    """
    ticker_list: list[StockData] = []
    for ticker in symbols:
        data: StockData = get_stock_data(symbol=ticker, provider=DATA_PROVIDER, start_date="2024-01-01", interval="1d")
        # Append the data to the stock_ticker_list
        ticker_list.append(data)
    return ticker_list


def log_stock_data(ticker_list):
    """
    Log stock data for given ticker list.

    Parameters
    ----------
    ticker_list : list
        list of stock data to log.
    """
    # Log stock_ticker_list as a prettified JSON
    ticker_list_json = json.dumps(
        [data.dict() for data in ticker_list], indent=2
    )
    print(ticker_list_json)


if __name__ == "__main__":
    # Read the ticker symbols from the CSV file
    ticker_symbols: list = read_ticker_symbols(file_path=TICKER_SYMBOLS_LIST, ticker_column="Symbol")
    print(ticker_symbols)

    stock_ticker_list: list[StockData] = fetch_stock_data(symbols=ticker_symbols)
    log_stock_data(stock_ticker_list)

    # Create a firestore database object
    firestore_db = FirestoreDB()

    # Store the data
    store_data(stock_data_list=stock_ticker_list, firestore_db=firestore_db)
