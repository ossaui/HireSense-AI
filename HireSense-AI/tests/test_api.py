from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_endpoint_accepts_text_resume():
    client = TestClient(app)
    resume_text = (
        "Ambar Gurav\nambar@example.com\nSkills\nPython\nSQL\nDocker\nFastAPI\n"
        "Experience\n3 years Python developer\nEducation\nBachelor of Engineering\n"
        "Projects\nResume ranking system\nCertifications\nAWS Certified"
    )

    response = client.post(
        "/analyze",
        data={
            "job_title": "AI Engineer",
            "job_description": "Need Python SQL Docker FastAPI. 3 years experience. Bachelor degree.",
        },
        files={"resumes": ("resume.txt", resume_text.encode("utf-8"), "text/plain")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["candidates"][0]["rank"] == 1
    assert data["candidates"][0]["candidate"]["name"] == "Ambar Gurav"
    assert "Python" in data["candidates"][0]["matched_skills"]
