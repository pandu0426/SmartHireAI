import re
import random
import os
from django.conf import settings

# ---------------------------------------------------------------------------
# Fallback Knowledge Base (used when Gemini is unavailable)
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    'resume_tips': [
        "Use the XYZ formula for bullet points: 'Accomplished [X] as measured by [Y], by doing [Z]'.",
        "Keep your resume to one page if you have less than 10 years of experience.",
        "Ensure your contact information is at the very top, including a link to your LinkedIn or portfolio.",
        "Remove objective statements. Use a professional summary instead if you are changing careers.",
        "Quantify your achievements with numbers, percentages, and dollar amounts wherever possible."
    ],
    'job_search': [
        "Don't just apply online. Reach out to recruiters and engineering managers directly on LinkedIn.",
        "Tailor your resume for every application by including keywords from the job description.",
        "Treat your job search like a full-time job. Set daily goals for applications, networking, and skill-building.",
        "Leverage weak ties. Often, jobs come from acquaintances rather than close friends.",
        "Use niche job boards in addition to the big ones like LinkedIn and Indeed."
    ],
    'interview_prep': [
        "Use the STAR method for behavioral questions: Situation, Task, Action, Result.",
        "Always have 2-3 thoughtful questions prepared to ask the interviewer at the end.",
        "Research the company's culture and recent news before the interview.",
        "Practice answering 'Tell me about yourself' out loud until it sounds natural.",
        "It's okay to ask for a moment to think before answering a complex technical question."
    ],
    'trending_skills': [
        "Cloud Computing (AWS, Azure, GCP)",
        "Artificial Intelligence / Machine Learning (Python, PyTorch, TensorFlow)",
        "Data Engineering and Analytics (SQL, Snowflake, Pandas)",
        "Full-Stack Development (React, Node.js, Django)",
        "DevOps & CI/CD (Docker, Kubernetes, GitHub Actions)"
    ]
}


# ---------------------------------------------------------------------------
# Gemini AI Response (primary)
# ---------------------------------------------------------------------------
def generate_ai_response(user_input, resume_text, job_description, chat_history=None):
    """
    Calls the Gemini API with the full conversation history and resume context.
    Returns the AI response text, or None on failure.
    """
    print("Gemini started")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Gemini failed: GEMINI_API_KEY is missing or not set")
        return None

    safe_resume = resume_text or ""
    safe_job    = job_description or ""

    # Build the system prompt — context-aware, NOT locked to "give resume tips"
    system_prompt = """You are SmartHire AI Coach — a friendly, knowledgeable career assistant.

You have access to the user's resume and (optionally) a job description they are targeting.
You MUST respond directly and helpfully to whatever the user actually says or asks.

Guidelines:
- If they ask a general career/project/industry question, answer it conversationally.
- If they ask about their resume specifically, reference the resume text and give tailored advice.
- If they want something rewritten, rewrite it clearly.
- If they are sharing something (e.g., "I am working on a project"), acknowledge it and offer relevant, specific career guidance — e.g., how to frame it on their resume, how to showcase it to employers, what to highlight, etc.
- Keep responses concise and readable. Use markdown bullet points only when listing multiple items.
- NEVER give the same generic "improve your resume" bullet list when the user is asking something else.
- Be warm, encouraging, and professional.

Resume Context (extracted text, first 2000 chars):
\"\"\"
{resume}
\"\"\"

Job Description they are targeting:
\"\"\"
{job_desc}
\"\"\"
""".format(
        resume=safe_resume[:2000] if safe_resume else "Not provided — user has not uploaded/analysed a resume yet.",
        job_desc=safe_job[:1000] if safe_job else "Not provided."
    )

    # Build conversation history for Gemini (last 10 turns to stay within token limits)
    history_text = ""
    if chat_history:
        recent = chat_history[-10:]  # last 10 messages
        for msg in recent:
            role = "User" if msg['role'] == 'user' else "Assistant"
            history_text += f"{role}: {msg['content']}\n\n"

    full_prompt = f"{system_prompt}\n\n--- Conversation so far ---\n{history_text}User: {user_input}\n\nAssistant:"

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        # Try models in order — lite first (more free-tier quota), then fallback
        models_to_try = ["gemini-2.0-flash-lite", "gemini-2.5-flash", "gemini-2.0-flash"]
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt
                )
                if response and response.text:
                    print(f"Gemini success (model: {model_name})")
                    return response.text.strip()
            except Exception as model_err:
                print(f"Gemini model {model_name} failed: {model_err}")
                continue

        print("Gemini failed: All models exhausted")
        return None

    except ImportError:
        # Fallback to legacy library if new SDK not installed
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=api_key)
            model = genai_legacy.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(full_prompt)
            if response and hasattr(response, 'text') and response.text:
                print("Gemini success (legacy SDK)")
                return response.text.strip()
        except Exception as legacy_err:
            print(f"Gemini legacy SDK failed: {legacy_err}")
        return None


