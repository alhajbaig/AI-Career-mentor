"""
AI Career Mentor - Custom CSS Styles
Clean, premium glassmorphism dark theme.
"""

def get_custom_css() -> str:
    return """
<style>
    /* ═══════════════════════════════════════════════════════════════
       FONTS & ROOT (Modern Tech Typography)
    ═══════════════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

    :root {
        --primary: #8B5CF6;
        --primary-glow: rgba(139, 92, 246, 0.3);
        --primary-soft: rgba(139, 92, 246, 0.12);
        --accent: #10B981;
        --accent-glow: rgba(16, 185, 129, 0.3);
        --accent-soft: rgba(16, 185, 129, 0.12);
        --danger: #EF4444;
        --warning: #F59E0B;
        --bg: #07090e;
        --surface: rgba(15, 18, 28, 0.65);
        --surface-2: rgba(26, 31, 46, 0.75);
        --border: rgba(255, 255, 255, 0.07);
        --border-focus: rgba(139, 92, 246, 0.5);
        --text: #F8FAFC;
        --text-muted: #94A3B8;
        --text-dim: #64748B;
        --radius: 14px;
        --radius-sm: 8px;
        --radius-lg: 20px;
    }

    /* ═══════════════════════════════════════════════════════════════
       GLOBAL & MESH GRADIENTS
    ═══════════════════════════════════════════════════════════════ */
    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at 10% 15%, rgba(139, 92, 246, 0.1) 0%, transparent 40%),
                    radial-gradient(circle at 90% 85%, rgba(16, 185, 129, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 50% 50%, rgba(99, 102, 241, 0.04) 0%, transparent 60%),
                    var(--bg) !important;
        color: var(--text) !important;
    }

    .stApp > header { background: transparent !important; }

    .block-container {
        max-width: 1120px !important;
        padding: 1.5rem 1.5rem 5rem !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       SIDEBAR
    ═══════════════════════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: rgba(11, 14, 22, 0.95) !important;
        border-right: 1px solid var(--border) !important;
        padding-top: 1rem !important;
        backdrop-filter: blur(20px);
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        color: var(--text-muted) !important;
    }

    /* Profile badge in sidebar */
    .profile-badge {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(16, 185, 129, 0.04));
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: var(--radius);
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }
    .profile-badge:hover {
        border-color: rgba(139, 92, 246, 0.4);
        box-shadow: 0 4px 25px rgba(139, 92, 246, 0.15);
    }
    .profile-badge-name {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.2rem;
    }
    .profile-badge-detail {
        font-size: 0.78rem;
        color: var(--text-muted);
        line-height: 1.6;
    }

    /* ═══════════════════════════════════════════════════════════════
       TYPOGRAPHY
    ═══════════════════════════════════════════════════════════════ */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        color: var(--text) !important;
    }

    .page-title {
        font-family: 'Syne', sans-serif !important;
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #FFFFFF 10%, #C084FC 50%, #6366F1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.4rem !important;
        letter-spacing: -0.03em !important;
        text-shadow: 0 0 40px rgba(139, 92, 246, 0.15);
    }

    .page-subtitle {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.94rem;
        color: var(--text-muted);
        margin-bottom: 1.8rem;
        line-height: 1.6;
    }

    /* ═══════════════════════════════════════════════════════════════
       CARDS (Glassmorphic containers)
    ═══════════════════════════════════════════════════════════════ */
    .card, [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.35rem 1.6rem !important;
        margin-bottom: 1.2rem !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }

    .card:hover, [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(139, 92, 246, 0.35) !important;
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15), 0 0 1px 1px rgba(139, 92, 246, 0.15) inset !important;
    }

    .card-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(20, 25, 38, 0.6) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.35rem !important;
        backdrop-filter: blur(12px);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }

    .metric-card:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(139, 92, 246, 0.35) !important;
        box-shadow: 0 12px 30px rgba(139, 92, 246, 0.15) !important;
    }

    .metric-value {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 1.9rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFFFFF, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.3rem 0;
        word-break: break-word;
        line-height: 1.2;
        text-shadow: 0 0 25px rgba(192, 132, 252, 0.25);
    }

    .metric-label {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-muted);
        margin-top: 0.2rem;
    }

    .metric-icon {
        font-size: 1.6rem;
        margin-bottom: 0.2rem;
    }

    /* ═══════════════════════════════════════════════════════════════
       BUTTONS - Cool, Modern Gradient Hover Effects
    ═══════════════════════════════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem 1.6rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.03em !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
        cursor: pointer !important;
        line-height: 1.4 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        overflow: hidden !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5) !important;
        filter: brightness(1.1);
    }

    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 3px 10px rgba(139, 92, 246, 0.2) !important;
    }

    /* Secondary button style */
    .stButton > button[kind="secondary"] {
        background: rgba(29, 35, 51, 0.6) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        box-shadow: none !important;
        backdrop-filter: blur(8px);
    }
    .stButton > button[kind="secondary"]:hover {
        background: rgba(37, 44, 63, 0.8) !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
        transform: translateY(-2px) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       FORM INPUTS
    ═══════════════════════════════════════════════════════════════ */
    .stTextInput > div > div,
    .stTextArea > div > div,
    .stSelectbox > div > div,
    .stNumberInput > div > div,
    .stMultiSelect > div > div {
        background: rgba(15, 18, 28, 0.8) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div:focus-within,
    .stTextArea > div > div:focus-within,
    .stSelectbox > div > div:focus-within {
        border-color: var(--border-focus) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
    }

    .stSlider > div > div > div {
        background: var(--primary) !important;
    }

    .stRadio > div {
        gap: 0.5rem !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       SKILL TAGS
    ═══════════════════════════════════════════════════════════════ */
    .skill-tag {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 24px;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 4px;
        transition: all 0.2s ease;
    }
    .skill-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
    }

    .skill-tag-have {
        background: var(--accent-soft);
        color: var(--accent);
        border: 1px solid rgba(16, 185, 129, 0.25);
    }

    .skill-tag-missing {
        background: rgba(239, 68, 68, 0.1);
        color: var(--danger);
        border: 1px solid rgba(239, 68, 68, 0.25);
    }

    .skill-tag-neutral {
        background: var(--primary-soft);
        color: var(--primary);
        border: 1px solid rgba(139, 92, 246, 0.25);
    }

    /* ═══════════════════════════════════════════════════════════════
       PROGRESS BAR
    ═══════════════════════════════════════════════════════════════ */
    .progress-bar-custom {
        background: var(--surface-2);
        border-radius: 6px;
        overflow: hidden;
        height: 8px;
        margin: 0.4rem 0;
    }

    .progress-fill {
        height: 100%;
        border-radius: 6px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        transition: width 0.8s ease;
    }

    /* ═══════════════════════════════════════════════════════════════
       EXPANDERS
    ═══════════════════════════════════════════════════════════════ */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] > div:first-child {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: var(--text) !important;
        padding: 0.7rem 1.1rem !important;
        backdrop-filter: blur(8px);
        transition: all 0.2s ease !important;
    }

    [data-testid="stExpander"] > div:first-child:hover {
        border-color: rgba(139, 92, 246, 0.35) !important;
        background: var(--surface-2) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       FILE UPLOADER
    ═══════════════════════════════════════════════════════════════ */
    .stFileUploader > div {
        background: var(--surface) !important;
        border: 2px dashed var(--border) !important;
        border-radius: var(--radius) !important;
        transition: all 0.3s ease;
    }

    .stFileUploader > div:hover {
        border-color: var(--primary) !important;
        background: rgba(139, 92, 246, 0.03) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       CHAT
    ═══════════════════════════════════════════════════════════════ */
    .stChatMessage {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        padding: 1.1rem 1.3rem !important;
        margin-bottom: 0.6rem !important;
        backdrop-filter: blur(12px);
    }

    [data-testid="stChatInput"] {
        background: rgba(15, 18, 28, 0.9) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       TABS
    ═══════════════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 18, 28, 0.9) !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--border) !important;
        padding: 5px !important;
        gap: 3px !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm) !important;
        color: var(--text-muted) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 8px 18px !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }

    /* ═══════════════════════════════════════════════════════════════
       SUCCESS / INFO / WARNING ALERTS
    ═══════════════════════════════════════════════════════════════ */
    [data-testid="stAlert"] {
        border-radius: var(--radius-sm) !important;
        border: none !important;
        backdrop-filter: blur(8px);
    }

    /* ═══════════════════════════════════════════════════════════════
       PHASE / ROADMAP CARDS
    ═══════════════════════════════════════════════════════════════ */
    .phase-card {
        background: rgba(20, 25, 38, 0.55);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.1rem 1.35rem;
        margin-bottom: 0.7rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }

    .phase-card:hover {
        border-color: rgba(139, 92, 246, 0.4);
        transform: translateY(-2px) translateX(4px);
        background: rgba(29, 35, 51, 0.7);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }

    .phase-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.98rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.2rem;
    }

    .phase-duration {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
    }

    /* ═══════════════════════════════════════════════════════════════
       HERO / PAGE HEADER
    ═══════════════════════════════════════════════════════════════ */
    .hero-title {
        font-family: 'Syne', sans-serif !important;
        font-size: 1.95rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }

    .hero-subtitle {
        font-size: 0.92rem;
        color: var(--text-muted);
        margin-bottom: 1.6rem;
        line-height: 1.5;
    }

    /* ═══════════════════════════════════════════════════════════════
       DIVIDERS
    ═══════════════════════════════════════════════════════════════ */
    hr {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 1.2rem 0 !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       SCROLLBAR
    ═══════════════════════════════════════════════════════════════ */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(139, 92, 246, 0.4);
        border-radius: 4px;
    }

    /* ═══════════════════════════════════════════════════════════════
       OPTION MENU FIXES (prevent double text / icon overlap)
    ═══════════════════════════════════════════════════════════════ */
    nav[data-testid="stSidebarNav"] { display: none !important; }

    /* Fix the streamlit_option_menu arrow icon overlap bug */
    ul[class*="nav"] li a span:first-child {
        display: inline !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       HIDE STREAMLIT DEFAULTS
    ═══════════════════════════════════════════════════════════════ */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stDecoration"] { display: none; }

    /* ═══════════════════════════════════════════════════════════════
       PROFILE PAGE
    ═══════════════════════════════════════════════════════════════ */
    .avatar-circle {
        width: 85px;
        height: 85px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.1rem;
        font-weight: 800;
        color: white;
        margin: 0 auto 1.1rem;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.35);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }

    .profile-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.65rem 0;
        border-bottom: 1px solid var(--border);
        font-size: 0.9rem;
    }

    .profile-stat:last-child { border-bottom: none; }

    .profile-stat-key {
        color: var(--text-muted);
        font-weight: 500;
    }

    .profile-stat-val {
        color: var(--text);
        font-weight: 600;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Suggested prompt chips */
    .prompt-chip {
        display: inline-block;
        background: rgba(29, 35, 51, 0.5);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 7px 16px;
        font-size: 0.84rem;
        color: var(--text-muted);
        cursor: pointer;
        margin: 5px;
        transition: all 0.2s ease;
    }
    .prompt-chip:hover {
        border-color: var(--primary);
        color: var(--text);
        background: var(--primary-soft);
        transform: translateY(-1px);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .card, .metric-card, .phase-card {
        animation: fadeIn 0.4s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }

    /* ═══════════════════════════════════════════════════════════════
       CAREER QUIZ - Swipe-Card Style
    ═══════════════════════════════════════════════════════════════ */
    .quiz-progress-bar {
        display: flex;
        gap: 6px;
        margin-bottom: 1.5rem;
    }
    .quiz-progress-dot {
        flex: 1;
        height: 5px;
        border-radius: 3px;
        background: var(--surface-2);
        transition: all 0.4s ease;
    }
    .quiz-progress-dot.active {
        background: var(--primary);
        box-shadow: 0 0 10px var(--primary);
    }
    .quiz-progress-dot.done {
        background: var(--accent);
    }

    .quiz-question-num {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--primary);
        margin-bottom: 0.4rem;
    }

    .quiz-question-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 1.2rem;
        line-height: 1.4;
    }

    .quiz-option {
        background: var(--surface-2);
        border: 1.5px solid var(--border);
        border-radius: var(--radius);
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.55rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .quiz-option:hover {
        border-color: var(--primary);
        background: rgba(139, 92, 246, 0.06);
        transform: translateX(4px);
    }
    .quiz-option.selected {
        border-color: var(--primary);
        background: var(--primary-soft);
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15);
    }
    .quiz-option-emoji {
        font-size: 1.5rem;
        min-width: 36px;
        text-align: center;
    }
    .quiz-option-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text);
        line-height: 1.4;
    }

    .quiz-result-card {
        background: rgba(29, 35, 51, 0.5);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.6rem;
        animation: fadeIn 0.5s ease forwards;
        transition: all 0.3s ease;
    }
    .quiz-result-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.15);
    }
    .quiz-result-rank {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1rem;
        color: var(--text-muted);
        margin-bottom: 0.25rem;
    }
    .quiz-result-career {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.4rem;
    }
    .quiz-result-bar-bg {
        background: var(--surface);
        border-radius: 6px;
        height: 8px;
        overflow: hidden;
    }
    .quiz-result-bar-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 1s ease;
    }

</style>
"""
