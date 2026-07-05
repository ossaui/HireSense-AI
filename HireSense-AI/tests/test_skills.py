from app.services.skills import extract_skills


def test_extract_skills_detects_catalog_terms():
    text = "Built FastAPI services with Python, SQL, Docker, AWS, and Scikit-learn."
    skills = extract_skills(text)
    assert "Python" in skills
    assert "SQL" in skills
    assert "Docker" in skills
    assert "AWS" in skills
    assert "FastAPI" in skills
    assert "Scikit-learn" in skills
