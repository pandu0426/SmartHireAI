from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ResumeUploadForm
from .models import Resume
import os

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    context = {
        'resumes': resumes
    }
    return render(request, 'resume/dashboard.html', context)

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            from analysis.models import AnalysisReport
            report = AnalysisReport.objects.create(resume=resume, status='processing')
            from analysis.tasks import process_resume_task
            process_resume_task(report.id)
            messages.success(request, 'Resume uploaded and analyzed successfully!')
            # Provide an automatic redirect to analyze the resume immediately.
            # We haven't created the analysis view yet, but the URL will be 'analyze_resume'
            return redirect('analyze_resume', resume_id=resume.id)
    else:
        form = ResumeUploadForm()
    return render(request, 'resume/upload.html', {'form': form})

@login_required
def delete_resume(request, resume_id):
    resume = Resume.objects.get(id=resume_id, user=request.user)
    if resume.file:
        if os.path.isfile(resume.file.path):
            os.remove(resume.file.path)
    resume.delete()
    messages.success(request, 'Resume deleted.')
    return redirect('dashboard')
