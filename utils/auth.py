import firebase_admin
from firebase_admin import auth

def signup_user(email, password, name):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )
        return {"success": True, "uid": user.uid}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user(email):
    try:
        user = auth.get_user_by_email(email)
        return {"success": True, "uid": user.uid, "name": user.display_name}
    except Exception as e:
        return {"success": False, "error": str(e)}
