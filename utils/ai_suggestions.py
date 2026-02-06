def ai_feedback(role, level, missing_skills):
    feedback = f"Your resume is rated **{level}** for the role **{role}**.\n\n"

    if missing_skills:
        feedback += "### Skills to Improve:\n"
        for skill in missing_skills:
            feedback += f"- Learn and practice **{skill}**\n"

    feedback += "\n### AI Career Advice:\n"
    feedback += "- Build 2–3 real-world projects\n"
    feedback += "- Add measurable achievements\n"
    feedback += "- Optimize resume for keywords\n"

    return feedback
