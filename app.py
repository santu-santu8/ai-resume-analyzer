import streamlit as st
from datetime import datetime
from firebase_init import init_firebase
from utils.auth import signup_user, login_user
from utils.ats_score import calculate_ats
from utils.ai_suggestions import ai_feedback
from utils.resume_rewrite import rewrite_resume

# ------------------- PAGE -------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("📄 AI Resume Analyzer")

# ------------------- FIRESTORE -------------------
db = init_firebase()

# ------------------- SESSION STATE -------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "uid" not in st.session_state:
    st.session_state.uid = None

# ------------------- AUTH -------------------
if st.session_state.user is None:
    st.subheader("🔐 Authentication")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # -------- LOGIN --------
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(email, password)
            if result["success"]:
                st.session_state.user = email
                st.session_state.uid = result["uid"]
                st.success(f"Welcome {email}")
                st.rerun()
            else:
                st.error(result["error"])

    # -------- SIGN UP --------
    with tab2:
        name = st.text_input("Name")
        new_email = st.text_input("New Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            result = signup_user(new_email, password)
            if result["success"]:
                st.success("Account created successfully. Please login.")
            else:
                st.error(result["error"])

    st.stop()

# ------------------- LOGGED-IN USER -------------------
st.success(f"Logged in as {st.session_state.user}")

if st.button("Logout"):
    st.session_state.user = None
    st.session_state.uid = None
    st.rerun()

st.divider()

# ------------------- BRANCH → ROLE → SKILLS -------------------
BRANCH_ROLE_SKILLS = {
    "CSE": {
        "Python Developer": ["python", "oops", "git", "api", "django"],
        "Data Scientist": ["python", "statistics", "ml", "sql", "pandas"],
        "Web Developer": ["html", "css", "javascript", "react", "api"]
    },
    "ECE": {
        "Embedded Engineer": ["c", "c++", "microcontroller", "iot"],
        "IoT Engineer": ["iot", "arduino", "raspberry pi", "sensors"]
    },
    "MECH": {
        "Design Engineer": ["autocad", "solidworks", "gd&t"],
        "Manufacturing Engineer": ["cnc", "manufacturing", "quality"]
    }
}

branch = st.selectbox("Select Branch", BRANCH_ROLE_SKILLS.keys())
role = st.selectbox("Select Job Role", BRANCH_ROLE_SKILLS[branch].keys())
resume = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

# ------------------- ANALYZE RESUME -------------------
if st.button("Analyze Resume"):
    if resume is None:
        st.error("❌ Please upload a resume")
        st.stop()

    resume_text = resume.read().decode("utf-8", errors="ignore").lower()
    required_skills = BRANCH_ROLE_SKILLS[branch][role]

    ats, level, matched, missing = calculate_ats(
        resume_text,
        required_skills
    )

    st.subheader("📊 ATS Result")
    st.metric("ATS Score", f"{ats}%")
    st.write("Level:", level)

    st.success("✅ Matched Skills")
    st.write(matched if matched else "None")

    st.error("❌ Missing Skills")
    st.write(missing if missing else "None")

    st.subheader("🤖 AI Suggestions")
    st.markdown(ai_feedback(role, level, missing))

    st.subheader("✍ Resume Rewrite")
    st.markdown(rewrite_resume(role, missing))

    # Save ATS Result
    db.collection("ats_results").add({
        "uid": st.session_state.uid,
        "name": st.session_state.user,
        "branch": branch,
        "role": role,
        "ats_score": ats,
        "level": level,
        "matched_skills": matched,
        "missing_skills": missing,
        "created_at": datetime.utcnow()
    })
    st.success("📁 Results saved to Firebase")
