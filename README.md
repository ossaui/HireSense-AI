# 🚀 HireSense AI

> **AI-Powered Resume Screening & Candidate Ranking Platform**

HireSense AI is an intelligent recruitment platform that helps recruiters automate resume screening using Artificial Intelligence. It extracts candidate information, compares resumes with job descriptions, calculates semantic match scores, identifies skill gaps, ranks applicants, and generates AI-powered hiring insights and interview questions.

---

## 🎥 Demo

<p align="center">
  <img src="assets/demo.gif" alt="HireSense AI Demo" width="95%">
</p>


### 🌐 Live Application

**Frontend**

https://hiresense-ai-4r3pcjrfsdfrgkp7t5hnpw.streamlit.app/

**Backend API**

https://hiresense-ai-2-kyaw.onrender.com/docs

---

# 📸 Screenshots

| Dashboard | Candidate Analysis |
|-----------|--------------------|
| ![](assets/dashboard.png) | ![](assets/analysis.png) |

| Resume Ranking | Interview Questions |
|----------------|---------------------|
| ![](assets/ranking.png) | ![](assets/questions.png) |

---

# ✨ Features

### 📄 Resume Parsing

- Extracts candidate information
- Supports PDF, DOCX and TXT resumes
- Automatically detects
  - Skills
  - Education
  - Experience
  - Contact Details

---

### 🎯 Intelligent Candidate Matching

- Job Description Analysis
- Semantic Resume Matching
- AI Match Score
- Skill Gap Analysis
- Resume Ranking

---

### 🤖 AI Recruiter Assistant

- Candidate Summary
- Resume Strength Analysis
- Weakness Detection
- Hiring Recommendation
- Interview Question Generation

---

### 📊 Recruiter Dashboard

- Candidate Rankings
- Resume Insights
- Skill Comparison
- Hiring Analytics

---

# 🏗 System Workflow

```text
                Resume Upload
                      │
                      ▼
             Resume Parsing Engine
                      │
                      ▼
         Candidate Information Extraction
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
 Job Description            Skill Extraction
      Analysis
         │                         │
         └────────────┬────────────┘
                      ▼
             Match Score Engine
                      ▼
            AI Explanation Engine
                      ▼
      Interview Question Generator
                      ▼
          Recruiter Dashboard
```

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| AI | Google Gemini |
| NLP | spaCy, Sentence Transformers |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Resume Parsing | PyMuPDF, pdfplumber |
| Deployment | Render, Streamlit Cloud |

---

# ⚙️ Project Structure

```text
HireSense-AI
│
├── backend/
│
├── frontend/
│
├── assets/
│
├── docs/
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/ossaui/HireSense-AI.git
```

Move into the project

```bash
cd HireSense-AI
```

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Backend

```bash
uvicorn app.main:app --reload
```

Run Frontend

```bash
streamlit run streamlit_app.py
```

---

# 📈 How It Works

1. Upload one or multiple resumes.
2. Enter a job description.
3. Resume information is extracted.
4. Skills are identified.
5. Semantic similarity is calculated.
6. Match scores are generated.
7. Missing skills are detected.
8. AI explains candidate suitability.
9. Recruiters receive ranked applicants.
10. AI generates interview questions.

---

# 🎯 Use Cases

- AI Resume Screening
- Applicant Tracking Assistance
- Campus Hiring
- Talent Acquisition
- Recruitment Automation
- Resume Ranking
- HR Analytics

---

# 🔮 Future Improvements

- Multi-resume Batch Processing
- Resume Embeddings
- Vector Database Search
- RAG-based Candidate Search
- Authentication System
- Docker Deployment
- CI/CD Pipeline
- Recruiter Analytics Dashboard
- ATS Resume Optimizer

---

# 🤝 Contributing

Contributions are welcome.

1. Fork this repository
2. Create your feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Ambar**

Data Science | Machine Learning | Artificial Intelligence

GitHub

https://github.com/ossaui

---

## ⭐ If you found this project helpful, please consider giving it a Star!
