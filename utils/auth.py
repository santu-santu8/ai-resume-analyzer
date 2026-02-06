import pyrebase

# Replace with your Firebase project settings
config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT.firebaseapp.com",
    "databaseURL": "",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "",
    "messagingSenderId": "YOUR_SENDER_ID",
    "appId": "YOUR_APP_ID"
}

firebase = pyrebase.initialize_app(config)
auth_client = firebase.auth()

def signup_user(email, password):
    try:
        user = auth_client.create_user_with_email_and_password(email, password)
        return {"success": True, "uid": user['localId']}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user(email, password):
    try:
        user = auth_client.sign_in_with_email_and_password(email, password)
        return {"success": True, "uid": user['localId']}
    except Exception as e:
        return {"success": False, "error": str(e)}
