"""
AI Career Mentor - Skill Engine
Handles skill gap analysis, job matching, and career readiness scoring.
"""

from modules.config import CAREER_SKILLS, SKILL_SYNONYMS


def normalize_skill(skill: str) -> str:
    """Normalize a skill name using synonyms."""
    lower = skill.lower().strip()
    return SKILL_SYNONYMS.get(lower, skill.strip().title())


def normalize_skills(skills: list) -> list:
    """Normalize a list of skills."""
    normalized = set()
    for s in skills:
        normalized.add(normalize_skill(s))
    return sorted(list(normalized))


def get_skill_gap(current_skills: list, target_career: str) -> dict:
    """
    Analyze skill gaps for a target career.
    Returns matched, missing, and optional skills.
    """
    career_data = CAREER_SKILLS.get(target_career, {})
    if not career_data:
        # Try fuzzy match
        for career, data in CAREER_SKILLS.items():
            if target_career.lower() in career.lower():
                career_data = data
                target_career = career
                break

    if not career_data:
        return {"matched": [], "missing": [], "optional": [], "coverage": 0}

    required = set(s.lower() for s in career_data.get("core", []))
    optional = set(s.lower() for s in career_data.get("optional", []))
    current = set(normalize_skill(s).lower() for s in current_skills)

    matched = required.intersection(current)
    missing = required - current
    optional_matched = optional.intersection(current)
    optional_missing = optional - current

    coverage = (len(matched) / len(required) * 100) if required else 0

    return {
        "target_career": target_career,
        "matched": sorted([s.title() for s in matched]),
        "missing": sorted([s.title() for s in missing]),
        "optional_have": sorted([s.title() for s in optional_matched]),
        "optional_missing": sorted([s.title() for s in optional_missing]),
        "coverage": round(coverage, 1),
        "total_required": len(required),
        "total_matched": len(matched),
    }


def calculate_job_match(user_skills: list, job_skills: list) -> dict:
    """
    Calculate match score between user skills and job requirements.
    """
    user_set = set(normalize_skill(s).lower() for s in user_skills)
    job_set = set(normalize_skill(s).lower() for s in job_skills)

    matched = user_set.intersection(job_set)
    missing = job_set - user_set
    extra = user_set - job_set

    match_pct = (len(matched) / len(job_set) * 100) if job_set else 0

    return {
        "match_score": round(match_pct, 1),
        "matched_skills": sorted([s.title() for s in matched]),
        "missing_skills": sorted([s.title() for s in missing]),
        "extra_skills": sorted([s.title() for s in extra]),
        "total_required": len(job_set),
        "total_matched": len(matched),
    }


def calculate_readiness_score(
    skills: list,
    target_career: str,
    resume_score: int = 0,
    certifications: list = None,
    projects_count: int = 0,
    experience_years: float = 0
) -> dict:
    """
    Calculate overall career readiness score (0-100).
    Based on: Skills (40%), Resume (20%), Certifications (15%),
    Projects (15%), Experience (10%).
    """
    certifications = certifications or []

    # Skill coverage score (40 points max)
    gap = get_skill_gap(skills, target_career)
    skill_score = (gap["coverage"] / 100) * 40

    # Resume score (20 points max)
    resume_pts = min((resume_score / 100) * 20, 20)

    # Certifications (15 points max)
    cert_pts = min(len(certifications) * 5, 15)

    # Projects (15 points max)
    if projects_count >= 5:
        project_pts = 15
    elif projects_count >= 3:
        project_pts = 10
    elif projects_count >= 1:
        project_pts = 6
    else:
        project_pts = 0

    # Experience (10 points max)
    if experience_years >= 3:
        exp_pts = 10
    elif experience_years >= 1:
        exp_pts = 6
    elif experience_years >= 0.5:
        exp_pts = 3
    else:
        exp_pts = 0

    total = skill_score + resume_pts + cert_pts + project_pts + exp_pts

    return {
        "total": round(total),
        "skill_score": round(skill_score),
        "resume_score": round(resume_pts),
        "certification_score": round(cert_pts),
        "project_score": round(project_pts),
        "experience_score": round(exp_pts),
        "breakdown": {
            "Skills": {"score": round(skill_score), "max": 40},
            "Resume": {"score": round(resume_pts), "max": 20},
            "Certifications": {"score": round(cert_pts), "max": 15},
            "Projects": {"score": round(project_pts), "max": 15},
            "Experience": {"score": round(exp_pts), "max": 10},
        },
        "level": _get_readiness_level(total),
    }


def _get_readiness_level(score: float) -> str:
    """Get readiness level label."""
    if score >= 85:
        return "🌟 Excellent - You're job ready!"
    elif score >= 70:
        return "✅ Good - Almost there, minor gaps"
    elif score >= 50:
        return "⚡ Moderate - Focused effort needed"
    elif score >= 30:
        return "🔄 Developing - Keep building skills"
    else:
        return "🚀 Starting Out - Begin your journey!"


def get_career_match_scores(user_skills: list) -> list:
    """Get match scores for all defined careers."""
    results = []
    for career, data in CAREER_SKILLS.items():
        match = calculate_job_match(user_skills, data["core"])
        results.append({
            "career": career,
            "icon": data.get("icon", "💼"),
            "match_score": match["match_score"],
            "matched": match["matched_skills"],
            "missing": match["missing_skills"],
        })
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
