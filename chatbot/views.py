from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from resume.models import Resume
from .utils import generate_intelligent_response

@login_required
def chat_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Get resume text if analysis report exists, otherwise None
    resume_text = None
    if hasattr(resume, 'analysis'):
        resume_text = resume.analysis.extracted_text
        
    # Chat history stored in session
    session_key = f'chat_history_{resume_id}'
    if session_key not in request.session:
        request.session[session_key] = [
            {'role': 'assistant', 'content': f"Hello! I am SmartHire AI Coach. I have reviewed **'{resume.file.name.split('/')[-1]}'**.\n\nYou can ask me anything — for example:\n- *How can I improve my resume?*\n- *What skills should I learn?*\n- *Give me interview tips*\n- *Rewrite: Managed a team of 5*\n- *I'm working on a project, how do I add it to my resume?*"}
        ]
        
    chat_history = request.session[session_key]
    
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            # Add user message
            chat_history.append({'role': 'user', 'content': user_message})
            
            # Get job description if exists
            from analysis.models import JobMatchResult
            latest_match = JobMatchResult.objects.filter(resume=resume).order_by('-created_at').first()
            job_description = latest_match.job_description if latest_match else None

            # Generate intelligent response — pass full history for context
            bot_response = generate_intelligent_response(
                message=user_message,
                resume_text=resume_text,
                job_description=job_description,
                chat_history=chat_history[:-1]  # exclude current message (already appended)
            )
            chat_history.append({'role': 'assistant', 'content': bot_response})
            
            # Save to session
            request.session[session_key] = chat_history
            request.session.modified = True
            
    context = {
        'resume': resume,
        'chat_history': chat_history
    }
    return render(request, 'chatbot/chat.html', context)

