"""
AI Career Mentor - Configuration & Constants
Contains all career data, skill mappings, course/project recommendations.
"""

import os

# ─── API Keys ────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# ─── Career Domains & Required Skills ────────────────────────────────────────
CAREER_SKILLS = {
    "AI Engineer": {
        "core": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
                 "NLP", "Computer Vision", "MLOps", "Docker", "Kubernetes", "Git"],
        "optional": ["Rust", "C++", "ONNX", "Triton", "Ray", "Spark"],
        "icon": "🤖"
    },
    "Data Scientist": {
        "core": ["Python", "SQL", "Machine Learning", "Statistics", "Pandas", "NumPy",
                 "Scikit-learn", "Data Visualization", "Tableau", "R", "Jupyter"],
        "optional": ["Spark", "Hadoop", "SAS", "SPSS", "Bayesian Methods"],
        "icon": "📊"
    },
    "Software Engineer": {
        "core": ["Python", "Java", "JavaScript", "Data Structures", "Algorithms", "SQL",
                 "Git", "REST API", "Docker", "System Design", "OOP"],
        "optional": ["Go", "Rust", "Kubernetes", "GraphQL", "Microservices"],
        "icon": "💻"
    },
    "Cloud Engineer": {
        "core": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
                 "Linux", "Networking", "CI/CD", "Python", "Bash"],
        "optional": ["Ansible", "Pulumi", "Vault", "Prometheus", "Grafana"],
        "icon": "☁️"
    },
    "Cybersecurity Analyst": {
        "core": ["Networking", "Linux", "Python", "Firewalls", "SIEM",
                 "Penetration Testing", "Cryptography", "Wireshark", "Nmap", "Incident Response"],
        "optional": ["Malware Analysis", "Forensics", "Burp Suite", "Metasploit"],
        "icon": "🔒"
    },
    "Data Analyst": {
        "core": ["SQL", "Excel", "Python", "Tableau", "Power BI", "Statistics",
                 "Data Cleaning", "Pandas", "Data Visualization", "ETL"],
        "optional": ["R", "Looker", "Google Analytics", "Alteryx"],
        "icon": "📈"
    },
    "Full Stack Developer": {
        "core": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL",
                 "Git", "REST API", "MongoDB", "TypeScript", "Docker"],
        "optional": ["Next.js", "GraphQL", "Redis", "AWS", "Tailwind CSS"],
        "icon": "🌐"
    },
    "DevOps Engineer": {
        "core": ["Docker", "Kubernetes", "CI/CD", "Jenkins", "Linux", "Git",
                 "Terraform", "AWS", "Python", "Bash", "Monitoring"],
        "optional": ["ArgoCD", "Helm", "Ansible", "Prometheus", "ELK Stack"],
        "icon": "⚙️"
    },
    "ML Engineer": {
        "core": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
                 "Docker", "MLOps", "SQL", "Git", "AWS", "Data Pipelines"],
        "optional": ["Kubeflow", "MLflow", "Airflow", "Spark", "Feature Store"],
        "icon": "🧠"
    },
    "Blockchain Developer": {
        "core": ["Solidity", "Ethereum", "Smart Contracts", "Web3.js", "JavaScript",
                 "Cryptography", "DeFi", "Git", "Node.js", "Truffle"],
        "optional": ["Rust", "Hyperledger", "IPFS", "Polygon", "Hardhat"],
        "icon": "⛓️"
    },
}

