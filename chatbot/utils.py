import re
import random
import os
from django.conf import settings

# ---------------------------------------------------------------------------
# Fallback Knowledge Base (used when Gemini is unavailable)
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    'resume_tips': [
        "Use the XYZ formula: 'Accomplished [X] as measured by [Y], by doing [Z]'.",
        "Keep your resume to one page if you have less than 10 years of experience.",
        "Put contact info at the very top — include your LinkedIn and GitHub links.",
        "Drop objective statements. Use a 2-line professional summary instead.",
        "Quantify every achievement with numbers, percentages, or dollar amounts."
    ],
    'job_search': [
        "Skip the apply button. Message the hiring manager directly on LinkedIn.",
        "Tailor your resume per role — paste 5 exact keywords from the JD.",
        "Treat job hunting like a pipeline: track applications in a spreadsheet.",
        "Weak ties matter more than strong ones — contact ex-colleagues and alumni.",
        "Set up job alerts on LinkedIn, Indeed, and the company's own careers page."
    ],
    'interview_prep': [
        "Use STAR for behavioral questions: Situation, Task, Action, Result — keep it under 2 minutes.",
        "Prepare 3 sharp questions to ask the interviewer — shows you did your research.",
        "Research the company's last 3 press releases before any interview.",
        "Practice 'Tell me about yourself' out loud until it's 60 seconds clean.",
        "Pause before answering complex questions — it signals confidence, not confusion."
    ],
    'trending_skills': [
        "Cloud Computing (AWS, Azure, GCP) — essential for most engineering roles.",
        "AI/ML (Python, PyTorch, TensorFlow) — fastest growing demand globally.",
        "Data Engineering (SQL, Snowflake, dbt, Pandas) — highly paid niche.",
        "Full-Stack (React, Node.js, Django, FastAPI) — versatile and in-demand.",
        "DevOps & CI/CD (Docker, Kubernetes, GitHub Actions) — every team needs it."
    ]
}

# ---------------------------------------------------------------------------
# Response Post-Processing
# ---------------------------------------------------------------------------
def _trim_response(text, max_chars=800):
    """
    Safely trim AI response to max_chars by cutting at the last full sentence.
    Preserves bullet-point structure. Returns the trimmed string.
    """
    if not text:
        return text
    text = text.strip()
    if len(text) <= max_chars:
        return text

    # Cut at last sentence boundary within limit
    chunk = text[:max_chars]
    # Try to cut at last bullet point or sentence end
    for sep in ['\n', '. ', '! ', '? ']:
        idx = chunk.rfind(sep)
        if idx > max_chars * 0.5:  # don't cut too early
            return chunk[:idx + len(sep)].strip()

    return chunk.strip()


def _is_rewrite_request(user_input):
    """Detect if the user wants a sentence/bullet rewritten."""
    triggers = ['rewrite', 'improve this', 'fix this', 'reword', 'rephrase', 'make this better']
    lower = user_input.lower()
    return any(t in lower for t in triggers)


