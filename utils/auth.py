import pyrebase
import os

config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
}

firebase = pyrebase.initialize_app(config)
auth_client = firebase.auth()


def signup_user(name, email, password):
    try:
        user = auth_client.create_user_with_email_and_password(email, password)
        return True, user
    except Exception as e:
        return False, str(e)


def login_user(email, password):
    try:
        user = auth_client.sign_in_with_email_and_password(email, password)
        return True, user
    except Exception as e:
        return False, str(e)
