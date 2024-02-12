from helpers.read_csv import read_ticker_symbols
from config.app_config import DATA_PROVIDER, TICKER_SYMBOLS_LIST
from data_models.stock_price_data import get_stock_data

import json

if __name__ == "__main__":
    # Read the ticker symbols from the CSV file
    # path = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
    ticker_symbols = read_ticker_symbols(file_path=TICKER_SYMBOLS_LIST, ticker_column="Symbol")
    print(ticker_symbols)

    stock_ticker_list = []

    for ticker in ticker_symbols:
        data = get_stock_data(symbol=ticker, provider=DATA_PROVIDER, start_date="2024-01-01", interval="1d")
        # Append the data to the stock_ticker_list
        stock_ticker_list.append(data)

    # Log stock_ticker_list as a prettified JSON
    stock_ticker_list_json = json.dumps(
        [data.dict() for data in stock_ticker_list], indent=2
    )
    print(stock_ticker_list_json)
