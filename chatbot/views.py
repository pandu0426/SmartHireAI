import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from resume.models import Resume
from .utils import generate_intelligent_response


def _get_resume_text(resume):
    """Safely extract resume text from analysis if available."""
    if hasattr(resume, 'analysis') and resume.analysis:
        return resume.analysis.extracted_text
    return None


def _get_job_description(resume):
    """Safely get latest job description for this resume."""
    try:
        from analysis.models import JobMatchResult
        match = JobMatchResult.objects.filter(resume=resume).order_by('-created_at').first()
        return match.job_description if match else None
    except Exception:
        return None


def _get_or_init_chat(request, resume):
    """Return chat history from session, creating initial message if needed."""
    session_key = f'chat_history_{resume.id}'
    if session_key not in request.session:
        filename = resume.file.name.split('/')[-1] if resume.file else "your resume"
        request.session[session_key] = [
            {
                'role': 'assistant',
                'content': (
                    f"I've reviewed **'{filename}'**. "
                    "I'm your Senior Recruiter AI — I give direct, no-fluff career advice.\n\n"
                    "Ask me anything:\n"
                    "- *Is my resume ATS-ready?*\n"
                    "- *Should I apply for this role?*\n"
                    "- *Rewrite: [paste your bullet here]*\n"
                    "- *What skills am I missing for a DevOps role?*"
                )
            }
        ]
    return session_key, request.session[session_key]


# ---------------------------------------------------------------------------
# Main chat view (existing POST-based — preserved for backward compatibility)
# ---------------------------------------------------------------------------
@login_required
def chat_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    resume_text = _get_resume_text(resume)
    session_key, chat_history = _get_or_init_chat(request, resume)

    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            chat_history.append({'role': 'user', 'content': user_message})
            job_description = _get_job_description(resume)

            bot_response = generate_intelligent_response(
                message=user_message,
                resume_text=resume_text,
                job_description=job_description,
                chat_history=chat_history[:-1]
            )
            chat_history.append({'role': 'assistant', 'content': bot_response})
            request.session[session_key] = chat_history
            request.session.modified = True

    context = {
        'resume': resume,
        'chat_history': chat_history
    }
    return render(request, 'chatbot/chat.html', context)


# ---------------------------------------------------------------------------
# AJAX endpoint — NEW, additive only
# ---------------------------------------------------------------------------
@login_required
@require_POST
def chat_ajax(request, resume_id):
    """
    AJAX handler that returns JSON. Called by the frontend fetch() in chat.html.
    Falls back gracefully on any error — never returns a 500 to the client.
    """
    try:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        resume_text = _get_resume_text(resume)
        session_key, chat_history = _get_or_init_chat(request, resume)

        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        chat_history.append({'role': 'user', 'content': user_message})
        job_description = _get_job_description(resume)

        bot_response = generate_intelligent_response(
            message=user_message,
            resume_text=resume_text,
            job_description=job_description,
            chat_history=chat_history[:-1]
        )

        chat_history.append({'role': 'assistant', 'content': bot_response})
        request.session[session_key] = chat_history
        request.session.modified = True

        return JsonResponse({'response': bot_response, 'role': 'assistant'})

    except Exception as e:
        print(f"chat_ajax error: {e}")
        return JsonResponse(
            {'response': 'Something went wrong. Please try again.', 'role': 'assistant'},
            status=200  # return 200 so frontend still renders the message
        )


# ---------------------------------------------------------------------------
# Clear chat endpoint — NEW, additive only
# ---------------------------------------------------------------------------
@login_required
@require_POST
def clear_chat(request, resume_id):
    """Clears chat history from session and resets to welcome message."""
    try:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        session_key = f'chat_history_{resume.id}'
        if session_key in request.session:
            del request.session[session_key]
        request.session.modified = True
        return JsonResponse({'status': 'cleared'})
    except Exception as e:
        print(f"clear_chat error: {e}")
        return JsonResponse({'status': 'error'}, status=200)
