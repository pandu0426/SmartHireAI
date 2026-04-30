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
    """Legacy wrapper for backward compatibility."""
    return calculate_ats_score_v2(text)

def calculate_ats_score_v2(text):
    """
    Advanced ATS Scoring Engine (v2).
    A multi-factor weighted index (0-100):
    - Relevance (40%): Skill density and technical depth
    - Impact (30%): Action verbs and measurable achievements
    - Structure (20%): Layout friendliness and section coverage
    - Presence (10%): Contact accessibility and professional links
    """
    if not text or not text.strip():
        return 0

    text_lower = text.lower()
    words = text.split()
    total_words = len(words)
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # --- 1. Relevance (40 pts) ---
    # Measure technical entity density against a professional baseline (approx 12 skills)
    tech_entities = _extract_technical_entities(text)
    relevance_score = min((len(tech_entities) / 12) * 40, 40)
    
    # Keyword stuffing penalty (If > 20% of words are tech keywords, it looks unnatural)
    if total_words > 50:
        density = len(tech_entities) / total_words
        if density > 0.20:
            relevance_score *= 0.7  # 30% penalty for stuffing

    # --- 2. Impact (30 pts) ---
    # A. Action Verb Detection (Check if lines start with impact verbs)
    impact_verbs = {'developed', 'built', 'designed', 'spearheaded', 'managed', 'implemented', 'optimized', 'led', 'created', 'automated'}
    verb_hits = 0
    for line in lines[:50]: # Scan first 50 lines
        first_word = re.sub(r'[^a-zA-Z]', '', line.split()[0].lower()) if line.split() else ""
        if first_word in impact_verbs:
            verb_hits += 1
    
    # B. Metric Detection (Numbers followed by units)
    metric_patterns = [r'\d+%', r'\$\d+', r'\d+\s*(?:years?|yrs?|users?|projects?|employees?|clients?)']
    metrics_found = 0
    for pattern in metric_patterns:
        metrics_found += len(re.findall(pattern, text_lower))
    
    impact_score = min((verb_hits * 4) + (metrics_found * 6), 30)

    # --- 3. Structure (20 pts) ---
    # A. Section Coverage
    core_sections = ['education', 'experience', 'skills', 'projects', 'summary']
    sections_found = sum(1 for s in core_sections if s in text_lower)
    
    # B. Layout Heuristics
    # Check for excessive short lines (often indicates complex columns/graphics)
    short_lines = sum(1 for line in lines if len(line) < 15)
    layout_penalty = 0
    if len(lines) > 10 and (short_lines / len(lines)) > 0.5:
        layout_penalty = 5 # Penalty for potentially unreadable layout
        
    structure_score = max((sections_found * 4) - layout_penalty, 0)

    # --- 4. Presence (10 pts) ---
    # Validate contact info and professional profiles
    has_email = 1 if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text) else 0
    has_phone = 1 if re.search(r'\+?\d{10,15}', text) else 0
    has_linkedin = 1 if 'linkedin.com' in text_lower else 0
    has_github = 1 if 'github.com' in text_lower else 0
    
    presence_score = (has_email * 2.5) + (has_phone * 2.5) + (has_linkedin * 2.5) + (has_github * 2.5)

    # Final Computation
    total_score = relevance_score + impact_score + structure_score + presence_score
    
    # Length Correction (Global)
    if total_words < 200: total_score *= 0.8 # Too brief
    if total_words > 1500: total_score *= 0.9 # Too verbose
    
    return min(int(total_score), 100)

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

# ============================================================
# DEEP TECHNICAL PARSING ENGINE — PROFESSIONAL TAXONOMY
# ============================================================

# --- Programming & Scripting (Versions & Dialects) ---
_LANGUAGES = {
    'python', 'python 3', 'python 2', 'java', 'java 8', 'java 11', 'java 17', 'javascript', 'js', 'es6', 'typescript', 'ts', 'golang', 'go', 'rust',
    'c++', 'cpp', 'c#', 'dotnet', '.net', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab',
    'perl', 'bash', 'shell', 'sh', 'powershell', 'haskell', 'lua', 'dart',
    'elixir', 'clojure', 'groovy', 'solidity', 'assembly', 'fortran',
    'cobol', 'vba', 'objective-c', 'f#', 'erlang', 'zig', 'carbon',
}

# --- Frontend & UI Stacks ---
_FRAMEWORKS_FRONTEND = {
    'react', 'react.js', 'vue', 'vue.js', 'angular', 'angularjs', 'nextjs', 'next.js', 'nuxtjs', 'nuxt.js', 'svelte', 'sveltekit', 'ember',
    'tailwindcss', 'tailwind', 'bootstrap', 'material-ui', 'mui', 'chakra ui', 'ant design', 'daisyui',
    'redux', 'redux toolkit', 'zustand', 'mobx', 'recoil', 'jotai', 'tanstack query', 'react query',
    'graphql', 'apollo', 'relay', 'webgl', 'three.js', 'd3.js', 'webpack', 'vite', 'vite.js', 'babel', 'eslint', 'prettier',
    'storybook', 'pWA', 'webworkers', 'websocket',
}

