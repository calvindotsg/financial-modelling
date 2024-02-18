from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore

from config.app_config import FIRESTORE_SERVICE_ACCOUNT


def firestore_init(path_to_key: str):
    """
    Initialise Firestore with the given service account key.

    Parameters
    ----------
        path_to_key: str
            Path to the service account key file.

    Returns
    -------
        firestore.client.Client:
            Firestore client object.
    """
    # Use a service account
    cred = credentials.Certificate(path_to_key)
    firebase_admin.initialize_app(cred)
    client = firestore.client()

    return client


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

    def get_most_recent_date(self, ticker: str) -> Any | None:
        """
        Return the most recent date of the stock data for a given ticker symbol.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol, e.g. "AAPL" for Apple Inc.

        Returns
        -------
        Any | None
            The most recent date of the stock data in ISO format, e.g. "2024-02-18", or None if the ticker collection is empty.

        Notes
        -----
        1. Rationale
            This method is used to determine the start date for fetching new stock data for a given ticker symbol.

        2. Implementation Details
            - The method first gets the ticker collection reference from the firestore database object.
            - Then, it queries the ticker collection for the most recent document by ordering the documents by
            the date field in descending order and limiting the result to one document.
            - Next, it checks if the query result is empty. If yes, it returns None.
            If no, it gets the first document from the result and extracts the date field from the document.
            - Finally, it returns the date as the output.
        """

        # Get the ticker collection reference
        ticker_ref = self.db.collection(ticker)

        # Query the ticker collection for the most recent document
        query = ticker_ref.order_by("date", direction=firestore.Query.DESCENDING).limit(1)

        # Get the query result
        result = query.get()

        # Check if the result is empty
        if len(result) == 0:
            # Return None
            return None
        else:
            # Get the first document
            doc = result[0]

            # Get the date field from the document
            date = doc.get("date")

            # Return the date
            return date

    @staticmethod
    def create_document(collection, doc_id, data):
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

    @staticmethod
    def get_document(collection, doc_id):
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

    @staticmethod
    def update_document(document, data):
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
