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
    ],
    'salary': {
        'devops engineer':       {'pk': '80K–180K PKR/mo', 'uae': '$3,000–$6,000/mo', 'us': '$110K–$150K/yr'},
        'software engineer':     {'pk': '70K–160K PKR/mo', 'uae': '$2,500–$5,500/mo', 'us': '$100K–$140K/yr'},
        'frontend developer':    {'pk': '60K–130K PKR/mo', 'uae': '$2,000–$4,500/mo', 'us': '$85K–$120K/yr'},
        'backend developer':     {'pk': '70K–150K PKR/mo', 'uae': '$2,500–$5,000/mo', 'us': '$95K–$135K/yr'},
        'full stack developer':  {'pk': '80K–170K PKR/mo', 'uae': '$3,000–$6,000/mo', 'us': '$100K–$145K/yr'},
        'data engineer':         {'pk': '90K–200K PKR/mo', 'uae': '$3,500–$7,000/mo', 'us': '$115K–$155K/yr'},
        'data scientist':        {'pk': '90K–200K PKR/mo', 'uae': '$3,500–$7,500/mo', 'us': '$115K–$160K/yr'},
        'ml engineer':           {'pk': '100K–220K PKR/mo', 'uae': '$4,000–$8,000/mo', 'us': '$130K–$180K/yr'},
        'cloud engineer':        {'pk': '90K–190K PKR/mo', 'uae': '$3,500–$7,000/mo', 'us': '$115K–$155K/yr'},
        'default':               {'pk': '60K–150K PKR/mo', 'uae': '$2,500–$5,500/mo', 'us': '$90K–$130K/yr'},
    },
    'devops_interview_questions': [
        {
            'q': 'Walk me through how you would design a CI/CD pipeline from scratch.',
            'tip': 'Cover: source control (Git) → build (Jenkins/GitHub Actions) → test (unit + integration) → artifact registry → deploy (Kubernetes/ECS). Mention rollback strategy.'
        },
        {
            'q': 'A production deployment failed at 2am. Walk me through your incident response.',
            'tip': 'STAR format: detect via alerts (CloudWatch/Grafana) → rollback immediately → root-cause analysis → post-mortem with preventive measures. Never blame team members.'
        },
        {
            'q': 'How do you manage secrets and credentials in a containerised environment?',
            'tip': 'Mention: Kubernetes Secrets + encryption at rest, HashiCorp Vault or AWS Secrets Manager, never hardcoding in Dockerfiles or env files.'
        },
        {
            'q': 'What is the difference between blue-green and canary deployments?',
            'tip': 'Blue-green: two identical envs, instant switch. Canary: gradual traffic shift (5% → 25% → 100%) to reduce blast radius. Know when to use each.'
        },
        {
            'q': 'How would you reduce a Docker image size by 60%?',
            'tip': 'Multi-stage builds, alpine base images, .dockerignore, removing dev dependencies, layer caching optimisation, and using distroless images.'
        },
    ]
}