# ─── Skill Synonyms (for fuzzy matching) ─────────────────────────────────────
SKILL_SYNONYMS = {
    "ml": "Machine Learning", "dl": "Deep Learning", "ai": "Artificial Intelligence",
    "nlp": "NLP", "cv": "Computer Vision", "ds": "Data Structures",
    "dsa": "Data Structures", "algo": "Algorithms", "tf": "TensorFlow",
    "pytorch": "PyTorch", "sk-learn": "Scikit-learn", "sklearn": "Scikit-learn",
    "js": "JavaScript", "ts": "TypeScript", "react.js": "React",
    "reactjs": "React", "node": "Node.js", "nodejs": "Node.js",
    "mongo": "MongoDB", "postgres": "PostgreSQL", "k8s": "Kubernetes",
    "aws": "AWS", "gcp": "GCP", "azure": "Azure",
    "html5": "HTML", "css3": "CSS", "cpp": "C++", "c++": "C++",
    "data science": "Data Science", "power bi": "Power BI",
    "ci cd": "CI/CD", "ci/cd": "CI/CD", "rest": "REST API",
    "restful": "REST API", "oop": "OOP", "dbms": "SQL",
    "rdbms": "SQL", "mysql": "SQL", "sqlite": "SQL",
    "tensorflow": "TensorFlow", "keras": "TensorFlow",
    "scikit-learn": "Scikit-learn", "pandas": "Pandas", "numpy": "NumPy",
    "matplotlib": "Data Visualization", "seaborn": "Data Visualization",
    "plotly": "Data Visualization", "docker": "Docker",
    "kubernetes": "Kubernetes", "linux": "Linux", "git": "Git",
    "github": "Git", "gitlab": "Git", "python": "Python",
    "java": "Java", "javascript": "JavaScript", "sql": "SQL",
    "r": "R", "bash": "Bash", "shell": "Bash",
    "deep learning": "Deep Learning", "machine learning": "Machine Learning",
    "natural language processing": "NLP",
    "computer vision": "Computer Vision",
}

