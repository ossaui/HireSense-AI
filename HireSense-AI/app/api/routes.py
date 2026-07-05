from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.schemas import AnalysisResponse, ErrorResponse
from app.services.analysis import analyze_resumes
from app.services.skills import load_skill_catalog

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/skills/catalog")
def skills_catalog() -> dict[str, list[str]]:
    return load_skill_catalog()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={400: {"model": ErrorResponse}},
)
async def analyze(
    job_description: str = Form(...),
    job_title: str = Form("Untitled Role"),
    resumes: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    if not resumes:
        raise HTTPException(status_code=400, detail="At least one resume file is required.")

    resume_payloads = []
    for resume in resumes:
        content = await resume.read()
        if not content:
            raise HTTPException(status_code=400, detail=f"{resume.filename} is empty.")
        resume_payloads.append((resume.filename or "resume", content))

    return analyze_resumes(
        resume_payloads=resume_payloads,
        job_description=job_description,
        job_title=job_title,
        db=db,
    )
