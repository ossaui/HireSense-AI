from __future__ import annotations

import io
import re
from pathlib import Path

from docx import Document

from app.models.schemas import ResumeProfile
from app.services.cleaner import clean_text, split_sections
from app.services.skills import extract_skills

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")


def parse_resume_file(filename: str, content: bytes) -> ResumeProfile:
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        raw_text = _extract_pdf_text(content)
    elif suffix == ".docx":
        raw_text = _extract_docx_text(content)
    else:
        raw_text = content.decode("utf-8", errors="ignore")

    text = clean_text(raw_text)
    sections = split_sections(text)
    email = _first_match(EMAIL_RE, text)
    phone = _first_match(PHONE_RE, text)
    name = _extract_name(text, email)
    skills = extract_skills(text)

    return ResumeProfile(
        name=name,
        email=email,
        phone=phone,
        education=sections.get("Education", []),
        skills=skills,
        experience=sections.get("Experience", []),
        projects=sections.get("Projects", []),
        certifications=sections.get("Certifications", []),
        raw_text=text,
    )


def _extract_pdf_text(content: bytes) -> str:
    try:
        import fitz

        with fitz.open(stream=content, filetype="pdf") as document:
            return "\n".join(page.get_text("text") for page in document)
    except Exception:
        import pdfplumber

        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)


def _extract_docx_text(content: bytes) -> str:
    document = Document(io.BytesIO(content))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(0).strip() if match else None


def _extract_name(text: str, email: str | None) -> str:
    for line in text.splitlines()[:8]:
        line = line.strip()
        if not line or EMAIL_RE.search(line) or PHONE_RE.search(line):
            continue
        if len(line.split()) <= 5 and not any(char.isdigit() for char in line):
            return line
    return email.split("@")[0].replace(".", " ").title() if email else "Unknown Candidate"
