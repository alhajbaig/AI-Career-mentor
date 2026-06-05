"""
AI Career Mentor - UI Component Helpers
Reusable HTML/Streamlit component functions for the main app.
"""

import streamlit as st
import plotly.graph_objects as go


def render_metric_card(icon: str, value: str, label: str, gradient: str = "1") -> str:
    """Render a premium metric card."""
    grad_map = {
        "1": "linear-gradient(135deg, #6C63FF 0%, #00D4AA 100%)",
        "2": "linear-gradient(135deg, #FF6B6B 0%, #FFA726 100%)",
        "3": "linear-gradient(135deg, #6C63FF 0%, #E040FB 100%)",
        "4": "linear-gradient(135deg, #00D4AA 0%, #26C6DA 100%)",
    }
    grad = grad_map.get(gradient, grad_map["1"])
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value" style="background: {grad}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def render_skill_tags(skills: list, tag_class: str = "neutral") -> str:
    """Render skill tags HTML."""
    tags = ""
    for s in skills:
        tags += f'<span class="skill-tag skill-tag-{tag_class}">{s}</span>'
    return f'<div style="margin: 0.5rem 0;">{tags}</div>'


def render_progress_bar(value: float, label: str = "", color: str = None) -> str:
    """Render a custom progress bar."""
    if color is None:
        if value >= 75:
            color = "#00D4AA"
        elif value >= 50:
            color = "#FFA726"
        else:
            color = "#FF6B6B"

    return f"""
    <div style="margin: 0.5rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #FAFAFA; font-size: 0.85rem; font-weight: 500;">{label}</span>
            <span style="color: {color}; font-size: 0.85rem; font-weight: 700;">{value:.0f}%</span>
        </div>
        <div class="progress-bar-custom">
            <div class="progress-fill" style="width: {value}%; background: {color};"></div>
        </div>
    </div>
    """


def render_score_gauge(score: int, max_score: int = 100, label: str = "") -> go.Figure:
    """Create a Plotly gauge chart for scores."""
    if score >= 75:
        color = "#00D4AA"
    elif score >= 50:
        color = "#FFA726"
    else:
        color = "#FF6B6B"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(suffix=f"/{max_score}", font=dict(size=36, color="white")),
        title=dict(text=label, font=dict(size=16, color="#9CA3AF")),
        gauge=dict(
            axis=dict(range=[0, max_score], tickcolor="#333", tickwidth=1,
                      dtick=25, tickfont=dict(color="#666", size=10)),
            bar=dict(color=color, thickness=0.8),
            bgcolor="rgba(26,29,41,0.8)",
            borderwidth=2,
            bordercolor="rgba(108,99,255,0.2)",
            steps=[
                dict(range=[0, max_score * 0.3], color="rgba(255,107,107,0.1)"),
                dict(range=[max_score * 0.3, max_score * 0.7], color="rgba(255,167,38,0.1)"),
                dict(range=[max_score * 0.7, max_score], color="rgba(0,212,170,0.1)"),
            ],
            threshold=dict(
                line=dict(color=color, width=3),
                thickness=0.8, value=score
            ),
        ),
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans"),
    )
    return fig


def render_career_bar_chart(predictions: list) -> go.Figure:
    """Create horizontal bar chart for career predictions."""
    careers = [p[0] for p in predictions][::-1]
    probs = [p[1] for p in predictions][::-1]

    colors = []
    for p in probs:
        if p >= 15:
            colors.append("#6C63FF")
        elif p >= 10:
            colors.append("#8B83FF")
        elif p >= 5:
            colors.append("#ABA3FF")
        else:
            colors.append("#CBC3FF")

    fig = go.Figure(go.Bar(
        x=probs,
        y=careers,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(width=0),
            cornerradius=6,
        ),
        text=[f"{p:.1f}%" for p in probs],
        textposition="outside",
        textfont=dict(size=12, color="white", family="Plus Jakarta Sans"),
    ))

    fig.update_layout(
        title=dict(text="🎯 Career Match Probabilities", font=dict(size=18, color="white", family="Outfit"), x=0.5),
        xaxis=dict(
            title="Match Probability (%)",
            showgrid=True, gridcolor="rgba(108,99,255,0.08)",
            color="#666", range=[0, max(probs) * 1.3],
            titlefont=dict(family="Plus Jakarta Sans"),
            tickfont=dict(family="Plus Jakarta Sans"),
        ),
        yaxis=dict(color="white", tickfont=dict(size=12, family="Plus Jakarta Sans")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=max(300, len(careers) * 50),
        margin=dict(l=20, r=60, t=50, b=40),
        hoverlabel=dict(bgcolor="#1A1D29", font_size=13, font_color="white", font_family="Plus Jakarta Sans"),
    )
    return fig


def render_readiness_radar(breakdown: dict) -> go.Figure:
    """Create radar chart for readiness breakdown."""
    categories = list(breakdown.keys())
    values = [breakdown[c]["score"] for c in categories]
    max_values = [breakdown[c]["max"] for c in categories]
    normalized = [(v / m * 100) if m > 0 else 0 for v, m in zip(values, max_values)]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=normalized + [normalized[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(108,99,255,0.15)",
        line=dict(color="#6C63FF", width=2),
        marker=dict(size=8, color="#6C63FF"),
        name="Your Score",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showline=False, tickfont=dict(color="#666")),
            angularaxis=dict(tickfont=dict(color="white", size=12)),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
        margin=dict(l=50, r=50, t=20, b=20),
    )
    return fig


def render_phase_card(phase: dict) -> str:
    """Render a learning phase card."""
    skills_html = ""
    for s in phase["skills"]:
        cls = "skill-tag-have" if s["completed"] else "skill-tag-missing"
        icon = "✅" if s["completed"] else "⬜"
        skills_html += f'<span class="skill-tag {cls}">{icon} {s["name"]}</span>'

    progress = phase["progress"]
    bar_color = "#00D4AA" if progress >= 75 else "#FFA726" if progress >= 40 else "#FF6B6B"

    return f"""
    <div class="phase-card" style="border-left: 4px solid {phase['color']};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="phase-title">{phase['phase']}</div>
            <span style="color: {bar_color}; font-weight: 700; font-size: 0.9rem;">{progress}%</span>
        </div>
        <div class="phase-duration">⏱️ {phase['duration']} • {phase['completed_count']}/{phase['total_count']} skills</div>
        <div class="progress-bar-custom">
            <div class="progress-fill" style="width: {progress}%; background: {bar_color};"></div>
        </div>
        <div style="margin-top: 0.5rem;">{skills_html}</div>
    </div>
    """
