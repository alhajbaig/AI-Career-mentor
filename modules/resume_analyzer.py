"""
AI Career Mentor - Resume Analyzer
Extracts skills, education, certifications from uploaded resumes.
Provides resume scoring and analysis.
"""

import re
import os
from collections import Counter

# Try importing PDF libraries
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

from modules.config import SKILL_SYNONYMS, CAREER_SKILLS

# ─── Master Skill List ───────────────────────────────────────────────────────
MASTER_SKILLS = set()
for career_data in CAREER_SKILLS.values():
    MASTER_SKILLS.update(s.lower() for s in career_data["core"])
    MASTER_SKILLS.update(s.lower() for s in career_data["optional"])

# Add more common skills
EXTRA_SKILLS = {
    "python", "java", "javascript", "c++", "c", "c#", "ruby", "go", "rust",
    "swift", "kotlin", "php", "scala", "perl", "matlab", "r", "julia",
    "html", "css", "react", "angular", "vue", "node.js", "express",
    "django", "flask", "fastapi", "spring", "spring boot",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "plotly", "opencv", "nltk", "spacy",
    "hugging face", "transformers", "langchain",
    "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra",
    "elasticsearch", "neo4j", "dynamodb", "firebase",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "jenkins", "github actions", "gitlab ci", "circleci",
    "linux", "bash", "powershell", "git", "jira", "confluence",
    "tableau", "power bi", "looker", "excel",
    "machine learning", "deep learning", "nlp", "computer vision",
    "data science", "data analysis", "data engineering",
    "rest api", "graphql", "grpc", "websocket",
    "agile", "scrum", "kanban", "devops", "ci/cd", "mlops",
    "hadoop", "spark", "kafka", "airflow", "dbt",
    "figma", "photoshop", "illustrator",
    "solidity", "ethereum", "web3",
    "selenium", "pytest", "junit", "cypress",
    "networking", "tcp/ip", "dns", "http",
    "data structures", "algorithms", "system design", "oop",
    "microservices", "serverless", "api gateway",
}
MASTER_SKILLS.update(EXTRA_SKILLS)


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from uploaded PDF file."""
    text = ""

    if HAS_PDFPLUMBER:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception:
            pass

    if HAS_PYMUPDF:
        try:
            uploaded_file.seek(0)
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            if text.strip():
                return text
        except Exception:
            pass

    return text


def extract_skills(text: str) -> list:
    """Extract skills from text using pattern matching."""
    text_lower = text.lower()
    found_skills = set()

    # Direct match against master skills
    for skill in MASTER_SKILLS:
        # Word boundary matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            # Normalize via synonyms
            normalized = SKILL_SYNONYMS.get(skill, skill.title())
            found_skills.add(normalized)

    # Check for synonym matches
    for synonym, canonical in SKILL_SYNONYMS.items():
        pattern = r'\b' + re.escape(synonym) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(canonical)

    return sorted(list(found_skills))


def extract_education(text: str) -> list:
    """Extract education details from resume text."""
    education = []
    degree_patterns = [
        r"(B\.?Tech|B\.?E\.?|Bachelor(?:'s)?)\s*(?:in|of)?\s*([\w\s&]+?)(?:\n|,|\d)",
        r"(M\.?Tech|M\.?S\.?|Master(?:'s)?)\s*(?:in|of)?\s*([\w\s&]+?)(?:\n|,|\d)",
        r"(Ph\.?D\.?|Doctorate)\s*(?:in|of)?\s*([\w\s&]+?)(?:\n|,|\d)",
        r"(MBA|MCA|BCA|BBA|BSc|MSc)\s*(?:in|of)?\s*([\w\s&]*?)(?:\n|,|\d)",
        r"(B\.?Tech|BE|BTech|M\.?Tech|MTech|MBA|BCA|MCA|BSc|MSc|PhD)",
    ]
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                degree = " ".join(match).strip()
            else:
                degree = match.strip()
            if degree and len(degree) > 2:
                education.append(degree)

    return list(set(education))[:5]


def extract_certifications(text: str) -> list:
    """Extract certifications from resume text."""
    cert_patterns = [
        r"(AWS\s+Certified[\w\s\-]+)",
        r"(Google\s+Cloud[\w\s\-]+)",
        r"(Azure[\w\s\-]+(?:Certified|Associate|Expert))",
        r"(Certified\s+[\w\s\-]+(?:Professional|Associate|Engineer|Developer))",
        r"(TensorFlow\s+Developer\s+Certificate)",
        r"(Deep Learning\s+Specialization)",
        r"(Machine Learning\s+Specialization)",
        r"(PMP|CISSP|CEH|CCNA|CCNP|CKA|CKAD|CompTIA[\w\s\+]+)",
    ]
    certs = []
    for pattern in cert_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        certs.extend([m.strip() for m in matches])

    return list(set(certs))[:10]


def extract_experience_years(text: str) -> float:
    """Estimate years of experience from resume."""
    patterns = [
        r"(\d+)\+?\s*years?\s*(?:of)?\s*experience",
        r"experience\s*[:]\s*(\d+)\+?\s*years?",
        r"(\d+)\+?\s*years?\s*(?:of)?\s*(?:professional|work|industry)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return 0.0


def extract_projects_count(text: str) -> int:
    """Estimate number of projects from resume."""
    project_headers = re.findall(
        r"(?:project|projects)\s*(?:\d|:|\n|–|-)", text, re.IGNORECASE
    )
    project_bullets = re.findall(
        r"(?:•|▪|◦|►|→|-)\s*(?:Built|Developed|Created|Designed|Implemented|Deployed)",
        text, re.IGNORECASE
    )
    return max(len(project_headers), len(project_bullets), 0)


def calculate_resume_score(text: str, skills: list, education: list,
                           certifications: list, target_career: str = None) -> dict:
    """Calculate comprehensive resume score."""
    scores = {}

    # Skills score (30 points)
    skill_count = len(skills)
    if skill_count >= 15:
        scores["skills"] = 30
    elif skill_count >= 10:
        scores["skills"] = 25
    elif skill_count >= 5:
        scores["skills"] = 18
    elif skill_count >= 3:
        scores["skills"] = 12
    else:
        scores["skills"] = 5

    # Education score (20 points)
    edu_score = min(len(education) * 10, 20)
    scores["education"] = max(edu_score, 5)

    # Certifications (15 points)
    cert_score = min(len(certifications) * 5, 15)
    scores["certifications"] = cert_score

    # Experience (15 points)
    years = extract_experience_years(text)
    if years >= 5:
        scores["experience"] = 15
    elif years >= 3:
        scores["experience"] = 12
    elif years >= 1:
        scores["experience"] = 8
    else:
        scores["experience"] = 3

    # Projects (10 points)
    projects = extract_projects_count(text)
    if projects >= 5:
        scores["projects"] = 10
    elif projects >= 3:
        scores["projects"] = 7
    elif projects >= 1:
        scores["projects"] = 4
    else:
        scores["projects"] = 1

    # Formatting/Length (10 points)
    word_count = len(text.split())
    if 300 <= word_count <= 1200:
        scores["formatting"] = 10
    elif 200 <= word_count <= 1500:
        scores["formatting"] = 7
    else:
        scores["formatting"] = 4
    total = sum(scores.values())
    scores["total"] = total

    return scores


def extract_email(text: str) -> str:
    """Extract email from resume text."""
    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    match = re.search(pattern, text)
    return match.group(0) if match else ""

def extract_name(text: str) -> str:
    """Extract candidate name from resume text (usually the first non-empty line)."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        candidate = lines[0]
        words = candidate.split()
        if len(words) <= 4 and all(word[0].isupper() for word in words if word.isalpha()):
            return candidate
    return ""

