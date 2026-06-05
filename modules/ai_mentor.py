"""
AI Career Mentor - AI Mentor Chatbot
Powered by Groq API for personalized career counseling.
"""

import json


def get_groq_client(api_key: str):
    """Initialize Groq client."""
    try:
        from groq import Groq
        return Groq(api_key=api_key)
    except ImportError:
        return None
    except Exception:
        return None


def build_system_prompt(user_context: dict) -> str:
    """Build a rich system prompt with user context."""
    prompt = """You are an expert AI Career Mentor — a warm, knowledgeable, and highly personalized career counselor for students and early-career professionals in tech.

Your personality:
- Encouraging but honest — you celebrate progress while being transparent about gaps
- You speak in a clear, structured manner using bullet points and headers
- You give actionable, specific advice — not generic platitudes
- You reference the student's actual data (skills, scores, predicted career) in every response
- You use relevant emojis to make responses engaging

YOUR STUDENT'S PROFILE:
"""
    if user_context.get("predicted_career"):
        prompt += f"\n🎯 Predicted Career Path: {user_context['predicted_career']}"

    if user_context.get("current_skills"):
        prompt += f"\n💡 Current Skills: {', '.join(user_context['current_skills'])}"

    if user_context.get("missing_skills"):
        prompt += f"\n📌 Missing Skills (Skill Gap): {', '.join(user_context['missing_skills'])}"

    if user_context.get("resume_score"):
        prompt += f"\n📄 Resume Score: {user_context['resume_score']}/100"

    if user_context.get("readiness_score"):
        prompt += f"\n📊 Career Readiness: {user_context['readiness_score']}%"

    if user_context.get("interests"):
        prompt += f"\n🔥 Interests: {', '.join(user_context['interests'])}"

    if user_context.get("education"):
        prompt += f"\n🎓 Education: {user_context['education']}"

    prompt += """

GUIDELINES:
1. Always reference the student's actual profile data in your responses
2. If asked about choosing between technologies, consider their current skills and target career
3. Give time-bound, phased advice (e.g., "In the next 2 weeks, focus on...")
4. Recommend specific free resources (YouTube channels, courses, documentation)
5. When discussing career paths, relate to their readiness score and skill gaps
6. Be encouraging but realistic about timelines
7. If they ask about interview prep, give career-specific questions and tips
8. Format responses with headers, bullet points, and emojis for readability
9. Keep responses concise but comprehensive (aim for 200-400 words)
10. End each response with a motivating next step or action item
"""
    return prompt


def chat_with_mentor(
    api_key: str,
    user_message: str,
    chat_history: list,
    user_context: dict,
    model: str = "llama-3.1-8b-instant"
) -> str:
    """Send message to AI mentor and get response."""
    client = get_groq_client(api_key)
    if not client:
        return "⚠️ Could not connect to AI service. Please check your API key."

    system_prompt = build_system_prompt(user_context)

    messages = [{"role": "system", "content": system_prompt}]

    # Add recent chat history (last 10 messages for context)
    for msg in chat_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "auth" in error_msg.lower():
            return "🔑 Invalid API key. Please check your Groq API key in the sidebar."
        elif "rate" in error_msg.lower():
            return "⏳ Rate limit reached. Please wait a moment and try again."
        else:
            return f"⚠️ Error: {error_msg}"


def generate_interview_questions(
    api_key: str,
    career: str,
    skills: list,
    difficulty: str = "Intermediate"
) -> str:
    """Generate career-specific interview questions."""
    client = get_groq_client(api_key)
    if not client:
        return None

    prompt = f"""Generate 10 interview questions for a {career} position.
The candidate has these skills: {', '.join(skills)}
Difficulty level: {difficulty}

Format:
## Technical Questions (7)
1. [Question]
   💡 Key points to cover: [brief hints]

## Behavioral Questions (3)
1. [Question]
   💡 Approach: [brief tips]

Make questions specific and practical, not generic."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a senior technical interviewer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception:
        return None