# --- Backend & API Frameworks ---
_FRAMEWORKS_BACKEND = {
    'django', 'django rest framework', 'drf', 'fastapi', 'flask', 'fastify', 'express', 'express.js', 'nestjs', 'spring',
    'springboot', 'spring boot', 'laravel', 'rails', 'ruby on rails', 'asp.net', 'net core', '.net core',
    'gin', 'fiber', 'echo', 'go-kit', 'phoenix', 'micronaut', 'quarkus', 'ktor',
    'pydantic', 'sqlalchemy', 'alembic', 'hibernate', 'jpa', 'marshmallow', 'prisma', 'typeorm', 'sequelize', 'mongoose',
}

# --- Cloud & Edge Infrastructure ---
_CLOUD = {
    'aws', 'amazon web services', 'azure', 'microsoft azure', 'gcp', 'google cloud', 'digitalocean', 'heroku',
    'cloudflare', 'cloudflare workers', 'vercel', 'netlify', 'render', 'fly.io', 'railway', 'supabase',
    'ec2', 's3', 'lambda', 'rds', 'eks', 'ecs', 'fargate', 'sqs', 'sns', 'athena', 'glue', 'redshift', 'aurora',
    'cloudwatch', 'cloudformation', 'cdk', 'route53', 'api gateway', 'step functions',
    'aks', 'azure functions', 'cosmos db', 'azure ad', 'adf', 'blob storage',
    'bigquery', 'dataflow', 'pubsub', 'gke', 'cloud run', 'vertex ai',
    'vpc', 'iam', 'kms', 'waf', 'cdn', 'security groups', 'multi-region',
}

# --- DevOps / SRE / Platform Engineering ---
_DEVOPS = {
    'docker', 'kubernetes', 'k8s', 'helm', 'kustomize', 'argocd', 'flux', 'fluxcd', 'istio', 'linkerd',
    'terraform', 'ansible', 'puppet', 'chef', 'pulumi', 'crossplane', 'opentofu',
    'jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci', 'azure devops', 'bitbucket pipelines',
    'ci/cd', 'gitops', 'devops', 'devsecops', 'mlops', 'dataops', 'llmops',
    'prometheus', 'grafana', 'alertmanager', 'loki', 'jaeger', 'opentelemetry', 'otel', 'new relic', 'dynatrace',
    'elk', 'elasticsearch', 'logstash', 'kibana', 'datadog', 'splunk', 'graylog',
    'linux', 'ubuntu', 'centos', 'rhel', 'debian', 'alpine', 'nginx', 'apache', 'haproxy', 'traefik',
    'vagrant', 'packer', 'vault', 'hashicorp vault', 'consul', 'nomad', 'etcd',
    'sonarqube', 'snyk', 'trivy', 'aquasecurity', 'falco', 'checkov',
}

# --- Databases & Vector Stores ---
_DATABASES = {
    'postgresql', 'postgres', 'mysql', 'mariadb', 'sqlite', 'oracle',
    'mssql', 'sql server', 'mongodb', 'redis', 'cassandra', 'dynamodb',
    'firestore', 'couchdb', 'neo4j', 'influxdb', 'clickhouse', 'timescaledb',
    'snowflake', 'redshift', 'bigquery', 'hive', 'hbase', 
    'pinecone', 'weaviate', 'qdrant', 'chroma', 'milvus', 'pgvector', 'valkey',
    'cockroachdb', 'planetscale', 'arangodb', 'memcached', 'rocksdb',
}

# --- Data, Streaming & Messaging ---
_DATA_STREAMING = {
    'kafka', 'rabbitmq', 'activemq', 'pulsar', 'nats', 'kinesis', 'eventbridge',
    'flink', 'spark', 'pyspark', 'hadoop', 'hive', 'presto', 'trino', 'dbt',
    'airflow', 'prefect', 'luigi', 'dagster', 'mage-ai',
    'tableau', 'power bi', 'looker', 'superset', 'metabase',
    'pandas', 'numpy', 'polars', 'dask', 'ray', 'spark streaming',
    'etl', 'elt', 'data lake', 'lakehouse', 'data mesh', 'data pipeline',
}

