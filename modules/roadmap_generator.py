"""
AI Career Mentor - Roadmap Generator
Generates personalized career roadmaps with interactive visualizations.
"""

import plotly.graph_objects as go
from modules.config import CAREER_SKILLS


# ─── Roadmap Templates ───────────────────────────────────────────────────────
ROADMAP_TEMPLATES = {
    "AI Engineer": [
        {"phase": "Foundation", "duration": "1-2 months", "skills": ["Python", "Git", "Linux"], "color": "#6C63FF"},
        {"phase": "Mathematics", "duration": "1-2 months", "skills": ["Linear Algebra", "Statistics", "Probability", "Calculus"], "color": "#7C73FF"},
        {"phase": "Data Science Basics", "duration": "1-2 months", "skills": ["NumPy", "Pandas", "Data Visualization", "SQL"], "color": "#8B83FF"},
        {"phase": "Machine Learning", "duration": "2-3 months", "skills": ["Scikit-learn", "Supervised Learning", "Unsupervised Learning", "Model Evaluation"], "color": "#9B93FF"},
        {"phase": "Deep Learning", "duration": "2-3 months", "skills": ["TensorFlow", "PyTorch", "CNNs", "RNNs", "Transformers"], "color": "#ABA3FF"},
        {"phase": "Specialization", "duration": "2-3 months", "skills": ["NLP", "Computer Vision", "GANs", "Reinforcement Learning"], "color": "#BBB3FF"},
        {"phase": "MLOps & Production", "duration": "1-2 months", "skills": ["Docker", "Kubernetes", "MLOps", "Model Deployment", "CI/CD"], "color": "#CBC3FF"},
        {"phase": "Advanced & Projects", "duration": "Ongoing", "skills": ["Research Papers", "Kaggle Competitions", "Open Source", "Portfolio Projects"], "color": "#DBD3FF"},
    ],
    "Data Scientist": [
        {"phase": "Foundation", "duration": "1-2 months", "skills": ["Python", "Git", "Jupyter"], "color": "#00D4AA"},
        {"phase": "Mathematics & Stats", "duration": "1-2 months", "skills": ["Statistics", "Probability", "Linear Algebra", "Hypothesis Testing"], "color": "#10E4BA"},
        {"phase": "Data Manipulation", "duration": "1-2 months", "skills": ["Pandas", "NumPy", "SQL", "Data Cleaning"], "color": "#20F4CA"},
        {"phase": "Visualization", "duration": "1 month", "skills": ["Matplotlib", "Seaborn", "Plotly", "Tableau"], "color": "#30FFDA"},
        {"phase": "Machine Learning", "duration": "2-3 months", "skills": ["Scikit-learn", "Feature Engineering", "Model Selection", "Cross-validation"], "color": "#40FFEA"},
        {"phase": "Advanced ML", "duration": "2 months", "skills": ["XGBoost", "Ensemble Methods", "Time Series", "NLP Basics"], "color": "#50FFFA"},
        {"phase": "Big Data", "duration": "1-2 months", "skills": ["Spark", "Hadoop", "Cloud Platforms", "ETL Pipelines"], "color": "#60FFFF"},
        {"phase": "Projects & Portfolio", "duration": "Ongoing", "skills": ["End-to-end Projects", "Kaggle", "Blog Writing", "Presentations"], "color": "#70FFFF"},
    ],
    "Software Engineer": [
        {"phase": "Programming Basics", "duration": "1-2 months", "skills": ["Python", "Java", "Git", "Terminal"], "color": "#FF6B6B"},
        {"phase": "DSA", "duration": "2-3 months", "skills": ["Data Structures", "Algorithms", "Problem Solving", "LeetCode"], "color": "#FF7B7B"},
        {"phase": "OOP & Design", "duration": "1-2 months", "skills": ["OOP", "Design Patterns", "SOLID Principles", "Clean Code"], "color": "#FF8B8B"},
        {"phase": "Databases", "duration": "1 month", "skills": ["SQL", "PostgreSQL", "MongoDB", "Redis"], "color": "#FF9B9B"},
        {"phase": "Web Development", "duration": "2-3 months", "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"], "color": "#FFABAB"},
        {"phase": "Backend & APIs", "duration": "2 months", "skills": ["REST API", "System Design", "Authentication", "Testing"], "color": "#FFBBBB"},
        {"phase": "DevOps", "duration": "1-2 months", "skills": ["Docker", "CI/CD", "Cloud (AWS)", "Kubernetes"], "color": "#FFCBCB"},
        {"phase": "Career Prep", "duration": "Ongoing", "skills": ["System Design", "Open Source", "Portfolio", "Mock Interviews"], "color": "#FFDBDB"},
    ],
    "Cloud Engineer": [
        {"phase": "IT Fundamentals", "duration": "1-2 months", "skills": ["Linux", "Networking", "TCP/IP", "DNS"], "color": "#FFA726"},
        {"phase": "Scripting", "duration": "1 month", "skills": ["Python", "Bash", "PowerShell", "Git"], "color": "#FFB736"},
        {"phase": "Cloud Basics", "duration": "2-3 months", "skills": ["AWS", "IAM", "EC2", "S3", "VPC"], "color": "#FFC746"},
        {"phase": "Containers", "duration": "1-2 months", "skills": ["Docker", "Kubernetes", "Container Orchestration"], "color": "#FFD756"},
        {"phase": "IaC & Automation", "duration": "1-2 months", "skills": ["Terraform", "Ansible", "CloudFormation"], "color": "#FFE766"},
        {"phase": "CI/CD & DevOps", "duration": "1-2 months", "skills": ["Jenkins", "GitHub Actions", "ArgoCD", "GitOps"], "color": "#FFF776"},
        {"phase": "Monitoring", "duration": "1 month", "skills": ["Prometheus", "Grafana", "ELK Stack", "CloudWatch"], "color": "#FFFF86"},
        {"phase": "Certifications", "duration": "Ongoing", "skills": ["AWS SAA", "CKA", "GCP Associate", "Azure Fundamentals"], "color": "#FFFF96"},
    ],
    "Cybersecurity Analyst": [
        {"phase": "IT Basics", "duration": "1-2 months", "skills": ["Networking", "Linux", "Windows", "TCP/IP"], "color": "#E040FB"},
        {"phase": "Security Fundamentals", "duration": "1-2 months", "skills": ["CIA Triad", "Cryptography", "Firewalls", "VPN"], "color": "#EA50FF"},
        {"phase": "Tools & Recon", "duration": "1-2 months", "skills": ["Nmap", "Wireshark", "Burp Suite", "Metasploit"], "color": "#F460FF"},
        {"phase": "Ethical Hacking", "duration": "2-3 months", "skills": ["Penetration Testing", "OWASP Top 10", "Web App Security"], "color": "#FE70FF"},
        {"phase": "Defense", "duration": "1-2 months", "skills": ["SIEM", "Incident Response", "Forensics", "Malware Analysis"], "color": "#FF80FF"},
        {"phase": "Compliance", "duration": "1 month", "skills": ["ISO 27001", "GDPR", "HIPAA", "Risk Assessment"], "color": "#FF90FF"},
        {"phase": "Certifications", "duration": "Ongoing", "skills": ["CompTIA Security+", "CEH", "OSCP", "CISSP"], "color": "#FFA0FF"},
    ],
    "Full Stack Developer": [
        {"phase": "Frontend Basics", "duration": "1-2 months", "skills": ["HTML", "CSS", "JavaScript", "Responsive Design"], "color": "#26C6DA"},
        {"phase": "Frontend Framework", "duration": "2 months", "skills": ["React", "TypeScript", "State Management", "Tailwind CSS"], "color": "#36D6EA"},
        {"phase": "Backend", "duration": "2 months", "skills": ["Node.js", "Express", "REST API", "Authentication"], "color": "#46E6FA"},
        {"phase": "Databases", "duration": "1-2 months", "skills": ["SQL", "MongoDB", "Redis", "ORM"], "color": "#56F6FF"},
        {"phase": "DevOps & Deploy", "duration": "1-2 months", "skills": ["Docker", "CI/CD", "AWS/Vercel", "Nginx"], "color": "#66FFFF"},
        {"phase": "Advanced", "duration": "Ongoing", "skills": ["GraphQL", "WebSocket", "Microservices", "System Design"], "color": "#76FFFF"},
    ],
    "Data Analyst": [
        {"phase": "Foundation", "duration": "1 month", "skills": ["Excel", "Statistics", "SQL Basics"], "color": "#66BB6A"},
        {"phase": "SQL Mastery", "duration": "1-2 months", "skills": ["SQL", "Joins", "Window Functions", "CTEs"], "color": "#76CB7A"},
        {"phase": "Python for Data", "duration": "1-2 months", "skills": ["Python", "Pandas", "NumPy"], "color": "#86DB8A"},
        {"phase": "Visualization", "duration": "1-2 months", "skills": ["Tableau", "Power BI", "Plotly", "Storytelling"], "color": "#96EB9A"},
        {"phase": "Analytics", "duration": "1-2 months", "skills": ["A/B Testing", "Cohort Analysis", "Funnel Analysis"], "color": "#A6FBAA"},
        {"phase": "Advanced", "duration": "Ongoing", "skills": ["Machine Learning Basics", "ETL", "Data Modeling"], "color": "#B6FFBA"},
    ],
    "DevOps Engineer": [
        {"phase": "Linux & Scripting", "duration": "1-2 months", "skills": ["Linux", "Bash", "Python", "Git"], "color": "#EF5350"},
        {"phase": "Networking", "duration": "1 month", "skills": ["TCP/IP", "DNS", "HTTP", "Load Balancing"], "color": "#FF6360"},
        {"phase": "Containers", "duration": "1-2 months", "skills": ["Docker", "Docker Compose", "Container Security"], "color": "#FF7370"},
        {"phase": "Orchestration", "duration": "2 months", "skills": ["Kubernetes", "Helm", "Service Mesh"], "color": "#FF8380"},
        {"phase": "CI/CD", "duration": "1-2 months", "skills": ["Jenkins", "GitHub Actions", "ArgoCD"], "color": "#FF9390"},
        {"phase": "IaC", "duration": "1-2 months", "skills": ["Terraform", "Ansible", "Pulumi"], "color": "#FFA3A0"},
        {"phase": "Monitoring & Cloud", "duration": "Ongoing", "skills": ["Prometheus", "Grafana", "AWS", "ELK Stack"], "color": "#FFB3B0"},
    ],
    "ML Engineer": [
        {"phase": "Foundation", "duration": "1-2 months", "skills": ["Python", "Git", "Linux", "SQL"], "color": "#AB47BC"},
        {"phase": "ML Fundamentals", "duration": "2-3 months", "skills": ["Scikit-learn", "Feature Engineering", "Model Evaluation"], "color": "#BB57CC"},
        {"phase": "Deep Learning", "duration": "2 months", "skills": ["TensorFlow", "PyTorch", "Neural Networks"], "color": "#CB67DC"},
        {"phase": "Data Engineering", "duration": "1-2 months", "skills": ["Data Pipelines", "Spark", "Airflow"], "color": "#DB77EC"},
        {"phase": "MLOps", "duration": "2-3 months", "skills": ["Docker", "MLflow", "Kubeflow", "Model Serving"], "color": "#EB87FC"},
        {"phase": "Production ML", "duration": "Ongoing", "skills": ["A/B Testing", "Monitoring", "Feature Stores", "CI/CD for ML"], "color": "#FB97FF"},
    ],
    "Blockchain Developer": [
        {"phase": "Web Basics", "duration": "1-2 months", "skills": ["JavaScript", "Node.js", "Git"], "color": "#FFD54F"},
        {"phase": "Blockchain Fundamentals", "duration": "1-2 months", "skills": ["Cryptography", "Consensus", "Distributed Systems"], "color": "#FFE55F"},
        {"phase": "Ethereum & Solidity", "duration": "2-3 months", "skills": ["Solidity", "Ethereum", "Smart Contracts", "ERC Standards"], "color": "#FFF56F"},
        {"phase": "DApp Development", "duration": "2 months", "skills": ["Web3.js", "Ethers.js", "Truffle", "Hardhat"], "color": "#FFFF7F"},
        {"phase": "DeFi & Advanced", "duration": "Ongoing", "skills": ["DeFi Protocols", "NFTs", "Layer 2", "Cross-chain"], "color": "#FFFF8F"},
    ],
}


