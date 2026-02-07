import streamlit as st
from datetime import datetime

from firebase_init import init_firebase
from utils.auth import signup_user, login_user
from utils.resume_reader import read_resume
from utils.ats_score import calculate_ats
from utils.ai_suggestions import ai_feedback
from utils.roadmap import get_roadmap

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# -------------------------
# FIREBASE INIT
# -------------------------
db = init_firebase()

# -------------------------
# SESSION STATE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "auth"

# -------------------------
# INDUSTRY BRANCH DATA
# -------------------------
BRANCH_DATA = {
    "Computer Science (CSE)": {
        "roles": {
            "Python Developer": ["python", "oops", "django", "flask", "api", "git"],
            "Data Scientist": ["python", "pandas", "numpy", "ml", "statistics", "sql"],
            "Web Developer": ["html", "css", "javascript", "react", "api"]
        }
    },
    "Electronics (ECE)": {
        "roles": {
            "Embedded Engineer": ["c", "c++", "microcontroller", "iot", "arduino"],
            "VLSI Engineer": ["verilog", "vlsi", "fpga", "asic"]
        }
    },
    "Mechanical": {
        "roles": {
            "Design Engineer": ["autocad", "solidworks", "gd&t", "manufacturing"],
            "Production Engineer": ["quality", "six sigma", "lean", "operations"]
        }
    }
}

# -------------------------
# AUTH PAGE
# -------------------------
def auth_page():
    st.title("🔐 Authentication")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_btn"):
            ok, res = login_user(email, password)
            if ok:
                st.session_state.user = email
                st.session_state.page = "app"
                st.success(f"Welcome back, {email}")
                st.experimental_rerun()
            else:
                st.error(res)

    with tab2:
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("New Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up", key="signup_btn"):
            ok, res = signup_user(email, password)
            if ok:
                db.collection("users").document(email).set({
                    "name": name,
                    "email": email,
                    "created_at": datetime.utcnow()
                })
                st.success("Account created. Please login.")
            else:
                st.error(res)

# -------------------------
# MAIN APP
# -------------------------
def resume_analyzer():
    st.title("📄 AI Resume Analyzer (Industry ATS)")
    st.write(f"👤 Logged in as **{st.session_state.user}**")

    if st.button("Logout", key="logout_btn"):
        st.session_state.user = None
        st.session_state.page = "auth"
        st.experimental_rerun()

    branch = st.selectbox("Select Branch", BRANCH_DATA.keys(), key="branch")
    role = st.selectbox(
        "Select Job Role",
        BRANCH_DATA[branch]["roles"].keys(),
        key="role"
    )

    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume")

    if st.button("Analyze Resume", key="analyze"):
        if not resume:
            st.error("Please upload a resume")
            return

        resume_text = read_resume(resume)
        skills = BRANCH_DATA[branch]["roles"][role]

        ats, matched, missing = calculate_ats(resume_text.lower(), skills)

        st.subheader("📊 ATS Score")
        st.metric("ATS Match", f"{ats}%")

        st.success(f"Matched Skills: {', '.join(matched) if matched else 'None'}")
        st.error(f"Missing Skills: {', '.join(missing) if missing else 'None'}")

        st.subheader("🤖 AI Suggestions")
        st.markdown(ai_feedback(role, ats, missing))

        st.subheader("🛣️ Improvement Roadmap")
        for step in get_roadmap(branch, missing):
            st.write("•", step)

        db.collection("ats_results").add({
            "email": st.session_state.user,
            "branch": branch,
            "role": role,
            "ats_score": ats,
            "matched": matched,
            "missing": missing,
            "timestamp": datetime.utcnow()
        })

# -------------------------
# ROUTER
# -------------------------
if st.session_state.page == "auth":
    auth_page()
else:
    resume_analyzer()