# --- Security & Networking ---
_SECURITY_NETWORKING = {
    'owasp', 'siem', 'iam', 'sso', 'oauth2', 'jwt', 'saml', 'zero trust',
    'ssl', 'tls', 'mtls', 'vpn', 'sd-wan', 'ssh', 'ftp', 'sftp', 'http/2', 'http/3', 'quic',
    'grpc', 'rest api', 'soap', 'tcp/ip', 'udp', 'dns', 'bgp', 'icmp',
    'dhcp', 'subnetting', 'firewall', 'ips/ids', 'ddos protection',
    'penetration testing', 'kali linux', 'burpsuite', 'metasploit', 'nmap', 'wireshark',
    'sast', 'dast', 'sbom', 'cve', 'soc2', 'iso27001', 'gdpr', 'pci-dss',
}

# --- AI, ML & GenAI ---
_AI_ML = {
    'machine learning', 'deep learning', 'nlp', 'computer vision', 'reinforcement learning',
    'generative ai', 'genai', 'llm', 'gpt-4', 'llama', 'claude', 'mistral',
    'rag', 'retrieval augmented generation', 'fine-tuning', 'prompt engineering',
    'embeddings', 'vector embeddings', 'langchain', 'llamaindex', 'huggingface',
    'transformers', 'pytorch', 'tensorflow', 'keras', 'scikit-learn', 'xgboost',
    'model serving', 'triton', 'bentoml', 'onnx',
}

# --- Architectural Patterns ---
_ARCHITECTURE = {
    'microservices', 'monolith', 'serverless', 'event-driven', 'soa',
    'restful api', 'graphql api', 'grpc service', 'distributed systems',
    'high availability', 'ha', 'scalability', 'fault tolerance',
    'domain driven design', 'ddd', 'test driven development', 'tdd',
    'behavior driven development', 'bdd', 'clean architecture', 'hexagonal architecture',
    'mvc', 'mvvm', 'pub/sub', 'message queueing', 'cqrs', 'event sourcing',
}

# --- Technical Stacks (Bonus logic) ---
_STACKS = {
    'mern': {'mongodb', 'express', 'react', 'node.js'},
    'mean': {'mongodb', 'express', 'angular', 'node.js'},
    'lamp': {'linux', 'apache', 'mysql', 'php'},
    'jamstack': {'javascript', 'api', 'markup'},
}

# --- Experience Level Signals ---
_SENIORITY = {
    'junior': 1, 'entry level': 1, 'entry-level': 1, 'associate': 1,
    'mid level': 2, 'mid-level': 2, 'intermediate': 2,
    'senior': 3, 'lead': 3, 'principal': 4, 'staff': 4,
    'architect': 4, 'director': 5, 'head of': 5, 'vp': 5, 'manager': 3,
}

# --- Education Signals ---
_EDUCATION = {
    "bachelor's", 'bachelor', 'bs', 'b.s.', 'b.e.', 'bsc', 'b.sc.',
    "master's", 'master', 'ms', 'm.s.', 'msc', 'm.sc.', 'mba',
    'phd', 'ph.d.', 'doctorate', 'degree', 'computer science',
    'engineering', 'information technology', 'software engineering',
    'data science', 'mathematics', 'statistics',
}

# --- Certification Signals ---
_CERTIFICATIONS = {
    'aws certified', 'azure certified', 'gcp certified', 'cka', 'ckad', 'cks',
    'terraform associate', 'docker certified', 'cissp', 'ceh', 'security+',
    'pmp', 'csp', 'csm', 'cspo', 'prince2', 'itil', 'togaf',
    'databricks', 'google professional', 'microsoft certified',
}

# Combined set for fast entity extraction
_TECH_KNOWLEDGE_BASE = (
    _LANGUAGES | _FRAMEWORKS_FRONTEND | _FRAMEWORKS_BACKEND | _CLOUD |
    _DEVOPS | _DATABASES | _DATA_STREAMING | _SECURITY_NETWORKING |
    _AI_ML | _ARCHITECTURE
)

_YOE_PATTERN = re.compile(r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)', re.IGNORECASE)

def _extract_technical_entities(text):
    """
    Precision extraction of technical entities.
    Handles special characters like C++, .NET, Vue.js, and versioned tech.
    """
    text_lower = ' ' + text.lower().replace('\n', ' ') + ' '
    found = set()

    # Match multi-word or special character tech (longest first)
    multi_word = sorted(
        [s for s in _TECH_KNOWLEDGE_BASE if len(s.split()) > 1 or any(c in s for c in '+.#/-')],
        key=len, reverse=True
    )
    for tech in multi_word:
        # Use word boundaries for non-symbol tech
        pattern = re.escape(tech)
        if tech.isalnum():
            pattern = rf'\b{pattern}\b'
        
        if re.search(pattern, text_lower):
            found.add(tech)
            text_lower = re.sub(pattern, ' __TECH_MATCHED__ ', text_lower)

    # Match remaining single-word alphanumeric tech
    remaining_words = set(re.findall(r'\b[a-zA-Z0-9]{2,}\b', text_lower))
    for tech in _TECH_KNOWLEDGE_BASE:
        if tech in remaining_words:
            found.add(tech)

    # Stack detection
    for stack_name, components in _STACKS.items():
        if stack_name in text_lower:
            found.add(stack_name)
    
    return found