def extract_bio(text: str) -> str:
    """Extract summary/objective from resume text."""
    headers = [r"summary", r"objective", r"profile", r"about me"]
    text_lower = text.lower()
    for header in headers:
        match = re.search(r'\b' + header + r'\b', text_lower)
        if match:
            start_idx = match.end()
            subset = text[start_idx:start_idx+350].strip()
            parts = re.split(r'\n\n|\n[A-Z\s]{4,}\b', subset)
            if parts:
                return parts[0].strip().replace("\n", " ")
    return ""


def extract_details_with_llm(text: str) -> dict:
    """Extract structured details from resume text using Groq LLM."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {}
        
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        prompt = f"""
        Extract the following details from this resume text as a JSON object:
        - name: Full name of candidate. If not found, return "".
        - email: Candidate email. If not found, return "".
        - bio: A professional bio or summary statement (2-3 sentences max). If not found, create a brief, engaging summary based on their background.
        - branch: The closest academic field or branch from: ["Computer Science", "Information Technology", "Electronics & Comm", "Data Science", "Mechanical", "Electrical", "Civil", "Business Administration"]. If not found, match the closest one or leave blank.
        - cgpa: A float representing CGPA (out of 10.0 or 100). If not found, return 8.5.
        - target_career: The closest matching career field.
        
        Resume Text:
        ---
        {text[:4000]}
        ---
        
        Return ONLY valid JSON. Do not include markdown wraps like ```json.
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a precise data extraction system that returns only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        import json
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"LLM extraction error: {e}")
        return {}


def analyze_resume(uploaded_file) -> dict:
    """Complete resume analysis pipeline."""
    text = extract_text_from_pdf(uploaded_file)
    if not text.strip():
        return {"error": "Could not extract text from PDF. Please ensure it's not an image-based PDF."}

    skills = extract_skills(text)
    education = extract_education(text)
    certifications = extract_certifications(text)
    experience = extract_experience_years(text)
    projects = extract_projects_count(text)
    score = calculate_resume_score(text, skills, education, certifications)
    
    # Try LLM extraction first
    llm_details = extract_details_with_llm(text)
    
    name = llm_details.get("name") or extract_name(text)
    email = llm_details.get("email") or extract_email(text)
    bio = llm_details.get("bio") or extract_bio(text)
    branch = llm_details.get("branch")
    cgpa = llm_details.get("cgpa")
    target_career = llm_details.get("target_career")

    return {
        "text": text,
        "name": name,
        "email": email,
        "bio": bio,
        "branch": branch,
        "cgpa": cgpa,
        "target_career": target_career,
        "skills": skills,
        "education": education,
        "certifications": certifications,
        "experience_years": experience,
        "projects_count": projects,
        "score": score,
        "word_count": len(text.split()),
    }