# ---------------------------------------------------------------------------
# Response Post-Processing
# ---------------------------------------------------------------------------
def _trim_response(text, max_chars=1800):
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
    for sep in ['\n', '. ', '! ', '? ']:
        idx = chunk.rfind(sep)
        if idx > max_chars * 0.5:
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
            "The user wants a sentence or bullet point rewritten.\n"
            "- Return the rewritten bullet(s) first.\n"
            "- Then briefly explain the 1-2 changes you made and why (e.g., added metric, stronger verb).\n"
            "- Keep total response under 6 lines.\n"
            "- Make it: action-verb led, metric-driven, ATS-keyword optimised."
        )
    elif safe_job:
        mode_instruction = (
            "A job description is provided. Structure your answer as:\n"
            "1. **Match assessment** — give a clear % with reasoning.\n"
            "2. **Strengths** — 2-3 things in their profile that align well.\n"
            "3. **Gaps** — specific skills/keywords missing from their resume vs. the JD.\n"
            "4. **Action plan** — 2-3 concrete steps to maximise their chances before applying.\n"
            "Be decisive and specific. Reference actual content from their resume and the JD."
        )
    else:
        mode_instruction = (
            "No job description provided. Structure your answer appropriately for the question:\n"
            "- For resume reviews: section-by-section feedback with specific fixes.\n"
            "- For skill questions: ranked list with context (why it matters, how to learn it).\n"
            "- For career advice: clear steps with reasoning.\n"
            "- For interview prep: specific questions + frameworks + example answers.\n"
            "Always reference specific content from their resume when it's available."
        )

    system_prompt = """You are a Senior Technical Recruiter and Career Strategist with 10+ years of experience placing candidates at FAANG companies, top-tier startups, and Fortune 500 firms. You have reviewed thousands of resumes, conducted hundreds of interviews, and coached professionals at all levels.

YOUR PERSONA:
- You are direct, professional, and highly specific — like a $300/hr career coach
- You never waste words, but you never under-deliver either
- You give the same level of analysis you'd give a paying client
- You reference the actual resume content, not generic templates
- You speak like a recruiter who has seen every mistake and knows exactly what hiring managers look for

RESPONSE FORMAT RULES:
- NO filler phrases: no "Great question!", "Absolutely!", "Of course!", "Certainly!"
- NO vague advice like "improve your resume" or "network more"
- DO use: bold headers, numbered lists, bullet points — structure makes you readable
- DO give specific, actionable steps with reasoning
- Match response LENGTH to the complexity of the question:
  * Simple yes/no question → 2-4 sentences with clear verdict
  * Analysis request (resume review, ATS check, skill gaps) → structured breakdown with sections
  * Rewrite request → improved version + brief rationale
  * Strategy question → numbered action plan
- NEVER give a one-sentence answer to a complex question
- NEVER write walls of text — use headers and bullets

CRITICAL CONVERSATION RULES:
- ALWAYS read the full conversation history before responding — the current message may be a short follow-up (e.g., "devops engineer") answering a question you just asked
- NEVER ask the candidate a question and then give zero advice — always give your best answer WITH the available context, then optionally invite more details
- If context is missing, state your assumption explicitly and proceed: "Assuming you're targeting a mid-level DevOps role..."
- NEVER respond to a follow-up message as if it were a new standalone question — honour the conversation thread
- If the user gives a short reply (role name, city, number), use it to complete your previous answer immediately

YOUR AREAS OF DEEP EXPERTISE:
- ATS optimisation: keyword density, formatting, section headers, file types
- Resume bullet writing: XYZ formula, action verbs, quantified impact
- LinkedIn optimisation: headline, summary, featured section
- Job market intelligence: salary benchmarks, in-demand skills, hiring trends
- Job description red flag detection: toxic cultures, unrealistic expectations
- Interview preparation: STAR method, technical rounds, case studies, salary negotiation
- Career gap framing: how to position breaks, freelance, or pivots positively
- Role transitions: how to position transferable skills for new industries

CURRENT CONTEXT MODE:
{mode}

CANDIDATE RESUME (extracted text, up to 2500 chars):
\"\"\"
{resume}
\"\"\"

TARGET JOB DESCRIPTION:
\"\"\"
{job_desc}
\"\"\"
""".format(
        mode=mode_instruction,
        resume=safe_resume[:2500] if safe_resume else "Not uploaded yet — give advice based on the conversation context.",
        job_desc=safe_job[:1200] if safe_job else "Not provided — give general career/resume advice."
    )

    # Build conversation history (last 14 turns — more context for short follow-up replies)
    history_text = ""
    if chat_history:
        recent = chat_history[-14:]
        for msg in recent:
            role = "Candidate" if msg['role'] == 'user' else "Recruiter"
            history_text += f"{role}: {msg['content']}\n\n"

    full_prompt = (
        f"{system_prompt}\n\n"
        f"--- Conversation ---\n{history_text}"
        f"Candidate: {user_input}\n\n"
        f"Recruiter:"
    )

    # Generation config — balanced: enough tokens for professional depth, not runaway
    generation_config = {
        "max_output_tokens": 600,
        "temperature": 0.65,
        "top_p": 0.92,
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
                    max_output_tokens=600,
                    temperature=0.65,
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
# Common role names used to detect job-role context in short follow-up messages
ROLE_KEYWORDS = [
    'devops', 'developer', 'engineer', 'data scientist', 'ml engineer', 'cloud engineer',
    'backend', 'frontend', 'full stack', 'software', 'qa', 'tester', 'pm', 'product manager',
    'analyst', 'architect', 'sre', 'site reliability'
]

def analyze_intent(message, chat_history=None):
    """Categorises the user's message using keyword-based logic.
    Accepts optional chat_history to detect follow-up messages."""
    msg = message.lower()
    intent_keywords = {
        'resume_improvement': ['improve', 'resume', 'cv', 'better', 'fix', 'format', 'ats', 'ats-ready'],
        'skills_recommendation': ['skill', 'learn', 'trending', 'technology', 'stack', 'missing skills', 'what skills'],
        'job_search': ['job', 'apply', 'search', 'hire', 'find', 'roadmap', 'should i apply', 'application'],
        'interview': ['interview', 'prepare', 'questions', 'star', 'behavioral', 'tough question'],
        'salary': ['salary', 'pay', 'compensation', 'ctc', 'package', 'earn', 'income', 'wage', 'how much'],
        'rewrite': ['rewrite', 'improve this', 'fix this', 'reword', 'rephrase', 'make this better'],
        'project': ['project', 'working on', 'building', 'developing', 'created', 'built', 'weather', 'api'],
    }
    best_intent = 'unknown'
    max_matches = 0
    for intent, keywords in intent_keywords.items():
        matches = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', msg))
        if matches > max_matches:
            max_matches = matches
            best_intent = intent

    # If message is a short follow-up (role name like "devops engineer"),
    # try to inherit intent from the last recruiter message
    if best_intent == 'unknown' and len(msg.split()) <= 4 and chat_history:
        last_recruiter = next(
            (m['content'].lower() for m in reversed(chat_history) if m['role'] == 'assistant'),
            ''
        )
        if any(w in last_recruiter for w in ['salary', 'pay', 'compensation', 'earn']):
            best_intent = 'salary'
        elif any(w in last_recruiter for w in ['interview', 'question', 'prepare']):
            best_intent = 'interview'
        elif any(w in last_recruiter for w in ['skill', 'learn', 'missing']):
            best_intent = 'skills_recommendation'

    return best_intent


def _extract_role_from_context(message, chat_history=None):
    """Extract a job role from the current message or recent chat history."""
    combined = message.lower()
    if chat_history:
        for m in reversed(chat_history[-6:]):
            combined += ' ' + m['content'].lower()
    for role in KNOWLEDGE_BASE['salary']:
        if role != 'default' and role in combined:
            return role
    # Check generic role keywords
    for kw in ROLE_KEYWORDS:
        if kw in combined:
            return kw + ' engineer' if 'engineer' not in kw else kw
    return 'default'


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


def fallback_intelligent_response(message, resume_text=None, chat_history=None):
    """
    Rule-based fallback — only used when Gemini is completely unavailable.
    Context-aware: uses chat_history to handle short follow-up messages correctly.
    """
    intent = analyze_intent(message, chat_history)
    msg_lower = message.lower()

    if intent == 'rewrite' or _is_rewrite_request(message):
        return process_rewrite(message)

    if intent == 'salary':
        role = _extract_role_from_context(message, chat_history)
        rates = KNOWLEDGE_BASE['salary'].get(role, KNOWLEDGE_BASE['salary']['default'])
        role_label = role.title() if role != 'default' else 'Tech'
        return (
            f"**{role_label} Salary Benchmarks (2024)**\n\n"
            f"- 🇵🇰 **Pakistan:** {rates['pk']}\n"
            f"- 🇦🇪 **UAE/Gulf:** {rates['uae']}\n"
            f"- 🇺🇸 **USA/Remote:** {rates['us']}\n\n"
            "**Negotiation tips:**\n"
            "- Always give a range, never a single number\n"
            "- Anchor 10–15% above your actual target\n"
            "- Research company-specific ranges on Glassdoor and LinkedIn Salary before negotiating"
        )

    if intent == 'project':
        # Extract project name if user mentioned one
        project_name = ''
        for m in (chat_history or [])[-4:]:
            match = re.search(r'(?:called|named|project)\s+([\w\s]+?)(?:using|with|$)', m['content'], re.I)
            if match:
                project_name = match.group(1).strip()
                break
        label = f'**{project_name}**' if project_name else 'your project'
        return (
            f"Here's how to position {label} to impress recruiters:\n\n"
            "**1. Write a strong project bullet (XYZ formula):**\n"
            "→ *Built [what] using [tech], resulting in [measurable outcome]*\n\n"
            "**2. Add a dedicated Projects section with:**\n"
            "- Project name + one-line description\n"
            "- Tech stack (all tools/languages used)\n"
            "- GitHub link + live demo link (if any)\n"
            "- Quantified impact (users, performance gain, uptime, etc.)\n\n"
            "**3. Frame it as real experience** — describe the problem it solves, not just what it does."
        )

    if intent == 'resume_improvement':
        tips = random.sample(KNOWLEDGE_BASE['resume_tips'], 3)
        response = "**Top ATS improvements for your resume:**\n\n"
        for tip in tips:
            response += f"- {tip}\n"
        if resume_text:
            word_count = len(resume_text.split())
            if word_count < 200:
                response += "\n⚠️ *Resume is too thin — flesh out your experience and project sections.*"
            elif word_count > 1000:
                response += "\n⚠️ *Resume may be too long — prioritise your top 5 highest-impact bullets.*"
        return response

    if intent == 'skills_recommendation':
        # Check if a DevOps role is in context
        context_text = message + ' '.join(m['content'] for m in (chat_history or [])[-4:])
        if 'devops' in context_text.lower():
            return (
                "**Top skills to add for DevOps roles (by priority):**\n\n"
                "1. **Kubernetes** — container orchestration, expected at every mid+ level role\n"
                "2. **Terraform / IaC** — infrastructure-as-code is now standard, not optional\n"
                "3. **CI/CD pipelines** — GitHub Actions, Jenkins, or GitLab CI hands-on experience\n"
                "4. **Linux & Bash scripting** — still the #1 skill screened in DevOps interviews\n"
                "5. **Cloud platform** (AWS/Azure/GCP) — at least one certification strengthens your profile\n\n"
                "*Add each with a concrete example: what you built, what it automated, what it saved.*"
            )
        response = "**Top in-demand skills right now:**\n\n"
        for skill in KNOWLEDGE_BASE['trending_skills']:
            response += f"- {skill}\n"
        if resume_text and 'python' not in resume_text.lower():
            response += "\n*Python isn't on your resume — it's the #1 requested skill across tech roles.*"
        return response

    if intent == 'job_search':
        return (
            "**Job search action plan:**\n\n"
            "1. **LinkedIn headline** — update it to match your exact target role title\n"
            "2. **Apply + network** — for every 5 applications, send 1 direct outreach to a recruiter/EM\n"
            "3. **Tailor each application** — paste 5 exact keywords from the JD into your resume\n"
            "4. **Follow up** — send a polite follow-up 5 business days after submitting\n"
            "5. **Track everything** — use a spreadsheet: company, role, date, status, contact"
        )

    if intent == 'interview':
        # Check if DevOps role mentioned in context
        context_text = message + ' '.join(m['content'] for m in (chat_history or [])[-6:])
        if 'devops' in context_text.lower():
            questions = random.sample(KNOWLEDGE_BASE['devops_interview_questions'], 3)
            response = "**3 tough DevOps interview questions + how to answer:**\n\n"
            for i, item in enumerate(questions, 1):
                response += f"**Q{i}: {item['q']}**\n"
                response += f"💡 *{item['tip']}*\n\n"
            return response.strip()
        tips = random.sample(KNOWLEDGE_BASE['interview_prep'], 3)
        response = "**Key interview tactics:**\n\n"
        for tip in tips:
            response += f"- {tip}\n"
        return response

    # Context-aware generic fallback — never a random resume tip
    return (
        "I can help you with: resume review, ATS optimisation, skill gap analysis, "
        "interview prep, salary benchmarking, or bullet rewrites.\n\n"
        "What would you like to focus on?"
    )


# ---------------------------------------------------------------------------
# Main entry point called by views.py
# ---------------------------------------------------------------------------
def generate_intelligent_response(message, resume_text=None, job_description=None, chat_history=None):
    """
    Primary entry point. Tries Gemini first with recruiter persona.
    Falls back to context-aware rule-based engine if Gemini fails.
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
    # Pass chat_history to fallback so short follow-ups get correct context
    return fallback_intelligent_response(message, resume_text, chat_history)