def _infer_seniority(text):
    """Extract seniority level from text (1=junior … 5=exec)."""
    text_lower = text.lower()
    levels = []
    for keyword, level in _SENIORITY.items():
        if keyword in text_lower:
            levels.append(level)
    return round(sum(levels) / len(levels)) if levels else 2  # default = mid


def _extract_years(text):
    """Extract max years of experience requirement from text."""
    matches = _YOE_PATTERN.findall(text)
    if matches:
        return max(int(m) for m in matches)
    return 0


def _extract_education(text):
    """Return set of education-level signals present in text."""
    text_lower = text.lower()
    return {e for e in _EDUCATION if e in text_lower}


def _extract_certifications(text):
    """Return set of certification signals present in text."""
    text_lower = text.lower()
    return {c for c in _CERTIFICATIONS if c in text_lower}


def get_stop_words():
    """Legacy stop-word set — kept for backward compatibility."""
    return {
        'and', 'the', 'is', 'in', 'to', 'with', 'for', 'a', 'of', 'on', 'as', 'an',
        'are', 'be', 'this', 'that', 'from', 'by', 'your', 'you', 'we', 'our', 'will',
        'can', 'or', 'at', 'have', 'has', 'it', 'not', 'all', 'such', 'skills',
        'experience', 'work', 'job', 'team', 'years', 'looking', 'role', 'must',
        'strong', 'ability', 'knowledge', 'development', 'design', 'working',
        'using', 'required', 'preferred',
    }


def _get_technical_category(tech):
    if tech in _LANGUAGES: return 'Programming Language'
    if tech in _FRAMEWORKS_FRONTEND: return 'Frontend Tech'
    if tech in _FRAMEWORKS_BACKEND: return 'Backend Tech'
    if tech in _CLOUD: return 'Cloud Infrastructure'
    if tech in _DEVOPS: return 'DevOps & SRE'
    if tech in _DATABASES: return 'Database & Storage'
    if tech in _DATA_STREAMING: return 'Data & Streaming'
    if tech in _SECURITY_NETWORKING: return 'Security & Networks'
    if tech in _AI_ML: return 'AI & Machine Learning'
    if tech in _ARCHITECTURE: return 'Architecture & Methodology'
    return 'Technical Tool'

def match_job_description(resume_text, job_desc):
    """
    Technical-First Match Engine.
    Evaluates: Tech Stack, Architecture, Seniority, and Granular Skills.
    """
    if not resume_text or not job_desc:
        return 0, [], [], ["Technical data missing for parsing."]

    # 1. Extract Deep Technical Entities
    resume_tech = _extract_technical_entities(resume_text)
    jd_tech = _extract_technical_entities(job_desc)

    # Fallback to basic keywords if no technical entities found
    if not jd_tech:
        resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
        jd_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', job_desc.lower())) - get_stop_words()
        matched = list(resume_words & jd_words)[:12]
        missing = list(jd_words - resume_words)[:12]
        overlap_pct = int((len(matched) / max(len(jd_words), 1)) * 100)
        return overlap_pct, matched, missing, ["Enhance your resume with specific technical tools and frameworks mentioned in the JD."]

    matched_tech = resume_tech & jd_tech
    missing_tech = jd_tech - resume_tech

    # 2. Weighted Scoring (Technical Focus)
    # Technical Knowledge (60%) + Seniority/YOE (25%) + Education/Architecture (15%)
    
    # Tech Score (normalized)
    tech_score = len(matched_tech) / len(jd_tech)
    
    # Architecture overlap (bonus weight)
    res_arch = {t for t in resume_tech if t in _ARCHITECTURE}
    jd_arch = {t for t in jd_tech if t in _ARCHITECTURE}
    arch_score = (len(res_arch & jd_arch) / len(jd_arch)) if jd_arch else 1.0

    # Seniority & YOE
    res_seniority = _infer_seniority(resume_text)
    jd_seniority = _infer_seniority(job_desc)
    yoe_match = 1.0 if _extract_years(resume_text) >= _extract_years(job_desc) else 0.5
    seniority_score = (1.0 if res_seniority >= jd_seniority else 0.5) * yoe_match

    # Final Weighted Computation
    final_score = (tech_score * 0.6) + (seniority_score * 0.25) + (arch_score * 0.15)
    match_percentage = min(int(final_score * 100), 98)

    # 3. Categorized Lists for Professional UI
    matched_list = sorted(list(matched_tech), key=len)[:15]
    missing_list = sorted(list(missing_tech), key=len)[:15]

    # 4. Technical Strategy Suggestions
    suggestions = []
    
    # Priority missing categories
    missing_cats = {}
    for mt in missing_tech:
        cat = _get_technical_category(mt)
        missing_cats.setdefault(cat, []).append(mt.title())

    for cat, techs in list(missing_cats.items())[:3]:
        label = ", ".join(techs[:3])
        suggestions.append(f"<strong>Missing {cat}:</strong> {label}. Add these to your Skills and provide implementation details in your experience bullets.")

    if jd_arch and not (res_arch & jd_arch):
        important_arch = list(jd_arch)[0].upper()
        suggestions.append(f"<strong>Architectural Gap:</strong> The role emphasizes <strong>{important_arch}</strong>. Reframe your projects to highlight your experience with this pattern.")

    if match_percentage < 60:
        suggestions.append("Technical overlap is low. Consider building a <strong>targeted side project</strong> using the missing tech above to bridge the gap.")
    else:
        suggestions.append("Apply now. Ensure your summary lists the exact tech stack mentioned in the JD to pass strict automated filters.")

    return match_percentage, matched_list, missing_list, suggestions[:6]

