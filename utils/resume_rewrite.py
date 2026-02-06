def rewrite_resume(role, missing_skills):
    rewrite = "### Resume Improvement Suggestions\n"

    rewrite += f"\n**Target Role:** {role}\n\n"

    rewrite += "Add bullet points like:\n"

    for skill in missing_skills:
        rewrite += f"- Hands-on experience with {skill} through projects\n"

    rewrite += "- Used industry best practices\n"
    rewrite += "- Improved system performance and scalability\n"

    return rewrite
