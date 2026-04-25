from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from resume.models import Resume
from .models import AnalysisReport
from .forms import JobDescriptionForm
from .utils import extract_text_from_pdf, calculate_ats_score, extract_skills, match_job_description, analyze_smart_assistant

@login_required
def analyze_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if hasattr(resume, 'analysis'):
        report = resume.analysis
        
        if report.status == 'processing' or report.status == 'pending' or report.status == 'failed':
            return render(request, 'analysis/processing_report.html', {'resume': resume, 'report': report})
            
        context = {
            'resume': resume,
            'report': report,
        }
        return render(request, 'analysis/ats_report.html', context)
    else:
        return render(request, 'analysis/processing_report.html', {'resume': resume, 'report': None})

@login_required
def job_match(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    report = get_object_or_404(AnalysisReport, resume=resume)
    
    from .models import JobMatchResult
    latest_match = JobMatchResult.objects.filter(resume=resume).order_by('-created_at').first()
    
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            job_desc = form.cleaned_data['job_description']
            
            new_match = JobMatchResult.objects.create(
                resume=resume,
                job_description=job_desc,
                status='processing'
            )
            
            from .tasks import process_job_match_task
            process_job_match_task(new_match.id)
            
            from django.shortcuts import redirect
            return redirect('job_match', resume_id=resume.id)
    else:
        form = JobDescriptionForm()
        
    context = {
        'resume': resume,
        'form': form,
        'latest_match': latest_match,
    }
    return render(request, 'analysis/job_match.html', context)

import io
from django.http import FileResponse
from .utils import generate_pdf_report

@login_required
def download_pdf_report(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    report = get_object_or_404(AnalysisReport, resume=resume)
    
    from .models import JobMatchResult
    last_match = JobMatchResult.objects.filter(resume=resume).order_by('-created_at').first()
    
    match_pct = last_match.match_percentage if last_match else None
    matched = last_match.matched_keywords if last_match else []
    missing = last_match.missing_keywords if last_match else []
    suggestions = last_match.suggestions if last_match else []
    
    # Generate PDF in memory
    buffer = io.BytesIO()
    generate_pdf_report(
        buffer=buffer,
        user_name=request.user.username,
        resume_name=resume.file.name.split('/')[-1],
        ats_score=report.ats_score,
        match_percentage=match_pct,
        matched_skills=matched,
        missing_skills=missing,
        suggestions=suggestions
    )
    buffer.seek(0)
    
    filename = f"SmartHire_ATS_Report_{request.user.username}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)

from django.http import JsonResponse

@login_required
def status_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if hasattr(resume, 'analysis'):
        return JsonResponse({'status': resume.analysis.status, 'error': resume.analysis.error_message})
    return JsonResponse({'status': 'pending', 'error': None})

@login_required
def status_job_match(request, match_id):
    from .models import JobMatchResult
    match = get_object_or_404(JobMatchResult, id=match_id, resume__user=request.user)
    return JsonResponse({'status': match.status, 'error': match.error_message})

@login_required
def smart_job_assistant(request, match_id):
    from .models import JobMatchResult
    match = get_object_or_404(JobMatchResult, id=match_id, resume__user=request.user)
    
    # Analyze using the new smart engine
    analysis = analyze_smart_assistant(match)
    
    context = {
        'match': match,
        'analysis': analysis,
    }
    return render(request, 'analysis/smart_assistant.html', context)