def generate_resume_feedback(text):
    """
    Advanced Professional Feedback Engine.
    Provides targeted advice based on structural and linguistic gaps.
    """
    feedback = []
    text_lower = text.lower()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # 1. Structural Auditing
    core_sections = {
        'education': 'Missing <b>Education</b> section. Recruiters use this to verify your qualifications.',
        'experience': 'Missing <b>Professional Experience</b>. This is the most critical section for ATS ranking.',
        'skills': 'No <b>Skills</b> section detected. Group your technical expertise for better readability.',
        'projects': 'Missing <b>Projects</b>. Use this section to prove your skills with real-world examples.'
    }
    for key, msg in core_sections.items():
        if key not in text_lower:
            feedback.append(f"<strong>Structural Gap:</strong> {msg}")

    # 2. Impact & Action Verbs
    impact_verbs = {'developed', 'built', 'designed', 'spearheaded', 'managed', 'implemented', 'optimized', 'led'}
    verb_count = 0
    for line in lines[:50]:
        first_word = re.sub(r'[^a-zA-Z]', '', line.split()[0].lower()) if line.split() else ""
        if first_word in impact_verbs:
            verb_count += 1
    
    if verb_count < 4:
        feedback.append("<strong>Weak Phrasing:</strong> Many bullet points don't start with <b>Action Verbs</b>. Use words like <i>Spearheaded</i> or <i>Optimized</i> to show leadership.")

    # 3. Measurable Results
    if not re.search(r'\d+%', text) and not re.search(r'\$\d+', text):
        feedback.append("<strong>Static Content:</strong> No quantifiable metrics detected (%, $). Professional resumes should show <b>measurable impact</b>.")

    # 4. Professional Presence
    if 'linkedin.com' not in text_lower:
        feedback.append("<strong>Missing LinkedIn:</strong> Include your profile link. 87% of recruiters use LinkedIn to vet candidates.")
    
    if 'github.com' not in text_lower and any(tech in text_lower for tech in ['python', 'javascript', 'java']):
        feedback.append("<strong>Missing GitHub:</strong> For technical roles, a GitHub link acts as a live portfolio.")

    # 5. ATS Layout Friendliness
    short_lines = sum(1 for line in lines if len(line) < 15)
    if len(lines) > 10 and (short_lines / len(lines)) > 0.45:
        feedback.append("<strong>Layout Warning:</strong> Excessive short lines detected. Avoid <b>multi-column layouts</b> or graphics that can confuse older ATS parsers.")

    # Fallback
    if not feedback:
        feedback.append("<strong>Excellent Profile:</strong> Your resume follows professional standards. Focus on tailoring it to specific job descriptions next!")
        
    return feedback[:6]

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(buffer, user_name, resume_name, ats_score, match_percentage, matched_skills, missing_skills, suggestions, feedback=None, action_verbs=None, metrics=None):
    """
    Generates a premium Resume Intelligence PDF Report.
    """
    from reportlab.lib.units import inch
    
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary = colors.HexColor('#3b82f6')
    dark = colors.HexColor('#0f172a')
    muted = colors.HexColor('#64748b')
    bg_light = colors.HexColor('#f8fafc')
    success = colors.HexColor('#10b981')
    
    # Custom Styles
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=28, spaceAfter=10, textColor=dark, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Normal'], fontSize=11, spaceAfter=25, textColor=muted)
    section_title = ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=16, spaceBefore=25, spaceAfter=15, textColor=primary, fontName='Helvetica-Bold')
    card_title = ParagraphStyle('CardTitle', parent=styles['Normal'], fontSize=10, textColor=muted, alignment=1, fontName='Helvetica-Bold', spaceAfter=5)
    card_value = ParagraphStyle('CardValue', parent=styles['Normal'], fontSize=22, textColor=dark, alignment=1, fontName='Helvetica-Bold')
    bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontSize=10, leftIndent=15, spaceAfter=12, leading=16, textColor=colors.HexColor('#334155'))
    tag_style = ParagraphStyle('TagStyle', parent=styles['Normal'], fontSize=9, textColor=dark, leading=14)
    
    elements = []
    
    # --- Header ---
    elements.append(Paragraph("Resume Intelligence Report", title_style))
    elements.append(Paragraph(f"<b>Candidate:</b> {user_name}  |  <b>Document:</b> {resume_name}  |  <b>Report Date:</b> {re.sub(r' .*', '', str(colors.black))}", subtitle_style))
    elements.append(Spacer(1, 10))
    
    # --- Score Overview Table (Modern Cards) ---
    score_data = [
        [Paragraph("ATS COMPATIBILITY", card_title), Paragraph("JOB MATCH SCORE", card_title)],
        [Paragraph(f"{ats_score}/100", card_value), Paragraph(f"{match_percentage}%" if match_percentage is not None else "N/A", card_value)]
    ]
    score_table = Table(score_data, colWidths=[2.8*inch, 2.8*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 15),
        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 20))

    # --- Intelligence Audit (Action Verbs & Metrics) ---
    if action_verbs or metrics:
        elements.append(Paragraph("Linguistic Intelligence Audit", section_title))
        audit_data = [
            [Paragraph(f"<b>{len(action_verbs) if action_verbs else 0}</b> Impact Verbs Found", tag_style), 
             Paragraph(f"<b>{len(metrics) if metrics else 0}</b> Measurable Metrics", tag_style)]
        ]
        audit_table = Table(audit_data, colWidths=[2.8*inch, 2.8*inch])
        audit_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#bfdbfe')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        elements.append(audit_table)
        elements.append(Spacer(1, 10))

    # --- Improvement Roadmap (The main focus) ---
    elements.append(Paragraph("Actionable Improvement Roadmap", section_title))
    if feedback:
        for i, item in enumerate(feedback, 1):
            clean_item = re.sub(r'<[^>]+>', '', item)
            elements.append(Paragraph(f"<b>{i}.</b> {clean_item}", bullet_style))
    else:
        elements.append(Paragraph("• Continue optimizing your resume with quantifiable metrics.", bullet_style))

    # --- Technical Skills Gap (If Job Match exists) ---
    if match_percentage is not None:
        elements.append(Paragraph("Keyword Gap Analysis", section_title))
        
        # Missing Keywords
        elements.append(Paragraph("<b>Priority Keywords to Integrate:</b>", tag_style))
        if missing_skills:
            missing_str = ", ".join([word.title() for word in missing_skills[:12]])
            elements.append(Paragraph(missing_str, ParagraphStyle('SmallStyle', fontSize=10, textColor=muted, spaceBefore=5)))
        else:
            elements.append(Paragraph("Excellent! No major technical gaps found.", ParagraphStyle('SmallStyle', fontSize=10, textColor=success, spaceBefore=5)))
            
        elements.append(Spacer(1, 15))
        
        # Strategic Advice
        elements.append(Paragraph("<b>Strategic Recommendation:</b>", tag_style))
        for item in suggestions[:3]:
            clean_item = re.sub(r'<[^>]+>', '', item)
            elements.append(Paragraph(f"• {clean_item}", ParagraphStyle('AdviceStyle', fontSize=9, textColor=muted, spaceBefore=5)))
            
    # --- Footer ---
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("<i>This report was generated by SmartHireAI Intelligence Engine v2.0. Recommended for professional use only.</i>", 
                             ParagraphStyle('Footer', fontSize=8, textColor=muted, alignment=1)))
        
    doc.build(elements)


