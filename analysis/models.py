from django.db import models
from resume.models import Resume


class AnalysisReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='analysis')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    error_message = models.TextField(blank=True, null=True)
    extracted_text = models.TextField(blank=True, null=True)
    ats_score = models.IntegerField(default=0)
    skills_found = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.resume}"

class JobMatchResult(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='job_matches')
    job_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    error_message = models.TextField(blank=True, null=True)
    match_percentage = models.IntegerField(null=True, blank=True)
    matched_keywords = models.JSONField(default=list, blank=True)
    missing_keywords = models.JSONField(default=list, blank=True)
    suggestions = models.JSONField(default=list, blank=True)
    resume_feedback = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job Match for {self.resume} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
