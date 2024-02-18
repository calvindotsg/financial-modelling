from config.app_config import TICKER_SYMBOLS_LIST
from src.main.helpers.read_csv import read_ticker_symbols
from src.main.helpers.firestore_update import FirestoreDB, process_stock_data


if __name__ == "__main__":
    # Read the ticker symbols from the CSV file
    ticker_symbols: list[str] = list(read_ticker_symbols(file_path=TICKER_SYMBOLS_LIST,
                                                         ticker_column="Symbol"))
    print(ticker_symbols)

    # Create a firestore database object
    firestore_db = FirestoreDB()

    # Loop through each ticker symbol
    for ticker in ticker_symbols:
        # Process the stock data for the ticker
        process_stock_data(ticker=ticker, firestore_db=firestore_db)
