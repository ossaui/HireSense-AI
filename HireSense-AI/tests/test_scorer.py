from app.models.schemas import JobProfile, ResumeProfile
from app.services.scorer import score_candidate


def test_score_candidate_uses_weighted_formula():
    resume = ResumeProfile(
        name="Ambar Gurav",
        skills=["Python", "SQL", "Docker"],
        education=["Bachelor of Engineering"],
        experience=["3 years Python developer"],
        projects=["Resume matcher"],
        certifications=["AWS Certified"],
        raw_text="Skills Python SQL Docker Experience 3 years Education Bachelor Projects Certifications",
    )
    job = JobProfile(
        title="AI Engineer",
        required_skills=["Python", "SQL", "Docker", "AWS"],
        education=["Bachelor"],
        min_years_experience=3,
        raw_text="Need Python SQL Docker AWS 3 years Bachelor",
    )

    score = score_candidate(resume, job, ["Python", "SQL", "Docker"], semantic_score=80)

    assert score.skills_match == 75
    assert score.experience == 100
    assert score.education == 100
    assert score.final_score > 80
