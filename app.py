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
# INIT FIREBASE
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
# BRANCH → ROLE → SKILLS (Industry-style)
# -------------------------
BRANCH_DATA = {
    "Computer Science (CSE)": {
        "Python Developer": ["python", "oops", "django", "flask", "api", "git"],
        "Data Scientist": ["python", "pandas", "numpy", "ml", "statistics", "sql"],
        "Web Developer": ["html", "css", "javascript", "react", "api"]
    },
    "Electronics (ECE)": {
        "Embedded Engineer": ["c", "c++", "microcontroller", "iot", "arduino"],
        "VLSI Engineer": ["verilog", "vlsi", "fpga", "asic"]
    },
    "Mechanical": {
        "Design Engineer": ["autocad", "solidworks", "gd&t", "manufacturing"],
        "Production Engineer": ["quality", "six sigma", "lean", "operations"]
    }
}

# -------------------------
# HELPER: ATS LEVEL
# -------------------------
def ats_level(score):
    if score >= 75:
        return "Strong Fit"
    elif score >= 50:
        return "Medium Fit"
    else:
        return "Poor Fit"

# -------------------------
# AUTH PAGE
# -------------------------
def auth_page():
    st.title("🔐 Authentication")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ---- LOGIN ----
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

    # ---- SIGN UP ----
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
                st.success("Account created successfully. Please login.")
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

    # ---- BRANCH ----
    branch = st.selectbox(
        "Select Branch",
        list(BRANCH_DATA.keys()),
        key="branch_select"
    )

    # ---- ROLE ----
    role = st.selectbox(
        "Select Job Role",
        list(BRANCH_DATA[branch].keys()),
        key="role_select"
    )

    # ---- RESUME ----
    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="resume_upload"
    )

    if st.button("Analyze Resume", key="analyze_btn"):
        if resume_file is None:
            st.error("❌ Please upload a resume PDF")
            return

        with st.spinner("Analyzing resume..."):
            resume_text = read_resume(resume_file).lower()
            skills = BRANCH_DATA[branch][role]

            ats, matched, missing = calculate_ats(resume_text, skills)
            level = ats_level(ats)

            # ---- ATS RESULT ----
            st.subheader("📊 ATS Result")
            st.metric("ATS Score", f"{ats}%")
            st.write("Level:", level)

            st.success(f"Matched Skills: {', '.join(matched) if matched else 'None'}")
            st.error(f"Missing Skills: {', '.join(missing) if missing else 'None'}")

            # ---- AI FEEDBACK ----
            st.subheader("🤖 AI Feedback")
            st.markdown(ai_feedback(role, level, missing))

            # ---- ROADMAP ----
            st.subheader("🛣️ Improvement Roadmap")
            for step in get_roadmap(branch, missing):
                st.write("•", step)

            # ---- SAVE TO FIREBASE ----
            db.collection("ats_results").add({
                "email": st.session_state.user,
                "branch": branch,
                "role": role,
                "ats_score": ats,
                "level": level,
                "matched_skills": matched,
                "missing_skills": missing,
                "timestamp": datetime.utcnow()
            })

# -------------------------
# ROUTER
# -------------------------
if st.session_state.page == "auth":
    auth_page()
else:
    resume_analyzer()
