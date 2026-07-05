from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str


class ResumeProfile(BaseModel):
    name: str = "Unknown Candidate"
    email: str | None = None
    phone: str | None = None
    education: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    raw_text: str = ""


class JobProfile(BaseModel):
    title: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    min_years_experience: int = 0
    raw_text: str


class ScoreBreakdown(BaseModel):
    skills_match: float
    experience: float
    education: float
    projects: float
    formatting: float
    certifications: float
    weighted_total: float
    semantic_score: float
    final_score: float


class CandidateAnalysis(BaseModel):
    rank: int
    filename: str
    candidate: ResumeProfile
    matched_skills: list[str]
    missing_skills: list[str]
    skill_coverage: float
    score: ScoreBreakdown
    explanation: list[str]
    interview_questions: list[str]
    recruiter_report: str


class AnalysisResponse(BaseModel):
    job: JobProfile
    candidates: list[CandidateAnalysis]
    top_missing_skills: list[str]
    average_score: float
