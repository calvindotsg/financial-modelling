from config.app_config import FIRESTORE_SERVICE_ACCOUNT
from src.main.helpers.firestore_init import firestore_init
from src.main.data_models.stock_price_data import StockData, StockPriceData


class FirestoreDB:
    """
    A class to interact with the firestore database.

    Attributes
    ----------
    db: firestore.Client
        The firestore client object.
    """

    def __init__(self):
        """
        Initialize the firestore client.

        Notes
        -----
        1. Rationale
            This method initializes the firestore client using the service account
            credentials specified in the app config file.

        2. Implementation Details
            - The firestore_init function from the firestore_init module is used to
              create the firestore client object.
            - The FIRESTORE_SERVICE_ACCOUNT constant from the app config file is used
              to provide the service account credentials.
        """
        self.db = firestore_init(FIRESTORE_SERVICE_ACCOUNT)

    def create_collection(self, name):
        """
        Create a collection with the given name and return a reference to it.

        Parameters
        ----------
        name: str
            The name of the collection to create.

        Returns
        -------
        firestore.CollectionReference
            A reference to the created collection.

        Notes
        -----
        1. Rationale
            This method creates a collection with the given name in the firestore
            database, allowing the user to store and retrieve documents in the collection.

        2. Implementation Details
            - The collection method of the firestore client object is used to create
              and return a collection reference with the given name.
        """
        return self.db.collection(name)

    def get_collection(self, name):
        """
        Get a reference to the collection with the given name or None if it does not exist.

        Parameters
        ----------
        name: str
            The name of the collection to get.

        Returns
        -------
        firestore.CollectionReference or None
            A reference to the collection with the given name or None if the collection
            does not exist.

        Notes
        -----
        1. Rationale
            This method gets a reference to the collection with the given name in the
            firestore database, allowing the user to access and manipulate the documents
            in the collection.

        2. Implementation Details
            - The collection method of the firestore client object is used to get and
              return a collection reference with the given name.
            - A try-except block is used to handle the possible exception raised if the
              collection does not exist.
        """
        try:
            return self.db.collection(name)
        except ValueError as ve:
            raise ValueError(f"Error getting collection {name}: {ve}") from ve

    def document(self, ticker, date):
        """
        Get a reference to the document with the given ticker and date or None if it does not exist.

        Parameters
        ----------
        ticker: str
            The ticker symbol of the stock.
        date: str
            The date of the stock price data.

        Returns
        -------
        firestore.DocumentReference or None
            A reference to the document with the given ticker and date or None if the
            document does not exist.

        Notes
        -----
        1. Rationale
            This method gets a reference to the document with the given ticker and date
            in the firestore database, allowing the user to access and manipulate the
            stock price data stored in the document.

        2. Implementation Details
            - The document method of the firestore client object is used to get and
              return a document reference with the given ticker and date as the path.
            - A try-except block is used to handle the possible exception raised if the
              document does not exist.
        """
        try:
            return self.db.document(f"{ticker}/{date}")
        except ValueError as ve:
            raise ValueError(f"Error getting document {ticker}/{date}: {ve}") from ve

    def create_document(self, collection, doc_id, data):
        """
        Create a document with the given id and data in the collection and return a reference to it.

        Parameters
        ----------
        collection: firestore.CollectionReference
            A reference to the collection where the document will be created.
        doc_id: str
            The id of the document to create.
        data: dict
            The data of the document to create.

        Returns
        -------
        firestore.DocumentReference
            A reference to the created document.

        Notes
        -----
        1. Rationale
            This method creates a document with the given id and data in the collection
            in the firestore database, allowing the user to store and retrieve the
            stock price data in the document.

        2. Implementation Details
            - The document method of the collection reference object is used to create
              and return a document reference with the given id.
            - The set method of the document reference object is used to set the data
              of the document.
        """
        return collection.document(doc_id).set(data)

    def get_document(self, collection, doc_id):
        """
        Get a reference to the document with the given id in the collection or None if it does not exist.

        Parameters
        ----------
        collection: firestore.CollectionReference
            A reference to the collection where the document is located.
        doc_id: str
            The id of the document to get.

        Returns
        -------
        firestore.DocumentReference or None
            A reference to the document with the given id in the collection or None if
            the document does not exist.

        Notes
        -----
        1. Rationale
            This method gets a reference to the document with the given id in the
            collection in the firestore database, allowing the user to access and
            manipulate the stock price data stored in the document.

        2. Implementation Details
            - The document method of the collection reference object is used to get and
              return a document reference with the given id.
            - A try-except block is used to handle the possible exception raised if the
              document does not exist.
        """
        try:
            return collection.document(doc_id)
        except ValueError as ve:
            raise ValueError(f"Error getting document {doc_id}: {ve}") from ve

    def update_document(self, document, data):
        """
        Update the document with the given data and return a reference to it.

        Parameters
        ----------
        document: firestore.DocumentReference
            A reference to the document to update.
        data: dict
            The data to update the document with.

        Returns
        -------
        firestore.DocumentReference
            A reference to the updated document.

        Notes
        -----
        1. Rationale
            This method updates the document with the given data in the firestore
            database, allowing the user to modify the stock price data stored in the
            document.

        2. Implementation Details
            - The update method of the document reference object is used to update the
              data of the document and return a reference to the updated document.
        """
        return document.update(data)


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
