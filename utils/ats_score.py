def calculate_ats(resume_text, required_skills):
    resume_text = resume_text.lower()

    matched = []
    missing = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    ats_score = int((len(matched) / len(required_skills)) * 100)

    if ats_score > 80:
        level = "Strong"
    elif ats_score > 50:
        level = "Medium"
    else:
        level = "Poor"

    return ats_score, level, matched, missing
