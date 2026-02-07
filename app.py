import streamlit as st

from utils.auth import login_user, signup_user
from utils.resume_reader import read_resume
from utils.ats_score import calculate_ats
from utils.ai_suggestions import ai_feedback
from utils.roadmap import generate_roadmap
from utils.resume_rewrite import rewrite_resume

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# --------------------------------------------------
# BRANCH + ROLE DATA (INDUSTRY RELEVANT)
# --------------------------------------------------
BRANCH_DATA = {
    "Computer Science / IT": {
        "roles": {
            "Python Developer": ["python", "oops", "git", "api", "django"],
            "Java Developer": ["java", "oops", "spring", "hibernate", "sql"],
            "Full Stack Developer": ["html", "css", "javascript", "react", "api"],
            "Data Scientist": ["python", "statistics", "machine learning", "pandas", "sql"],
        }
    },
    "Electronics / ECE": {
        "roles": {
            "Embedded Engineer": ["c", "c++", "microcontroller", "rtos", "embedded"],
            "VLSI Engineer": ["verilog", "vlsi", "asic", "fpga"],
        }
    },
    "Mechanical": {
        "roles": {
            "Design Engineer": ["autocad", "solidworks", "catia"],
            "Manufacturing Engineer": ["cnc", "lean", "six sigma"],
        }
    },
    "Civil": {
        "roles": {
            "Site Engineer": ["construction", "estimation", "autocad"],
            "Structural Engineer": ["staad", "etabs", "structural analysis"],
        }
    },
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# --------------------------------------------------
# AUTHENTICATION UI
# --------------------------------------------------
st.title("📄 AI Resume Analyzer")
st.subheader("🔐 Authentication")

auth_tab = st.radio("Choose", ["Login", "Sign Up"])

if not st.session_state.logged_in:
    if auth_tab == "Login":
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            ok, res = login_user(email, password)
            if ok:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(f"Welcome back, {email}")
                st.experimental_rerun()
            else:
                st.error(res)

    else:
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("New Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Sign Up"):
            ok, res = signup_user(name, email, password)
            if ok:
                st.success("Account created. Please login.")
            else:
                st.error(res)

# --------------------------------------------------
# MAIN APP (AFTER LOGIN)
# --------------------------------------------------
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state.user_email}")

    st.divider()

    # -----------------------------
    # STEP 1: BRANCH
    # -----------------------------
    branch = st.selectbox(
        "🎓 Select Branch",
        list(BRANCH_DATA.keys())
    )

    # -----------------------------
    # STEP 2: ROLE
    # -----------------------------
    role = st.selectbox(
        "💼 Select Job Role",
        list(BRANCH_DATA[branch]["roles"].keys())
    )

    required_skills = BRANCH_DATA[branch]["roles"][role]

    # -----------------------------
    # STEP 3: RESUME UPLOAD
    # -----------------------------
    st.subheader("📄 Upload Resume")

    resume_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"]
    )

    if resume_file:
        resume_text = read_resume(resume_file)
        st.success("Resume uploaded successfully")

    # -----------------------------
    # ANALYZE
    # -----------------------------
    if st.button("Analyze Resume"):
        if not resume_file:
            st.error("Please upload a resume first")
            st.stop()

        ats, level, matched, missing = calculate_ats(
            resume_text,
            required_skills
        )

        st.divider()
        st.subheader("📊 ATS Result")

        st.metric("ATS Score", f"{ats}%")
        st.write("Level:", level)

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
        for step in generate_roadmap(missing):
            st.write("•", step)

        # -----------------------------
        # RESUME REWRITE
        # -----------------------------
        st.subheader("✍ Resume Rewrite Suggestions")
        st.markdown(rewrite_resume(role, missing))
