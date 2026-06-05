"""
AI Career Mentor - Main Streamlit Application
A premium, feature-rich, and interactive career guidance platform.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import json
from streamlit_option_menu import option_menu

# Set Page Config first
st.set_page_config(
    page_title="AI Career Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize/Retrieve Groq API Key from environment, streamlit secrets, or session state
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = os.environ.get("GROQ_API_KEY", "")
    if not st.session_state.groq_api_key:
        try:
            st.session_state.groq_api_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            pass

GROQ_API_KEY = st.session_state.groq_api_key
if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Import Modules
from modules.styles import get_custom_css
from modules.ui_components import (
    render_metric_card,
    render_skill_tags,
    render_progress_bar,
    render_score_gauge,
    render_career_bar_chart,
    render_readiness_radar,
    render_phase_card
)
from modules.ml_engine import CareerPredictor
from modules.resume_analyzer import analyze_resume
from modules.skill_engine import (
    get_skill_gap,
    calculate_job_match,
    calculate_readiness_score,
    get_career_match_scores
)
from modules.roadmap_generator import get_roadmap, create_roadmap_visualization, create_skill_network
from modules.ai_mentor import chat_with_mentor, generate_interview_questions
from modules.config import CAREER_SKILLS, PROJECT_RECOMMENDATIONS, COURSE_RECOMMENDATIONS, INTERVIEW_QUESTIONS

# Inject Styles
st.markdown(get_custom_css(), unsafe_allow_html=True)

def sync_profile_states():
    ALL_PRESET_SKILLS = sorted(list(set([skill for career in CAREER_SKILLS.values() for skill in career["core"] + career["optional"]])))
    PRESET_INTERESTS = sorted(list(set(["AI", "Data Science", "Machine Learning", "Cloud Computing", "Cybersecurity", "Blockchain", "Web Development", "Mobile Apps", "DevOps", "Database Systems", "UI/UX Design", "Product Management", "Software Engineering"])))
    
    st.session_state.selected_preset_skills = [s for s in st.session_state.skills if s in ALL_PRESET_SKILLS]
    st.session_state.custom_skills_input = ", ".join([s for s in st.session_state.skills if s not in ALL_PRESET_SKILLS])
    st.session_state.selected_preset_interests = [i for i in st.session_state.interests if i in PRESET_INTERESTS]
    st.session_state.custom_interests_input = ", ".join([i for i in st.session_state.interests if i not in PRESET_INTERESTS])

# Initialize Session States
if "name" not in st.session_state:
    st.session_state.name = "Alex"
if "email" not in st.session_state:
    st.session_state.email = "alex@example.com"
if "bio" not in st.session_state:
    st.session_state.bio = "Aspiring Data Scientist passionate about artificial intelligence, data pipelines, and machine learning models."
if "skills" not in st.session_state:
    st.session_state.skills = ["Python", "SQL", "Machine Learning", "Pandas", "NumPy", "Git", "Data Visualization"]
if "interests" not in st.session_state:
    st.session_state.interests = ["AI", "Data Science", "Machine Learning"]

# Initialize UI-bound states
ALL_PRESET_SKILLS = sorted(list(set([skill for career in CAREER_SKILLS.values() for skill in career["core"] + career["optional"]])))
PRESET_INTERESTS = sorted(list(set(["AI", "Data Science", "Machine Learning", "Cloud Computing", "Cybersecurity", "Blockchain", "Web Development", "Mobile Apps", "DevOps", "Database Systems", "UI/UX Design", "Product Management", "Software Engineering"])))

if "selected_preset_skills" not in st.session_state:
    st.session_state.selected_preset_skills = [s for s in st.session_state.skills if s in ALL_PRESET_SKILLS]
if "custom_skills_input" not in st.session_state:
    st.session_state.custom_skills_input = ", ".join([s for s in st.session_state.skills if s not in ALL_PRESET_SKILLS])
if "selected_preset_interests" not in st.session_state:
    st.session_state.selected_preset_interests = [i for i in st.session_state.interests if i in PRESET_INTERESTS]
if "custom_interests_input" not in st.session_state:
    st.session_state.custom_interests_input = ", ".join([i for i in st.session_state.interests if i not in PRESET_INTERESTS])
if "branch" not in st.session_state:
    st.session_state.branch = "Computer Science"
if "cgpa" not in st.session_state:
    st.session_state.cgpa = 8.5
if "certifications" not in st.session_state:
    st.session_state.certifications = []
if "resume_analyzed" not in st.session_state:
    st.session_state.resume_analyzed = False
if "resume_data" not in st.session_state:
    st.session_state.resume_data = {}
if "selected_career" not in st.session_state:
    st.session_state.selected_career = "Data Scientist"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "personality_scores" not in st.session_state:
    # Default scores biased toward tech/data careers
    st.session_state.personality_scores = {
        "O_score": 8.5,
        "C_score": 8.0,
        "E_score": 5.5,
        "A_score": 6.0,
        "N_score": 4.0,
        "Numerical Aptitude": 9.0,
        "Spatial Aptitude": 7.0,
        "Perceptual Aptitude": 7.0,
        "Abstract Reasoning": 9.0,
        "Verbal Reasoning": 7.5
    }
if "career_predictions" not in st.session_state:
    st.session_state.career_predictions = []
if "completed_skills" not in st.session_state:
    st.session_state.completed_skills = set()
if "quiz_step" not in st.session_state:
    st.session_state.quiz_step = 0
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# Initialize ML Predictor
@st.cache_resource
def get_predictor():
    return CareerPredictor()

predictor = get_predictor()

# ─── SIDEBAR NAVIGATION ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-top: 0.5rem;'>🎓 Career Mentor</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--text-muted); font-size: 0.82rem;'>AI-Powered Career Guidance & Roadmaps</p>", unsafe_allow_html=True)
    st.write("---")
    
    # API Key Input
    st.markdown("### 🔑 API Configuration")
    user_key = st.text_input(
        "Groq API Key",
        value=st.session_state.groq_api_key,
        type="password",
        help="Enter your Groq API Key. Get it from console.groq.com"
    )
    if user_key != st.session_state.groq_api_key:
        st.session_state.groq_api_key = user_key
        st.rerun()
        
    st.write("---")
    
    selected_page = option_menu(
        menu_title=None,
        options=["My Profile", "Dashboard", "Career Assessment", "Resume Analyzer", "Job Matching", "Interactive Roadmap", "AI Mentor Chatbot", "Interview Prep"],
        icons=["person", "speedometer2", "clipboard2-check", "file-earmark-person", "briefcase", "map", "chat-square-dots", "question-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#7C6FF7", "font-size": "1rem"},
            "nav-link": {"font-size": "0.88rem", "text-align": "left", "margin": "0px", "color": "#FAFAFA", "border-radius": "8px"},
            "nav-link-selected": {"background-color": "rgba(124, 111, 247, 0.12)", "border": "1px solid rgba(124, 111, 247, 0.25)"},
        }
    )
    
    st.write("---")
    st.markdown("### Active Profile")
    st.markdown(f"""
    <div class="profile-badge">
        <div class="profile-badge-name">🧑‍💼 {st.session_state.get('name', 'Alex')}</div>
        <div class="profile-badge-detail">
            <b>Branch:</b> {st.session_state.branch}<br/>
            <b>Target:</b> {st.session_state.selected_career}<br/>
            <b>Skills:</b> {len(st.session_state.skills)} active
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Reset State button
    if st.button("Reset Session Data", type="secondary"):
        st.session_state.name = "Alex"
        st.session_state.email = "alex@example.com"
        st.session_state.bio = "Aspiring Data Scientist passionate about artificial intelligence, data pipelines, and machine learning models."
        st.session_state.skills = ["Python", "SQL"]
        st.session_state.interests = ["AI", "Data Science"]
        st.session_state.branch = "Computer Science"
        st.session_state.cgpa = 8.5
        st.session_state.certifications = []
        st.session_state.resume_analyzed = False
        st.session_state.resume_data = {}
        st.session_state.chat_history = []
        st.session_state.completed_skills = set()
        st.success("Session reset successfully!")
        st.rerun()

