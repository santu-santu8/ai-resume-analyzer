import streamlit as st
from PyPDF2 import PdfReader

from utils.auth import login_user, signup_user
from utils.ats_score import calculate_ats
from utils.ai_suggestions import ai_feedback
from utils.resume_rewrite import rewrite_resume
from utils.roadmap import generate_roadmap

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")

# --------------------------------------------------
# SESSION STATE INITIALIZATION (CRITICAL)
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------
if not st.session_state.logged_in:
    st.subheader("🔐 Authentication")

    auth_choice = st.radio("Choose", ["Login", "Sign Up"])

    if auth_choice == "Login":
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            res = login_user(email, password)
            if res.get("success"):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"Welcome back, {email}")
                st.rerun()
            else:
                st.error(res.get("error"))

    else:
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("New Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            res = signup_user(email, password)
            if res.get("success"):
                st.success("Account created successfully. Please login.")
            else:
                st.error(res.get("error"))

    st.stop()

# --------------------------------------------------
# LOGGED IN UI
# --------------------------------------------------
st.success(f"Logged in as {st.session_state.user_email}")

# --------------------------------------------------
# BRANCH & ROLE DATA (INDUSTRY-RELEVANT)
# --------------------------------------------------
BRANCH_DATA = {
    "Computer Science / IT": {
        "Full Stack Developer": ["html", "css", "javascript", "react", "node", "api"],
        "Backend Developer": ["python", "django", "flask", "sql", "api"],
        "Data Scientist": ["python", "statistics", "machine learning", "pandas", "sql"],
        "AI / ML Engineer": ["python", "machine learning", "deep learning", "tensorflow"]
    },
    "Electronics / ECE": {
        "Embedded Engineer": ["c", "embedded systems", "microcontrollers"],
        "IoT Engineer": ["iot", "sensors", "python", "cloud"]
    },
    "Mechanical": {
        "Design Engineer": ["autocad", "solidworks", "design"],
        "Manufacturing Engineer": ["manufacturing", "quality", "process"]
    }
}

# --------------------------------------------------
# BRANCH SELECTION
# --------------------------------------------------
st.subheader("🎓 Select Branch")
branch = st.selectbox("Branch", list(BRANCH_DATA.keys()))

# --------------------------------------------------
# ROLE SELECTION
# --------------------------------------------------
st.subheader("💼 Select Job Role")
role = st.selectbox("Role", list(BRANCH_DATA[branch].keys()))
required_skills = BRANCH_DATA[branch][role]

# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------
st.subheader("📄 Upload Resume")
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

resume_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        if page.extract_text():
            resume_text += page.extract_text().lower()
    st.success("Resume uploaded successfully ✅")

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------
if st.button("Analyze Resume") and resume_text:
    ats, level, matched, missing = calculate_ats(resume_text, required_skills)

    st.subheader("📊 ATS Result")
    st.metric("ATS Score", f"{ats}%")
    st.write("Level:", level)

    st.subheader("✅ Matched Skills")
    st.write(matched if matched else "No matched skills")

    st.subheader("❌ Missing Skills")
    st.write(missing if missing else "None")

    st.subheader("🤖 AI Suggestions")
    st.markdown(ai_feedback(role, level, missing))

    st.subheader("✍ Resume Rewrite Tips")
    st.markdown(rewrite_resume(role, missing))

    st.subheader("🛣 Career Roadmap")
    roadmap = generate_roadmap(missing)
    for step in roadmap:
        st.write("•", step)

elif st.button("Analyze Resume") and not resume_text:
    st.warning("Please upload a resume first.")
