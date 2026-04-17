from django.urls import path
from . import views

urlpatterns = [
    path('report/<int:resume_id>/', views.analyze_resume, name='analyze_resume'),
    path('match/<int:resume_id>/', views.job_match, name='job_match'),
    path('download-report/<int:resume_id>/', views.download_pdf_report, name='download_pdf_report'),
    path('status/resume/<int:resume_id>/', views.status_resume, name='status_resume'),
    path('status/match/<int:match_id>/', views.status_job_match, name='status_job_match'),
]
