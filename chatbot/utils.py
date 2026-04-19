import re
import random
import os
from django.conf import settings

# Predefined Knowledge Base
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

def analyze_intent(message):
    """
    Categorizes the user's message using keyword-based NLP logic.
    """
    msg = message.lower()
    
    intent_keywords = {
        'resume_improvement': ['improve', 'resume', 'cv', 'better', 'fix', 'format', 'ats'],
        'skills_recommendation': ['skill', 'learn', 'trending', 'technology', 'stack'],
        'job_search': ['job', 'apply', 'search', 'hire', 'find', 'roadmap'],
        'interview': ['interview', 'prepare', 'questions', 'star', 'behavioral'],
        'rewrite': ['rewrite', 'sentence', 'bullet', 'fix this', 'reword']
    }
    
    # Calculate intent matching score
    best_intent = 'unknown'
    max_matches = 0
    
    for intent, keywords in intent_keywords.items():
        matches = sum(1 for kw in keywords if re.search(r'\b' + kw + r'\b', msg))
        if matches > max_matches:
            max_matches = matches
            best_intent = intent
            
    return best_intent

def process_rewrite(message):
    """Simple logic to reword a sentence to sound more professional."""
    # Assuming user said "Rewrite: I managed a team and did good work"
    # We just strip the intent word and try to make it sound better.
    text = re.sub(r'rewrite|fix this|reword|sentence|bullet', '', message, flags=re.IGNORECASE).strip(' :.,')
    if not text:
        return "Please provide the specific sentence you want me to rewrite."
        
    # Basic simulated NLP rewrites
    if "managed" in text.lower() or "team" in text.lower():
        return f"Try this professional rewrite: **'Spearheaded a cross-functional team, driving strategic initiatives and delivering high-quality results.'**"
    elif "helped" in text.lower() or "worked" in text.lower():
        return f"Try this professional rewrite: **'Collaborated closely with stakeholders to execute project goals and optimize workflows.'**"
    elif "built" in text.lower() or "made" in text.lower():
        return f"Try this professional rewrite: **'Architected and implemented robust solutions, resulting in improved system efficiency.'**"
        
    return f"Here is a more impactful way to phrase that: **'Successfully executed initiatives related to {text}, consistently exceeding performance benchmarks.'**"

def fallback_intelligent_response(message, resume_text=None):
    """
    Response engine that uses intent recognition to provide structured answers.
    """
    intent = analyze_intent(message)
    msg_lower = message.lower()
    
    if intent == 'rewrite' or msg_lower.startswith('rewrite') or msg_lower.startswith('fix'):
        return process_rewrite(message)

    if intent == 'resume_improvement':
        response = "Based on ATS standards, here are top ways to improve your resume:\n\n"
        for tip in random.sample(KNOWLEDGE_BASE['resume_tips'], 2):
            response += f"• {tip}\n"
            
        if resume_text:
            # Simple check of resume length based on text
            word_count = len(resume_text.split())
            if word_count < 200:
                response += "\n*Coach Note: Your resume seems a bit short. Make sure you describe your experiences fully using bullet points.*"
            elif word_count > 1000:
                response += "\n*Coach Note: Your resume might be too long. Try prioritizing your most impactful achievements.*"
                
        return response

    elif intent == 'skills_recommendation':
        response = "To stay competitive, consider these trending skills:\n\n"
        for skill in KNOWLEDGE_BASE['trending_skills']:
            response += f"• {skill}\n"
            
        if resume_text:
            if "python" not in resume_text.lower():
                response += "\n*Coach Note: I noticed you didn't mention Python. It might be a great addition to your skill set!*"
        return response

    elif intent == 'job_search':
        return "Here is a quick roadmap for your job search:\n\n1. Optimize your LinkedIn profile to match your resume.\n2. Set up automated job alerts on Indeed and LinkedIn.\n3. Dedicate 20% of your time to applying, and 80% to networking.\n4. Don't be afraid to send polite follow-up messages a week after applying."

    elif intent == 'interview':
        response = "Preparation is key for interviews! Here is my top advice:\n\n"
        for tip in random.sample(KNOWLEDGE_BASE['interview_prep'], 2):
            response += f"• {tip}\n"
        response += "\nWould you like a sample behavioral question to practice?"
        return response

    else:
        # Fallback response
        tip = random.choice(KNOWLEDGE_BASE['resume_tips'])
        return f"I'm still learning how to answer that specific question, but here's a helpful tip: {tip}\n\nYou can ask me to 'improve your resume', 'recommend skills', or 'rewrite a sentence'!"

def generate_ai_response(user_input, resume_text, job_description):
    import google.generativeai as genai
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    genai.configure(api_key=api_key)
    # Use gemini-1.5-flash which is the standard fast & cost-effective text model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are a professional AI Resume Coach.
    Analyze the following resume and job description (if provided).
    Provide clear, concise advice in 5-7 bullet points maximum.
    Ensure responses are:
    - Professional
    - Actionable
    - Resume-focused
    
    Format your response cleanly in markdown.

    User's Message: {user_input}
    
    Job Description: {job_description if job_description else 'Not provided'}
    
    Resume Text Context (first 1500 chars to save tokens): {resume_text[:1500] if resume_text else 'Not provided'}
    """
    
    response = model.generate_content(prompt)
    if not response or not hasattr(response, 'text') or not response.text:
        return None
        
    return response.text

def generate_intelligent_response(message, resume_text=None, job_description=None):
    if settings.ENABLE_AI_COACH:
        try:
            ai_text = generate_ai_response(message, resume_text, job_description)
            if ai_text:
                return ai_text
        except Exception as e:
            # Silently fallback
            print(f"AI Coach Error: {e}")
            pass
            
    return fallback_intelligent_response(message, resume_text)
