from django import forms

class JobDescriptionForm(forms.Form):
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Paste job description here...'}),
        label="Target Job Description"
    )
