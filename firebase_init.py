import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    if not firebase_admin._apps:
        # Replace path with your service account JSON path
        cred = credentials.Certificate("C:/Users/LENOVO/Desktop/resume/firebase_key.json")
        firebase_admin.initialize_app(cred)

    return firestore.client()
