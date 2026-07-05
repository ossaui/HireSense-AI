import os

import altair as alt
import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("HIRESENSE_API_URL", "http://localhost:8000")

st.set_page_config(page_title="HireSense AI", layout="wide")

st.title("HireSense AI")
st.caption("Resume screening, candidate ranking, and recruiter reports.")

with st.sidebar:
    st.header("Job Description")
    job_title = st.text_input("Role title", value="AI/ML Intern")
    job_description = st.text_area(
        "Paste job description",
        height=260,
        value=(
            "Need Python, SQL, Docker, FastAPI, Scikit-learn and NLP experience. "
            "3 years experience preferred. Bachelor degree in computer science or engineering."
        ),
    )
    uploaded_resumes = st.file_uploader(
        "Upload resumes",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
    )
    analyze = st.button("Analyze candidates", type="primary", use_container_width=True)


def call_api():
    files = [
        ("resumes", (resume.name, resume.getvalue(), resume.type or "application/octet-stream"))
        for resume in uploaded_resumes
    ]
    response = requests.post(
        f"{API_URL}/analyze",
        data={"job_title": job_title, "job_description": job_description},
        files=files,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


if analyze:
    if not uploaded_resumes:
        st.error("Upload at least one resume.")
    elif not job_description.strip():
        st.error("Paste a job description.")
    else:
        with st.spinner("Analyzing resumes..."):
            try:
                st.session_state["analysis"] = call_api()
            except requests.RequestException as exc:
                st.error(f"Could not analyze resumes: {exc}")

analysis = st.session_state.get("analysis")

if not analysis:
    st.info("Upload resumes and paste a job description to begin.")
    st.stop()

candidates = analysis["candidates"]
summary_df = pd.DataFrame(
    [
        {
            "Rank": item["rank"],
            "Candidate": item["candidate"]["name"],
            "Score": item["score"]["final_score"],
            "Semantic": item["score"]["semantic_score"],
            "Coverage": item["skill_coverage"],
            "Matched": len(item["matched_skills"]),
            "Missing": len(item["missing_skills"]),
        }
        for item in candidates
    ]
)

metric_cols = st.columns(3)
metric_cols[0].metric("Candidates", len(candidates))
metric_cols[1].metric("Average score", analysis["average_score"])
metric_cols[2].metric("Top candidate", candidates[0]["candidate"]["name"])

st.subheader("Candidate Ranking")
st.dataframe(summary_df, use_container_width=True, hide_index=True)

chart = (
    alt.Chart(summary_df)
    .mark_bar()
    .encode(
        x=alt.X("Score:Q", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("Candidate:N", sort="-x"),
        color=alt.Color("Coverage:Q", scale=alt.Scale(scheme="tealblues")),
        tooltip=["Candidate", "Score", "Semantic", "Coverage"],
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)

left, right = st.columns([2, 1])

with left:
    st.subheader("Candidate Details")
    for item in candidates:
        with st.expander(f"#{item['rank']} {item['candidate']['name']} - {item['score']['final_score']}/100"):
            st.write(item["recruiter_report"])

            detail_cols = st.columns(2)
            detail_cols[0].markdown("**Matched skills**")
            detail_cols[0].write(", ".join(item["matched_skills"]) or "None detected")
            detail_cols[1].markdown("**Missing skills**")
            detail_cols[1].write(", ".join(item["missing_skills"]) or "None")

            st.markdown("**Score breakdown**")
            breakdown = {
                key: value
                for key, value in item["score"].items()
                if key not in {"final_score"}
            }
            st.dataframe(pd.DataFrame([breakdown]), use_container_width=True, hide_index=True)

            st.markdown("**Why this score**")
            for reason in item["explanation"]:
                st.write(reason)

            st.markdown("**Interview questions**")
            for question in item["interview_questions"]:
                st.write(f"- {question}")

with right:
    st.subheader("Skill Gaps")
    missing = analysis["top_missing_skills"]
    if missing:
        st.write(", ".join(missing))
    else:
        st.success("No repeated required skill gaps found.")