def get_roadmap(career: str, current_skills: list = None) -> list:
    """Get roadmap phases for a career, marking completed skills."""
    current_skills = current_skills or []
    current_lower = set(s.lower() for s in current_skills)

    template = ROADMAP_TEMPLATES.get(career)
    if not template:
        # Try partial match
        for key in ROADMAP_TEMPLATES:
            if career.lower() in key.lower() or key.lower() in career.lower():
                template = ROADMAP_TEMPLATES[key]
                break

    if not template:
        # Default generic roadmap
        template = ROADMAP_TEMPLATES.get("Software Engineer", [])

    roadmap = []
    for phase in template:
        skills_status = []
        for skill in phase["skills"]:
            completed = skill.lower() in current_lower
            skills_status.append({"name": skill, "completed": completed})

        completed_count = sum(1 for s in skills_status if s["completed"])
        total = len(skills_status)
        progress = (completed_count / total * 100) if total > 0 else 0

        roadmap.append({
            "phase": phase["phase"],
            "duration": phase["duration"],
            "skills": skills_status,
            "color": phase["color"],
            "progress": round(progress),
            "completed_count": completed_count,
            "total_count": total,
        })

    return roadmap


def create_roadmap_visualization(roadmap: list, career: str) -> go.Figure:
    """Create an interactive Plotly roadmap visualization."""
    fig = go.Figure()

    n_phases = len(roadmap)
    y_positions = list(range(n_phases - 1, -1, -1))

    for i, (phase, y_pos) in enumerate(zip(roadmap, y_positions)):
        progress = phase["progress"]
        color = phase["color"]
        skills_text = "<br>".join(
            [f"{'✅' if s['completed'] else '⬜'} {s['name']}" for s in phase["skills"]]
        )

        # Phase node
        fig.add_trace(go.Scatter(
            x=[0.5], y=[y_pos],
            mode="markers+text",
            marker=dict(
                size=50 + progress * 0.3,
                color=color,
                opacity=0.9,
                line=dict(width=3, color="white"),
                symbol="circle",
            ),
            text=f"<b>{phase['phase']}</b>",
            textposition="middle center",
            textfont=dict(size=11, color="white"),
            hovertext=f"<b>{phase['phase']}</b><br>"
                      f"Duration: {phase['duration']}<br>"
                      f"Progress: {progress}%<br><br>"
                      f"{skills_text}",
            hoverinfo="text",
            showlegend=False,
        ))

        # Progress bar
        fig.add_trace(go.Bar(
            x=[progress / 100],
            y=[y_pos],
            orientation="h",
            marker=dict(color=color, opacity=0.6),
            base=1.2,
            width=0.4,
            hoverinfo="skip",
            showlegend=False,
        ))

        # Progress text
        fig.add_trace(go.Scatter(
            x=[2.4], y=[y_pos],
            mode="text",
            text=f"{progress}%",
            textfont=dict(size=12, color=color),
            hoverinfo="skip",
            showlegend=False,
        ))

        # Duration label
        fig.add_trace(go.Scatter(
            x=[-0.5], y=[y_pos],
            mode="text",
            text=f"<b>{phase['duration']}</b>",
            textfont=dict(size=10, color="#888"),
            hoverinfo="skip",
            showlegend=False,
        ))

        # Connector line
        if i < n_phases - 1:
            next_y = y_positions[i + 1]
            fig.add_trace(go.Scatter(
                x=[0.5, 0.5], y=[y_pos - 0.3, next_y + 0.3],
                mode="lines",
                line=dict(color="#444", width=2, dash="dot"),
                hoverinfo="skip",
                showlegend=False,
            ))

    fig.update_layout(
        title=dict(
            text=f"🗺️ {career} Learning Roadmap",
            font=dict(size=20, color="white"),
            x=0.5,
        ),
        xaxis=dict(
            showgrid=False, showticklabels=False, zeroline=False,
            range=[-1.2, 3],
        ),
        yaxis=dict(
            showgrid=False, showticklabels=False, zeroline=False,
            range=[-1, n_phases],
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=max(400, n_phases * 100),
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="#1A1D29",
            font_size=13,
            font_color="white",
        ),
    )

    return fig


