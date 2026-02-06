import firebase_admin
from firebase_admin import credentials, firestore, auth

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db
