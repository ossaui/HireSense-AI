from app.models.schemas import JobProfile, ResumeProfile, ScoreBreakdown


def build_explanation(
    resume: ResumeProfile,
    job: JobProfile,
    matched_skills: list[str],
    missing_skills: list[str],
    score: ScoreBreakdown,
) -> list[str]:
    explanation = []

    for skill in matched_skills:
        explanation.append(f"+ {skill} matched the job description.")

    for skill in missing_skills:
        explanation.append(f"- Missing required skill: {skill}.")

    if job.min_years_experience and score.experience < 100:
        explanation.append(f"- Experience appears below the requested {job.min_years_experience} years.")

    if job.education and score.education < 100:
        explanation.append("- Education requirements were only partially matched.")

    if not resume.projects:
        explanation.append("- No dedicated projects section was detected.")

    if not resume.certifications:
        explanation.append("- No certifications section was detected.")

    explanation.append(f"Semantic similarity between resume and job description is {score.semantic_score}%.")
    explanation.append(f"Final ranking score is {score.final_score}/100.")

    return explanation