def create_skill_network(career: str, current_skills: list = None) -> go.Figure:
    """Create an interactive skill dependency network graph."""
    current_skills = current_skills or []
    current_lower = set(s.lower() for s in current_skills)

    career_data = CAREER_SKILLS.get(career, {})
    core = career_data.get("core", [])
    optional = career_data.get("optional", [])

    nodes_x, nodes_y, node_colors, node_sizes, node_texts, hover_texts = [], [], [], [], [], []
    edge_x, edge_y = [], []

    # Center node (career)
    nodes_x.append(0)
    nodes_y.append(0)
    node_colors.append("#6C63FF")
    node_sizes.append(40)
    node_texts.append(career)
    hover_texts.append(f"<b>{career}</b><br>Target Career")

    import math
    # Core skills in inner ring
    for i, skill in enumerate(core):
        angle = 2 * math.pi * i / len(core)
        x = 2 * math.cos(angle)
        y = 2 * math.sin(angle)
        nodes_x.append(x)
        nodes_y.append(y)
        has_skill = skill.lower() in current_lower
        node_colors.append("#00D4AA" if has_skill else "#FF6B6B")
        node_sizes.append(25)
        node_texts.append(skill)
        status = "✅ You have this" if has_skill else "❌ Need to learn"
        hover_texts.append(f"<b>{skill}</b><br>Core Skill<br>{status}")

        edge_x.extend([0, x, None])
        edge_y.extend([0, y, None])

    # Optional skills in outer ring
    for i, skill in enumerate(optional):
        angle = 2 * math.pi * i / max(len(optional), 1) + 0.3
        x = 3.5 * math.cos(angle)
        y = 3.5 * math.sin(angle)
        nodes_x.append(x)
        nodes_y.append(y)
        has_skill = skill.lower() in current_lower
        node_colors.append("#00D4AA" if has_skill else "#FFA726")
        node_sizes.append(18)
        node_texts.append(skill)
        status = "✅ You have this" if has_skill else "📌 Optional"
        hover_texts.append(f"<b>{skill}</b><br>Optional Skill<br>{status}")

        edge_x.extend([0, x, None])
        edge_y.extend([0, y, None])

    fig = go.Figure()

    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=1, color="rgba(100,100,100,0.4)"),
        hoverinfo="skip", showlegend=False,
    ))

    # Nodes
    fig.add_trace(go.Scatter(
        x=nodes_x, y=nodes_y, mode="markers+text",
        marker=dict(size=node_sizes, color=node_colors,
                    line=dict(width=2, color="rgba(255,255,255,0.3)")),
        text=node_texts,
        textposition="top center",
        textfont=dict(size=9, color="white"),
        hovertext=hover_texts,
        hoverinfo="text",
        showlegend=False,
    ))

    fig.update_layout(
        title=dict(
            text=f"🕸️ {career} Skill Network",
            font=dict(size=18, color="white"), x=0.5,
        ),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, scaleanchor="x"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=550,
        margin=dict(l=20, r=20, t=50, b=20),
        hoverlabel=dict(bgcolor="#1A1D29", font_size=12, font_color="white"),
    )

    return fig
