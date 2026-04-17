import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def calculate_ats_score(text):
    """
    A simulated ATS scoring algorithm.
    Checks for common resume sections and standard keywords.
    """
    score = 40 # Base score

    text_lower = text.lower()
    
    # Check for sections
    sections = ['education', 'experience', 'skills', 'projects', 'summary', 'objective']
    for section in sections:
        if section in text_lower:
            score += 5
            
    # Check for quantifiable bullet points (simulated by checking for numbers/digits)
    if re.search(r'\d+', text):
        score += 10
        
    # Check length
    word_count = len(text.split())
    if 300 < word_count < 1000:
        score += 10
    elif word_count >= 1000:
        score -= 5 # too long
        
    # Cap at 100
    return min(score, 100)

def extract_skills(text):
    """
    Very basic skill extraction using a predefined list.
    """
    common_skills = [
        'python', 'java', 'javascript', 'c++', 'html', 'css', 'react', 'django', 
        'sql', 'aws', 'docker', 'machine learning', 'data analysis', 'excel',
        'communication', 'leadership', 'agile', 'scrum', 'git', 'node.js',
        'bootstrap', 'linux'
    ]
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))

def get_stop_words():
    return {'and', 'the', 'is', 'in', 'to', 'with', 'for', 'a', 'of', 'on', 'as', 'an', 'are', 'be', 'this', 'that', 'from', 'by', 'your', 'you', 'we', 'our', 'will', 'can', 'or', 'at', 'have', 'has', 'it', 'not', 'all', 'such', 'skills', 'experience', 'work', 'job', 'team', 'years', 'looking', 'role', 'must', 'strong', 'ability', 'knowledge', 'development', 'design', 'working', 'using', 'required', 'preferred'}

def match_job_description(resume_text, job_desc):
    """
    Simulated job description matching based on keyword overlap.
    Returns: match_percentage, matched_keywords, missing_keywords, suggestions
    """
    resume_words = set(re.findall(r'[a-zA-Z]{3,}', resume_text.lower()))
    jd_words = set(re.findall(r'[a-zA-Z]{3,}', job_desc.lower()))
    
    stop_words = get_stop_words()
    jd_keywords = jd_words - stop_words
    
    if not jd_keywords:
        return 0, [], [], []
        
    overlap = jd_keywords.intersection(resume_words)
    missing = jd_keywords - resume_words
    
    match_percentage = int((len(overlap) / len(jd_keywords)) * 100)
    
    matched_list = list(overlap)[:15]
    missing_list = list(missing)[:15]
    
    # Generate Smart Suggestions
    suggestions = []
    if missing_list:
        suggestions.append(f"Add more experience related to: <strong>{missing_list[0].title()}</strong> and <strong>{missing_list[1].title() if len(missing_list)>1 else ''}</strong>.")
        suggestions.append(f"Include specific projects demonstrating your ability in <strong>{missing_list[-1].title()}</strong>.")
    
    if match_percentage < 50:
        suggestions.append("Tailor your professional summary to explicitly state your interest and basic capabilities in this specific role.")
    
    suggestions.append("Highlight achievements with measurable impact (e.g., 'Increased efficiency by 20%').")
    suggestions.append("Use strong action verbs such as: Architected, Orchestrated, Optimized, and Spearheaded.")
    
    return match_percentage, matched_list, missing_list, suggestions

def generate_resume_feedback(text):
    """Analyze resume text and give feedback on weak areas"""
    feedback = []
    text_lower = text.lower()
    
    if not re.search(r'\d+', text):
        feedback.append("<strong>Lack of Metrics:</strong> No numbers detected. Quantify your achievements (e.g., team size, budgets, percentages).")
        
    if 'project' not in text_lower:
        feedback.append("<strong>Missing Projects:</strong> Consider adding a 'Projects' section to showcase practical applications of your skills.")
        
    word_count = len(text.split())
    if word_count < 250:
        feedback.append("<strong>Brief Content:</strong> Your resume seems too short. Expand on your responsibilities and achievements.")
        
    if 'education' not in text_lower:
        feedback.append("<strong>Missing Education:</strong> Ensure your educational background is clearly labeled.")
        
    if not feedback:
        feedback.append("<strong>Solid Foundation:</strong> Your resume hits the basic structural requirements. Focus on keyword optimization next!")
        
    return feedback

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(buffer, user_name, resume_name, ats_score, match_percentage, matched_skills, missing_skills, suggestions):
    """
    Generates a professional PDF report containing the resume analysis and job match results.
    """
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=24, spaceAfter=20, textColor=colors.HexColor('#0f172a'))
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Normal'], fontSize=12, spaceAfter=20, textColor=colors.HexColor('#64748b'))
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=16, spaceBefore=20, spaceAfter=10, textColor=colors.HexColor('#3b82f6'))
    normal_style = styles['Normal']
    list_style = ParagraphStyle('ListStyle', parent=styles['Normal'], leftIndent=20, spaceAfter=5)
    
    elements = []
    
    # Header
    elements.append(Paragraph(f"SmartHireAI ATS Report", title_style))
    elements.append(Paragraph(f"Prepared for: <b>{user_name}</b> | Resume file: {resume_name}", subtitle_style))
    elements.append(Spacer(1, 20))
    
    # Overview Score Table
    data = [
        ['Overall ATS Score', 'Job Description Match'],
        [f'{ats_score}/100', f'{match_percentage}%' if match_percentage is not None else 'N/A']
    ]
    t = Table(data, colWidths=[250, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('TEXTCOLOR', (0,1), (-1,1), colors.HexColor('#3b82f6')),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 18),
        ('TOPPADDING', (0,1), (-1,1), 15),
        ('BOTTOMPADDING', (0,1), (-1,1), 15),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1'))
    ]))
    elements.append(t)
    elements.append(Spacer(1, 30))
    
    if match_percentage is not None:
        # Keywords Section
        elements.append(Paragraph("Keyword Analysis", heading_style))
        
        # Matched Skills
        elements.append(Paragraph("<b>✅ Matched Keywords:</b>", normal_style))
        if matched_skills:
            matched_str = ", ".join([word.title() for word in matched_skills])
            elements.append(Paragraph(matched_str, list_style))
        else:
            elements.append(Paragraph("None detected.", list_style))
        elements.append(Spacer(1, 10))
            
        # Missing Skills
        elements.append(Paragraph("<b>❌ Missing Keywords to Add:</b>", normal_style))
        if missing_skills:
            missing_str = ", ".join([word.title() for word in missing_skills])
            elements.append(Paragraph(missing_str, list_style))
        else:
            elements.append(Paragraph("Perfect! No major keywords missing.", list_style))
        elements.append(Spacer(1, 30))
        
        # Improvement Suggestions
        elements.append(Paragraph("Recommendations to Improve Resume", heading_style))
        for item in suggestions:
            # remove html tags manually for pdf parsing
            clean_item = re.sub(r'<[^>]+>', '', item)
            elements.append(Paragraph(f"• {clean_item}", list_style))
            
    else:
        elements.append(Paragraph("Job description analysis was not performed. Upload a job posting to see specific keyword gaps and recommendations.", normal_style))
        
    doc.build(elements)
