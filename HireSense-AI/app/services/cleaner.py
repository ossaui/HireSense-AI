import re

SECTION_ALIASES = {
    "education": "Education",
    "experience": "Experience",
    "work experience": "Experience",
    "professional experience": "Experience",
    "projects": "Projects",
    "certifications": "Certifications",
    "licenses": "Certifications",
    "skills": "Skills",
}


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\bpage\s+\d+\s*(of\s+\d+)?\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[_=]{3,}", " ", text)

    lines = [re.sub(r"[^\S\r\n]+", " ", line).strip() for line in text.splitlines()]
    compacted: list[str] = []
    for line in lines:
        if line:
            compacted.append(line)
        elif compacted and compacted[-1] != "":
            compacted.append("")

    return "\n".join(compacted).strip()


def normalize_skill(skill: str) -> str:
    special = {
        "aws": "AWS",
        "gcp": "GCP",
        "sql": "SQL",
        "nlp": "NLP",
        "api": "API",
        "fastapi": "FastAPI",
        "pytorch": "PyTorch",
        "scikit-learn": "Scikit-learn",
        "sklearn": "Scikit-learn",
        "tensorflow": "TensorFlow",
        "xgboost": "XGBoost",
    }
    key = skill.strip().lower()
    if key in special:
        return special[key]
    return " ".join(part.capitalize() for part in re.split(r"\s+", key) if part)


def split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = "Summary"

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        normalized = re.sub(r"[:\-]+$", "", line).strip().lower()
        if normalized in SECTION_ALIASES:
            current = SECTION_ALIASES[normalized]
            sections.setdefault(current, [])
            continue

        sections.setdefault(current, []).append(line)

    return sections
