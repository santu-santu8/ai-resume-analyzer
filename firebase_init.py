import firebase_admin
from firebase_admin import credentials, firestore
import os

def init_firebase():
    if not firebase_admin._apps:
        # Relative path to the JSON in the project folder
        cred_path = os.path.join(os.path.dirname(__file__), "firebase_key.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()
