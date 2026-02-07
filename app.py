import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import os

# ---------------- FIREBASE INIT ---------------- #
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate({
            "type": os.getenv("FIREBASE_TYPE"),
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
        })
        firebase_admin.initialize_app(cred)

    return firestore.client()


db = init_firebase()

# ---------------- UI ---------------- #
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("📄 AI Resume Analyzer")
st.subheader("🔐 Authentication")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

# ---------------- LOGIN ---------------- #
with tab1:
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        try:
            user = auth.get_user_by_email(login_email)
            st.success(f"Welcome back, {user.email}")
            st.session_state["user"] = user.email
        except Exception as e:
            st.error("User not found. Please sign up first.")

# ---------------- SIGNUP ---------------- #
with tab2:
    signup_name = st.text_input("Name", key="signup_name")
    signup_email = st.text_input("New Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        try:
            user = auth.create_user(
                email=signup_email,
                password=signup_password
            )

            db.collection("users").document(user.uid).set({
                "name": signup_name,
                "email": signup_email
            })

            st.success("Signup successful! You can now login.")
        except Exception as e:
            st.error(str(e))

# ---------------- AFTER LOGIN ---------------- #
if "user" in st.session_state:
    st.success(f"Logged in as {st.session_state['user']}")
    st.write("🎯 Resume Analyzer features will appear here.")
