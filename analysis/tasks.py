import logging
from resume.models import Resume
from analysis.models import AnalysisReport, JobMatchResult
from analysis.utils import extract_text_from_pdf, calculate_ats_score, extract_skills, match_job_description, generate_resume_feedback

logger = logging.getLogger(__name__)

def process_resume_task(report_id):
    try:
        report = AnalysisReport.objects.select_related('resume').get(id=report_id)
    except AnalysisReport.DoesNotExist:
        logger.error(f"AnalysisReport with id={report_id} does not exist.")
        return

    try:
        resume = report.resume
        if not resume or not resume.file:
            raise ValueError("No resume file found for this report.")

        text = extract_text_from_pdf(resume.file.path)
        
        # Validations and fallbacks
        if not text or not text.strip():
            logger.warning(f"Extracted text is empty for report_id={report_id}")
            text = "Could not extract text from document."
            score = 0
            skills = []
        else:
            score = calculate_ats_score(text)
            skills = extract_skills(text)
        
        report.extracted_text = text
        report.ats_score = score
        report.skills_found = skills
        
        # Ensure values are safely set before confirming success
        report.status = 'completed'
        report.error_message = ""
        report.save()
        logger.info(f"Successfully processed resume for report_id={report_id}")
        
    except Exception as e:
        error_msg = f"Error processing resume: {str(e)}"
        logger.error(f"{error_msg} for report_id={report_id}", exc_info=True)
        # Update state ensuring it is always handled and constrained to proper length limit
        report.status = 'failed'
        report.error_message = error_msg[:500]
        report.save(update_fields=['status', 'error_message'])


def process_job_match_task(job_match_id):
    try:
        job_match = JobMatchResult.objects.select_related('resume__analysis').get(id=job_match_id)
    except JobMatchResult.DoesNotExist:
        logger.error(f"JobMatchResult with id={job_match_id} does not exist.")
        return

    try:
        # Validate that resume analysis actually exists
        if not hasattr(job_match.resume, 'analysis') or not job_match.resume.analysis:
            raise ValueError("Resume analysis is incomplete or missing.")
            
        resume_text = job_match.resume.analysis.extracted_text
        if not resume_text or not resume_text.strip():
            resume_text = ""
            
        job_desc = job_match.job_description if job_match.job_description else ""
        results = match_job_description(resume_text, job_desc)
        
        # Validate result tuple before unpacking exactly 4 fields
        if not isinstance(results, (tuple, list)) or len(results) != 4:
            logger.warning(f"Unexpected return from match_job_description: {results}")
            match_percentage, matched_list, missing_list, suggestions = 0, [], [], ["Parsing error during job match."]
        else:
            match_percentage, matched_list, missing_list, suggestions = results
            
        feedback = generate_resume_feedback(resume_text)
        
        # Map values with fallbacks
        job_match.match_percentage = match_percentage
        job_match.matched_keywords = matched_list if matched_list else []
        job_match.missing_keywords = missing_list if missing_list else []
        job_match.suggestions = suggestions if suggestions else []
        job_match.resume_feedback = feedback if feedback else []
        
        job_match.status = 'completed'
        job_match.error_message = ""
        job_match.save()
        logger.info(f"Successfully processed job match for job_match_id={job_match_id}")
        
    except Exception as e:
        error_msg = f"Error processing job match: {str(e)}"
        logger.error(f"{error_msg} for job_match_id={job_match_id}", exc_info=True)
        job_match.status = 'failed'
        job_match.error_message = error_msg[:500]
        job_match.save(update_fields=['status', 'error_message'])