def _extract_action_verbs(text):
    """Detects high-impact professional action verbs."""
    verbs = {
        'spearheaded', 'orchestrated', 'architected', 'optimized', 'streamlined',
        'accelerated', 'pioneered', 'implemented', 'designed', 'developed',
        'automated', 'managed', 'led', 'negotiated', 'transformed', 'delivered',
        'achieved', 'increased', 'reduced', 'saved', 'mentored', 'coordinated',
        'maximized', 'authored', 'established', 'facilitated', 'executed'
    }
    found = {v for v in verbs if v in text.lower()}
    return list(found)

def _extract_metrics(text):
    """Detects quantifiable metrics (percentages, currency, large numbers)."""
    patterns = [
        r'\d+%', r'%\s+improvement', r'\$\d+', r'\d+\s*k', r'\d+\s*m',
        r'increased\s+by\s+\d+', r'reduced\s+by\s+\d+', r'saved\s+\d+', r'managed\s+\d+'
    ]
    matches = []
    for p in patterns:
        matches.extend(re.findall(p, text.lower()))
    return list(set(matches))

def _get_partial_matches(missing_skills, resume_skills):
    """
    Implements a semantic neighbor check.
    If a required skill is missing, check if the user has a closely related skill.
    """
    clusters = [
        {'react', 'nextjs', 'next.js', 'redux', 'vue', 'angular', 'svelte'}, # Frontend
        {'django', 'flask', 'fastapi', 'pyramid', 'backend'}, # Python Backend
        {'nodejs', 'node.js', 'express', 'nestjs', 'javascript', 'typescript'}, # JS Backend
        {'aws', 'azure', 'gcp', 'cloud', 'digitalocean', 'lambda', 's3'}, # Cloud
        {'postgresql', 'postgres', 'mysql', 'sql', 'mariadb', 'oracle', 'sqlite'}, # SQL
        {'mongodb', 'redis', 'cassandra', 'dynamodb', 'nosql'}, # NoSQL
        {'docker', 'kubernetes', 'k8s', 'helm', 'containers'}, # Containerization
        {'terraform', 'ansible', 'pulumi', 'cloudformation', 'iac'}, # IaC
    ]
    partials = []
    for missing in missing_skills:
        for cluster in clusters:
            if missing in cluster:
                # User has a neighbor but not the exact skill
                neighbors = cluster.intersection(resume_skills)
                if neighbors:
                    partials.append({'missing': missing, 'have': list(neighbors)[0]})
                    break
    return partials


