import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def firestore_init(path_to_key):
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

    return firestore.client()