# ---------------------------------------------------------------------------
# Fallback rule-based engine (when Gemini is unavailable)
# ---------------------------------------------------------------------------
def analyze_intent(message):
    """Categorizes the user's message using keyword-based logic."""
    msg = message.lower()
    intent_keywords = {
        'resume_improvement': ['improve', 'resume', 'cv', 'better', 'fix', 'format', 'ats'],
        'skills_recommendation': ['skill', 'learn', 'trending', 'technology', 'stack'],
        'job_search': ['job', 'apply', 'search', 'hire', 'find', 'roadmap'],
        'interview': ['interview', 'prepare', 'questions', 'star', 'behavioral'],
        'rewrite': ['rewrite', 'sentence', 'bullet', 'fix this', 'reword'],
        'project': ['project', 'working on', 'building', 'developing', 'created', 'built']
    }
    best_intent = 'unknown'
    max_matches = 0
    for intent, keywords in intent_keywords.items():
        matches = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', msg))
        if matches > max_matches:
            max_matches = matches
            best_intent = intent
    return best_intent


def process_rewrite(message):
    """Rewrites a sentence to sound more professional."""
    text = re.sub(r'rewrite|fix this|reword|sentence|bullet', '', message, flags=re.IGNORECASE).strip(' :.,')
    if not text:
        return "Please provide the specific sentence you'd like me to rewrite."
    if "managed" in text.lower() or "team" in text.lower():
        return "**Rewrite:** *'Spearheaded a cross-functional team, driving strategic initiatives and delivering measurable results.'*"
    elif "helped" in text.lower() or "worked" in text.lower():
        return "**Rewrite:** *'Collaborated closely with stakeholders to execute project goals and optimize workflows.'*"
    elif "built" in text.lower() or "made" in text.lower():
        return "**Rewrite:** *'Architected and implemented robust solutions, resulting in improved system efficiency.'*"
    return f"**Rewrite:** *'Successfully delivered {text}, consistently exceeding performance benchmarks.'*"


def fallback_intelligent_response(message, resume_text=None):
    """
    Rule-based fallback — only used when Gemini is completely unavailable.
    """
    intent = analyze_intent(message)
    msg_lower = message.lower()

    if intent == 'rewrite' or msg_lower.startswith('rewrite') or msg_lower.startswith('fix'):
        return process_rewrite(message)

    if intent == 'project':
        return (
            "That sounds great! Here's how to showcase your project effectively:\n\n"
            "- **Add a Projects section** to your resume with the project name, tech stack, and outcome.\n"
            "- **Quantify the impact**: e.g., 'Reduced deployment time by 40%' or 'Handles 1K+ requests/day'.\n"
            "- **Link to it**: Add a GitHub link so recruiters can see your code.\n"
            "- **Frame it as experience**: Treat it like real work — emphasise what problem it solves.\n\n"
            "Tell me more about your project and I can help you write a great bullet point for it!"
        )

    if intent == 'resume_improvement':
        response = "Here are some quick ATS-focused improvements for your resume:\n\n"
        for tip in random.sample(KNOWLEDGE_BASE['resume_tips'], 3):
            response += f"- {tip}\n"
        if resume_text:
            word_count = len(resume_text.split())
            if word_count < 200:
                response += "\n*Your resume looks short — make sure you fully describe your experiences.*"
            elif word_count > 1000:
                response += "\n*Your resume may be too long — prioritise your most impactful achievements.*"
        return response

    elif intent == 'skills_recommendation':
        response = "Here are the most in-demand skills right now:\n\n"
        for skill in KNOWLEDGE_BASE['trending_skills']:
            response += f"- {skill}\n"
        if resume_text and "python" not in resume_text.lower():
            response += "\n*Tip: Python isn't on your resume yet — it's highly valued across tech roles!*"
        return response

    elif intent == 'job_search':
        return (
            "Here's a job search roadmap:\n\n"
            "1. Optimise your LinkedIn to match your resume.\n"
            "2. Set up job alerts on LinkedIn, Indeed and company career pages.\n"
            "3. Spend 20% of your time applying, 80% networking.\n"
            "4. Send polite follow-ups one week after applying."
        )

    elif intent == 'interview':
        response = "Key interview tips:\n\n"
        for tip in random.sample(KNOWLEDGE_BASE['interview_prep'], 3):
            response += f"- {tip}\n"
        response += "\nWould you like me to give you a sample behavioural question to practise?"
        return response

    else:
        tip = random.choice(KNOWLEDGE_BASE['resume_tips'])
        return (
            f"I'm here to help with your career! Here's a quick tip: *{tip}*\n\n"
            "You can ask me things like:\n"
            "- *How can I improve my resume?*\n"
            "- *What skills should I learn for a DevOps role?*\n"
            "- *I'm working on a Python project — how do I add it to my resume?*"
        )


# ---------------------------------------------------------------------------
# Main entry point called by views.py
# ---------------------------------------------------------------------------
def generate_intelligent_response(message, resume_text=None, job_description=None, chat_history=None):
    """
    Tries Gemini first. Falls back to rule-based engine if Gemini fails.
    """
    if settings.ENABLE_AI_COACH:
        try:
            ai_text = generate_ai_response(message, resume_text, job_description, chat_history)
            if ai_text:
                return ai_text
        except Exception as e:
            print(f"Gemini failed unexpectedly: {e}")

    print("Fallback used")
    return fallback_intelligent_response(message, resume_text)
