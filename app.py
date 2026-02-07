import streamlit as st
from datetime import datetime

from firebase_init import init_firebase
from utils.auth import signup_user, login_user
from utils.resume_reader import read_resume
from utils.ats_score import calculate_ats, BRANCH_DATA
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
# AUTH PAGE
# -------------------------
def auth_page():
    st.title("🔐 Authentication")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # -------- LOGIN --------
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

    # -------- SIGN UP --------
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
# MAIN RESUME ANALYZER
# -------------------------
def resume_analyzer():
    st.title("📄 AI Resume Analyzer (Industry ATS)")

    st.write(f"👤 Logged in as **{st.session_state.user}**")

    if st.button("Logout", key="logout_btn"):
        st.session_state.user = None
        st.session_state.page = "auth"
        st.experimental_rerun()

    st.markdown("### 🧭 Step 1: Select Branch")
    branch = st.selectbox(
        "Branch",
        list(BRANCH_DATA.keys()),
        key="branch_select"
    )

    st.markdown("### 💼 Step 2: Select Job Role")
    role = st.selectbox(
        "Job Role",
        BRANCH_DATA[branch]["roles"],
        key="role_select"
    )

    st.markdown("### 📄 Step 3: Upload Resume (PDF)")
    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        key="resume_upload"
    )

    if st.button("Analyze Resume", key="analyze_btn"):
        if resume_file is None:
            st.error("❌ Please upload a resume PDF")
            st.stop()

        with st.spinner("Analyzing resume..."):
            resume_text = read_resume(resume_file)

            ats, matched, missing = calculate_ats(
                resume_text,
                branch,
                role
            )

            # -------------------------
            # RESULTS
            # -------------------------
            st.subheader("📊 ATS Score")
            st.metric("ATS Match", f"{ats}%")

            st.success(
                f"✅ Matched Skills: {', '.join(matched) if matched else 'None'}"
            )
            st.error(
                f"❌ Missing Skills: {', '.join(missing) if missing else 'None'}"
            )

            # -------------------------
            # AI SUGGESTIONS
            # -------------------------
            st.subheader("🤖 AI Suggestions")
            st.markdown(ai_feedback(role, ats, missing))

            # -------------------------
            # ROADMAP
            # -------------------------
            st.subheader("🛣️ Improvement Roadmap")
            roadmap = get_roadmap(branch, missing)
            for step in roadmap:
                st.write("•", step)

            # -------------------------
            # SAVE RESULT TO FIREBASE
            # -------------------------
            db.collection("ats_results").add({
                "email": st.session_state.user,
                "branch": branch,
                "role": role,
                "ats_score": ats,
                "matched_skills": matched,
                "missing_skills": missing,
                "timestamp": datetime.utcnow()
            })

            # -------------------------
            # FINAL VERDICT
            # -------------------------
            st.subheader("📌 Final Verdict")
            if ats >= 75:
                st.success("Strong industry-ready profile 💼")
            elif ats >= 50:
                st.warning("Medium fit – Upskill required 📚")
            else:
                st.error("Low fit – Major skill gap ⚠️")

# -------------------------
# ROUTER
# -------------------------
if st.session_state.page == "auth":
    auth_page()
else:
    resume_analyzer()