def _generate_improvement_roadmap(match_data, resume_text, jd_text):
    """
    JD-Aware logic to generate a structured, professional improvement roadmap.
    """
    roadmap = []
    
    # 1. Critical Fixes (High Priority)
    critical = []
    missing_tech = match_data.get('missing_skills', [])
    if missing_tech:
        top_missing = ", ".join([s.title() for s in missing_tech[:3]])
        critical.append(f"Add projects or certifications related to <strong>{top_missing}</strong>. These are focal points in the JD.")
    
    if match_data.get('tech_score', 100) < 50:
        critical.append("Your tech stack alignment is below 50%. Focus on bridging the core technical gaps before applying.")
    
    if critical:
        roadmap.append({'title': 'Critical Fixes', 'items': critical, 'priority': 'HIGH', 'color': 'danger'})

    # 2. Strengthen Resume (Mid Priority)
    strengthen = []
    partials = match_data.get('partial_matches', [])
    for p in partials[:2]:
        strengthen.append(f"Highlight your <strong>{p['have'].title()}</strong> experience more clearly to substitute for the requested <strong>{p['missing'].title()}</strong>.")
    
    # JD-specific context detection (Simple pattern matching)
    jd_lower = jd_text.lower()
    if 'scale' in jd_lower or 'performance' in jd_lower:
        strengthen.append("The JD emphasizes system performance. Add details about how you optimized code or handled high traffic.")
    if 'team' in jd_lower or 'collaborate' in jd_lower:
        strengthen.append("Collaborative culture detected. Mention cross-functional teamwork or peer code reviews.")
        
    if strengthen:
        roadmap.append({'title': 'Strengthen Alignment', 'items': strengthen, 'priority': 'MEDIUM', 'color': 'warning'})

    # 3. Content & Verb Optimization
    optimize = []
    verbs = match_data.get('verb_list', [])
    if len(verbs) < 5:
        optimize.append("Replace passive phrases like 'worked on' or 'helped with' with stronger verbs like <strong>'Architected'</strong> or <strong>'Spearheaded'</strong>.")
    else:
        optimize.append("Good use of action verbs. Ensure they are placed at the start of each bullet point for maximum impact.")
        
    roadmap.append({'title': 'Content Optimization', 'items': optimize, 'priority': 'LOW', 'color': 'primary'})

    # 4. Quantifiable Impact
    impact = []
    metrics = match_data.get('metric_list', [])
    if len(metrics) < 3:
        impact.append("Missing metrics. Add quantifiable results like <strong>'% improvement'</strong> or <strong>'time saved'</strong> to validate your achievements.")
    else:
        impact.append("Metrics detected! Ensure these are highlighted in your most recent experience section.")
        
    roadmap.append({'title': 'Quantifiable Impact', 'items': impact, 'priority': 'MEDIUM', 'color': 'success'})

    # 5. Keyword Injection
    keywords = []
    jd_words = set(re.findall(r'\b[a-z]{4,}\b', jd_text.lower()))
    resume_words = set(re.findall(r'\b[a-z]{4,}\b', resume_text.lower()))
    missing_keywords = list(jd_words - resume_words - set(get_stop_words()))[:6]
    
    if missing_keywords:
        kw_list = ", ".join([k.title() for k in missing_keywords])
        keywords.append(f"Naturally integrate these keywords: <strong>{kw_list}</strong> into your Professional Summary.")
        
    roadmap.append({'title': 'Keyword Injection', 'items': keywords, 'priority': 'LOW', 'color': 'info'})

    return roadmap

