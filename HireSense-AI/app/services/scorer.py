from app.models.schemas import JobProfile, ResumeProfile, ScoreBreakdown

WEIGHTS = {
    "skills_match": 0.40,
    "experience": 0.20,
    "education": 0.10,
    "projects": 0.15,
    "formatting": 0.10,
    "certifications": 0.05,
}


def score_candidate(
    resume: ResumeProfile,
    job: JobProfile,
    matched_skills: list[str],
    semantic_score: float,
) -> ScoreBreakdown:
    skills_score = _ratio(len(matched_skills), len(job.required_skills))
    experience_score = _experience_score(resume, job)
    education_score = _education_score(resume, job)
    projects_score = 100.0 if resume.projects else 50.0 if _mentions_project(resume.raw_text) else 0.0
    formatting_score = _formatting_score(resume.raw_text)
    certifications_score = 100.0 if resume.certifications else 50.0 if _mentions_certification(resume.raw_text) else 0.0

    weighted_total = (
        skills_score * WEIGHTS["skills_match"]
        + experience_score * WEIGHTS["experience"]
        + education_score * WEIGHTS["education"]
        + projects_score * WEIGHTS["projects"]
        + formatting_score * WEIGHTS["formatting"]
        + certifications_score * WEIGHTS["certifications"]
    )
    final_score = (weighted_total * 0.70) + (semantic_score * 0.30)

    return ScoreBreakdown(
        skills_match=round(skills_score, 2),
        experience=round(experience_score, 2),
        education=round(education_score, 2),
        projects=round(projects_score, 2),
        formatting=round(formatting_score, 2),
        certifications=round(certifications_score, 2),
        weighted_total=round(weighted_total, 2),
        semantic_score=round(semantic_score, 2),
        final_score=round(final_score, 2),
    )


def _ratio(part: int, whole: int) -> float:
    if whole <= 0:
        return 100.0
    return min(part / whole, 1.0) * 100


def _experience_score(resume: ResumeProfile, job: JobProfile) -> float:
    if job.min_years_experience <= 0:
        return 100.0

    resume_years = _extract_resume_years(resume.raw_text)
    return _ratio(resume_years, job.min_years_experience)


def _education_score(resume: ResumeProfile, job: JobProfile) -> float:
    if not job.education:
        return 100.0

    text = " ".join(resume.education + [resume.raw_text]).lower()
    matches = sum(1 for item in job.education if item.lower() in text)
    return _ratio(matches, len(job.education))


def _formatting_score(text: str) -> float:
    required_markers = ["skills", "experience", "education"]
    lower = text.lower()
    marker_score = _ratio(sum(marker in lower for marker in required_markers), len(required_markers))
    length_score = 100.0 if 800 <= len(text) <= 8000 else 65.0
    return (marker_score * 0.7) + (length_score * 0.3)


def _extract_resume_years(text: str) -> int:
    import re

    matches = re.findall(r"(\d+)\+?\s*(?:years|yrs)\b", text, flags=re.IGNORECASE)
    return max((int(match) for match in matches), default=0)


def _mentions_project(text: str) -> bool:
    return "project" in text.lower()


def _mentions_certification(text: str) -> bool:
    lower = text.lower()
    return "certification" in lower or "certified" in lower
