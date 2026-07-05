from app.services.cleaner import clean_text, normalize_skill, split_sections


def test_clean_text_removes_page_markers_and_extra_spaces():
    text = "Python     developer\n\n\nPage 1 of 2\nSQL"
    assert clean_text(text) == "Python developer\n\nSQL"


def test_normalize_skill_handles_common_uppercase_terms():
    assert normalize_skill("python") == "Python"
    assert normalize_skill("aws") == "AWS"
    assert normalize_skill("FASTAPI") == "FastAPI"


def test_split_sections_groups_known_headings():
    sections = split_sections("Skills\nPython\nExperience\n3 years")
    assert sections["Skills"] == ["Python"]
    assert sections["Experience"] == ["3 years"]