def _identify_recommended_roles(skills):
    """
    Maps detected skills to 3-5 entry-level job roles.
    """
    role_mapping = {
        'Python Developer': ['python', 'django', 'flask', 'fastapi'],
        'Backend Developer': ['python', 'java', 'node.js', 'sql', 'postgresql', 'api', 'rest'],
        'Frontend Developer': ['javascript', 'react', 'vue', 'angular', 'html', 'css', 'typescript'],
        'Full Stack Developer': ['python', 'javascript', 'react', 'django', 'node.js', 'sql'],
        'Data Analyst': ['python', 'sql', 'pandas', 'numpy', 'data analysis', 'excel', 'tableau'],
        'DevOps Specialist': ['docker', 'kubernetes', 'aws', 'linux', 'ci/cd', 'terraform', 'ansible'],
    }
    
    recommended = []
    skills_lower = [s.lower() for s in skills]
    
    for role, required in role_mapping.items():
        # If user has at least 2 matching skills for a role, recommend it
        match_count = len([s for s in required if s in skills_lower])
        if match_count >= 2:
            recommended.append(role)
            
    # Default fallback if no roles matched
    if not recommended:
        recommended = ['Software Engineer', 'Technical Associate']
        
    return recommended[:4]

def _generate_job_links(role):
    """
    Generates dynamic search URLs for major job boards.
    """
    import urllib.parse
    query = urllib.parse.quote(f"{role} fresher india")
    
    return {
        'role': role,
        'linkedin': f"https://www.linkedin.com/jobs/search/?keywords={query}",
        'indeed': f"https://in.indeed.com/jobs?q={query}",
        'naukri': f"https://www.naukri.com/{role.lower().replace(' ', '-')}-jobs"
    }

def analyze_smart_assistant(job_match):
    """
    Advanced technical analysis engine. 
    70% Semantic Tech Match | 15% Verbs | 15% Metrics
    """
    resume_text = job_match.resume.analysis.extracted_text
    jd_text = job_match.job_description
    
    # Base Tech Analysis
    tech_pct, matched_tech, missing_tech, _ = match_job_description(resume_text, jd_text)
    
    # Semantic Intelligence
    partials = _get_partial_matches(missing_tech, _extract_technical_entities(resume_text))
    boost = min(len(partials) * 2, 10)
    adjusted_tech = min(tech_pct + boost, 100)
    
    # Action Verbs
    verbs = _extract_action_verbs(resume_text)
    verb_score = min((len(verbs) / 12) * 100, 100)
    
    # Metrics
    metrics = _extract_metrics(resume_text)
    metric_score = min((len(metrics) / 6) * 100, 100)
    
    # Final Formula
    raw_smart_score = (adjusted_tech * 0.70) + (verb_score * 0.15) + (metric_score * 0.15)
    
    match_data = {
        'tech_score': int(adjusted_tech),
        'verb_score': int(verb_score),
        'metric_score': int(metric_score),
        'matched_skills': matched_tech,
        'missing_skills': missing_tech,
        'partial_matches': partials,
        'verb_list': verbs[:8],
        'metric_list': metrics[:6]
    }
    
    # Generate the Smart Roadmap
    roadmap = _generate_improvement_roadmap(match_data, resume_text, jd_text)
    
    # Generate Role Recommendations
    all_skills = list(set(matched_tech) | set(_extract_technical_entities(resume_text)))
    recommended_roles = _identify_recommended_roles(all_skills)
    job_opportunities = [_generate_job_links(role) for role in recommended_roles]
    
    return {
        'smart_score': int(raw_smart_score),
        'tech_score': match_data['tech_score'],
        'verb_score': match_data['verb_score'],
        'metric_score': match_data['metric_score'],
        'verb_count': len(verbs),
        'metric_count': len(metrics),
        'matched_skills': matched_tech,
        'missing_skills': missing_tech,
        'partial_matches': partials[:3],
        'verb_list': match_data['verb_list'],
        'metric_list': match_data['metric_list'],
        'roadmap': roadmap,
        'recommended_roles': job_opportunities
    }