# ─── Project Recommendations ─────────────────────────────────────────────────
PROJECT_RECOMMENDATIONS = {
    "AI Engineer": {
        "Beginner": [
            {"name": "Iris Flower Classification", "skills": ["Python", "Scikit-learn"], "desc": "Classify iris species using classic ML algorithms"},
            {"name": "MNIST Digit Recognition", "skills": ["Python", "TensorFlow"], "desc": "Build a neural network to recognize handwritten digits"},
            {"name": "Sentiment Analysis Tool", "skills": ["Python", "NLP"], "desc": "Analyze sentiment of movie reviews using NLP"},
        ],
        "Intermediate": [
            {"name": "Resume Screening System", "skills": ["Python", "NLP", "Scikit-learn"], "desc": "Auto-classify resumes by job category using NLP"},
            {"name": "Object Detection App", "skills": ["Python", "Computer Vision", "TensorFlow"], "desc": "Real-time object detection using YOLO/SSD"},
            {"name": "Chatbot with Intent Recognition", "skills": ["Python", "NLP", "Deep Learning"], "desc": "Build an intent-based chatbot with transformer models"},
        ],
        "Advanced": [
            {"name": "RAG-Powered Knowledge Assistant", "skills": ["Python", "NLP", "LangChain"], "desc": "Build a retrieval-augmented generation system"},
            {"name": "AI Career Mentor Platform", "skills": ["Python", "ML", "NLP", "GenAI"], "desc": "Full-stack AI career guidance system"},
            {"name": "Medical Image Diagnosis AI", "skills": ["Python", "Deep Learning", "Computer Vision"], "desc": "Diagnose diseases from X-ray/MRI images"},
        ],
    },
    "Data Scientist": {
        "Beginner": [
            {"name": "House Price Prediction", "skills": ["Python", "Pandas", "Scikit-learn"], "desc": "Predict house prices using regression models"},
            {"name": "Titanic Survival Analysis", "skills": ["Python", "Pandas", "Data Visualization"], "desc": "Analyze and predict Titanic passenger survival"},
            {"name": "Sales Dashboard", "skills": ["Python", "Plotly", "Pandas"], "desc": "Interactive sales analytics dashboard"},
        ],
        "Intermediate": [
            {"name": "Customer Churn Prediction", "skills": ["Python", "ML", "Feature Engineering"], "desc": "Predict and analyze customer churn patterns"},
            {"name": "A/B Testing Framework", "skills": ["Python", "Statistics", "Pandas"], "desc": "Statistical framework for experiment analysis"},
            {"name": "Recommendation Engine", "skills": ["Python", "ML", "Collaborative Filtering"], "desc": "Build a movie/product recommendation system"},
        ],
        "Advanced": [
            {"name": "Time Series Forecasting Platform", "skills": ["Python", "Deep Learning", "Statistics"], "desc": "Forecast stock/weather using LSTM/Prophet"},
            {"name": "NLP-Powered Survey Analyzer", "skills": ["Python", "NLP", "Topic Modeling"], "desc": "Extract insights from survey responses using NLP"},
            {"name": "End-to-End ML Pipeline", "skills": ["Python", "MLOps", "Docker"], "desc": "Production ML pipeline with monitoring and CI/CD"},
        ],
    },
    "Software Engineer": {
        "Beginner": [
            {"name": "Todo App with REST API", "skills": ["Python", "Flask", "SQL"], "desc": "Full CRUD application with REST API backend"},
            {"name": "CLI Task Manager", "skills": ["Python", "OOP", "File I/O"], "desc": "Command-line task management tool with persistence"},
            {"name": "Calculator with Unit Tests", "skills": ["Python", "Testing", "OOP"], "desc": "Calculator app with comprehensive test coverage"},
        ],
        "Intermediate": [
            {"name": "URL Shortener Service", "skills": ["Python", "Flask", "SQL", "Docker"], "desc": "Scalable URL shortener with analytics"},
            {"name": "Real-time Chat Application", "skills": ["JavaScript", "Node.js", "WebSocket"], "desc": "Live chat app with rooms and file sharing"},
            {"name": "E-Commerce Backend", "skills": ["Python", "Django", "PostgreSQL"], "desc": "Full e-commerce API with auth and payments"},
        ],
        "Advanced": [
            {"name": "Distributed Task Queue", "skills": ["Python", "Redis", "Docker", "System Design"], "desc": "Celery-like distributed task processing system"},
            {"name": "Microservices Architecture", "skills": ["Docker", "Kubernetes", "gRPC"], "desc": "Decomposed application with service mesh"},
            {"name": "Compiler/Interpreter", "skills": ["Python", "Data Structures", "Algorithms"], "desc": "Build a programming language interpreter"},
        ],
    },
    "Cloud Engineer": {
        "Beginner": [
            {"name": "Static Website on S3", "skills": ["AWS", "HTML", "DNS"], "desc": "Deploy a static website with CloudFront CDN"},
            {"name": "Linux Server Setup", "skills": ["Linux", "Bash", "Networking"], "desc": "Configure a web server from scratch"},
            {"name": "Docker Containerization", "skills": ["Docker", "Linux", "Python"], "desc": "Containerize and orchestrate applications"},
        ],
        "Intermediate": [
            {"name": "CI/CD Pipeline", "skills": ["Jenkins", "Docker", "Git", "AWS"], "desc": "Automated build, test, and deploy pipeline"},
            {"name": "Infrastructure as Code", "skills": ["Terraform", "AWS", "Python"], "desc": "Manage cloud infra with Terraform modules"},
            {"name": "Kubernetes Cluster", "skills": ["Kubernetes", "Docker", "Helm"], "desc": "Deploy and manage a K8s cluster with monitoring"},
        ],
        "Advanced": [
            {"name": "Multi-Cloud Architecture", "skills": ["AWS", "GCP", "Terraform"], "desc": "Design fault-tolerant multi-cloud infrastructure"},
            {"name": "Serverless Data Pipeline", "skills": ["AWS Lambda", "S3", "DynamoDB"], "desc": "Event-driven serverless data processing"},
            {"name": "Cloud Security Hardening", "skills": ["AWS", "IAM", "VPC", "Encryption"], "desc": "Implement zero-trust cloud security framework"},
        ],
    },
}

