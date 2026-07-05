import re

from app.models.schemas import JobProfile
from app.services.cleaner import clean_text
from app.services.skills import extract_skills

EDUCATION_TERMS = [
    "bachelor",
    "master",
    "phd",
    "degree",
    "computer science",
    "engineering",
    "statistics",
    "mathematics",
]


def parse_job_description(title: str, description: str) -> JobProfile:
    text = clean_text(description)
    skills = extract_skills(text)
    preferred = _extract_preferred_skills(text, skills)
    required = [skill for skill in skills if skill not in preferred]

    return JobProfile(
        title=title.strip() or "Untitled Role",
        required_skills=required,
        preferred_skills=preferred,
        education=_extract_education(text),
        min_years_experience=_extract_years(text),
        raw_text=text,
    )


def _extract_preferred_skills(text: str, skills: list[str]) -> list[str]:
    preferred_window = re.findall(
        r"(?:preferred|nice to have|good to have|bonus)(.{0,180})",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    preferred_text = " ".join(preferred_window)
    return [skill for skill in skills if skill.lower() in preferred_text.lower()]


def _extract_education(text: str) -> list[str]:
    lower = text.lower()
    return sorted({term.title() for term in EDUCATION_TERMS if term in lower})


def _extract_years(text: str) -> int:
    matches = re.findall(r"(\d+)\+?\s*(?:years|yrs)\b", text, flags=re.IGNORECASE)
    if not matches:
        return 0
    return max(int(match) for match in matches)
