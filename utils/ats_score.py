BRANCH_DATA = {
    "Computer Science": {
        "Software Engineer": [
            "python", "java", "data structures", "algorithms",
            "git", "sql", "oop"
        ],
        "Data Scientist": [
            "python", "machine learning", "statistics",
            "pandas", "numpy", "sql"
        ]
    },
    "Electronics": {
        "Embedded Engineer": [
            "c", "c++", "microcontrollers",
            "embedded systems", "rtos"
        ]
    }
}


def calculate_ats(resume_text, branch, role):
    resume_text = resume_text.lower()
    required_skills = BRANCH_DATA[branch][role]

    matched = []
    missing = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    ats_score = int((len(matched) / len(required_skills)) * 100)

    if ats_score >= 80:
        level = "Strong"
    elif ats_score >= 50:
        level = "Medium"
    else:
        level = "Poor"

    return ats_score, missing, level
