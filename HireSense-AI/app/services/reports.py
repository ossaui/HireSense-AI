from app.models.schemas import JobProfile, ResumeProfile, ScoreBreakdown

DEFAULT_QUESTIONS = [
    "Explain one project where you used the most relevant skill for this role.",
    "How do you validate that a model or data pipeline is production ready?",
    "Describe a time you handled messy or incomplete data.",
]

SKILL_QUESTION_BANK = {
    "Python": "Walk me through how you structure a production Python project.",
    "SQL": "How would you optimize a slow SQL query?",
    "Docker": "How would you containerize and debug a FastAPI application?",
    "AWS": "Which AWS services would you use to deploy this project and why?",
    "FastAPI": "How do dependencies and validation work in FastAPI?",
    "TensorFlow": "How do you prevent overfitting in a TensorFlow model?",
    "PyTorch": "How would you debug exploding gradients in PyTorch?",
    "Scikit-learn": "How do you choose between cross validation strategies in scikit-learn?",
    "NLP": "How would you evaluate an NLP matching system beyond accuracy?",
}


def generate_interview_questions(
    matched_skills: list[str],
    missing_skills: list[str],
    limit: int = 5,
) -> list[str]:
    questions = []
    for skill in matched_skills + missing_skills:
        question = SKILL_QUESTION_BANK.get(skill)
        if question and question not in questions:
            questions.append(question)

    for question in DEFAULT_QUESTIONS:
        if question not in questions:
            questions.append(question)

    return questions[:limit]


def generate_recruiter_report(
    resume: ResumeProfile,
    job: JobProfile,
    matched_skills: list[str],
    missing_skills: list[str],
    score: ScoreBreakdown,
) -> str:
    strengths = ", ".join(matched_skills[:8]) if matched_skills else "No direct skill matches detected"
    gaps = ", ".join(missing_skills[:8]) if missing_skills else "No major required skill gaps detected"

    recommendation = "Strong fit"
    if score.final_score < 60:
        recommendation = "Needs review"
    elif score.final_score < 75:
        recommendation = "Moderate fit"

    return (
        f"{resume.name} scored {score.final_score}/100 for {job.title}. "
        f"Strengths: {strengths}. "
        f"Gaps: {gaps}. "
        f"Recommendation: {recommendation}. "
        "Use the interview questions to validate practical depth and project ownership."
    )
