from collections import Counter

from sqlalchemy.orm import Session

from app.models.database_models import Candidate, CandidateSkill, Job, Match, Resume
from app.models.schemas import AnalysisResponse, CandidateAnalysis
from app.services.explainability import build_explanation
from app.services.job_parser import parse_job_description
from app.services.matcher import SemanticMatcher
from app.services.parser import parse_resume_file
from app.services.reports import generate_interview_questions, generate_recruiter_report
from app.services.scorer import score_candidate
from app.services.skills import categorize_skills


def analyze_resumes(
    resume_payloads: list[tuple[str, bytes]],
    job_description: str,
    job_title: str,
    db: Session | None = None,
) -> AnalysisResponse:
    job = parse_job_description(job_title, job_description)
    matcher = SemanticMatcher()
    analyses: list[CandidateAnalysis] = []
    all_missing: list[str] = []

    db_job = _save_job(db, job.title, job.raw_text)

    for filename, content in resume_payloads:
        resume = parse_resume_file(filename, content)
        required = set(job.required_skills)
        resume_skills = set(resume.skills)
        matched = sorted(required.intersection(resume_skills))
        missing = sorted(required.difference(resume_skills))
        all_missing.extend(missing)

        semantic_score = matcher.score(resume.raw_text, job.raw_text)
        score = score_candidate(resume, job, matched, semantic_score)
        explanation = build_explanation(resume, job, matched, missing, score)
        questions = generate_interview_questions(matched, missing)
        report = generate_recruiter_report(resume, job, matched, missing, score)

        analysis = CandidateAnalysis(
            rank=0,
            filename=filename,
            candidate=resume,
            matched_skills=matched,
            missing_skills=missing,
            skill_coverage=round((len(matched) / len(required) * 100) if required else 100.0, 2),
            score=score,
            explanation=explanation,
            interview_questions=questions,
            recruiter_report=report,
        )
        analyses.append(analysis)
        _save_candidate_analysis(db, db_job, analysis)

    analyses.sort(key=lambda item: item.score.final_score, reverse=True)
    for index, analysis in enumerate(analyses, start=1):
        analysis.rank = index

    average_score = round(
        sum(item.score.final_score for item in analyses) / len(analyses),
        2,
    )
    top_missing = [skill for skill, _ in Counter(all_missing).most_common(10)]

    if db is not None:
        db.commit()

    return AnalysisResponse(
        job=job,
        candidates=analyses,
        top_missing_skills=top_missing,
        average_score=average_score,
    )


def _save_job(db: Session | None, title: str, description: str) -> Job | None:
    if db is None:
        return None
    job = Job(title=title, description=description)
    db.add(job)
    db.flush()
    return job


def _save_candidate_analysis(db: Session | None, job: Job | None, analysis: CandidateAnalysis) -> None:
    if db is None or job is None:
        return

    candidate = Candidate(
        name=analysis.candidate.name,
        email=analysis.candidate.email,
        phone=analysis.candidate.phone,
    )
    db.add(candidate)
    db.flush()

    resume = Resume(
        candidate_id=candidate.id,
        filename=analysis.filename,
        resume_text=analysis.candidate.raw_text,
    )
    db.add(resume)
    db.flush()

    db.add(
        Match(
            resume_id=resume.id,
            job_id=job.id,
            score=analysis.score.final_score,
            semantic_score=analysis.score.semantic_score,
            explanation="\n".join(analysis.explanation),
        )
    )

    categorized = categorize_skills(analysis.candidate.skills)
    for category, skills in categorized.items():
        for skill in skills:
            db.add(CandidateSkill(candidate_id=candidate.id, skill_name=skill, category=category))