# ---------------------------------------------------------------------------
# Gemini AI Response (primary)
# ---------------------------------------------------------------------------
def generate_ai_response(user_input, resume_text, job_description, chat_history=None):
    """
    Calls the Gemini API with full conversation history and resume context.
    Returns trimmed AI response text, or None on failure.
    """
    print("Gemini started")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Gemini failed: GEMINI_API_KEY is missing or not set")
        return None

    safe_resume = (resume_text or "").strip()
    safe_job    = (job_description or "").strip()
    is_rewrite  = _is_rewrite_request(user_input)

    # -----------------------------------------------------------------------
    # RECRUITER PERSONA SYSTEM PROMPT
    # -----------------------------------------------------------------------
    if is_rewrite:
        mode_instruction = (
            "The user wants their sentence/bullet rewritten.\n"
            "Return ONLY the improved sentence — no explanation, no preamble.\n"
            "Make it: concise, metric-driven, action-verb led, ATS-optimised.\n"
            "Example output: 'Built and shipped a REST API reducing response latency by 40%.'"
        )
    elif safe_job:
        mode_instruction = (
            "A job description is provided. Your job:\n"
            "1. Identify how well the candidate matches this role (give a % estimate).\n"
            "2. Name the top 1-2 missing skills or keywords from their resume vs. the JD.\n"
            "3. Give one concrete action they can take TODAY to improve their chances.\n"
            "Be decisive. If they ask 'should I apply?' — tell them yes or no and why."
        )
    else:
        mode_instruction = (
            "No job description provided. Focus on:\n"
            "- ATS optimisation and resume quality\n"
            "- Career strategy and positioning\n"
            "- Skill gaps and market relevance\n"
            "Reference specific details from their resume when giving advice."
        )

    system_prompt = """You are a Senior Technical Recruiter with 10+ years of experience placing candidates at FAANG companies, top startups, and Fortune 500 firms. You are also a certified career strategist who charges $300/hr for resume reviews.

YOUR COMMUNICATION RULES (NON-NEGOTIABLE):
- Reply in EITHER: max 3–5 bullet points, OR max 2–3 short sentences. NEVER both. NEVER long paragraphs.
- Be direct and specific. No motivational fluff. No filler phrases like "Great question!" or "Absolutely!".
- Lead with the most important insight first.
- Use action verbs and metrics whenever possible.
- If you don't have enough context, ask ONE targeted question.
- NEVER repeat the user's question back to them.
- NEVER give generic advice that any chatbot would give.

YOUR EXPERTISE:
- ATS keyword optimisation and formatting rules
- Resume bullet rewriting with quantified impact
- LinkedIn headline and summary optimisation
- Salary benchmarking and offer negotiation
- Identifying red flags in job descriptions
- Interview preparation with company-specific patterns
- Career gap framing and narrative building
- Role transition strategy (e.g., from engineer to PM)

CURRENT MODE:
{mode}

CANDIDATE RESUME (first 2000 chars):
\"\"\"
{resume}
\"\"\"

TARGET JOB DESCRIPTION:
\"\"\"
{job_desc}
\"\"\"
""".format(
        mode=mode_instruction,
        resume=safe_resume[:2000] if safe_resume else "Not uploaded — give general advice based on the conversation.",
        job_desc=safe_job[:1000] if safe_job else "Not provided."
    )

    # Build conversation history (last 8 turns to stay within context)
    history_text = ""
    if chat_history:
        recent = chat_history[-8:]
        for msg in recent:
            role = "Candidate" if msg['role'] == 'user' else "Recruiter"
            history_text += f"{role}: {msg['content']}\n\n"

    full_prompt = (
        f"{system_prompt}\n\n"
        f"--- Conversation ---\n{history_text}"
        f"Candidate: {user_input}\n\n"
        f"Recruiter:"
    )

    # Generation config — hard cap on token output
    generation_config = {
        "max_output_tokens": 250,
        "temperature": 0.5,
        "top_p": 0.9,
    }

    try:
        from google import genai
        from google.genai import types as genai_types

        client = genai.Client(api_key=api_key)

        models_to_try = ["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-flash"]
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                    config=genai_types.GenerateContentConfig(
                        max_output_tokens=generation_config["max_output_tokens"],
                        temperature=generation_config["temperature"],
                        top_p=generation_config["top_p"],
                    )
                )
                if response and response.text and response.text.strip():
                    result = _trim_response(response.text.strip())
                    print(f"Gemini success (model: {model_name})")
                    return result
            except Exception as model_err:
                print(f"Gemini model {model_name} failed: {model_err}")
                continue

        print("Gemini failed: All models exhausted")
        return None

    except ImportError:
        # Fallback to legacy google-generativeai SDK
        try:
            import google.generativeai as genai_legacy
            from google.generativeai.types import GenerationConfig

            genai_legacy.configure(api_key=api_key)
            model = genai_legacy.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                full_prompt,
                generation_config=GenerationConfig(
                    max_output_tokens=250,
                    temperature=0.5,
                )
            )
            if response and hasattr(response, 'text') and response.text and response.text.strip():
                result = _trim_response(response.text.strip())
                print("Gemini success (legacy SDK)")
                return result
        except Exception as legacy_err:
            print(f"Gemini legacy SDK failed: {legacy_err}")
        return None

    except Exception as e:
        print(f"Gemini failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Fallback rule-based engine (when Gemini is unavailable)
# ---------------------------------------------------------------------------
def analyze_intent(message):
    """Categorises the user's message using keyword-based logic."""
    msg = message.lower()
    intent_keywords = {
        'resume_improvement': ['improve', 'resume', 'cv', 'better', 'fix', 'format', 'ats'],
        'skills_recommendation': ['skill', 'learn', 'trending', 'technology', 'stack'],
        'job_search': ['job', 'apply', 'search', 'hire', 'find', 'roadmap', 'should i apply'],
        'interview': ['interview', 'prepare', 'questions', 'star', 'behavioral'],
        'rewrite': ['rewrite', 'improve this', 'fix this', 'reword', 'rephrase'],
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
    """Rewrites a sentence to be concise, metric-driven, and ATS-optimised."""
    text = re.sub(
        r'\b(rewrite|fix this|reword|improve this|rephrase|make this better)\b',
        '', message, flags=re.IGNORECASE
    ).strip(' :.,-')

    if not text:
        return "Paste the sentence you'd like me to rewrite — I'll make it ATS-ready and metric-driven."

    lower = text.lower()
    if any(w in lower for w in ['managed', 'led', 'team']):
        return "**Rewrite:** Led a cross-functional team of engineers, delivering a high-priority feature 2 weeks ahead of schedule."
    elif any(w in lower for w in ['helped', 'worked', 'assisted']):
        return "**Rewrite:** Collaborated with cross-functional stakeholders to streamline workflows, reducing delivery time by 25%."
    elif any(w in lower for w in ['built', 'made', 'created', 'developed']):
        return "**Rewrite:** Engineered and shipped a production-ready solution that improved system throughput by 35%."
    elif any(w in lower for w in ['worked on', 'involved in']):
        return "**Rewrite:** Drove end-to-end implementation of a core platform feature adopted by 5,000+ users."
    return f"**Rewrite:** Successfully delivered {text}, achieving measurable improvements in efficiency and stakeholder satisfaction."


def fallback_intelligent_response(message, resume_text=None):
    """
    Rule-based fallback — only used when Gemini is completely unavailable.
    Kept intentionally lean and recruiter-toned.
    """
    intent = analyze_intent(message)
    msg_lower = message.lower()

    if intent == 'rewrite' or _is_rewrite_request(message):
        return process_rewrite(message)

    if intent == 'project':
        return (
            "To showcase this project effectively:\n\n"
            "- **Add it to a Projects section** with: name, tech stack, and measurable outcome.\n"
            "- **Quantify the impact** — e.g., 'Handles 1K+ requests/min' or 'Reduced load time by 40%'.\n"
            "- **Link to the GitHub repo** so recruiters can verify your work."
        )

    if intent == 'resume_improvement':
        tips = random.sample(KNOWLEDGE_BASE['resume_tips'], 3)
        response = "Top 3 ATS improvements for your resume:\n\n"
        for tip in tips:
            response += f"- {tip}\n"
        if resume_text:
            word_count = len(resume_text.split())
            if word_count < 200:
                response += "\n⚠️ *Resume is too thin — flesh out your experience sections.*"
            elif word_count > 1000:
                response += "\n⚠️ *Resume is too long — cut to your top 5 most impactful bullets.*"
        return response

    if intent == 'skills_recommendation':
        response = "Top in-demand skills right now:\n\n"
        for skill in KNOWLEDGE_BASE['trending_skills'][:4]:
            response += f"- {skill}\n"
        if resume_text and "python" not in resume_text.lower():
            response += "\n*Python isn't on your resume — it's the #1 requested skill in tech.*"
        return response

    if intent == 'job_search':
        return (
            "Job search priorities:\n\n"
            "- Optimise LinkedIn headline to match your target role title.\n"
            "- Apply to 5–10 roles/day; spend equal time on networking.\n"
            "- Follow up with hiring managers 5 business days after submitting."
        )

    if intent == 'interview':
        tips = random.sample(KNOWLEDGE_BASE['interview_prep'], 3)
        response = "Key interview tactics:\n\n"
        for tip in tips:
            response += f"- {tip}\n"
        return response

    # Generic fallback
    tip = random.choice(KNOWLEDGE_BASE['resume_tips'])
    return (
        f"Quick tip: *{tip}*\n\n"
        "Ask me anything — resume rewrites, job match analysis, interview prep, or salary benchmarking."
    )


# ---------------------------------------------------------------------------
# Main entry point called by views.py
# ---------------------------------------------------------------------------
def generate_intelligent_response(message, resume_text=None, job_description=None, chat_history=None):
    """
    Primary entry point. Tries Gemini first with recruiter persona.
    Falls back to rule-based engine if Gemini fails for any reason.
    Always returns a non-empty string.
    """
    if settings.ENABLE_AI_COACH:
        try:
            ai_text = generate_ai_response(message, resume_text, job_description, chat_history)
            if ai_text and ai_text.strip():
                return ai_text
        except Exception as e:
            print(f"Gemini failed unexpectedly: {e}")

    print("Fallback used")
    return fallback_intelligent_response(message, resume_text)