# ─── MAIN PAGES ──────────────────────────────────────────────────────────────

# ─── PAGE 0: MY PROFILE ───────────────────────────────────────────────────────
if selected_page == "My Profile":
    st.markdown("<h1 class='page-title'>👤 My Professional Profile</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Define your background, skills, interests, and target career to customize your learning roadmaps and AI mentoring.</p>", unsafe_allow_html=True)
    
    # 1. Quick templates & fast-track resume uploader
    col_t1, col_t2 = st.columns([1.2, 1])
    with col_t1:
        with st.container(border=True):
            st.write("### 🚀 Quick Start: Load Example Profile")
            cols_tpl = st.columns(3)
            with cols_tpl[0]:
                if st.button("AI Engineer", use_container_width=True):
                    st.session_state.name = "Sarah Connor"
                    st.session_state.email = "sarah@sky.net"
                    st.session_state.branch = "Computer Science"
                    st.session_state.cgpa = 9.2
                    st.session_state.selected_career = "AI Engineer"
                    st.session_state.bio = "Passionate about building deep learning neural networks, natural language processors, and computer vision tools."
                    st.session_state.skills = ["Python", "PyTorch", "TensorFlow", "NLP", "Machine Learning", "Git"]
                    st.session_state.interests = ["AI", "Machine Learning", "Deep Learning"]
                    sync_profile_states()
                    st.session_state.career_predictions = predictor.get_top_careers(st.session_state.personality_scores, top_n=5)
                    st.success("Loaded AI Engineer template!")
                    st.rerun()
                    
            with cols_tpl[1]:
                if st.button("DevOps Junior", use_container_width=True):
                    st.session_state.name = "John Doe"
                    st.session_state.email = "john.doe@devops.org"
                    st.session_state.branch = "Information Technology"
                    st.session_state.cgpa = 8.1
                    st.session_state.selected_career = "DevOps Engineer"
                    st.session_state.bio = "Fascinated by containerization, orchestration, automation pipelines, and infrastructure as code."
                    st.session_state.skills = ["Linux", "Docker", "Git", "Kubernetes", "CI/CD", "AWS"]
                    st.session_state.interests = ["DevOps", "Cloud Computing"]
                    sync_profile_states()
                    st.session_state.career_predictions = predictor.get_top_careers(st.session_state.personality_scores, top_n=5)
                    st.success("Loaded DevOps template!")
                    st.rerun()
                    
            with cols_tpl[2]:
                if st.button("Data Analyst", use_container_width=True):
                    st.session_state.name = "Jane Smith"
                    st.session_state.email = "jane.smith@data.com"
                    st.session_state.branch = "Business Administration"
                    st.session_state.cgpa = 8.8
                    st.session_state.selected_career = "Data Analyst"
                    st.session_state.bio = "Focused on business intelligence, data manipulation, cleaning, and descriptive statistics."
                    st.session_state.skills = ["SQL", "Excel", "Tableau", "Power BI", "Python", "Data Visualization"]
                    st.session_state.interests = ["Data Science", "UI/UX Design"]
                    sync_profile_states()
                    st.session_state.career_predictions = predictor.get_top_careers(st.session_state.personality_scores, top_n=5)
                    st.success("Loaded Data Analyst template!")
                    st.rerun()

    with col_t2:
        with st.container(border=True):
            st.write("### 📄 Fast-track: Import from Resume")
            uploaded_profile_pdf = st.file_uploader("Upload PDF resume to auto-fill details:", type=["pdf"], key="profile_resume_uploader", label_visibility="collapsed")
            if uploaded_profile_pdf is not None:
                file_key = f"parsed_profile_resume_{uploaded_profile_pdf.name}_{uploaded_profile_pdf.size}"
                if st.session_state.get(file_key) is not True:
                    with st.spinner("Extracting details..."):
                        analysis = analyze_resume(uploaded_profile_pdf)
                        if "error" not in analysis:
                            st.session_state.resume_analyzed = True
                            st.session_state.resume_data = analysis
                            
                            # Auto-fill fields if extracted
                            if analysis.get("name"):
                                st.session_state.name = analysis["name"]
                            if analysis.get("email"):
                                st.session_state.email = analysis["email"]
                            if analysis.get("bio"):
                                st.session_state.bio = analysis["bio"]
                            if analysis.get("cgpa"):
                                try:
                                    st.session_state.cgpa = float(analysis["cgpa"])
                                except (ValueError, TypeError):
                                    pass
                            if analysis.get("branch"):
                                st.session_state.branch = analysis["branch"]
                            if analysis.get("target_career") and analysis["target_career"] in CAREER_SKILLS:
                                st.session_state.selected_career = analysis["target_career"]
                            
                            # Match branch if found in education and branch was not set
                            if not analysis.get("branch"):
                                edu_list = analysis.get("education", [])
                                if edu_list:
                                    branches = ["Computer Science", "Information Technology", "Electronics & Comm", "Data Science", "Mechanical", "Electrical", "Civil", "Business Administration"]
                                    for edu_str in edu_list:
                                        for br in branches:
                                            if br.lower() in edu_str.lower():
                                                st.session_state.branch = br
                                                break
                                            
                            extracted_skills = analysis.get("skills", [])
                            if extracted_skills:
                                st.session_state.skills = list(set(st.session_state.skills + extracted_skills))
                            
                            st.session_state.certifications = analysis.get("certifications", [])
                            sync_profile_states()
                            st.session_state[file_key] = True
                            st.success("Resume parsed successfully! Skills and profile data updated.")
                            st.rerun()
                        else:
                            st.error(analysis["error"])

    col_p_left, col_p_right = st.columns([1.5, 1])
    with col_p_left:
        with st.container(border=True):
            st.write("### Edit Profile Details")
            
            st.text_input("Full Name", key="name")
            st.text_input("Email Address", key="email")
            
            c_ed1, c_ed2 = st.columns(2)
            with c_ed1:
                st.selectbox(
                    "Academic Field / Branch", 
                    ["Computer Science", "Information Technology", "Electronics & Comm", "Data Science", "Mechanical", "Electrical", "Civil", "Business Administration"], 
                    key="branch"
                )
            with c_ed2:
                st.number_input("Current CGPA / Percentage", 1.0, 10.0, step=0.1, key="cgpa")
                
            st.selectbox(
                "Target Career / Role", 
                list(CAREER_SKILLS.keys()), 
                key="selected_career"
            )
            
            st.text_area("Short Bio", key="bio")
            
            # Load preset collections
            ALL_PRESET_SKILLS = sorted(list(set([skill for career in CAREER_SKILLS.values() for skill in career["core"] + career["optional"]])))
            PRESET_INTERESTS = sorted(list(set(["AI", "Data Science", "Machine Learning", "Cloud Computing", "Cybersecurity", "Blockchain", "Web Development", "Mobile Apps", "DevOps", "Database Systems", "UI/UX Design", "Product Management", "Software Engineering"])))
            
            st.write("---")
            st.write("### Manage Skills & Interests")
            
            st.multiselect("Select Core Skills", options=ALL_PRESET_SKILLS, key="selected_preset_skills")
            st.text_input("Other / Custom Skills (comma-separated)", key="custom_skills_input")
            
            st.multiselect("Select Interests", options=PRESET_INTERESTS, key="selected_preset_interests")
            st.text_input("Other / Custom Interests (comma-separated)", key="custom_interests_input")
            
            if st.button("Save Profile & Update Dashboard", use_container_width=True):
                # Combine preset + custom
                combined_skills = list(set(st.session_state.selected_preset_skills + [s.strip() for s in st.session_state.custom_skills_input.split(",") if s.strip()]))
                combined_interests = list(set(st.session_state.selected_preset_interests + [i.strip() for i in st.session_state.custom_interests_input.split(",") if i.strip()]))
                
                st.session_state.skills = combined_skills
                st.session_state.interests = combined_interests
                
                # Trigger predictions update
                st.session_state.career_predictions = predictor.get_top_careers(st.session_state.personality_scores, top_n=5)
                st.success("Profile saved successfully!")
                st.rerun()
            
    with col_p_right:
        with st.container(border=True):
            first_letter = st.session_state.get("name", "Alex")[0].upper() if st.session_state.get("name", "Alex") else "A"
            st.markdown(f"""
            <div style="width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #7C6FF7, #34D399); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 800; color: white; margin: 1.5rem auto 1.5rem; box-shadow: 0 4px 12px rgba(124, 111, 247, 0.25); border: 2px solid rgba(255, 255, 255, 0.1);">{first_letter}</div>
            <h3 style="text-align: center; margin-bottom: 0.2rem; margin-top: 0.5rem;">{st.session_state.get('name', 'Alex')}</h3>
            <p style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1rem;">{st.session_state.get('email', 'alex@example.com')}</p>
            <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5; font-style: italic; text-align: center; margin-bottom: 1.5rem;">"{st.session_state.get('bio', '')}"</p>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='profile-stat'><span class='profile-stat-key'>Branch</span><span class='profile-stat-val'>" + st.session_state.branch + "</span></div>", unsafe_allow_html=True)
            st.markdown("<div class='profile-stat'><span class='profile-stat-key'>CGPA</span><span class='profile-stat-val'>" + f"{st.session_state.cgpa:.2f}" + "</span></div>", unsafe_allow_html=True)
            st.markdown("<div class='profile-stat'><span class='profile-stat-key'>Target Role</span><span class='profile-stat-val'>" + st.session_state.selected_career + "</span></div>", unsafe_allow_html=True)
            st.markdown("<div class='profile-stat'><span class='profile-stat-key'>Skills Count</span><span class='profile-stat-val'>" + str(len(st.session_state.skills)) + "</span></div>", unsafe_allow_html=True)

# ─── PAGE 1: DASHBOARD ────────────────────────────────────────────────────────
elif selected_page == "Dashboard":
    st.markdown("<h1 class='page-title'>🚀 Career Readiness Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Get a comprehensive view of your predicted career options, resume strength, skill coverage, and roadmap progress.</p>", unsafe_allow_html=True)
    
    # Calculate initial predictions if not done
    if not st.session_state.career_predictions:
        st.session_state.career_predictions = predictor.get_top_careers(st.session_state.personality_scores, top_n=5)
    
    # Always compute skill-based career selection for display in target card
    TECH_CAREERS = list(CAREER_SKILLS.keys())
    skill_matches = get_career_match_scores(st.session_state.skills)
    if skill_matches and skill_matches[0]["match_score"] > 0:
        st.session_state.selected_career = skill_matches[0]["career"]
    elif st.session_state.selected_career not in TECH_CAREERS:
        st.session_state.selected_career = "Data Scientist"
    
    # Core Metrics Calculations
    gap_analysis = get_skill_gap(st.session_state.skills, st.session_state.selected_career)
    resume_score = st.session_state.resume_data.get("score", {}).get("total", 60) if st.session_state.resume_analyzed else 0
    
    readiness = calculate_readiness_score(
        skills=st.session_state.skills,
        target_career=st.session_state.selected_career,
        resume_score=resume_score,
        certifications=st.session_state.certifications,
        projects_count=st.session_state.resume_data.get("projects_count", 2) if st.session_state.resume_analyzed else 1,
        experience_years=st.session_state.resume_data.get("experience_years", 0) if st.session_state.resume_analyzed else 0
    )
    
    # Grid of Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        career_display = st.session_state.selected_career
        if len(career_display) > 16:
            career_display = career_display[:14] + "..."
        st.markdown(render_metric_card("🎯", career_display, "Target Career", "1"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card("📊", f"{readiness['total']}%", "Readiness Score", "2"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card("📄", f"{resume_score}/100" if st.session_state.resume_analyzed else "N/A", "Resume Score", "3"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_card("⚙️", f"{gap_analysis['coverage']}%", "Skill Coverage", "4"), unsafe_allow_html=True)
        
    # Main Dashboard Visualizations
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        with st.container(border=True):
            st.write("### 🎯 Predicted Careers (Personality & Aptitude)")
            if st.session_state.career_predictions:
                for career, prob in st.session_state.career_predictions[:3]:
                    st.markdown(render_progress_bar(prob, career, color="#7C6FF7"), unsafe_allow_html=True)
            else:
                st.info("Complete the Career Assessment to see predictions.")
                
        with st.container(border=True):
            st.write("### 🛡️ Skill Inventory")
            st.write("**Your Current Skills:**")
            st.markdown(render_skill_tags(st.session_state.skills, "have"), unsafe_allow_html=True)
            st.write(f"**Missing Skills for {st.session_state.selected_career}:**")
            if gap_analysis["missing"]:
                st.markdown(render_skill_tags(gap_analysis["missing"], "missing"), unsafe_allow_html=True)
            else:
                st.success("🎉 You have all the required core skills for this career!")
        
    with col_right:
        with st.container(border=True):
            st.write("### 📈 Readiness Score Breakdown")
            st.markdown(f"<div style='background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.2); border-radius: 8px; padding: 0.5rem 1rem; margin-bottom: 1rem; text-align: center;'><span style='color: #34D399; font-weight: 700; font-size: 1.1rem;'>Professional Level: {readiness['level']}</span></div>", unsafe_allow_html=True)
            
            for cat, details in readiness["breakdown"].items():
                score_pct = (details["score"] / details["max"] * 100) if details["max"] > 0 else 0
                st.markdown(render_progress_bar(score_pct, f"{cat} ({details['score']}/{details['max']})", color="#34D399"), unsafe_allow_html=True)

# ─── PAGE 2: CAREER ASSESSMENT ────────────────────────────────────────────────
elif selected_page == "Career Assessment":
    st.markdown("<h1 class='page-title'>🧭 Discover Your Career Path</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Answer 5 quick, fun questions and we'll match you to your ideal tech career.</p>", unsafe_allow_html=True)

    # ── Quiz Data ──
    QUIZ_QUESTIONS = [
        {
            "question": "You're given a blank weekend — what sparks joy?",
            "options": [
                {"emoji": "💻", "label": "Build a side project or solve coding puzzles", "scores": {"Abstract Reasoning": 3, "Numerical Aptitude": 3}},
                {"emoji": "🎨", "label": "Design something beautiful — UI, art, or 3D", "scores": {"Spatial Aptitude": 4, "O_score": 1}},
                {"emoji": "🗣️", "label": "Organize a meetup, mentor someone, or write a blog", "scores": {"E_score": 2, "Verbal Reasoning": 3}},
                {"emoji": "📊", "label": "Analyze data, read research papers, or optimize a process", "scores": {"C_score": 2, "Perceptual Aptitude": 2, "Numerical Aptitude": 1}},
            ]
        },
        {
            "question": "A teammate says: 'This doesn't work.' — your instinct?",
            "options": [
                {"emoji": "🔍", "label": "Dig into the logs, debug line by line", "scores": {"Abstract Reasoning": 3, "Perceptual Aptitude": 2}},
                {"emoji": "🤝", "label": "Let's whiteboard this together and brainstorm", "scores": {"E_score": 3, "A_score": 2}},
                {"emoji": "📐", "label": "Redesign the approach — maybe the architecture is wrong", "scores": {"Spatial Aptitude": 3, "O_score": 2}},
                {"emoji": "📋", "label": "Check if we followed the spec correctly, step by step", "scores": {"C_score": 3, "Perceptual Aptitude": 2}},
            ]
        },
        {
            "question": "Which superpower would make you unstoppable at work?",
            "options": [
                {"emoji": "🧠", "label": "Instant pattern recognition — see connections no one else can", "scores": {"Abstract Reasoning": 4, "Numerical Aptitude": 2}},
                {"emoji": "🎯", "label": "Perfect focus — zero distractions, flawless execution", "scores": {"C_score": 4, "N_score": -1}},
                {"emoji": "💬", "label": "Mind-reading — understand exactly what users or clients need", "scores": {"E_score": 3, "Verbal Reasoning": 3}},
                {"emoji": "🔮", "label": "Future vision — predict trends and pivot before anyone else", "scores": {"O_score": 4, "Spatial Aptitude": 1}},
            ]
        },
        {
            "question": "You just joined a hackathon team — which role do you grab?",
            "options": [
                {"emoji": "⚙️", "label": "Backend wizard — APIs, databases, and system design", "scores": {"Numerical Aptitude": 3, "Abstract Reasoning": 2}},
                {"emoji": "✨", "label": "Frontend / Design lead — make it look stunning", "scores": {"Spatial Aptitude": 4, "O_score": 1}},
                {"emoji": "📢", "label": "Pitch presenter — I'll sell our idea to the judges", "scores": {"E_score": 3, "Verbal Reasoning": 3}},
                {"emoji": "🧪", "label": "Data / ML engineer — train a model, crunch the numbers", "scores": {"Numerical Aptitude": 4, "Perceptual Aptitude": 2}},
            ]
        },
        {
            "question": "What does your dream work day look like?",
            "options": [
                {"emoji": "🏠", "label": "Deep focus at home — headphones on, building something complex", "scores": {"C_score": 2, "Abstract Reasoning": 2, "N_score": -1}},
                {"emoji": "🏢", "label": "Collaborative office — stand-ups, pair programming, energy", "scores": {"E_score": 4, "A_score": 2}},
                {"emoji": "☕", "label": "Café vibes — sketching wireframes and prototyping ideas", "scores": {"Spatial Aptitude": 3, "O_score": 3}},
                {"emoji": "📚", "label": "Research lab — reading papers, running experiments, writing docs", "scores": {"Verbal Reasoning": 3, "Numerical Aptitude": 2, "C_score": 1}},
            ]
        },
    ]

    TOTAL_STEPS = len(QUIZ_QUESTIONS)
    step = st.session_state.quiz_step

    # ── Layout: Quiz Card (left) + Live Preview (right) ──
    col_quiz, col_preview = st.columns([1.6, 1])

    with col_quiz:
        if step < TOTAL_STEPS:
            # ── Step Progress Bar ──
            dots_html = ""
            for i in range(TOTAL_STEPS):
                if i < step:
                    dots_html += '<div class="quiz-progress-dot done"></div>'
                elif i == step:
                    dots_html += '<div class="quiz-progress-dot active"></div>'
                else:
                    dots_html += '<div class="quiz-progress-dot"></div>'
            st.markdown(f'<div class="quiz-progress-bar">{dots_html}</div>', unsafe_allow_html=True)

            q = QUIZ_QUESTIONS[step]

            # ── Question Card ──
            with st.container(border=True):
                st.markdown(f'<div class="quiz-question-num">Question {step + 1} of {TOTAL_STEPS}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="quiz-question-text">{q["question"]}</div>', unsafe_allow_html=True)

                # Render each option as a Streamlit button
                for idx, opt in enumerate(q["options"]):
                    btn_label = f'{opt["emoji"]}  {opt["label"]}'
                    if st.button(btn_label, key=f"quiz_opt_{step}_{idx}", use_container_width=True):
                        st.session_state.quiz_answers[step] = idx
                        st.session_state.quiz_step = step + 1
                        
                        # If last question, compute results
                        if step + 1 >= TOTAL_STEPS:
                            scores = {
                                "O_score": 5.0, "C_score": 5.0, "E_score": 5.0,
                                "A_score": 5.0, "N_score": 5.0,
                                "Numerical Aptitude": 5.0, "Spatial Aptitude": 5.0,
                                "Perceptual Aptitude": 5.0, "Abstract Reasoning": 5.0,
                                "Verbal Reasoning": 5.0
                            }
                            for q_idx, ans_idx in st.session_state.quiz_answers.items():
                                chosen = QUIZ_QUESTIONS[q_idx]["options"][ans_idx]
                                for trait, val in chosen["scores"].items():
                                    scores[trait] = scores.get(trait, 5.0) + val
                            for k in scores:
                                scores[k] = max(1.0, min(10.0, float(scores[k])))
                            st.session_state.personality_scores = scores
                            predictions = predictor.get_top_careers(scores, top_n=5)
                            st.session_state.career_predictions = predictions
                            if predictions:
                                st.session_state.selected_career = predictions[0][0]
                        st.rerun()

            # ── Back button ──
            if step > 0:
                if st.button("← Back", key="quiz_back"):
                    st.session_state.quiz_step = step - 1
                    st.rerun()

        else:
            # ── RESULTS VIEW ──
            dots_html = '<div class="quiz-progress-dot done"></div>' * TOTAL_STEPS
            st.markdown(f'<div class="quiz-progress-bar">{dots_html}</div>', unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown("<div class='quiz-question-num'>🎉 Assessment Complete</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='quiz-question-text'>Your top career match: {st.session_state.selected_career}</div>", unsafe_allow_html=True)

                # Render top 5 result cards
                colors = ["#7C6FF7", "#34D399", "#FBBF24", "#F87171", "#38BDF8"]
                if st.session_state.career_predictions:
                    max_prob = st.session_state.career_predictions[0][1]
                    for i, (career, prob) in enumerate(st.session_state.career_predictions[:5]):
                        pct = (prob / max_prob * 100) if max_prob > 0 else 0
                        color = colors[i % len(colors)]
                        rank_label = ["🥇 Best Match", "🥈 Strong Match", "🥉 Good Match", "4th Match", "5th Match"][i]
                        st.markdown(f"""
                        <div class="quiz-result-card" style="border-left: 3px solid {color};">
                            <div class="quiz-result-rank">{rank_label}</div>
                            <div class="quiz-result-career">{career}</div>
                            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                                <span style="font-size:0.8rem;color:var(--text-muted);">Match confidence</span>
                                <span style="font-size:0.8rem;font-weight:700;color:{color};">{prob:.1f}%</span>
                            </div>
                            <div class="quiz-result-bar-bg">
                                <div class="quiz-result-bar-fill" style="width:{pct:.0f}%;background:{color};"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Could not generate predictions. Please retake the quiz.")

            # Retake button
            if st.button("🔄 Retake Assessment", use_container_width=True):
                st.session_state.quiz_step = 0
                st.session_state.quiz_answers = {}
                st.rerun()

    with col_preview:
        # ── Live Profile Snapshot ──
        with st.container(border=True):
            st.write("### 👤 Your Profile")
            st.markdown(f"""
            <div style="text-align:center;margin-bottom:0.5rem;">
                <div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#7C6FF7,#34D399);display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:800;color:white;margin:0 auto;">
                    {st.session_state.get('name','A')[0].upper()}
                </div>
                <div style="font-weight:700;margin-top:0.4rem;">{st.session_state.get('name','Alex')}</div>
                <div style="font-size:0.78rem;color:var(--text-muted);">{st.session_state.branch} • CGPA {st.session_state.cgpa:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("**Current Skills:**")
            from modules.ui_components import render_skill_tags
            st.markdown(render_skill_tags(st.session_state.skills[:8], "have"), unsafe_allow_html=True)

        # ── Career Guide ──
        with st.container(border=True):
            st.write("### 💡 What This Quiz Measures")
            st.markdown("""
            We assess **5 core traits** to find your fit:
            
            🧮 **Numerical & Abstract** → AI, Data Science, Backend  
            🎨 **Spatial & Design** → UI/UX, Frontend, Graphics  
            🗣️ **Verbal & Social** → PM, Technical Writing  
            📋 **Conscientiousness** → QA, DevOps, Security  
            🔍 **Perceptual** → Testing, Cybersecurity
            """)

        # ── Quick predictions ──
        if st.session_state.career_predictions and step >= TOTAL_STEPS:
            with st.container(border=True):
                st.write("### 🚀 Recommended Next Steps")
                top_career = st.session_state.career_predictions[0][0]
                st.markdown(f"""
                1. Head to **Interactive Roadmap** to see your learning path for **{top_career}**
                2. Upload your resume in **Resume Analyzer** to check readiness
                3. Practice with **Interview Prep** for {top_career}-specific questions
                """)

# ─── PAGE 3: RESUME ANALYZER ──────────────────────────────────────────────────
elif selected_page == "Resume Analyzer":
    st.markdown("<h1 class='page-title'>📄 Resume Analyzer & Parser</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Upload your resume PDF to extract skills, certifications, and calculate a job-readiness score.</p>", unsafe_allow_html=True)
    
    col_upload, col_result = st.columns([1, 1.2])
    
    with col_upload:
        with st.container(border=True):
            st.write("### Upload Resume PDF")
            uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
            if uploaded_file is not None:
                file_key = f"parsed_analyzer_resume_{uploaded_file.name}_{uploaded_file.size}"
                if st.session_state.get(file_key) is not True:
                    with st.spinner("Extracting contents and analyzing..."):
                        analysis = analyze_resume(uploaded_file)
                        if "error" not in analysis:
                            st.session_state.resume_analyzed = True
                            st.session_state.resume_data = analysis
                            
                            # Auto-fill fields if extracted
                            if analysis.get("name"):
                                st.session_state.name = analysis["name"]
                            if analysis.get("email"):
                                st.session_state.email = analysis["email"]
                            if analysis.get("bio"):
                                st.session_state.bio = analysis["bio"]
                            if analysis.get("cgpa"):
                                try:
                                    st.session_state.cgpa = float(analysis["cgpa"])
                                except (ValueError, TypeError):
                                    pass
                            if analysis.get("branch"):
                                st.session_state.branch = analysis["branch"]
                            if analysis.get("target_career") and analysis["target_career"] in CAREER_SKILLS:
                                st.session_state.selected_career = analysis["target_career"]
                            
                            # Match branch if found in education and branch was not set
                            if not analysis.get("branch"):
                                edu_list = analysis.get("education", [])
                                if edu_list:
                                    branches = ["Computer Science", "Information Technology", "Electronics & Comm", "Data Science", "Mechanical", "Electrical", "Civil", "Business Administration"]
                                    for edu_str in edu_list:
                                        for br in branches:
                                            if br.lower() in edu_str.lower():
                                                st.session_state.branch = br
                                                break
                                                
                            for skill in analysis.get("skills", []):
                                if skill not in st.session_state.skills:
                                    st.session_state.skills.append(skill)
                            
                            st.session_state.certifications = analysis.get("certifications", [])
                            sync_profile_states()
                            st.session_state[file_key] = True
                            st.success("Resume parsed successfully!")
                            st.rerun()
                        else:
                            st.error(analysis["error"])
            st.write("---")
            st.markdown("""
            💡 **How to improve your score:**
            1. List standard skills explicitly (e.g., Python, Docker).
            2. Format clearly with headers for Education, Experience, Projects.
            3. Make sure it's not a scanned image PDF.
            """)

    with col_result:
        if st.session_state.resume_analyzed:
            with st.container(border=True):
                st.write("### Resume Analysis Results")
                
                score_data = st.session_state.resume_data.get("score", {})
                score_val = score_data.get("total", 0)
                st.markdown(render_progress_bar(score_val, "Resume Quality Score", color="#7C6FF7"), unsafe_allow_html=True)
                
                st.write("#### Score Breakdown")
                c_s1, c_s2 = st.columns(2)
                keys = [k for k in score_data.keys() if k != "total"]
                for idx, key in enumerate(keys):
                    val = score_data[key]
                    col = c_s1 if idx % 2 == 0 else c_s2
                    with col:
                        st.markdown(render_progress_bar(val if val <= 100 else val*10, key.title(), color="#34D399"), unsafe_allow_html=True)
                        
                st.write("---")
                st.write("### Extracted Details")
                st.write("**Extracted Skills:**")
                st.markdown(render_skill_tags(st.session_state.resume_data.get("skills", []), "have"), unsafe_allow_html=True)
                
                st.write("**Extracted Education:**")
                edu = st.session_state.resume_data.get("education", [])
                if isinstance(edu, list):
                    for e in edu:
                        st.markdown(f"- {e}")
                else:
                    st.write(edu)
                
                st.write("**Extracted Certifications:**")
                certs = st.session_state.resume_data.get("certifications", [])
                if isinstance(certs, list):
                    if certs:
                        for c in certs:
                            st.markdown(f"- {c}")
                    else:
                        st.write("None identified")
                else:
                    st.write(certs)
        else:
            with st.container(border=True):
                st.write("### Resume Details & Insights")
                st.info("Upload your resume on the left to unlock details, extracted skills, and quality scores.")
                st.markdown("""
                Our AI-powered analyzer parses your document to extract:
                * 🛠️ **Technical Skills**: Extracted from your experience and project sections.
                * 🎓 **Education Details**: Degree, academic field, and university.
                * 🏅 **Certifications**: Industry standard certifications recognized.
                * 📊 **Quality Score**: Assesses formatting, spelling, density of skills, and project descriptions.
                """)

# ─── PAGE 4: JOB MATCHING ─────────────────────────────────────────────────────
elif selected_page == "Job Matching":
    st.markdown("<h1 class='page-title'>💼 Job Matching & Analysis</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Compare your skill profile against jobs from our database or paste any job description.</p>", unsafe_allow_html=True)
    
    tab_db, tab_custom = st.tabs(["📂 Database Jobs", "✏️ Paste Custom Job Description"])
    
    with tab_db:
        with st.container(border=True):
            st.write("### Compare with Database Jobs")
            
            @st.cache_data
            def load_sample_jobs():
                try:
                    df_jobs = pd.read_csv("DataScientist.csv")
                    return df_jobs.head(50)
                except Exception:
                    return pd.DataFrame({
                        "Job Title": ["Data Scientist (AI/ML)", "Junior Data Analyst", "DevOps Engineer"],
                        "Company Name": ["Google", "Meta", "Amazon"],
                        "Location": ["Mountain View, CA", "Menlo Park, CA", "Seattle, WA"],
                        "Job Description": [
                            "We are looking for a Data Scientist with experience in Python, PyTorch, TensorFlow, NLP, and Machine Learning.",
                            "Meta is seeking a Junior Data Analyst proficient in SQL, Python, Excel, and Tableau.",
                            "Amazon is hiring a DevOps Engineer with knowledge of Linux, Docker, Git, Kubernetes, and AWS."
                        ]
                    })
                
            try:
                df_jobs = load_sample_jobs()
                job_titles = df_jobs["Job Title"].tolist()
                selected_job_idx = st.selectbox("Select a Job from dataset:", range(len(job_titles)), format_func=lambda x: job_titles[x])
                
                job_desc = df_jobs.iloc[selected_job_idx]["Job Description"]
                company = df_jobs.iloc[selected_job_idx]["Company Name"]
                location = df_jobs.iloc[selected_job_idx]["Location"]
                
                st.markdown(f"📍 **Company:** {company} | 🗺️ **Location:** {location}")
                
                from modules.resume_analyzer import extract_skills
                job_skills = extract_skills(job_desc)
                
                match_res = calculate_job_match(st.session_state.skills, job_skills)
                
                st.markdown(render_progress_bar(match_res["match_score"], "Profile Match Score", color="#7C6FF7"), unsafe_allow_html=True)
                
                st.write("#### Skill Matching Details")
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.write("**✅ Matched Skills:**")
                    if match_res["matched_skills"]:
                        st.markdown(render_skill_tags(match_res["matched_skills"], "have"), unsafe_allow_html=True)
                    else:
                        st.write("No matching skills found.")
                with col_m2:
                    st.write("**❌ Missing Skills:**")
                    if match_res["missing_skills"]:
                        st.markdown(render_skill_tags(match_res["missing_skills"], "missing"), unsafe_allow_html=True)
                    else:
                        st.success("🎉 No missing skills! You're a perfect match.")
                
                st.write("---")
                with st.expander("📖 Show Full Job Description"):
                    st.text(job_desc)
                    
            except Exception as e:
                st.error(f"Error loading jobs: {str(e)}")
                
    with tab_custom:
        with st.container(border=True):
            st.write("### Paste Custom Job Description")
            custom_desc = st.text_area("Paste the Job Description here:", height=200, placeholder="Paste a job description here to check your profile match score...")
            
            if custom_desc:
                from modules.resume_analyzer import extract_skills
                custom_job_skills = extract_skills(custom_desc)
                
                custom_match_res = calculate_job_match(st.session_state.skills, custom_job_skills)
                
                st.markdown(render_progress_bar(custom_match_res["match_score"], "Custom Job Match Score", color="#7C6FF7"), unsafe_allow_html=True)
                
                col_mc1, col_mc2 = st.columns(2)
                with col_mc1:
                    st.write("**✅ Matched Skills:**")
                    if custom_match_res["matched_skills"]:
                        st.markdown(render_skill_tags(custom_match_res["matched_skills"], "have"), unsafe_allow_html=True)
                    else:
                        st.write("No matching skills found.")
                with col_mc2:
                    st.write("**❌ Missing Skills:**")
                    if custom_match_res["missing_skills"]:
                        st.markdown(render_skill_tags(custom_match_res["missing_skills"], "missing"), unsafe_allow_html=True)
                    else:
                        st.success("🎉 No missing skills! You're a perfect match.")

# ─── PAGE 5: INTERACTIVE ROADMAP ──────────────────────────────────────────────
elif selected_page == "Interactive Roadmap":
    st.markdown("<h1 class='page-title'>🗺️ Personalized Career Roadmap</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Explore step-by-step career milestones, check off completed skills, and access curated learning material.</p>", unsafe_allow_html=True)
    
    col_sel, col_stat = st.columns([1.5, 1])
    with col_sel:
        target_career = st.selectbox(
            "Target Career Path:",
            list(CAREER_SKILLS.keys()),
            index=list(CAREER_SKILLS.keys()).index(st.session_state.selected_career) if st.session_state.selected_career in CAREER_SKILLS else 0
        )
        st.session_state.selected_career = target_career
        
    roadmap_data = get_roadmap(target_career, list(st.session_state.skills) + list(st.session_state.completed_skills))
    
    # Calculate overall roadmap progress
    total_skills = sum(phase["total_count"] for phase in roadmap_data)
    completed_skills = sum(phase["completed_count"] for phase in roadmap_data)
    overall_progress = int(completed_skills / total_skills * 100) if total_skills > 0 else 0
    
    with col_stat:
        st.markdown(f"<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown(render_progress_bar(overall_progress, "Overall Roadmap Completion", color="#7C6FF7"), unsafe_allow_html=True)
        
    st.write("---")
    
    st.write("### 📍 Roadmap Milestones")
    for phase_idx, phase in enumerate(roadmap_data):
        if phase["completed_count"] == phase["total_count"]:
            status_badge = "🟢 Complete"
            badge_bg = "rgba(52, 211, 153, 0.1)"
            badge_color = "#34D399"
        elif phase["completed_count"] > 0:
            status_badge = "🟡 In Progress"
            badge_bg = "rgba(251, 191, 36, 0.1)"
            badge_color = "#FBBF24"
        else:
            status_badge = "⚪ Not Started"
            badge_bg = "rgba(156, 163, 175, 0.1)"
            badge_color = "#9CA3AF"
            
        col_node, col_card = st.columns([0.08, 0.92])
        
        with col_node:
            is_last = (phase_idx == len(roadmap_data) - 1)
            line_height = "0px" if is_last else "140px"
            node_color = badge_color
            
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: flex-start; height: 100%; min-height: 155px; margin-top: 10px;">
                <div style="width: 30px; height: 30px; border-radius: 50%; background: {node_color}; display: flex; align-items: center; justify-content: center; color: #111827; font-size: 11px; font-weight: 800; box-shadow: 0 0 15px {node_color}80; border: 2px solid #fff;">
                    {phase_idx+1}
                </div>
                <div style="width: 2px; height: {line_height}; background: linear-gradient(180deg, {node_color}, rgba(255,255,255,0.03)); margin: 10px 0;"></div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_card:
            with st.container(border=True):
                st.markdown(f"""
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;'>
                    <h3 style='margin: 0; font-size: 1.15rem; color: #7C6FF7;'>🚩 Phase {phase_idx+1}: {phase['phase']} ({phase['duration']})</h3>
                    <span style='background: {badge_bg}; color: {badge_color}; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 700;'>{status_badge}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Checkbox columns for skills
                cols = st.columns(min(len(phase["skills"]), 4))
                for idx, skill in enumerate(phase["skills"]):
                    col_idx = idx % len(cols)
                    with cols[col_idx]:
                        skill_name = skill["name"]
                        is_checked = skill["completed"]
                        
                        checked = st.checkbox(skill_name, value=is_checked, key=f"roadmap_check_{phase['phase']}_{skill_name}")
                        if checked != is_checked:
                            if checked:
                                st.session_state.completed_skills.add(skill_name)
                            else:
                                st.session_state.completed_skills.discard(skill_name)
                            sync_profile_states()
                            st.rerun()
                
                # Curated material expander
                with st.expander("📚 Study Material & Projects"):
                    c_col1, c_col2 = st.columns(2)
                    with c_col1:
                        st.write("**Curated Courses & Resources:**")
                        found_any_course = False
                        for skill_status in phase["skills"]:
                            s_name = skill_status["name"]
                            courses = COURSE_RECOMMENDATIONS.get(s_name, [])
                            if courses:
                                found_any_course = True
                                st.markdown(f"*{s_name}:*")
                                for c in courses:
                                    st.markdown(f"- [{c['title']}]({c['url']}) ({c['platform']})")
                        if not found_any_course:
                            st.write("No courses found. Try searching on YouTube or Coursera.")
                    with c_col2:
                        st.write("**Target Projects to Build:**")
                        proj_career_data = PROJECT_RECOMMENDATIONS.get(target_career, PROJECT_RECOMMENDATIONS.get("Software Engineer", {}))
                        phase_skills_set = set(s["name"].lower() for s in phase["skills"])
                        found_any_project = False
                        
                        for level in ["Beginner", "Intermediate", "Advanced"]:
                            for proj in proj_career_data.get(level, []):
                                proj_skills_set = set(s.lower() for s in proj["skills"])
                                if proj_skills_set.intersection(phase_skills_set):
                                    found_any_project = True
                                    st.markdown(f"🛠️ **{proj['name']}** ({level})")
                                    st.write(proj["desc"])
                        if not found_any_project:
                            st.write("No specific projects mapped for this phase.")
# ─── PAGE 6: AI MENTOR CHATBOT ────────────────────────────────────────────────
elif selected_page == "AI Mentor Chatbot":
    st.markdown("<h1 class='page-title'>🤖 AI Mentor Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Get personalized career counseling, study plans, and advice powered by Groq LLaMA AI — with full context of your profile.</p>", unsafe_allow_html=True)
    
    api_key = GROQ_API_KEY
    
    # Pre-built Prompt Suggestions rendered as stylish clickable buttons
    st.write("💡 **Suggested questions for your mentor:**")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    suggested_q = None
    with col_p1:
        if st.button("How to prepare for my predicted career?"):
            suggested_q = "How should I prepare for my top predicted career path? Provide a step-by-step preparation list."
    with col_p2:
        if st.button("Compare TensorFlow and PyTorch"):
            suggested_q = "Should I learn TensorFlow or PyTorch for AI Engineer? Compare them and recommend one based on my profile."
    with col_p3:
        if st.button("Recommended projects for resume"):
            suggested_q = "What specific projects can I build to cover my missing skills and make my resume stand out?"
            
    st.write("---")
    
    gap_analysis = get_skill_gap(st.session_state.skills, st.session_state.selected_career)
    resume_score = st.session_state.resume_data.get("score", {}).get("total", 60) if st.session_state.resume_analyzed else 0
    readiness = calculate_readiness_score(
        skills=st.session_state.skills,
        target_career=st.session_state.selected_career,
        resume_score=resume_score
    )
    
    user_context = {
        "predicted_career": st.session_state.selected_career,
        "current_skills": st.session_state.skills,
        "missing_skills": gap_analysis["missing"],
        "resume_score": resume_score,
        "readiness_score": readiness["total"],
        "interests": st.session_state.interests,
        "education": st.session_state.branch,
    }
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    user_input = st.chat_input("Ask your Career Mentor...")
    
    if suggested_q:
        user_input = suggested_q
        
    if user_input:
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
        
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner("AI Mentor is thinking..."):
            response = chat_with_mentor(
                api_key=api_key,
                user_message=user_input,
                chat_history=st.session_state.chat_history,
                user_context=user_context
            )
            
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(response)
                
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
# ─── PAGE 7: INTERVIEW PREP ──────────────────────────────────────────────────
elif selected_page == "Interview Prep":
    st.markdown("<h1 class='page-title'>🎤 Interview Preparation</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Prepare for your upcoming interviews with career-specific technical and behavioral questions — plus AI-generated custom questions.</p>", unsafe_allow_html=True)
    
    tab_qa, tab_ai = st.tabs(["🎤 Interview Q&A Bank", "🔮 AI Mock Interview Generator"])
    
    with tab_qa:
        with st.container(border=True):
            st.write(f"### Standard {st.session_state.selected_career} Interview Questions")
            
            role_questions = INTERVIEW_QUESTIONS.get(st.session_state.selected_career, INTERVIEW_QUESTIONS.get("Software Engineer", {}))
            
            if role_questions:
                st.write("#### 🛠️ Technical Questions")
                for idx, q in enumerate(role_questions.get("Technical", [])):
                    with st.expander(f"Q{idx+1}: {q}"):
                        st.markdown("""
                        **💡 Points to cover in your answer:**
                        - Structure your answer clearly (definition, usage/concept, practical example).
                        - Explain the core steps and time/space complexity if applicable.
                        - Relate it to any project you have completed.
                        """)
                        
                        # Generate Answer button
                        if st.button("🤖 Generate Answer with AI", key=f"gen_ans_{st.session_state.selected_career}_tech_{idx}"):
                            with st.spinner("AI is crafting a model answer..."):
                                answer_prompt = f"Provide a concise, high-scoring model answer for this {st.session_state.selected_career} technical interview question: '{q}'. Use professional, structured language and include a brief example."
                                answer_text = chat_with_mentor(
                                    api_key=GROQ_API_KEY,
                                    user_message=answer_prompt,
                                    chat_history=[],
                                    user_context={}
                                )
                                st.session_state[f"ans_{st.session_state.selected_career}_tech_{idx}"] = answer_text
                                
                        if f"ans_{st.session_state.selected_career}_tech_{idx}" in st.session_state:
                            st.info("**Model Answer:**")
                            st.markdown(st.session_state[f"ans_{st.session_state.selected_career}_tech_{idx}"])
                            
                st.write("---")
                st.write("#### 🤝 Behavioral & HR Questions")
                for idx, q in enumerate(role_questions.get("HR", [])):
                    with st.expander(f"Q{idx+1}: {q}"):
                        st.markdown("""
                        **💡 Star Method (Situation, Task, Action, Result):**
                        - Describe the Situation and the Task you faced.
                        - Detail the Action you took.
                        - Highlight the Result achieved.
                        """)
                        
                        # Generate Answer button
                        if st.button("🤖 Generate Answer with AI", key=f"gen_ans_{st.session_state.selected_career}_hr_{idx}"):
                            with st.spinner("AI is crafting a model answer..."):
                                answer_prompt = f"Provide a concise, high-scoring model answer for this {st.session_state.selected_career} behavioral HR question: '{q}'. Use the STAR method (Situation, Task, Action, Result) with a generic professional project example."
                                answer_text = chat_with_mentor(
                                    api_key=GROQ_API_KEY,
                                    user_message=answer_prompt,
                                    chat_history=[],
                                    user_context={}
                                )
                                st.session_state[f"ans_{st.session_state.selected_career}_hr_{idx}"] = answer_text
                                
                        if f"ans_{st.session_state.selected_career}_hr_{idx}" in st.session_state:
                            st.info("**Model Answer:**")
                            st.markdown(st.session_state[f"ans_{st.session_state.selected_career}_hr_{idx}"])
            else:
                st.info("No preloaded questions for this career role. Try generating custom questions in the next tab.")
                
    with tab_ai:
        with st.container(border=True):
            st.write("### AI-Powered Custom Interview Generator")
            st.write("Generate a personalized set of interview questions based on your profile, skills, and target role using AI.")
            
            diff = st.selectbox("Interview Difficulty:", ["Junior", "Mid-level", "Senior"])
            
            if st.button("Generate Custom Questions", use_container_width=True):
                with st.spinner("Generating custom questions..."):
                    questions = generate_interview_questions(
                        api_key=GROQ_API_KEY,
                        career=st.session_state.selected_career,
                        skills=st.session_state.skills,
                        difficulty=diff
                    )
                    if questions:
                        st.session_state.custom_questions = questions
                        st.success("Custom questions generated!")
                    else:
                        st.error("Failed to generate questions. Check connection/API key.")
                        
            if "custom_questions" in st.session_state:
                st.write("---")
                st.markdown(st.session_state.custom_questions)
