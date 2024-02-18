from config.app_config import FIRESTORE_SERVICE_ACCOUNT
from src.main.helpers.firestore_init import firestore_init, FirestoreDB
from src.main.data_models.stock_price_data import StockData, StockPriceData


def store_data(stock_data_list: list[StockData], firestore_db: FirestoreDB) -> None:
    """
    Store the stock price data in the firestore database.

    Parameters
    ----------
    stock_data_list: list[StockData]
        A list of StockData objects containing the ticker and the stock price data.
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
    # Iterate over the stock price list
    for stock_data in stock_data_list:
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
