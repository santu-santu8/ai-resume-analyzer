import streamlit as st

from utils.auth import login_user, signup_user
from utils.resume_reader import read_resume
from utils.ats_score import calculate_ats
from utils.ai_suggestions import ai_feedback
from utils.roadmap import generate_roadmap
from utils.resume_rewrite import rewrite_resume

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# -------------------------------------------------
# BRANCHES & ROLES (INDUSTRY LEVEL)
# -------------------------------------------------
BRANCH_DATA = {
    "Computer Science / IT": {
        "Python Developer": ["python", "oops", "git", "api", "django"],
        "Java Developer": ["java", "oops", "spring", "hibernate", "sql"],
        "Full Stack Developer": ["html", "css", "javascript", "react", "api"],
        "Data Scientist": ["python", "statistics", "machine learning", "pandas", "sql"],
        "AI / ML Engineer": ["python", "machine learning", "deep learning", "tensorflow", "pytorch"],
    },
    "Electronics / ECE": {
        "Embedded Engineer": ["c", "c++", "microcontroller", "rtos", "embedded"],
        "VLSI Engineer": ["verilog", "vlsi", "asic", "fpga"],
    },
    "Mechanical": {
        "Design Engineer": ["autocad", "solidworks", "catia"],
        "Manufacturing Engineer": ["cnc", "lean", "six sigma"],
    },
    "Civil": {
        "Site Engineer": ["construction", "estimation", "autocad"],
        "Structural Engineer": ["staad", "etabs", "structural analysis"],
    },
}

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("📄 AI Resume Analyzer")

# -------------------------------------------------
# AUTHENTICATION
# -------------------------------------------------
if not st.session_state.logged_in:
    st.subheader("🔐 Authentication")

    mode = st.radio("Choose", ["Login", "Sign Up"], horizontal=True)

    if mode == "Login":
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            ok, res = login_user(email, password)
            if ok:
                st.session_state.logged_in = True
                st.session_state.email = email
                st.success(f"Welcome back, {email}")
                st.rerun()
            else:
                st.error(res)

    else:
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("New Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            ok, res = signup_user(name, email, password)
            if ok:
                st.success("Account created successfully. Please login.")
            else:
                st.error(res)

    st.stop()

# -------------------------------------------------
# MAIN APP (AFTER LOGIN)
# -------------------------------------------------
st.success(f"Logged in as {st.session_state.email}")
st.divider()

# -----------------------------
# BRANCH SELECTION
# -----------------------------
branch = st.selectbox(
    "🎓 Select Branch",
    list(BRANCH_DATA.keys()),
    key="branch_select"
)

# -----------------------------
# ROLE SELECTION
# -----------------------------
role = st.selectbox(
    "💼 Select Job Role",
    list(BRANCH_DATA[branch].keys()),
    key="role_select"
)

required_skills = BRANCH_DATA[branch][role]

# -----------------------------
# RESUME UPLOAD
# -----------------------------
st.subheader("📄 Upload Resume")

resume_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"],
    key="resume_upload"
)

resume_text = None
if resume_file is not None:
    resume_text = read_resume(resume_file)
    st.success("Resume uploaded successfully ✅")

# -----------------------------
# ANALYZE BUTTON
# -----------------------------
if st.button("Analyze Resume"):
    if resume_text is None:
        st.error("Please upload a resume PDF first")
        st.stop()

    ats, level, matched, missing = calculate_ats(resume_text, required_skills)

    st.divider()
    st.subheader("📊 ATS Result")

    st.metric("ATS Score", f"{ats}%")
    st.write("**Profile Strength:**", level)

    st.success(f"Matched Skills: {', '.join(matched) if matched else 'None'}")
    st.error(f"Missing Skills: {', '.join(missing) if missing else 'None'}")

    # -----------------------------
    # AI FEEDBACK
    # -----------------------------
    st.subheader("🤖 AI Feedback")
    st.markdown(ai_feedback(role, level, missing))

    # -----------------------------
    # ROADMAP
    # -----------------------------
    st.subheader("🛣️ Improvement Roadmap")
    roadmap = generate_roadmap(missing)
    for step in roadmap:
        st.write("•", step)

    # -----------------------------
    # RESUME REWRITE
    # -----------------------------
    st.subheader("✍ Resume Rewrite Suggestions")
    st.markdown(rewrite_resume(role, missing))

# -----------------------------
# LOGOUT
# -----------------------------
st.divider()
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.rerun()
