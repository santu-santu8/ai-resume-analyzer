import firebase_admin
from firebase_admin import credentials, auth

# Path to your service account JSON
cred = credentials.Certificate("C:/Users/LENOVO/Desktop/resume/firebase_key.json")
firebase_admin.initialize_app(cred)

# Create a test user
try:
    user = auth.create_user(
        email="testuser@example.com",
        password="test123",
        display_name="Test User"
    )
    print("✅ Created user UID:", user.uid)
except Exception as e:
    print("❌ Error:", e)
