import json
import re
from functools import lru_cache
from pathlib import Path

from app.services.cleaner import normalize_skill

SKILL_CATALOG_PATH = Path(__file__).resolve().parents[1] / "ml" / "skills.json"


@lru_cache
def load_skill_catalog() -> dict[str, list[str]]:
    with SKILL_CATALOG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def flatten_skill_catalog() -> dict[str, str]:
    flattened = {}
    for category, skills in load_skill_catalog().items():
        for skill in skills:
            flattened[normalize_skill(skill)] = category
    return flattened


def extract_skills(text: str) -> list[str]:
    normalized_text = f" {text.lower()} "
    detected: set[str] = set()

    for skill in flatten_skill_catalog():
        normalized = normalize_skill(skill)
        pattern = _skill_pattern(normalized)
        if re.search(pattern, normalized_text, flags=re.IGNORECASE):
            detected.add(normalized)

    return sorted(detected)


def categorize_skills(skills: list[str]) -> dict[str, list[str]]:
    catalog = flatten_skill_catalog()
    categorized: dict[str, list[str]] = {}
    for skill in skills:
        category = catalog.get(normalize_skill(skill), "Other")
        categorized.setdefault(category, []).append(normalize_skill(skill))
    return categorized


def _skill_pattern(skill: str) -> str:
    escaped = re.escape(skill.lower())
    escaped = escaped.replace(r"\ ", r"[\s\-]+")
    return rf"(?<![\w+#]){escaped}(?![\w+#])"
