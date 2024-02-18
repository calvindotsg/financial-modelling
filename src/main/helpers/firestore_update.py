import datetime

from src.main.helpers.firestore_init import FirestoreDB
from src.main.data_models.stock_price_data import StockData, StockPriceData, fetch_stock_data, log_stock_data


def store_data(stock_data: StockData, firestore_db: FirestoreDB) -> None:
    """
    Store the stock price data in the firestore database.

    Parameters
    ----------
    stock_data: StockData
        Object containing the ticker and the stock price data.
    firestore_db: FirestoreDB
        A FirestoreDB object representing the firestore database.

    Returns
    -------
    None

    Notes
    -----
    1. Rationale
        This function stores the stock price data in the firestore database, creating
        or updating the documents in the collections corresponding to the tickers.

    2. Implementation Details
        - The function iterates over the stock data list and gets the ticker and the
          stock price data for each StockData object.
        - The function checks if the ticker collection exists in the firestore database
          and creates a new collection if not.
        - The function iterates over the stock price data and gets the date for each
          stock price object.
        - The function uses the document path to get the date document in the ticker
          collection and tries to get the document snapshot.
        - The function checks if the document exists and updates the existing document
          or creates a new document with the stock price data.
    """
    # Get the ticker and the stock price data
    ticker: str = stock_data.ticker
    stock_price_data: list[StockPriceData] = stock_data.stock_price_data

    # Check if the ticker collection exists
    # If not, create a new collection
    collection = firestore_db.get_collection(ticker)
    if collection is None:
        collection = firestore_db.create_collection(ticker)

    # Iterate over the stock price data
    for stock_price in stock_price_data:
        # Get the date string
        date: str = stock_price.date

        # Use the document path to get the date document
        date_document = firestore_db.document(ticker=ticker, date=date)
        # Try to get the document snapshot
        date_document_snapshot = date_document.get()
        # Check if the document exists
        if date_document_snapshot.exists:
            # Update the existing document
            firestore_db.update_document(date_document, stock_price.to_dict())
        else:
            # Create a new document
            firestore_db.create_document(collection, date, stock_price.to_dict())


def process_stock_data(ticker: str, firestore_db: FirestoreDB) -> None:
    """
    Process the stock data for a given ticker symbol and a firestore database object.

    Parameters
    ----------
    ticker : str
        The stock ticker symbol, e.g. "AAPL" for Apple Inc.
    firestore_db : FirestoreDB
        The firestore database object that handles the connection and operations with firestore.

    Returns
    -------
    None

    Notes
    -----
    1. Rationale
        This function aims to update the stock data for a given ticker symbol in firestore, used for further analysis

    2. Implementation Details
        - The function first checks if the ticker collection exists in firestore.
        - If not, it creates a new collection for the ticker and sets the start date to an arbitrary date.
        - If yes, it gets the most recent date of the existing data and sets it as the start date.
        - Then, it sets the end date to the current date and fetches the stock data for the ticker and the date range,
        using OpenBB external API with yfinance data source.
        - Next, it logs the stock data using a custom logger function. Finally, it stores the data in firestore using a custom store function.
    """
    # Check if the ticker collection exists in firestore
    collection = firestore_db.get_collection(ticker)
    if collection is None:
        # Get the most recent date of the existing data
        start_date: str = firestore_db.get_most_recent_date(ticker)
    else:
        # Create a new collection for the ticker
        firestore_db.create_collection(ticker)
        # Set the start date to arbitrary start date
        start_date: str = "2024-02-01"  # Arbitrary start date

    # Set the end date to the current date
    end_date: str = datetime.date.today().isoformat()

    # Fetch the stock data for the ticker and the date range
    stock_data: StockData = fetch_stock_data(symbol=ticker, start_date=start_date, end_date=end_date)

    # Log the stock data
    log_stock_data(stock_data)

    # Store the data in firestore
    store_data(stock_data=stock_data, firestore_db=firestore_db)