# ─── Course Recommendations ──────────────────────────────────────────────────
COURSE_RECOMMENDATIONS = {
    "Python": [
        {"title": "Python for Everybody", "platform": "Coursera", "url": "https://www.coursera.org/specializations/python", "level": "Beginner"},
        {"title": "Automate the Boring Stuff", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", "level": "Beginner"},
    ],
    "Machine Learning": [
        {"title": "Machine Learning Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "level": "Intermediate"},
        {"title": "ML Course by Andrew Ng", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=jGwO_UgTS7I", "level": "Beginner"},
    ],
    "Deep Learning": [
        {"title": "Deep Learning Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/deep-learning", "level": "Intermediate"},
        {"title": "PyTorch for Deep Learning", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "level": "Intermediate"},
    ],
    "SQL": [
        {"title": "SQL for Data Science", "platform": "Coursera", "url": "https://www.coursera.org/learn/sql-for-data-science", "level": "Beginner"},
        {"title": "MySQL Full Course", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=7S_tz1z_5bA", "level": "Beginner"},
    ],
    "Docker": [
        {"title": "Docker Mastery", "platform": "Udemy", "url": "https://www.udemy.com/course/docker-mastery/", "level": "Intermediate"},
        {"title": "Docker in 100 Seconds", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=Gjnup-PuquQ", "level": "Beginner"},
    ],
    "TensorFlow": [
        {"title": "TensorFlow Developer Certificate", "platform": "Coursera", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice", "level": "Intermediate"},
        {"title": "TensorFlow 2.0 Complete Course", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=tPYj3fFJGjk", "level": "Beginner"},
    ],
    "AWS": [
        {"title": "AWS Cloud Practitioner", "platform": "Coursera", "url": "https://www.coursera.org/learn/aws-cloud-practitioner-essentials", "level": "Beginner"},
        {"title": "AWS Certified Solutions Architect", "platform": "Udemy", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate/", "level": "Intermediate"},
    ],
    "Kubernetes": [
        {"title": "Kubernetes for Beginners", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "level": "Beginner"},
        {"title": "CKA Certification Course", "platform": "Udemy", "url": "https://www.udemy.com/course/certified-kubernetes-administrator/", "level": "Advanced"},
    ],
    "NLP": [
        {"title": "NLP Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/natural-language-processing", "level": "Intermediate"},
        {"title": "Hugging Face NLP Course", "platform": "Hugging Face", "url": "https://huggingface.co/learn/nlp-course", "level": "Intermediate"},
    ],
    "Git": [
        {"title": "Git & GitHub Crash Course", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "level": "Beginner"},
    ],
    "React": [
        {"title": "React - The Complete Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide/", "level": "Beginner"},
        {"title": "Full React Course", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=bMknfKXIFA8", "level": "Beginner"},
    ],
    "JavaScript": [
        {"title": "JavaScript - The Complete Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced/", "level": "Beginner"},
        {"title": "JavaScript Full Course", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=PkZNo7MFNFg", "level": "Beginner"},
    ],
    "Data Visualization": [
        {"title": "Data Visualization with Python", "platform": "Coursera", "url": "https://www.coursera.org/learn/python-for-data-visualization", "level": "Beginner"},
    ],
    "MLOps": [
        {"title": "MLOps Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops", "level": "Advanced"},
        {"title": "MLOps Zoomcamp", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=s0uaFZSzwfI", "level": "Intermediate"},
    ],
    "PyTorch": [
        {"title": "PyTorch for Deep Learning", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "level": "Intermediate"},
    ],
    "Statistics": [
        {"title": "Statistics with Python", "platform": "Coursera", "url": "https://www.coursera.org/specializations/statistics-with-python", "level": "Beginner"},
    ],
    "Computer Vision": [
        {"title": "CS231n: CNNs for Visual Recognition", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=vT1JzLTH4G4", "level": "Advanced"},
    ],
    "Linux": [
        {"title": "Linux Command Line Basics", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=ZtqBQ68cfJc", "level": "Beginner"},
    ],
    "System Design": [
        {"title": "System Design Interview Course", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=FSR1s2b-l_I", "level": "Advanced"},
    ],
}

# ─── Interview Question Templates ────────────────────────────────────────────
INTERVIEW_QUESTIONS = {
    "AI Engineer": {
        "Technical": [
            "Explain the difference between supervised, unsupervised, and reinforcement learning.",
            "What is backpropagation and how does it work?",
            "Explain gradient descent and its variants (SGD, Adam, RMSProp).",
            "What are attention mechanisms in transformers?",
            "How do you handle overfitting in deep learning models?",
            "Explain the architecture of a transformer model.",
            "What is transfer learning and when would you use it?",
            "Describe the bias-variance tradeoff.",
            "What is batch normalization and why is it useful?",
            "Explain the difference between CNN, RNN, and Transformer architectures.",
        ],
        "HR": [
            "Tell me about yourself and your journey into AI.",
            "Describe a challenging AI project you worked on.",
            "How do you stay updated with the latest AI research?",
            "Where do you see AI heading in the next 5 years?",
            "How do you handle failure in experiments?",
        ],
    },
    "Data Scientist": {
        "Technical": [
            "Explain the difference between L1 and L2 regularization.",
            "What is cross-validation and why is it important?",
            "Explain the Central Limit Theorem.",
            "What is the curse of dimensionality?",
            "How do you handle missing data in a dataset?",
            "Explain A/B testing methodology.",
            "What is feature engineering? Give examples.",
            "Describe the ROC-AUC curve and its interpretation.",
            "What is the difference between bagging and boosting?",
            "How would you detect and handle outliers?",
        ],
        "HR": [
            "Describe a data-driven decision you helped make.",
            "How do you communicate technical findings to non-technical stakeholders?",
            "Tell me about a time you found an unexpected insight in data.",
            "How do you prioritize which problems to solve with data science?",
        ],
    },
    "Software Engineer": {
        "Technical": [
            "Explain the SOLID principles of object-oriented design.",
            "What is the time complexity of common sorting algorithms?",
            "Describe the differences between SQL and NoSQL databases.",
            "Explain RESTful API design principles.",
            "What is a microservices architecture?",
            "How does garbage collection work?",
            "Explain the CAP theorem.",
            "What are design patterns? Name a few you've used.",
            "How would you design a URL shortening service?",
            "Explain the difference between processes and threads.",
        ],
        "HR": [
            "Describe your approach to debugging complex issues.",
            "How do you handle disagreements with team members about technical decisions?",
            "Tell me about a project you're most proud of.",
        ],
    },
    "Cloud Engineer": {
        "Technical": [
            "Explain the shared responsibility model in cloud computing.",
            "What is Infrastructure as Code?",
            "Describe the differences between containers and virtual machines.",
            "How does auto-scaling work in AWS?",
            "What is a VPC and why is it important?",
            "Explain CI/CD pipeline stages.",
            "What is service mesh and when would you use it?",
            "How do you ensure high availability in cloud architectures?",
        ],
        "HR": [
            "Describe a time you had to troubleshoot a production outage.",
            "How do you approach learning new cloud services?",
        ],
    },
}

# ─── Lottie Animation URLs ───────────────────────────────────────────────────
LOTTIE_URLS = {
    "career": "https://lottie.host/6e9e3c64-8a6f-4c3a-9a1a-7c3b5e4d8f2a/aBcDeFgHiJ.json",
    "ai": "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json",
    "resume": "https://assets5.lottiefiles.com/packages/lf20_w51pcehl.json",
    "rocket": "https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json",
    "success": "https://assets5.lottiefiles.com/packages/lf20_touohxv0.json",
}
