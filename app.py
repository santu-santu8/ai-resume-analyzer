import streamlit as st

from firebase_init import init_firebase
from utils.auth import login_user, signup_user
from utils.ats_score import calculate_ats, BRANCH_DATA
from utils.ai_suggestions import ai_feedback
from utils.roadmap import generate_roadmap

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

# --------------------------------------------------
# Firebase init
# --------------------------------------------------
db = init_firebase()

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# --------------------------------------------------
# AUTH UI
# --------------------------------------------------
st.title("📄 AI Resume Analyzer")
st.subheader("🔐 Authentication")

tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        try:
            ok, res = login_user(login_email, login_password)
            if ok:
                st.session_state.user = login_email
                st.success(f"Welcome back, {login_email}")
                st.rerun()
            else:
                st.error(res)
        except Exception as e:
            st.error(str(e))

with tab2:
    signup_name = st.text_input("Name", key="signup_name")
    signup_email = st.text_input("New Email", key="signup_email")
    signup_password = st.text_input(
        "Password", type="password", key="signup_password"
    )

    if st.button("Sign Up"):
        try:
            ok, res = signup_user(signup_name, signup_email, signup_password)
            if ok:
                st.success("Account created! Please login.")
            else:
                st.error(res)
        except Exception as e:
            st.error(str(e))

# --------------------------------------------------
# STOP if not logged in
# --------------------------------------------------
if not st.session_state.user:
    st.stop()

# --------------------------------------------------
# MAIN APP
# --------------------------------------------------
st.success(f"Logged in as {st.session_state.user}")
st.divider()

st.header("📊 Resume Analysis")

# Select branch
branch = st.selectbox("Select Branch", list(BRANCH_DATA.keys()))

# Select role based on branch
role = st.selectbox("Select Role", list(BRANCH_DATA[branch].keys()))

# Resume input
resume_text = st.text_area(
    "Paste your resume content here",
    height=250,
    placeholder="Paste your resume text here..."
)

# --------------------------------------------------
# Analyze
# --------------------------------------------------
if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please paste your resume text.")
    else:
        ats_score, missing_skills, level = calculate_ats(
            resume_text, branch, role
        )

        st.subheader("✅ ATS Result")
        st.write(f"**ATS Score:** {ats_score}%")
        st.write(f"**Level:** {level}")

        st.subheader("🧠 AI Feedback")
        feedback = ai_feedback(role, level, missing_skills)
        st.markdown(feedback)

        st.subheader("🛣️ Learning Roadmap")
        roadmap = generate_roadmap(missing_skills)

        if roadmap:
            for step in roadmap:
                st.write("•", step)
        else:
            st.success("Great! No major skill gaps found 🎉")
