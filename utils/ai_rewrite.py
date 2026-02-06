def ai_suggestions(role, ats, missing_skills):
    tips = []
    if ats < 60:
        tips.append("Improve resume keywords for ATS systems.")
    for skill in missing_skills:
        tips.append(f"Add a project showcasing {skill}.")
    tips.append(f"Customize resume for {role}.")
    return tips
