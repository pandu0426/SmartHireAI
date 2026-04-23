import re
import random

# ============================================================
# COMPREHENSIVE CAREER KNOWLEDGE BASE
# ============================================================
KNOWLEDGE_BASE = {

    'resume_tips': [
        "Use the XYZ formula per bullet: 'Accomplished [X], as measured by [Y], by doing [Z]'.",
        "One page for under 10 years experience. Two pages max for 10+ years — never three.",
        "Include LinkedIn and GitHub URLs at the very top — recruiters check both in the first 30 seconds.",
        "Replace Objective Statements with a 2–3 line Professional Summary targeting your exact role.",
        "Every bullet must start with a past-tense action verb: Engineered, Automated, Led, Reduced, Shipped.",
        "Quantify every achievement — team size, % improvement, $ saved, users served, uptime achieved.",
        "Use a single-column layout — two-column designs frequently break ATS parsers.",
        "Save as PDF named: FirstName_LastName_Resume.pdf — not 'CV_final_v3.docx'.",
        "ATS scans for exact keyword matches — copy phrases verbatim from the job description.",
        "Strict reverse chronological order — most recent role first, always.",
        "Remove photos, headshots, logos, text boxes, tables, and headers/footers — all break ATS.",
        "Font: Calibri, Arial, or Garamond. Body: 10–12pt. Name: 14–16pt. Margins: 0.5–1 inch.",
        "Include a Skills section with 10–15 hard skills listed as comma-separated keywords.",
        "Don't list soft skills as bullet points — prove them through achievement bullets instead.",
        "Education goes after Experience unless you're a fresh grad or recent bootcamp graduate.",
        "Tailor your resume per application — embed 5 exact JD keywords in your bullets.",
        "Avoid first-person pronouns — write in implied-first-person: 'Engineered...' not 'I engineered...'",
    ],

    'ats_tips': [
        "ATS filters your resume before any human sees it — optimise for both machine and human readers.",
        "Use the exact job title from the posting in your resume headline and Professional Summary.",
        "Standard section headers only: Work Experience, Education, Skills, Projects, Certifications.",
        "Spell out acronyms first: 'Continuous Integration/Continuous Delivery (CI/CD)', then use CI/CD.",
        "Tables and multi-column layouts break most ATS parsers — avoid both entirely.",
        "White space matters — line spacing 1.0–1.15 keeps it readable and ATS-friendly.",
        "Include exact required skills from the JD in your Skills section — exact phrasing matters.",
        "Professional email only: firstname.lastname@gmail.com — not gamer_king99@hotmail.com.",
        "Avoid headers/footers — ATS often ignores content placed inside them.",
        "PDF is generally safe but some older ATS prefer .docx — check what the portal specifies.",
    ],

    'job_search': [
        "Apply + Network formula: for every 5 applications, send 1 personalised LinkedIn message to a recruiter at that company.",
        "Set up job alerts on LinkedIn, Indeed, Wellfound (startups), Glassdoor, and the company's own Careers page.",
        "Track every application: Company | Role | Date Applied | Status | Contact | Next Step.",
        "Follow up 5–7 business days after applying — most candidates never do this.",
        "Weak ties get you hired — ex-colleagues and alumni matter more than close friends.",
        "The 'Easy Apply' button means 500+ people clicked it. Direct applications convert 9x better.",
        "Target companies 1–2 tiers above your current employer — that's where 40–60% salary jumps live.",
        "Referrals are 9x more likely to result in an interview. Ask your network before applying cold.",
        "Cold outreach template: 1 sentence about them → 1 sentence about your background → 1 specific ask.",
        "Active job search typically takes 2–4 months for mid-level roles. Set weekly targets: 10 applications, 5 follow-ups, 2 coffee chats.",
    ],

    'linkedin_tips': [
        "Headline formula: [Role Title] | [Top Skill] | [Value Prop or Achievement] — NOT just your job title.",
        "Professional headshot (plain background, well-lit) — gets 14x more profile views than no photo.",
        "Open to Work (recruiter-only visibility) — turn it on the moment you start your search.",
        "Summary/About: 3 paragraphs — who you are + top 3 specialties + call to action with email.",
        "Featured section: pin your GitHub, portfolio, or a strong project — 90% of profiles leave this blank.",
        "Skills section: add 15–20 skills, get 5 endorsements on top skills — boosts keyword ranking.",
        "Post once a week: lesson learned, project update, industry insight — 10x recruiter visibility.",
        "Recommendations: give 2 genuine ones, receive 1. Ask past managers for role-specific outcomes.",
        "Personalise every connection request with 1–2 sentences — acceptance rate goes from 20% to 60%.",
        "LinkedIn SEO: use your target job title 3–4 times across headline, summary, and experience sections.",
        "Creator mode: turn it on if you post content — adds Follow button and boosts discoverability.",
        "Engage with target companies' recruiters posts — they track who comments.",
    ],

    'career_gap_tips': [
        "Never apologise for a career gap — frame it as intentional and growth-oriented.",
        "Gap framing formula: [why it happened] + [what you did during it] + [why you're ready now].",
        "If you freelanced or did contract work during the gap — list it as a role on your resume.",
        "Caregiving, health, family leave — 'Personal leave to care for a family member' is a complete explanation.",
        "Gaps under 6 months go unnoticed with year-only formatting: '2023–2024' not 'Mar 2023–Sep 2023'.",
        "Fill the gap on your resume: certifications, volunteer work, open-source contributions.",
        "Interview answer: 'I took time to [reason]. During that period I [activity]. I'm now ready because [reason].'",
        "Career pivot: lead with transferable skills, not your old title. Rewrite your summary immediately.",
        "Layoff/restructuring: 'The role was eliminated in a company-wide restructuring' — factual, complete.",
        "Honesty + brevity = the formula. A calm, concise answer moves you forward every time.",
    ],

    'certification_tips': [
        "Certifications are signal, not substance — always pair them with a project proving the skill.",
        "Free entry-level certs that punch above their weight: AWS Cloud Practitioner, GitHub Foundations.",
        "Cloud certs (AWS SAA, Azure AZ-104, GCP ACE) appear as requirements in most mid-level tech postings.",
        "List on resume: Name | Issuing Body | Year. Under a 'Certifications' section.",
        "Don't certify in skills you won't use — interviewers ask about certs in depth.",
        "Learning platforms: A Cloud Guru, Pluralsight, Coursera, edX, Linux Foundation, Udemy.",
        "Security certs: CompTIA Security+, CEH, CISSP — increasingly required for enterprise roles.",
        "Data certs: Google Data Analytics (Coursera), IBM Data Science, Databricks Associate.",
        "PM certs: CSPO, PMP, PRINCE2 — valued in tech and non-tech PM roles.",
    ],

    'project_tips': [
        "Every project needs: a README, a live demo link or screenshots, and a 1-line problem statement.",
        "Project bullet formula: 'Built [what] using [tech stack], resulting in [quantified outcome].'",
        "GitHub pinned repos: 4–6 polished projects with descriptions, tech badges, and live demo links.",
        "Quality beats quantity — 2 polished, documented projects > 10 half-finished repos.",
        "Choose projects that speak to your target role: DevOps → K8s deployment; Full Stack → SaaS clone.",
        "Contribute to open source — even small PRs (docs, bug fixes) show real-world collaboration.",
        "Write a project case study on LinkedIn: problem → approach → tech choices → outcome.",
        "Add unit tests — most junior developers don't. Tests signal production-ready thinking.",
        "Deploy everything — Vercel, Railway, Render are free. A live URL beats a dead GitHub link.",
        "Frame projects as solving a real problem, not just 'practicing a skill' — recruiters want product thinking.",
    ],

    'networking_tips': [
        "70–80% of roles are filled through referrals before they're posted publicly.",
        "Coffee chat formula: 15-min video call → ask about their role and journey → do NOT ask for a job.",
        "Follow up every coffee chat with a thank-you note + 1 specific takeaway within 24 hours.",
        "Alumni search: your university + target company on LinkedIn → message alumni directly.",
        "LinkedIn outreach: 'Hi [Name], I noticed you work at [Company]. Exploring [goal] — would value 15 minutes of your insight, no pressure if busy.'",
        "In-person conferences beat online networking 10:1 — one real conversation > ten cold messages.",
        "Give before you ask: share articles, make intros, engage with posts before reaching out for help.",
        "Referral ask: 'Would you be comfortable referring me? I'll send you my resume and the JD to make it easy.'",
        "Keep a networking CRM: Name | Company | Last Contact | Notes | Next Step.",
        "Follow and engage with recruiters at target companies — they track who engages with their posts.",
    ],

    'cover_letter_tips': [
        "Structure: Hook → Relevance + Proof → Close. Never exceed 3 paragraphs or 350 words.",
        "Opening hook: reference a specific product, news item, or challenge — not 'I am writing to apply...'",
        "Middle paragraph: connect 2 of your measurable achievements to their key role requirements.",
        "Closing: name a specific next step — 'I'd love to discuss this in a 20-minute call.'",
        "Tailor every letter — mention company name, role title, and one specific thing about them.",
        "Use the same keywords as the JD — cover letters can also go through ATS.",
        "Keep it under 350 words — hiring managers spend 30 seconds on cover letters.",
        "Don't restate your resume — add context, motivation, and personality the resume can't show.",
        "If you have a referral, lead with it: 'Your colleague [Name] recommended I reach out...'",
        "Proofread twice. A typo in a cover letter can eliminate an otherwise strong candidate.",
    ],

    'remote_work_tips': [
        "Remote job boards: Remote.co, We Work Remotely, Remote OK, Remotive, FlexJobs, Working Nomads.",
        "Remote resume signal: add 'Remote (UTC+5, flexible)' to your location field.",
        "Async communication mastery: mention Notion, Loom, Linear, Confluence, Slack in your profile.",
        "Mention your overlap hours with US/EU teams in your application where relevant.",
        "Video interview: camera on, good lighting, wired internet, clean background — always.",
        "Smart question to ask: 'How does the team handle async communication across time zones?'",
        "Salary arbitrage: US/EU companies paying USD/EUR — negotiate for international market rates.",
        "Vetted remote platforms: Arc.dev, Toptal (senior), Andela — pre-vet your skills for global placement.",
        "Build online presence — blog posts, GitHub activity, LinkedIn posts — remote employers hire what they can Google.",
    ],

    'freelancing_tips': [
        "Platform ladder: Fiverr (entry) → Upwork (mid) → Toptal/Arc.dev (senior) → direct clients (expert).",
        "Niche beats generalist — 'Django REST API developer' outbids 'Python Developer' every time.",
        "Your first 5 reviews are hardest — take slightly below market for the first few projects.",
        "Proposal formula: acknowledge problem → prove you understand it → show 1 relevant past work → CTA.",
        "Hourly for unclear scope. Fixed price for well-defined deliverables.",
        "Client red flags: vague scope, 'just a simple project', no budget listed, bad reviews.",
        "Portfolio site: 3–4 case studies with testimonials — signals professionalism over competitors.",
        "Convert project clients into monthly retainers (20 hrs/mo) — stabilises income.",
        "Milestone invoicing: 30% upfront, 40% mid-project, 30% on delivery — protects against ghosting.",
    ],

    'negotiation_tips': [
        "Never give your number first — 'I'd like to understand the full role and comp structure before settling on a number.'",
        "Anchor 10–15% above your real target — you can always negotiate down, never up.",
        "Negotiate the full package: base + bonus + equity + PTO + remote days + learning budget.",
        "Research before every negotiation: Glassdoor, LinkedIn Salary, Levels.fyi, Payscale.",
        "Competing offer? Use it ethically: 'I have another offer at X — I'd prefer your team, can you match it?'",
        "Silence is a negotiation tool — state your number, then stop talking. Whoever speaks next concedes.",
        "RSUs/Stock options: check vesting schedule, cliff, strike price, and last 409A valuation.",
        "Get everything in writing before you resign. Verbal offers collapse.",
        "If base is capped: negotiate signing bonus, extra PTO, remote days, or 6-month salary review.",
        "The cost of not negotiating: accepting initial offers vs. negotiating = $500K+ difference over a career.",
    ],

    'trending_tech': [
        "**AI/ML Engineering** — RAG architectures, LangChain, LlamaIndex, vector databases (Pinecone, Weaviate, pgvector) — highest growth area 2025.",
        "**Platform Engineering / IDP** — Internal Developer Platforms, Backstage — DevOps evolving into Platform Engineering.",
        "**Rust** — systems programming, WebAssembly, backend web (Axum). 9th consecutive year as most loved language.",
        "**TypeScript** — effectively mandatory for any modern JavaScript role. Plain JS is a yellow flag.",
        "**dbt + Snowflake / BigQuery** — analytics engineering is now a dedicated, high-paying discipline.",
        "**Kubernetes Operators + Service Mesh** — cloud-native maturity beyond basic K8s deployments.",
        "**OpenTelemetry** — becoming the standard for distributed tracing across all vendors.",
        "**Edge Computing** — Cloudflare Workers, AWS Lambda@Edge — compute closer to users, lower latency.",
        "**DevSecOps / Supply Chain Security** — SBOM, SAST/DAST in CI/CD — security is now every engineer's job.",
        "**Agentic AI** — autonomous agents, tool use, multi-step reasoning — frontier of applied AI engineering.",
        "**WebAssembly (WASM)** — near-native code in browser and server environments (Fastly, Cloudflare).",
        "**Full Stack + AI integration** — traditional engineers who can integrate LLM APIs are in very high demand.",
    ],

    'salary': {
        'software engineer':         {'pk': '80K–180K PKR/mo',  'uae': '$3,000–$7,000/mo',  'us': '$100K–$160K/yr',  'remote': '$60K–$120K/yr'},
        'senior software engineer':  {'pk': '150K–300K PKR/mo', 'uae': '$5,000–$10,000/mo', 'us': '$140K–$220K/yr',  'remote': '$90K–$150K/yr'},
        'frontend developer':        {'pk': '60K–140K PKR/mo',  'uae': '$2,000–$5,000/mo',  'us': '$85K–$130K/yr',   'remote': '$50K–$100K/yr'},
        'backend developer':         {'pk': '70K–160K PKR/mo',  'uae': '$2,500–$6,000/mo',  'us': '$95K–$145K/yr',   'remote': '$60K–$110K/yr'},
        'full stack developer':      {'pk': '80K–180K PKR/mo',  'uae': '$3,000–$7,000/mo',  'us': '$100K–$150K/yr',  'remote': '$65K–$120K/yr'},
        'devops engineer':           {'pk': '90K–200K PKR/mo',  'uae': '$3,500–$8,000/mo',  'us': '$110K–$170K/yr',  'remote': '$70K–$130K/yr'},
        'data engineer':             {'pk': '90K–210K PKR/mo',  'uae': '$3,500–$8,000/mo',  'us': '$115K–$165K/yr',  'remote': '$70K–$130K/yr'},
        'data scientist':            {'pk': '90K–200K PKR/mo',  'uae': '$4,000–$9,000/mo',  'us': '$115K–$170K/yr',  'remote': '$75K–$140K/yr'},
        'ml engineer':               {'pk': '100K–250K PKR/mo', 'uae': '$4,500–$10,000/mo', 'us': '$130K–$200K/yr',  'remote': '$85K–$160K/yr'},
        'machine learning engineer': {'pk': '100K–250K PKR/mo', 'uae': '$4,500–$10,000/mo', 'us': '$130K–$200K/yr',  'remote': '$85K–$160K/yr'},
        'cloud engineer':            {'pk': '90K–200K PKR/mo',  'uae': '$3,500–$8,000/mo',  'us': '$115K–$165K/yr',  'remote': '$70K–$130K/yr'},
        'sre':                       {'pk': '100K–230K PKR/mo', 'uae': '$4,000–$9,000/mo',  'us': '$130K–$190K/yr',  'remote': '$80K–$150K/yr'},
        'site reliability engineer': {'pk': '100K–230K PKR/mo', 'uae': '$4,000–$9,000/mo',  'us': '$130K–$190K/yr',  'remote': '$80K–$150K/yr'},
        'qa engineer':               {'pk': '50K–130K PKR/mo',  'uae': '$2,000–$5,000/mo',  'us': '$75K–$120K/yr',   'remote': '$45K–$95K/yr'},
        'product manager':           {'pk': '100K–250K PKR/mo', 'uae': '$4,000–$10,000/mo', 'us': '$120K–$200K/yr',  'remote': '$80K–$150K/yr'},
        'cybersecurity engineer':    {'pk': '80K–200K PKR/mo',  'uae': '$3,500–$8,000/mo',  'us': '$110K–$170K/yr',  'remote': '$70K–$140K/yr'},
        'mobile developer':          {'pk': '70K–160K PKR/mo',  'uae': '$2,500–$6,000/mo',  'us': '$95K–$150K/yr',   'remote': '$60K–$120K/yr'},
        'ui/ux designer':            {'pk': '50K–130K PKR/mo',  'uae': '$2,000–$5,500/mo',  'us': '$80K–$130K/yr',   'remote': '$50K–$100K/yr'},
        'blockchain developer':      {'pk': '100K–300K PKR/mo', 'uae': '$4,000–$12,000/mo', 'us': '$120K–$200K/yr',  'remote': '$80K–$160K/yr'},
        'data analyst':              {'pk': '60K–140K PKR/mo',  'uae': '$2,500–$6,000/mo',  'us': '$75K–$120K/yr',   'remote': '$50K–$100K/yr'},
        'default':                   {'pk': '60K–150K PKR/mo',  'uae': '$2,500–$6,000/mo',  'us': '$90K–$140K/yr',   'remote': '$55K–$100K/yr'},
    },

    'skills_by_role': {
        'devops': [
            "**Docker & Kubernetes** — containerisation is the entry ticket to any DevOps role",
            "**Terraform / Pulumi** — Infrastructure as Code; expected at every mid+ level position",
            "**CI/CD pipelines** — GitHub Actions, Jenkins, or GitLab CI; hands-on pipeline experience",
            "**Linux & Bash scripting** — the #1 screened DevOps skill; know sysadmin tasks cold",
            "**Cloud platform (AWS/Azure/GCP)** — go deep in one, pair with at least 1 associate cert",
            "**Monitoring & observability** — Prometheus + Grafana (metrics), ELK/Loki (logs)",
            "**Helm & ArgoCD** — Kubernetes package management and GitOps deployment model",
            "**Networking fundamentals** — VPC, subnets, load balancers, DNS, TLS — infrastructure design",
            "**Ansible** — configuration management; most in-demand in enterprise environments",
        ],
        'full stack developer': [
            "**React or Vue + TypeScript** — React has 4x more job posts; TypeScript is mandatory at mid+ level",
            "**Node.js + Express or Python (Django/FastAPI)** — pick a backend stack and own it end-to-end",
            "**SQL + PostgreSQL** — every full-stack role requires solid SQL; JOINs, indexing, transactions",
            "**Redis** — caching layer, pub/sub; in almost every production full-stack system",
            "**REST API design** — JWT/OAuth2 auth, versioning, error handling, pagination",
            "**Docker** — containerise development + CI environments; expected at mid-level",
            "**Testing** — Jest (frontend) + pytest (backend); shows production-readiness mindset",
        ],
        'backend developer': [
            "**Python (Django/FastAPI) or Java (Spring Boot) or Go** — pick one and achieve depth",
            "**SQL mastery** — complex JOINs, indexes, query plans, transactions, N+1 detection",
            "**REST + GraphQL API design** — auth, rate limiting, pagination, versioning, error standards",
            "**Redis** — caching, session management, distributed locking, Pub/Sub",
            "**Message queues (RabbitMQ or Kafka)** — async processing and event-driven architecture",
            "**Docker** — containerised services; understand multi-stage builds",
            "**System design fundamentals** — load balancers, CDN, database sharding, circuit breakers",
        ],
        'frontend developer': [
            "**React + TypeScript** — dominant frontend stack globally; TypeScript is mandatory at mid-level",
            "**CSS mastery** — Flexbox, Grid, responsive design, CSS variables, animations",
            "**State management** — Redux Toolkit, Zustand, or React Query / TanStack Query",
            "**Testing** — Jest + React Testing Library; Cypress or Playwright for E2E",
            "**Performance optimisation** — lazy loading, code splitting, Core Web Vitals",
            "**Accessibility (a11y)** — WCAG 2.1 standards, semantic HTML, keyboard navigation",
            "**Build tools** — Vite (modern) or Webpack + module bundling concepts",
        ],
        'data scientist': [
            "**Python (Pandas, NumPy, Matplotlib, Seaborn)** — fluency is a baseline requirement",
            "**Machine learning** — Scikit-learn for classical ML; XGBoost/LightGBM for structured data",
            "**Deep learning** — PyTorch (research-preferred) or TensorFlow/Keras for production",
            "**SQL** — every DS must query databases independently without assistance",
            "**Statistics & probability** — hypothesis testing, A/B test design, p-values, distributions",
            "**Data storytelling** — Tableau, Power BI, or Plotly for communicating to non-technical stakeholders",
            "**Feature engineering** — the most impactful practical ML skill",
            "**MLflow or DVC** — experiment tracking, model versioning; increasingly expected",
        ],
        'data engineer': [
            "**Apache Spark** — distributed large-scale data processing; PySpark is the standard",
            "**SQL + data modelling** — star schema, slowly changing dimensions, normalisation",
            "**Apache Airflow** — DAG-based workflow orchestration, scheduling, retry logic",
            "**dbt** — transforming data in the warehouse; standard at modern data teams",
            "**Cloud data warehouses** — Snowflake, BigQuery, or Redshift; compute/storage separation",
            "**Apache Kafka** — real-time streaming pipelines, producer/consumer patterns",
            "**Python** — scripting, ETL logic, API integrations; Pandas for medium-scale transforms",
        ],
        'ml engineer': [
            "**PyTorch** — the standard framework in applied ML and research roles",
            "**MLflow + DVC** — experiment tracking, model versioning, data versioning",
            "**FastAPI** — serving ML models as REST APIs in production",
            "**Docker + Kubernetes** — containerised model serving at production traffic scale",
            "**Feature stores** — Feast, Tecton — training/serving feature consistency",
            "**Kubeflow or SageMaker Pipelines** — end-to-end ML pipeline orchestration",
            "**Model monitoring** — detecting data drift and model performance degradation",
            "**LLM tooling** — LangChain, LlamaIndex, vector DBs (Pinecone, Weaviate) for applied AI",
        ],
        'cloud engineer': [
            "**AWS (most in-demand), Azure, or GCP** — go deep in one, know the second conceptually",
            "**Terraform** — IaC for any cloud; remote state, modules, workspaces",
            "**IAM** — identity and access management; least privilege principle; service accounts",
            "**VPC, subnetting, peering, NAT gateways** — network architecture fundamentals",
            "**Kubernetes (EKS/AKS/GKE)** — managed container orchestration on cloud platforms",
            "**Cost optimisation** — Reserved Instances, Spot, right-sizing, cost anomaly detection",
            "**Monitoring** — CloudWatch / Azure Monitor; alerting, dashboards, log insights",
        ],
        'software engineer': [
            "**Data Structures & Algorithms** — the foundation of every technical interview",
            "**System Design** — load balancers, caching (Redis), queues (Kafka), databases at scale",
            "**Primary language depth** — Python, Java, C++, or Go; know the stdlib and memory model",
            "**OOP and design patterns** — SOLID principles, Factory, Observer, Strategy, Decorator",
            "**Testing practices** — unit, integration, TDD basics; writing testable code is a seniority signal",
            "**Databases** — SQL proficiency required; basic NoSQL knowledge is a plus",
            "**Git mastery** — branching strategies, rebasing, cherry-pick, merge conflicts",
        ],
        'qa engineer': [
            "**Test automation** — Selenium, Playwright, or Cypress; pick one and go expert-level",
            "**API testing** — Postman for manual; pytest + requests or RestAssured for automation",
            "**CI/CD integration** — running test suites in GitHub Actions or Jenkins; fail-fast pipelines",
            "**Performance testing** — JMeter or Locust; load testing, stress testing, bottleneck identification",
            "**Bug tracking** — JIRA or Linear; clear, reproducible bug reports with steps and environment",
            "**Agile/Scrum** — sprint testing, test cases from user stories, regression planning",
            "**SQL basics** — validating the data layer in API and backend testing",
        ],
        'product manager': [
            "**SQL basics** — data-driven PMs who query their own metrics are rare and highly valued",
            "**Product roadmap tools** — Jira, ProductBoard, Linear, Notion",
            "**A/B testing** — hypothesis design, statistical significance, Optimizely/LaunchDarkly",
            "**User research** — interviews, surveys, UserTesting.com, card sorting",
            "**Figma** — wireframing and collaborating with design teams",
            "**OKRs and product metrics** — DAU, retention D7/D30, NPS, conversion rate, LTV",
            "**Stakeholder communication** — clear, concise upward reporting; writing PRDs",
        ],
        'sre': [
            "**SLOs / SLIs / Error Budgets** — defining and measuring reliability commitments",
            "**Incident management** — runbooks, on-call rotations, blameless post-mortems",
            "**Observability stack** — Prometheus + Grafana, ELK/Loki, Jaeger/Datadog APM",
            "**Chaos engineering** — Chaos Monkey, Gremlin; proactive reliability testing",
            "**Python or Go scripting** — automating operational tasks, internal tooling",
            "**Kubernetes + Helm** — production-grade container management and upgrades",
            "**Capacity planning** — predicting load growth, auto-scaling policies",
        ],
        'cybersecurity': [
            "**Network security fundamentals** — TCP/IP, firewalls, VPNs, TLS/SSL, Wireshark",
            "**OWASP Top 10** — standard web application security vulnerabilities; know all 10",
            "**Penetration testing** — Kali Linux, Metasploit, Burp Suite, Nmap, OWASP ZAP",
            "**SIEM tools** — Splunk, IBM QRadar, or Microsoft Sentinel for log analysis",
            "**IAM & Zero Trust model** — identity-centric security; least privilege; micro-segmentation",
            "**Python or Bash scripting** — automating security tasks, log parsing, custom tooling",
            "**Incident response lifecycle** — containment, eradication, recovery, lessons-learned",
        ],
        'mobile developer': [
            "**React Native or Flutter** — cross-platform; covers the bulk of mobile job postings",
            "**Swift (iOS) or Kotlin (Android)** — native for performance-critical applications",
            "**State management** — Redux/Context (React Native); BLoC or Provider (Flutter)",
            "**REST API integration** — Axios (RN), dio (Flutter); auth, error boundaries",
            "**Push notifications** — Firebase Cloud Messaging (FCM) on both platforms",
            "**App Store + Play Store deployment** — code signing, TestFlight, beta tracks",
            "**UI/UX principles** — Human Interface Guidelines (iOS) and Material Design 3 (Android)",
        ],
    },

    'interview_questions': {
        'devops': [
            {'q': 'Walk me through designing a CI/CD pipeline from scratch.',
             'tip': 'Cover: Git → build (GitHub Actions/Jenkins) → test (unit + integration) → artifact registry → deploy (K8s/ECS). Mention environment promotion (dev→staging→prod), rollback strategy, and failure notifications.'},
            {'q': 'A production deployment failed at 2 AM. Walk me through your incident response.',
             'tip': 'STAR: detect via alert → immediate rollback → stabilise → root-cause analysis → post-mortem with preventive actions. Emphasise: no blame, data-driven RCA, stakeholder communication.'},
            {'q': 'How do you manage secrets in a containerised environment?',
             'tip': 'K8s Secrets + encryption at rest (KMS), HashiCorp Vault, or AWS Secrets Manager. Golden rule: never hardcode in Dockerfiles or commit to Git. Mention secret rotation policy.'},
            {'q': 'Blue-green vs. canary deployments — when do you use each?',
             'tip': 'Blue-green: two identical envs, instant traffic switch, easy rollback — higher infra cost. Canary: gradual traffic shift (5%→25%→100%), validates with real traffic, reduces blast radius. Know when each is appropriate.'},
            {'q': 'How would you reduce a Docker image size by 60%?',
             'tip': 'Multi-stage builds, Alpine base images, .dockerignore, remove dev dependencies, layer caching optimisation, distroless images for runtime.'},
            {'q': 'How do you monitor a distributed microservices system?',
             'tip': 'Three pillars of observability: Metrics (Prometheus + Grafana), Logs (ELK or Loki), Traces (Jaeger or Datadog APM, OpenTelemetry). Define SLIs, set SLOs, alert on error budget burn rate.'},
        ],
        'full stack': [
            {'q': 'Explain the full lifecycle of a web request — browser to database and back.',
             'tip': 'DNS → TCP handshake → HTTPS/TLS → load balancer → web server → app server → ORM → DB query → JSON response. Know every layer and common failure points at each.'},
            {'q': 'How do you handle auth in a full-stack app?',
             'tip': 'JWT (stateless, scales easily) vs. session cookies (server-side, revocable). RBAC via middleware guards. Mention: token refresh flows, httpOnly cookies vs. localStorage tradeoffs, OAuth2 social login.'},
            {'q': 'How do you optimise a slow React app?',
             'tip': 'Profile first with React DevTools. Fix: React.memo + useMemo + useCallback (prevent re-renders), code splitting (React.lazy), list virtualisation (react-window), bundle analysis, image optimisation.'},
            {'q': 'Explain SSR, CSR, and SSG.',
             'tip': 'CSR (React SPA): fast after load, poor initial SEO. SSR (Next.js): rendered per request — great for SEO + dynamic data. SSG: pre-rendered at build time — fastest, ideal for blogs/docs. ISR = hybrid.'},
            {'q': 'How do you prevent SQL injection and XSS?',
             'tip': 'SQL injection: ORM parameterized queries by default — never raw string concatenation. XSS: Django templates auto-escape HTML. Use |safe only when you trust the source. Add CSP headers for defense-in-depth.'},
        ],
        'backend': [
            {'q': 'Design a URL shortener service (like bit.ly).',
             'tip': 'Core: Base62 hash → store {short: long} in DB → redirect service. Scale: Redis cache for hot URLs, read replicas, horizontal scaling. Think: CAP theorem, collision handling, analytics tracking.'},
            {'q': 'How do you handle race conditions in a high-concurrency API?',
             'tip': 'Optimistic locking (version field + CAS), pessimistic locking (SELECT FOR UPDATE), Redis distributed locks (Redlock), or atomic DB operations. Choose based on conflict frequency and latency tolerance.'},
            {'q': 'REST vs. GraphQL — when would you choose each?',
             'tip': 'REST: simple, cacheable, proven — best for public APIs and simple CRUD. GraphQL: flexible querying, no over/under-fetching — best for complex frontends with varying data needs.'},
            {'q': 'How do you structure error handling in a production API?',
             'tip': 'Consistent error schema (code, message, details, request_id), correct HTTP status codes (400, 401, 403, 404, 422, 429, 500), centralised middleware, structured JSON logging, alerting on 5xx spike.'},
        ],
        'frontend': [
            {'q': 'Explain the React reconciliation algorithm.',
             'tip': 'React diffs new vs. old virtual DOM using keys for list reconciliation, then batches minimal real DOM updates. Keys must be stable and unique — index keys cause bugs when list order changes.'},
            {'q': 'What are Core Web Vitals and how do you optimise for them?',
             'tip': 'LCP: optimise images, critical CSS, server response. INP: reduce JS execution, code splitting. CLS: explicit dimensions on images/ads, avoid late-injected content.'},
            {'q': 'Explain the JavaScript event loop.',
             'tip': 'Single-threaded: call stack runs synchronously. Async ops go to Web APIs. Callbacks enter macrotask queue (setTimeout) or microtask queue (Promises). Event loop: drain microtasks → process one macrotask → repeat.'},
            {'q': 'How do you make a web app accessible?',
             'tip': 'Semantic HTML first, ARIA roles where semantic HTML falls short, keyboard navigation, colour contrast ≥4.5:1, test with NVDA + Firefox or VoiceOver + Safari.'},
        ],
        'data scientist': [
            {'q': 'Walk me through your ML model building process end-to-end.',
             'tip': 'Problem framing → data collection + EDA → feature engineering → model selection → training + cross-validation → hyperparameter tuning → business-aligned evaluation → deployment considerations.'},
            {'q': 'How do you handle class imbalance?',
             'tip': 'SMOTE (oversample minority), random undersampling. Algorithm-level: class_weight in sklearn. Metrics: F1, precision-recall AUC — never accuracy for imbalanced data. Threshold tuning: move decision boundary based on FP/FN cost.'},
            {'q': 'Explain the bias-variance tradeoff.',
             'tip': 'High bias (underfitting): too simple, high error on train + test. High variance (overfitting): memorises train data, poor on test. Regularisation, more data, or simpler models reduce variance. Diagnose with learning curves.'},
            {'q': 'A feature has 30% missing values — how do you handle it?',
             'tip': 'Analyse missingness: MCAR, MAR, MNAR. Options: drop (MCAR + low predictive value); mean/median impute (simple); IterativeImputer (advanced); binary "is_missing" indicator; or XGBoost (handles NaN natively).'},
        ],
        'data engineer': [
            {'q': 'Design a pipeline for ingesting 10TB of daily clickstream data.',
             'tip': 'Ingest: Kafka. Store: S3/GCS partitioned by date. Process: Spark (batch), Flink (streaming). Transform: dbt in warehouse. Orchestrate: Airflow. Monitor: data quality checks, SLA alerts on missing data.'},
            {'q': 'ETL vs. ELT — what changed and why?',
             'tip': 'ETL: transform before loading — for legacy DBs. ELT: load raw first, transform in warehouse — modern approach since cloud warehouses (Snowflake, BigQuery) have elastic, cheap compute. dbt operationalises ELT.'},
            {'q': 'How do you handle schema evolution in a pipeline?',
             'tip': 'Confluent Schema Registry for Kafka (Avro/Protobuf). Backward-compatible changes: add nullable columns only. Breaking changes: version the topic. In dbt: schema tests catch regressions on every deploy.'},
        ],
        'software engineer': [
            {'q': 'Design a rate limiter.',
             'tip': 'Token bucket or sliding window counter. Redis INCR + EXPIRE for atomic operations. Return 429 with Retry-After header. Consider: user-level vs. IP-level vs. per-endpoint limits and burst allowance.'},
            {'q': 'Explain the CAP theorem.',
             'tip': 'Choose 2 of: Consistency, Availability, Partition tolerance. Partition tolerance is non-negotiable → choose CP (PostgreSQL, Zookeeper) or AP (DynamoDB, Cassandra) based on business requirements.'},
            {'q': 'Concurrency vs. parallelism.',
             'tip': 'Concurrency: multiple tasks interleaving on 1 core. Parallelism: multiple tasks simultaneously on multiple cores. Python: threading (I/O-bound), multiprocessing (CPU-bound, GIL limitation). async/await = concurrency.'},
            {'q': 'How would you refactor a legacy codebase safely?',
             'tip': 'Never rewrite — refactor incrementally. Add characterisation tests (lock current behaviour), identify hotspots, apply Strangler Fig pattern (new code replaces old piece by piece), measure with tests before merging.'},
        ],
        'product manager': [
            {'q': 'How do you prioritise your product backlog?',
             'tip': 'Frameworks: RICE (Reach×Impact×Confidence÷Effort), MoSCoW, Impact vs. Effort matrix. Always tie priorities to OKRs and customer evidence — not HiPPO (Highest Paid Person\'s Opinion).'},
            {'q': 'How would you increase DAU for a feature 80% of users ignore?',
             'tip': 'Diagnose first: discoverability? Onboarding failure? Value delivery gap? Habit formation? Solutions: empty-state improvements, onboarding tooltips, surfacing in high-traffic flows. Validate with A/B test.'},
            {'q': 'Engineering says 6 months. Stakeholders want it in 6 weeks. How do you handle this?',
             'tip': 'Scope negotiation: MVP delivering 80% value in 20% time. Present option set with tradeoffs — not just one answer. Never commit for engineering. Quantify cost of delay for stakeholders.'},
        ],
        'qa engineer': [
            {'q': 'How do you decide what to automate vs. test manually?',
             'tip': 'Automate: regression suites, smoke tests, happy paths run >5 times, data validation. Manual: exploratory testing, UX judgment, edge cases that run once. ROI rule: if you\'ll run it >5 times, automate it.'},
            {'q': 'A test suite is becoming flaky. How do you handle it?',
             'tip': 'Track flakiness rate per test. Root causes: async timing (explicit waits, not sleep), test data pollution (isolate data per run), environment inconsistency (containerise). Quarantine flaky tests immediately — they erode team trust.'},
        ],
    },

    'certifications_by_role': {
        'devops': [
            'AWS Certified DevOps Engineer – Professional',
            'CKA – Certified Kubernetes Administrator',
            'HashiCorp Terraform Associate',
            'Docker Certified Associate',
            'Google Cloud Professional DevOps Engineer',
        ],
        'cloud engineer': [
            'AWS Solutions Architect – Associate (SAA-C03)',
            'AWS Solutions Architect – Professional',
            'Google Cloud Professional Cloud Architect',
            'Azure AZ-104 Administrator Associate',
            'Azure AZ-305 Solutions Architect Expert',
        ],
        'data scientist': [
            'IBM Data Science Professional Certificate (Coursera)',
            'Google Professional Data Engineer',
            'Databricks ML Professional',
            'AWS ML – Specialty',
            'Deep Learning Specialization (deeplearning.ai)',
        ],
        'data engineer': [
            'Databricks Data Engineer Associate',
            'Google Professional Data Engineer',
            'AWS Data Analytics – Specialty',
            'dbt Analytics Engineering Certification',
            'Apache Kafka Developer Certificate (Confluent)',
        ],
        'sre': [
            'CKA – Certified Kubernetes Administrator',
            'Prometheus Certified Associate (PCA)',
            'AWS SysOps Administrator',
            'Google Cloud Professional SRE',
            'ITIL Foundation',
        ],
        'cybersecurity': [
            'CompTIA Security+',
            'CEH – Certified Ethical Hacker',
            'OSCP – Offensive Security',
            'CISSP (senior level)',
            'AWS Security Specialty',
        ],
        'product manager': [
            'CSPO – Certified Scrum Product Owner',
            'PMI-ACP – Agile Certified Practitioner',
            'Product School CPM Certificate',
            'Google Project Management Certificate',
            'PRINCE2 Foundation',
        ],
        'qa engineer': [
            'ISTQB Foundation Level (CTFL)',
            'LambdaTest Selenium Certification',
            'Postman API Fundamentals Expert',
            'AWS Developer Associate',
            'CSTE – Certified Software Test Engineer',
        ],
        'full stack developer': [
            'AWS Developer Associate',
            'MongoDB Associate Developer',
            'Meta Front-End Developer (Coursera)',
            'freeCodeCamp Full Stack Certification',
            'Google UX Design Certificate',
        ],
        'software engineer': [
            'AWS Developer Associate',
            'Google Associate Cloud Engineer',
            'Oracle Java SE 11 Developer',
            'Microsoft Azure Developer Associate (AZ-204)',
            'LeetCode — practice Blind 75 (not a cert but essential)',
        ],
        'default': [
            'AWS Cloud Practitioner (entry, free study materials)',
            'Google Associate Cloud Engineer',
            'Microsoft AZ-900 Azure Fundamentals',
            'CompTIA IT Fundamentals',
            'Scrum Master Certification (CSM)',
        ],
    },

    'companies': {
        'faang_info': (
            "**FAANG / Top Tech Interview Structure:**\n\n"
            "🔵 **Meta** — 2 coding rounds (LeetCode medium/hard) + 1 system design + 1 behavioural (product sense)\n"
            "🟠 **Amazon** — 2–3 coding + 1 system design + 2–3 Leadership Principles rounds (prepare all 14 LPs with STAR stories)\n"
            "🍎 **Apple** — 2–4 technical rounds + pair programming + 1 behavioural — deep domain expertise valued above all\n"
            "🎬 **Netflix** — culture fit (Netflix Culture Memo is essential reading) + system design + coding rounds\n"
            "🔵 **Google** — 4–6 rounds: 2 coding (LC hard), 1–2 system design, 1 Googleyness (behavioural) + role-specific\n"
            "🪟 **Microsoft** — 3–5 rounds: coding + system design + behavioural (growth mindset culture)\n\n"
            "**Prep essentials:**\n"
            "- LeetCode — Blind 75 list (free, curated)\n"
            "- Grokking the System Design Interview (educative.io)\n"
            "- 14 STAR stories for Amazon Leadership Principles\n"
            "- Company-specific engineering blogs and recent product launches"
        ),
        'top_companies_pk': [
            "**Systems Limited** — Pakistan's largest IT company, Fortune 500 clients, 6,000+ employees",
            "**Netsol Technologies** — Global fintech, NYSE-listed, strong DevOps and Java openings",
            "**10Pearls** — Top US-facing digital product studio, excellent remote culture",
            "**Arbisoft** — Fast-growing product + services company, Django/React heavy stack",
            "**Contour Software** — US-facing product company, known for excellent compensation",
            "**Genetech Solutions** — Cloud and DevOps heavy, growing US client base",
            "**Folio3** — SAP, AI, and mobile development",
            "**Afiniti** — AI-driven enterprise software, senior-level roles",
            "**Careem / Orascom** — Local tech giants, high compensation for senior engineers",
        ],
        'research_tips': [
            "Glassdoor: salary ranges, interview process reviews, culture insights — filter to last 12 months only.",
            "LinkedIn Company → People tab: see team composition, backgrounds, and identify potential interviewers.",
            "Read the last 3 posts from their Engineering or Product blog — reveals real tech stack and priorities.",
            "Check their GitHub org (if public) — languages, frameworks, and code quality tell the true tech story.",
            "Crunchbase: funding stage, investors, growth trajectory — essential for startup evaluation.",
            "CEO/CTO Twitter or LinkedIn posts — understand company vision and recent strategic bets.",
            "Glassdoor red flags to watch: 'high turnover', 'unpaid overtime', 'fake promises' — patterns matter.",
        ],
    },

    'action_verbs': {
        'engineering': ['Engineered', 'Architected', 'Developed', 'Deployed', 'Automated', 'Integrated',
                        'Optimised', 'Refactored', 'Migrated', 'Scaled', 'Shipped', 'Built', 'Designed', 'Implemented'],
        'leadership': ['Led', 'Managed', 'Mentored', 'Coordinated', 'Spearheaded', 'Directed',
                       'Oversaw', 'Established', 'Championed', 'Drove', 'Grew', 'Founded'],
        'analysis': ['Analysed', 'Evaluated', 'Assessed', 'Identified', 'Diagnosed', 'Investigated',
                     'Researched', 'Modelled', 'Measured', 'Benchmarked', 'Audited'],
        'improvement': ['Reduced', 'Increased', 'Improved', 'Streamlined', 'Enhanced', 'Accelerated',
                        'Eliminated', 'Saved', 'Boosted', 'Doubled', 'Cut'],
        'collaboration': ['Collaborated', 'Partnered', 'Liaised', 'Facilitated', 'Presented',
                          'Communicated', 'Negotiated', 'Aligned'],
    },
}

# ============================================================
# ROLE KEYWORD → KNOWLEDGE BASE KEY MAPPING
# ============================================================
ROLE_KEYWORDS = [
    'devops', 'developer', 'engineer', 'data scientist', 'ml engineer', 'machine learning',
    'cloud engineer', 'backend', 'frontend', 'full stack', 'fullstack', 'software engineer',
    'qa', 'tester', 'product manager', 'pm', 'analyst', 'architect', 'sre',
    'site reliability', 'cybersecurity', 'security', 'mobile', 'blockchain', 'data analyst',
    'data engineer', 'ui/ux', 'ux designer', 'ui designer',
]

ROLE_ALIAS_MAP = {
    'devops': 'devops engineer',
    'devops engineer': 'devops engineer',
    'full stack': 'full stack developer',
    'fullstack': 'full stack developer',
    'full stack developer': 'full stack developer',
    'backend': 'backend developer',
    'backend developer': 'backend developer',
    'frontend': 'frontend developer',
    'frontend developer': 'frontend developer',
    'data scientist': 'data scientist',
    'data science': 'data scientist',
    'data engineer': 'data engineer',
    'ml engineer': 'ml engineer',
    'machine learning': 'ml engineer',
    'machine learning engineer': 'ml engineer',
    'cloud engineer': 'cloud engineer',
    'cloud': 'cloud engineer',
    'software engineer': 'software engineer',
    'software developer': 'software engineer',
    'qa engineer': 'qa engineer',
    'qa': 'qa engineer',
    'tester': 'qa engineer',
    'product manager': 'product manager',
    'pm': 'product manager',
    'sre': 'sre',
    'site reliability': 'sre',
    'site reliability engineer': 'sre',
    'cybersecurity': 'cybersecurity engineer',
    'security engineer': 'cybersecurity engineer',
    'mobile developer': 'mobile developer',
    'mobile': 'mobile developer',
    'blockchain developer': 'blockchain developer',
    'data analyst': 'data analyst',
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================
def _trim_response(text, max_chars=2200):
    if not text:
        return text
    text = text.strip()
    if len(text) <= max_chars:
        return text
    chunk = text[:max_chars]
    for sep in ['\n', '. ', '! ', '? ']:
        idx = chunk.rfind(sep)
        if idx > max_chars * 0.6:
            return chunk[:idx + len(sep)].strip()
    return chunk.strip()


def _is_rewrite_request(user_input):
    triggers = ['rewrite', 'improve this', 'fix this', 'reword', 'rephrase',
                'make this better', 'polish this', 'optimise this bullet']
    return any(t in user_input.lower() for t in triggers)


def _analyze_resume_text(resume_text):
    """Deep resume analysis returning structured insights dict."""
    if not resume_text or len(resume_text.strip()) < 50:
        return None

    text_lower = resume_text.lower()

    skill_keywords = [
        'python', 'java', 'javascript', 'typescript', 'react', 'vue', 'angular',
        'node.js', 'nodejs', 'django', 'fastapi', 'flask', 'spring',
        'docker', 'kubernetes', 'terraform', 'ansible',
        'aws', 'azure', 'gcp', 'google cloud',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'kafka',
        'spark', 'airflow', 'dbt', 'snowflake', 'bigquery',
        'git', 'linux', 'bash',
        'html', 'css', 'rest api', 'graphql',
        'flutter', 'react native', 'swift', 'kotlin',
        'pytorch', 'tensorflow', 'scikit-learn', 'pandas', 'numpy',
        'ci/cd', 'jenkins', 'github actions', 'gitlab',
        'microservices', 'agile', 'scrum',
    ]
    detected_skills = [s for s in skill_keywords if s in text_lower]

    missing_sections = []
    has_experience = any(w in text_lower for w in ['experience', 'employment', 'worked at', 'position', 'role at'])
    has_education = any(w in text_lower for w in ['education', 'university', 'degree', 'bachelor', 'master', 'college', 'bsc', 'msc'])
    has_skills = any(w in text_lower for w in ['skills', 'technologies', 'tools', 'proficient', 'expertise'])
    has_projects = any(w in text_lower for w in ['project', 'portfolio', 'built', 'developed', 'created'])
    has_summary = any(w in text_lower for w in ['summary', 'profile', 'objective', 'overview', 'professional'])

    if not has_experience:
        missing_sections.append('Work Experience')
    if not has_education:
        missing_sections.append('Education')
    if not has_skills:
        missing_sections.append('Skills')
    if not has_projects:
        missing_sections.append('Projects')
    if not has_summary:
        missing_sections.append('Professional Summary')

    return {
        'word_count': len(resume_text.split()),
        'has_metrics': bool(re.search(
            r'\d+\s*[%$kmb]|\d+\s*(?:users|clients|team|projects|employees|requests|features|deployments)',
            text_lower
        )),
        'has_github': 'github' in text_lower,
        'has_linkedin': 'linkedin' in text_lower,
        'has_email': bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text)),
        'has_experience': has_experience,
        'has_education': has_education,
        'has_skills': has_skills,
        'has_projects': has_projects,
        'has_summary': has_summary,
        'has_action_verbs': bool(re.search(
            r'\b(engineered|architected|developed|deployed|automated|designed|built|led|managed|'
            r'optimised|optimized|reduced|increased|improved|scaled|shipped|delivered|streamlined)\b',
            text_lower
        )),
        'detected_skills': detected_skills,
        'missing_sections': missing_sections,
    }


def _extract_role_from_context(message, chat_history=None):
    """Extract the most specific job role from message + recent chat history."""
    combined = message.lower()
    if chat_history:
        for m in reversed(chat_history[-8:]):
            combined += ' ' + m['content'].lower()

    # Try salary KB keys first (most specific)
    for role in KNOWLEDGE_BASE['salary']:
        if role != 'default' and role in combined:
            return role

    # Try alias map
    for kw, alias in ROLE_ALIAS_MAP.items():
        if kw in combined:
            return alias

    # Generic role keywords
    for kw in ROLE_KEYWORDS:
        if kw in combined:
            return kw

    return 'default'


# ============================================================
# INTENT DETECTION
# ============================================================
def analyze_intent(message, chat_history=None):
    """Multi-signal intent classification using keyword matching + history context."""
    msg = message.lower().strip()

    intent_patterns = {
        'greeting':             ['hi', 'hello', 'hey', 'good morning', 'good evening', 'howdy', "what's up", 'start', 'begin', 'yo '],
        'rewrite':              ['rewrite', 'fix this', 'improve this', 'reword', 'rephrase', 'make this better', 'polish', 'optimise this bullet'],
        'ats_score':            ['ats score', 'ats rating', 'ats check', 'my score', 'score low', 'how is my ats', 'ats analysis', 'ats result'],
        'resume_improvement':   ['resume', ' cv ', 'improve my', 'fix my', 'review my', 'my resume', 'ats ready', 'format', 'bullet', 'rewrite my'],
        'skills_recommendation':['skill', 'learn', 'missing', 'technology', 'stack', 'trending', 'what should i', 'what to learn', 'in-demand', 'roadmap', 'which skill'],
        'job_search':           ['job search', 'find a job', 'job hunt', 'job board', 'where to apply', 'how to find', 'job market', 'how to get a job'],
        'interview':            ['interview', 'behavioral', 'behavioural', 'technical round', 'coding round', 'prepare', 'preparation', 'star method', 'common questions'],
        'salary':               ['salary', 'pay', 'compensation', 'ctc', 'package', 'earn', 'income', 'wage', 'how much', 'make money', 'benchmark', 'what does a', 'how much does'],
        'negotiation':          ['negotiat', 'counter offer', 'how to ask for more', 'first offer', 'ask for raise', 'offer letter', 'ask for more money'],
        'linkedin':             ['linkedin', 'profile', 'headline', 'summary section', 'open to work', 'linkedin tip', 'linkedin url'],
        'career_gap':           ['gap', 'career break', 'unemployed', 'out of work', 'career change', 'transition', 'pivot', 'sabbatical', 'explain my break', 'leave of absence'],
        'project':              ['project', 'portfolio', 'github', 'side project', 'i built', 'i made', 'i created', 'i developed', 'building'],
        'certification':        ['certification', 'certificate', 'cert', 'course', 'bootcamp', 'upskill', 'study for', 'should i get'],
        'company':              ['company', 'culture', 'glassdoor', 'faang', 'startup', 'employer', 'where to work', 'which company', 'amazon interview', 'google interview', 'meta interview', 'microsoft interview', 'interview process at', 'companies in pakistan', 'top companies', 'about amazon', 'about google', 'about meta', 'about microsoft', 'about faang'],
        'cover_letter':         ['cover letter', 'application letter', 'motivation letter', 'why this company'],
        'networking':           ['network', 'networking', 'referral', 'reach out', 'coffee chat', 'alumni', 'cold message', 'hidden job'],
        'freelancing':          ['freelance', 'upwork', 'fiverr', 'contract', 'gig', 'self-employed', 'consulting', 'client work', 'toptal'],
        'remote_work':          ['remote', 'work from home', 'wfh', 'hybrid', 'digital nomad', 'remote job', 'remote only'],
        'networking':           ['network', 'networking', 'referral', 'reach out', 'coffee chat', 'alumni', 'cold message', 'hidden job', 'linkedin outreach'],
        'trending':             ['trending', 'future', 'emerging', 'in demand', 'hot skill', 'next big', 'market demand', '2025', '2024 skill', 'ai trend'],
        'jd_match':             ['match', 'job description', 'should i apply', 'am i qualified', 'do i qualify', 'fit for this', 'ready for this role', 'missing for this role'],
    }

    scores = {intent: 0 for intent in intent_patterns}
    for intent, keywords in intent_patterns.items():
        for kw in keywords:
            if kw in msg:
                # Longer, more specific keywords carry more weight
                scores[intent] += 3 if len(kw) > 10 else (2 if len(kw) > 5 else 1)

    # Boost salary if salary word + role is detected (prevents skills collision)
    salary_trigger = any(w in msg for w in ['salary', 'pay', 'earn', 'compensation', 'how much', 'ctc', 'package'])
    if salary_trigger:
        scores['salary'] += 3

    # Role keyword + question → skills_recommendation
    question_words = ['what', 'how', 'tell', 'explain', 'describe', 'show', 'which']
    role_in_msg = any(kw in msg for kw in [
        'devops', 'full stack', 'backend', 'frontend', 'data scientist',
        'ml engineer', 'software engineer', 'cloud engineer', 'qa engineer',
    ])
    if role_in_msg and any(qw in msg for qw in question_words) and scores.get('skills_recommendation', 0) == 0:
        scores['skills_recommendation'] += 2

    best_intent = max(scores, key=scores.get)

    # If no signal, inherit from history
    if scores[best_intent] == 0 and len(msg.split()) <= 5 and chat_history:
        last_bot = next(
            (m['content'].lower() for m in reversed(chat_history) if m['role'] == 'assistant'),
            ''
        )
        if any(w in last_bot for w in ['salary', 'pay', 'compensation', 'earn']):
            return 'salary'
        if any(w in last_bot for w in ['interview', 'question', 'prepare']):
            return 'interview'
        if any(w in last_bot for w in ['skill', 'learn', 'missing', 'technology']):
            return 'skills_recommendation'
        if any(w in last_bot for w in ['certification', 'cert', 'course']):
            return 'certification'
        if any(w in last_bot for w in ['project', 'portfolio', 'github']):
            return 'project'
        return 'greeting'

    return best_intent if scores[best_intent] > 0 else 'unknown'


# ============================================================
# RESPONSE HANDLERS
# ============================================================
def process_rewrite(message):
    """Transform a weak resume bullet into an ATS-optimised, metric-driven one."""
    text = re.sub(
        r'\b(rewrite|fix this|reword|improve this|rephrase|make this better|polish|optimise this bullet)\b',
        '', message, flags=re.IGNORECASE
    ).strip(' :.,-')

    if len(text) < 5:
        return (
            "Paste the sentence or bullet you want rewritten and I'll make it ATS-ready.\n\n"
            "**Example input:**\n"
            "> *Rewrite: Worked on backend APIs for the user module.*\n\n"
            "I'll transform it into an action-verb-led, metric-driven, ATS-optimised bullet."
        )

    lower = text.lower()
    if any(w in lower for w in ['managed', 'led', 'team', 'supervised', 'headed']):
        return (
            f"**Original:** {text}\n\n"
            "**Rewrite:** Led a cross-functional team of 5 engineers to deliver a high-priority feature 2 weeks ahead of schedule, improving sprint velocity by 30%.\n\n"
            "**Changes made:**\n"
            "- Added team size (quantified scope)\n"
            "- Added outcome ('2 weeks ahead', '30% velocity')\n"
            "- Replaced passive phrasing with strong action-verb lead ('Led')"
        )
    elif any(w in lower for w in ['helped', 'worked', 'assisted', 'contributed', 'involved']):
        return (
            f"**Original:** {text}\n\n"
            "**Rewrite:** Collaborated with product and design teams to streamline the checkout flow, reducing cart abandonment by 18% and increasing conversion by 12%.\n\n"
            "**Changes made:**\n"
            "- Replaced weak verb with strong action verb ('Collaborated')\n"
            "- Added specific teams involved\n"
            "- Added quantified business outcomes"
        )
    elif any(w in lower for w in ['built', 'made', 'created', 'developed', 'coded']):
        return (
            f"**Original:** {text}\n\n"
            "**Rewrite:** Engineered and shipped a production-grade REST API service using FastAPI + PostgreSQL, reducing data retrieval latency by 40% and handling 10K+ daily requests.\n\n"
            "**Changes made:**\n"
            "- Upgraded verb to 'Engineered and shipped' (stronger, production-focused)\n"
            "- Added specific tech stack (ATS keyword signal)\n"
            "- Added quantified performance metrics"
        )
    elif any(w in lower for w in ['improved', 'optimised', 'optimized', 'enhanced', 'upgraded']):
        return (
            f"**Original:** {text}\n\n"
            "**Rewrite:** Optimised database query performance by refactoring N+1 queries and adding strategic indexes, reducing average API response time from 850ms to 120ms (86% improvement).\n\n"
            "**Changes made:**\n"
            "- Added HOW it was improved (technical depth)\n"
            "- Added before/after metrics (850ms → 120ms)\n"
            "- Added percentage for quick scanning"
        )
    elif any(w in lower for w in ['responsible', 'in charge', 'handled', 'worked on']):
        return (
            f"**Original:** {text}\n\n"
            "**Rewrite:** Owned end-to-end implementation of the user authentication module, cutting login failure rate by 25% and reducing auth-related support tickets by 40%.\n\n"
            "**Changes made:**\n"
            "- Replaced vague ownership with 'Owned end-to-end' — shows accountability\n"
            "- Specified the deliverable precisely\n"
            "- Added business impact metrics"
        )
    return (
        f"**Original:** {text}\n\n"
        f"**Rewrite:** Successfully delivered {text[:80]}, achieving measurable improvements in system performance and stakeholder satisfaction.\n\n"
        "**To make this stronger, tell me:**\n"
        "- What technology stack did you use?\n"
        "- What was the measurable result (% improvement, # users, time saved)?\n"
        "- What was the team size or project scale?\n\n"
        "With those details I'll write a much more powerful bullet."
    )


def handle_greeting(resume_text=None):
    insight = _analyze_resume_text(resume_text)

    if insight:
        skills_preview = ', '.join(insight['detected_skills'][:5]) if insight['detected_skills'] else 'none detected yet'
        missing = ', '.join(insight['missing_sections']) if insight['missing_sections'] else 'none — good structure'
        return (
            "I've reviewed your resume and I'm ready to give you direct, no-fluff career advice.\n\n"
            "**Quick resume snapshot:**\n"
            f"- Detected skills: {skills_preview}\n"
            f"- Missing sections: {missing}\n"
            f"- Quantified metrics: {'✅ Present' if insight['has_metrics'] else '❌ Missing — this is critical'}\n"
            f"- GitHub link: {'✅ Present' if insight['has_github'] else '❌ Missing — add it today'}\n"
            f"- LinkedIn URL: {'✅ Present' if insight['has_linkedin'] else '❌ Missing — add it today'}\n\n"
            "**What would you like to focus on?**\n"
            "- *Full ATS review of my resume*\n"
            "- *What skills am I missing for [Role]?*\n"
            "- *Prepare me for a [Role] interview*\n"
            "- *What salary should I ask for?*\n"
            "- *Rewrite: [paste your bullet here]*"
        )
    return (
        "I'm your Senior Recruiter AI — I give direct, no-fluff career advice.\n\n"
        "**I can help you with:**\n\n"
        "📄 **Resume** — ATS review, bullet rewrites, section feedback\n"
        "🎯 **Job Match** — Do you qualify? What's missing vs. the JD?\n"
        "🛠️ **Skills** — Role-specific skill gaps and learning roadmaps\n"
        "💰 **Salary** — Market benchmarks for PK / UAE / US / Remote\n"
        "🎙️ **Interviews** — Prep questions + answer strategies by role\n"
        "🔗 **LinkedIn** — Profile optimisation to attract recruiters\n"
        "🏢 **Companies** — FAANG prep, Pakistani tech companies, research tips\n"
        "📜 **Certifications** — What to get for your target role\n"
        "🌍 **Remote / Freelancing** — How to break in and negotiate\n"
        "📈 **Trending** — What skills are in demand for 2025\n\n"
        "What would you like to work on first?"
    )


def handle_resume_improvement(message, resume_text=None, chat_history=None):
    insight = _analyze_resume_text(resume_text)
    tips = random.sample(KNOWLEDGE_BASE['resume_tips'], 4)

    response = "**Resume Review — Direct Feedback:**\n\n"

    if insight:
        wins = []
        issues = []

        if not insight['has_metrics']:
            issues.append("❌ **No quantified metrics** — Add numbers to every bullet: team size, % improvement, # users, $ saved. This is the #1 weakness recruiters flag.")
        else:
            wins.append("✅ Metrics detected — solid foundation")

        if not insight['has_github']:
            issues.append("❌ **No GitHub link** — Every tech resume must have a GitHub URL at the top. Recruiters check it immediately.")
        else:
            wins.append("✅ GitHub linked")

        if not insight['has_linkedin']:
            issues.append("❌ **No LinkedIn URL** — Add it to your contact section. Recruiters cross-reference LinkedIn before deciding to call.")
        else:
            wins.append("✅ LinkedIn linked")

        if not insight['has_summary']:
            issues.append("❌ **No Professional Summary** — Add 2–3 lines targeting your exact role. It's the first thing a recruiter reads.")

        if not insight['has_action_verbs']:
            issues.append("❌ **Weak bullet verbs** — Start every bullet with: Engineered, Deployed, Automated, Led, Reduced. Avoid: 'Worked on', 'Helped with', 'Responsible for'.")
        else:
            wins.append("✅ Action verbs present")

        wc = insight['word_count']
        if wc < 200:
            issues.append(f"❌ **Resume too thin** ({wc} words) — Expand experience bullets and add a Projects section. Target 350–700 words.")
        elif wc > 1100:
            issues.append(f"⚠️ **Resume too long** ({wc} words) — Trim to top 5 highest-impact bullets per role. Every bullet must earn its place.")
        else:
            wins.append(f"✅ Length is solid ({wc} words)")

        if not insight['has_projects']:
            issues.append("❌ **No Projects section** — Add 2–3 projects with tech stack, GitHub link, and quantified outcomes. Critical for tech roles.")

        if wins:
            response += "**What's working:**\n" + '\n'.join(wins) + "\n\n"
        if issues:
            response += "**Critical fixes (priority order):**\n" + '\n'.join(issues) + "\n\n"
        if insight['detected_skills']:
            response += f"**Skills detected:** {', '.join(insight['detected_skills'])}\n\n"

    response += "**Universal ATS improvements:**\n"
    for tip in tips:
        response += f"- {tip}\n"

    return _trim_response(response)


def handle_ats_score(resume_text=None):
    if not resume_text:
        return (
            "**How ATS Scoring Works:**\n\n"
            "ATS (Applicant Tracking System) filters your resume before any human sees it. Key factors:\n\n"
            "1. **Keyword match (40%)** — Does your resume contain exact keywords from the JD?\n"
            "2. **Standard sections (20%)** — Work Experience, Education, Skills, Projects, Contact\n"
            "3. **Format compliance (20%)** — No tables, text boxes, or multi-column layouts\n"
            "4. **Quantified achievements (10%)** — Numbers and metrics throughout\n"
            "5. **File format (10%)** — PDF or .docx matching what the portal specifies\n\n"
            "**Quick wins to push above 80%:**\n"
            "- Copy 5 exact keyword phrases from the JD into your resume\n"
            "- Use standard section headers only\n"
            "- Add metrics to every bullet point\n"
            "- Single-column layout only\n\n"
            "Upload your resume to get a personalised ATS score estimate."
        )

    insight = _analyze_resume_text(resume_text)
    score = 40
    breakdown = []

    if insight['has_metrics']:
        score += 15
        breakdown.append("✅ Quantified metrics: +15 pts")
    else:
        breakdown.append("❌ No metrics: 0 pts (missing 15)")

    if insight['has_skills']:
        score += 10
        breakdown.append("✅ Skills section: +10 pts")
    else:
        breakdown.append("❌ No clear Skills section: 0 pts (missing 10)")

    if insight['has_experience']:
        score += 10
        breakdown.append("✅ Work Experience section: +10 pts")
    else:
        breakdown.append("❌ Work Experience unclear: 0 pts (missing 10)")

    if insight['has_education']:
        score += 5
        breakdown.append("✅ Education section: +5 pts")
    else:
        breakdown.append("❌ Education not clearly labeled: 0 pts (missing 5)")

    if insight['has_summary']:
        score += 5
        breakdown.append("✅ Professional Summary: +5 pts")
    else:
        breakdown.append("❌ No Professional Summary: 0 pts (missing 5)")

    if insight['has_action_verbs']:
        score += 5
        breakdown.append("✅ Strong action verbs: +5 pts")
    else:
        breakdown.append("❌ Weak bullet verbs: 0 pts (missing 5)")

    if insight['has_github']:
        score += 5
        breakdown.append("✅ GitHub link: +5 pts")
    if insight['has_linkedin']:
        score += 5
        breakdown.append("✅ LinkedIn URL: +5 pts")

    score = min(score, 100)
    grade = "🟢 Strong" if score >= 80 else "🟡 Needs work" if score >= 60 else "🔴 Needs major improvement"

    response = f"**ATS Score Estimate: {score}/100 — {grade}**\n\n**Score Breakdown:**\n"
    for item in breakdown:
        response += f"- {item}\n"
    response += (
        "\n**Note:** Actual ATS scores vary ±10–15 pts depending on the specific system and JD keyword matching.\n\n"
        "**To reach 85+:**\n"
        "- Tailor keywords from the JD into your resume\n"
        "- Fix all ❌ items above\n"
        "- Use a single-column, ATS-clean format"
    )
    return _trim_response(response)


def handle_skills(message, resume_text=None, chat_history=None):
    role = _extract_role_from_context(message, chat_history)
    insight = _analyze_resume_text(resume_text)

    # Find matching skills set
    role_skills = None
    role_label = role.title()
    for key in KNOWLEDGE_BASE['skills_by_role']:
        if key in role or role in key:
            role_skills = KNOWLEDGE_BASE['skills_by_role'][key]
            role_label = key.title()
            break

    if not role_skills:
        response = "**Top In-Demand Tech Skills (2025):**\n\n"
        for skill in KNOWLEDGE_BASE['trending_tech'][:8]:
            response += f"- {skill}\n"
        response += (
            "\n**Tell me your target role** (DevOps, Full Stack, Data Scientist, ML Engineer, "
            "Backend, Cybersecurity, etc.) and I'll give you a prioritised, role-specific skill roadmap."
        )
        return response

    response = f"**Top Skills to Master for {role_label} Roles (priority order):**\n\n"
    for i, skill in enumerate(role_skills, 1):
        response += f"{i}. {skill}\n"

    # Gap analysis from resume
    if insight and insight['detected_skills']:
        skills_text = ' '.join(role_skills).lower()
        gap_keywords = ['docker', 'kubernetes', 'terraform', 'aws', 'react', 'typescript',
                        'sql', 'python', 'git', 'linux', 'ci/cd', 'redis', 'kafka', 'spark']
        gaps = [s for s in gap_keywords if s in skills_text and s not in insight['detected_skills']]
        if gaps:
            response += f"\n**Based on your resume — skills you're missing for {role_label}:**\n"
            for gap in gaps[:4]:
                response += f"- `{gap.upper()}` — not detected in your resume\n"

    # Cert recommendations
    certs = None
    for key in KNOWLEDGE_BASE['certifications_by_role']:
        if key in role or role in key:
            certs = KNOWLEDGE_BASE['certifications_by_role'][key]
            break
    if not certs:
        certs = KNOWLEDGE_BASE['certifications_by_role']['default']

    response += "\n**Recommended certifications:**\n"
    for cert in certs[:3]:
        response += f"- {cert}\n"

    return _trim_response(response)


def handle_salary(message, chat_history=None):
    role = _extract_role_from_context(message, chat_history)
    rates = KNOWLEDGE_BASE['salary'].get(role, KNOWLEDGE_BASE['salary']['default'])
    role_label = role.title() if role != 'default' else 'Tech Professional'

    return (
        f"**{role_label} Salary Benchmarks (2024–2025)**\n\n"
        f"🇵🇰 **Pakistan:** {rates['pk']}\n"
        f"🇦🇪 **UAE / Gulf:** {rates['uae']}\n"
        f"🇺🇸 **USA (on-site):** {rates['us']}\n"
        f"🌍 **Remote (USD):** {rates['remote']}\n\n"
        "**Negotiation playbook:**\n"
        "- Never give your number first — 'I'd like to understand the full comp structure before discussing a number'\n"
        "- Anchor 10–15% above your real target; you can always negotiate down, never up\n"
        "- Negotiate the full package: base + bonus + equity + PTO + remote days + learning budget\n"
        "- Competing offer? Use it: 'I have another offer at X — I'd still prefer your team, can you match it?'\n"
        "- Silence after stating your number is your strongest negotiation tool\n\n"
        "**Research sources:** Glassdoor, LinkedIn Salary, Levels.fyi (tech), Payscale"
    )


def handle_interview(message, chat_history=None):
    role = _extract_role_from_context(message, chat_history)
    msg_lower = message.lower()

    # Match role to interview question set
    question_set = None
    role_label = role.title()
    for key in KNOWLEDGE_BASE['interview_questions']:
        if key in role or role in key or key in msg_lower:
            question_set = KNOWLEDGE_BASE['interview_questions'][key]
            role_label = key.title()
            break

    if question_set:
        selected = random.sample(question_set, min(3, len(question_set)))
        response = f"**{role_label} Interview Prep — 3 Real Questions + Strategies:**\n\n"
        for i, item in enumerate(selected, 1):
            response += f"**Q{i}: {item['q']}**\n"
            response += f"💡 *Strategy: {item['tip']}*\n\n"
        response += (
            "**Universal interview tips:**\n"
            "- Prepare 3 STAR stories that can flex to any behavioural question\n"
            "- Research the company's last 3 blog posts or news items before every round\n"
            "- Prepare 5 smart questions to ask at the end — filters red flags, shows initiative\n"
            "- Send a thank-you email within 24 hours — fewer than 20% of candidates do this"
        )
        return _trim_response(response)

    tips = random.sample(KNOWLEDGE_BASE['interview_prep'], 5)
    response = "**Interview Preparation Framework:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"
    response += (
        "\n**Tell me the specific role** (DevOps, Full Stack, Data Scientist, PM, Backend, etc.) "
        "and I'll give you 3 real role-specific questions with answer strategies."
    )
    return response


def handle_job_search(resume_text=None):
    insight = _analyze_resume_text(resume_text)
    tips = random.sample(KNOWLEDGE_BASE['job_search'], 5)

    response = "**Job Search Action Plan:**\n\n"
    for i, tip in enumerate(tips, 1):
        response += f"{i}. {tip}\n"

    if insight:
        if not insight['has_linkedin']:
            response += "\n⚠️ **Priority action:** Add your LinkedIn URL to your resume before applying anywhere."
        if not insight['has_github']:
            response += "\n⚠️ **Priority action:** Add your GitHub URL — tech recruiters check this in the first 60 seconds."

    response += (
        "\n\n**Best job boards by category:**\n"
        "- **General tech:** LinkedIn, Indeed, Glassdoor\n"
        "- **Startups:** Wellfound (AngelList), YC Jobs\n"
        "- **Remote only:** Remote.co, We Work Remotely, Remote OK\n"
        "- **Pakistan market:** Rozee.pk, Mustakbil, Naukri.pk\n"
        "- **Senior/vetted:** Toptal, Arc.dev, Hired"
    )
    return _trim_response(response)


def handle_linkedin(resume_text=None):
    insight = _analyze_resume_text(resume_text)
    tips = random.sample(KNOWLEDGE_BASE['linkedin_tips'], 5)

    response = "**LinkedIn Profile Optimisation — Recruiter View:**\n\n"

    if insight and not insight['has_linkedin']:
        response += "⚠️ **Immediate action:** Add your LinkedIn URL to your resume contact section.\n\n"

    for i, tip in enumerate(tips, 1):
        response += f"{i}. {tip}\n"

    response += (
        "\n**Sections that move the needle most:**\n"
        "1. **Headline** — Optimise for keywords, not just current job title\n"
        "2. **About** — 3 paragraphs: who you are → specialties → call to action with email\n"
        "3. **Featured** — Pin best project, GitHub, or portfolio — 90% of profiles leave this blank\n"
        "4. **Skills + endorsements** — 5 endorsements on top 3 skills boosts algorithm ranking\n"
        "5. **Activity** — 1 post/week minimum when job searching\n\n"
        "**Recruiter magnet moves:**\n"
        "- Turn on 'Open to Work' (recruiter-only visibility)\n"
        "- Use target job title 2–3 times across headline, summary, and experience\n"
        "- Complete ALL sections — incomplete profiles rank lower in recruiter searches"
    )
    return _trim_response(response)


def handle_career_gap(message, chat_history=None):
    tips = random.sample(KNOWLEDGE_BASE['career_gap_tips'], 4)

    response = "**Career Gap — How to Frame It Like a Pro:**\n\n"
    response += "Recruiters see career gaps every day. The gap rarely costs you the role — how you explain it does.\n\n"
    for tip in tips:
        response += f"- {tip}\n"

    response += (
        "\n**Gap framing formula (use this script):**\n"
        "> *'I took [duration] to [honest reason]. During that time I [specific activity: cert/freelance/study]. "
        "I'm now fully ready and energised because [reason tied to this specific role].'*\n\n"
        "**Resume strategy:**\n"
        "- Year-only formatting hides short gaps: '2022–2024' not 'Mar 2022–Sep 2023'\n"
        "- List freelance/consulting work during the gap as a proper role\n"
        "- Add certifications from the gap period to your Certifications section\n\n"
        "**Career pivot strategy:**\n"
        "- Rewrite your Professional Summary to align with the new direction immediately\n"
        "- Lead with transferable skills, not your old role title\n"
        "- Build 2 portfolio projects in your new field before applying"
    )
    return _trim_response(response)


def handle_project(message, chat_history=None):
    project_name = ''
    for m in (chat_history or [])[-6:]:
        match = re.search(
            r'(?:called|named|project|building|built|made|created)\s+([\w\s]+?)(?:using|with|in|on|$)',
            m['content'], re.I
        )
        if match:
            project_name = match.group(1).strip()
            break

    label = f'**{project_name}**' if project_name else 'your project'
    tips = random.sample(KNOWLEDGE_BASE['project_tips'], 4)

    response = f"**How to Maximise {label}'s Impact on Your Resume & Portfolio:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"

    response += (
        "\n**Strong project bullet formula:**\n"
        "> *Engineered [project name] using [tech stack], serving [X users / handling Y requests], "
        "resulting in [Z% improvement / specific outcome].*\n\n"
        "**Your GitHub README must include:**\n"
        "1. Project name + 1-sentence problem statement\n"
        "2. Tech stack badges\n"
        "3. Live demo link or screenshots\n"
        "4. Quick-start / installation instructions\n\n"
        "**Free deployment options:**\n"
        "- Frontend: Vercel, Netlify, GitHub Pages\n"
        "- Backend: Render, Railway, Fly.io (free tier)\n"
        "- Full stack: Railway or Render allow containerised apps on free tier"
    )
    return _trim_response(response)


def handle_certification(message, chat_history=None):
    role = _extract_role_from_context(message, chat_history)
    tips = random.sample(KNOWLEDGE_BASE['certification_tips'], 4)

    certs = None
    role_label = 'Your Target Role'
    for key in KNOWLEDGE_BASE['certifications_by_role']:
        if key in role or role in key:
            certs = KNOWLEDGE_BASE['certifications_by_role'][key]
            role_label = key.title()
            break

    response = "**Certification Strategy — What's Actually Worth It:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"

    if certs:
        response += f"\n**Top certifications for {role_label} roles:**\n"
        for cert in certs:
            response += f"- {cert}\n"
    else:
        response += "\n**High-ROI certifications for any tech career:**\n"
        for cert in KNOWLEDGE_BASE['certifications_by_role']['default']:
            response += f"- {cert}\n"
        response += "\n**Tell me your target role** for role-specific cert recommendations."

    response += (
        "\n\n**Study platforms:**\n"
        "- A Cloud Guru / Pluralsight — hands-on cloud labs\n"
        "- Coursera / edX — academic and professional certs\n"
        "- Udemy — $10–$15/course during sales (frequent)\n"
        "- Linux Foundation — LFCS, CKA, CKAD open-source certs\n"
        "- Vendor free tiers — AWS/GCP/Azure all have free practice sandboxes"
    )
    return _trim_response(response)


def handle_company(message):
    msg_lower = message.lower()

    if any(w in msg_lower for w in ['faang', 'google', 'meta', 'amazon', 'apple', 'netflix', 'microsoft', 'big tech']):
        return KNOWLEDGE_BASE['companies']['faang_info']

    if any(w in msg_lower for w in ['pakistan', 'pk', 'lahore', 'karachi', 'islamabad', 'local', 'pakistani']):
        response = "**Top Tech Companies in Pakistan (2024):**\n\n"
        for company in KNOWLEDGE_BASE['companies']['top_companies_pk']:
            response += f"- {company}\n"
        response += (
            "\n**How to land a role at these companies:**\n"
            "1. LinkedIn job alerts for each company directly\n"
            "2. Referrals — connect with alumni at these companies on LinkedIn\n"
            "3. Check company career pages directly — many roles never get posted elsewhere\n"
            "4. Rozee.pk and Mustakbil.com for Pakistan-specific postings"
        )
        return response

    tips = random.sample(KNOWLEDGE_BASE['companies']['research_tips'], 4)
    response = "**How to Research a Company Before Applying or Interviewing:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"
    response += (
        "\n**Key questions to answer in your research:**\n"
        "1. What's their actual tech stack? (GitHub org, job postings, engineering blog)\n"
        "2. What's the culture like? (Glassdoor, LinkedIn employee posts)\n"
        "3. What's their growth trajectory? (Crunchbase, LinkedIn headcount growth)\n"
        "4. Red flags? (High Glassdoor turnover, vague JDs, interview complaints)\n"
        "5. Who are the interviewers? (LinkedIn — prepare to reference their work)\n\n"
        "**Tell me a specific company** (Amazon, Arbisoft, Careem, Google, etc.) and I'll give you specific interview intel."
    )
    return _trim_response(response)


def handle_cover_letter(resume_text=None):
    tips = random.sample(KNOWLEDGE_BASE['cover_letter_tips'], 4)
    response = "**Cover Letter — Most Candidates Get This Wrong:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"

    response += (
        "\n**Proven 3-paragraph structure:**\n\n"
        "**Para 1 — Hook (2–3 sentences):**\n"
        "Reference a specific product, news item, or their engineering challenge — "
        "never start with 'I am writing to apply for...'\n\n"
        "**Para 2 — Relevance + Proof (3–4 sentences):**\n"
        "Connect 2 of your measurable achievements to their key requirements. "
        "Use numbers. Mirror their JD language.\n\n"
        "**Para 3 — Close (2–3 sentences):**\n"
        "'I'd love to discuss how I can contribute to [team] in a 20-minute call.' Include email + LinkedIn.\n\n"
        "**Template:**\n"
        "> *[Company]'s work on [specific thing] resonates because [genuine reason]. "
        "In my last role I [achievement with metric] and [achievement with metric] — "
        "both align directly with your need for [JD requirement]. "
        "I'd welcome a brief call to discuss: [email].*"
    )
    return _trim_response(response)


def handle_networking():
    tips = random.sample(KNOWLEDGE_BASE['networking_tips'], 5)
    response = "**Strategic Networking — Not the 'Let's Connect' Spam Version:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"
    response += (
        "\n**LinkedIn outreach that gets replies:**\n"
        "> *'Hi [Name], I saw your post about [specific topic] — great insight on [point]. "
        "I'm a [your role] exploring [their company/industry] and would genuinely value "
        "15 minutes of your perspective. Happy to work around your schedule.'*\n\n"
        "**Referral request (after 1 conversation):**\n"
        "> *'I noticed [Company] is hiring for [Role] — it looks like a strong fit. "
        "Would you be comfortable referring me? I'll send you my resume and JD to make it easy.'*\n\n"
        "**Track your network:** Name | Company | Last Contact | Next Step — follow up every 6 weeks."
    )
    return _trim_response(response)


def handle_remote_work():
    tips = random.sample(KNOWLEDGE_BASE['remote_work_tips'], 5)
    response = "**Breaking Into Remote Work — Practical Guide:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"
    response += (
        "\n**How to signal remote-readiness in your resume:**\n"
        "- Add 'Remote (UTC+5, flexible)' to your location field\n"
        "- List async tools: Notion, Loom, Linear, Confluence, Slack, Jira\n"
        "- Include a portfolio site or GitHub — remote employers hire what they can see online\n\n"
        "**Best platforms for remote engineering roles:**\n"
        "- **Remote.co, We Work Remotely** — curated remote-only postings\n"
        "- **Arc.dev** — vetted engineers matched with global companies\n"
        "- **Toptal** — elite network, rigorous screening, premium rates\n"
        "- **LinkedIn (filter: Remote)** — largest volume of remote postings"
    )
    return _trim_response(response)


def handle_negotiation():
    tips = random.sample(KNOWLEDGE_BASE['negotiation_tips'], 5)
    response = "**Salary Negotiation Playbook:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"
    response += (
        "\n**Exact scripts for common moments:**\n\n"
        "**When they ask your expectation first:**\n"
        "> *'I'd like to understand the full scope of the role and comp philosophy before settling on a number. "
        "Could you share the budgeted range for this position?'*\n\n"
        "**Counter-offer:**\n"
        "> *'Thank you for the offer — I'm genuinely excited. Based on market research and the value I'll bring, "
        "I was expecting [X+15%]. Is there flexibility to get closer to that?'*\n\n"
        "**When base is fixed:**\n"
        "> *'I understand the base is capped. Could we revisit the signing bonus, an extra week of PTO, or an accelerated 6-month review?'*\n\n"
        "**Golden rule:** Never accept or reject in the moment — always ask for 24–48 hours to review in writing."
    )
    return _trim_response(response)


def handle_freelancing():
    tips = random.sample(KNOWLEDGE_BASE['freelancing_tips'], 5)
    response = "**Breaking Into Freelancing — Realistic Guide:**\n\n"
    for tip in tips:
        response += f"- {tip}\n"
    response += (
        "\n**Platform comparison:**\n\n"
        "| Platform | Best For | Avg Rate | Competition |\n"
        "|---|---|---|---|\n"
        "| Fiverr | Entry-level, packages | $20–$100/task | Very high |\n"
        "| Upwork | Mid-level, ongoing projects | $25–$80/hr | High |\n"
        "| Toptal | Senior engineers (top 3%) | $80–$200/hr | Low (screened) |\n"
        "| Arc.dev | Remote-first developers | $60–$150/hr | Medium (vetted) |\n"
        "| Direct clients | Expert level, referrals | Custom | Low |\n\n"
        "**Getting your first client:**\n"
        "1. Announce on LinkedIn you're available for freelance work\n"
        "2. Offer a free audit (code review, resume review) to build trust\n"
        "3. Price competitively for first 3 projects, raise rates after 5 reviews\n"
        "4. Ask every satisfied client for a testimonial — this is your sales engine"
    )
    return _trim_response(response)


def handle_trending():
    response = "**Trending Technologies & Skills in 2024–2025:**\n\n"
    for tech in KNOWLEDGE_BASE['trending_tech']:
        response += f"- {tech}\n"

    response += (
        "\n**Highest-growth career paths right now:**\n"
        "1. **AI/ML Engineer** — LLM fine-tuning, RAG systems, model deployment — fastest growing in tech\n"
        "2. **Platform Engineer** — DevOps evolved; building Internal Developer Platforms (IDP)\n"
        "3. **Analytics Engineer** — dbt + Snowflake/BigQuery — sits between Data Eng and Data Science\n"
        "4. **DevSecOps** — security shifted left into every engineering team\n"
        "5. **Full Stack + AI integration** — engineers who integrate LLM APIs are in very high demand\n\n"
        "**Skills that future-proof any career:**\n"
        "- Cloud fundamentals (minimum 1 cloud cert)\n"
        "- Python — connective tissue of AI, data, and automation\n"
        "- System design — scales with your seniority level\n"
        "- Clear technical writing and communication"
    )
    return _trim_response(response)


def handle_jd_match(message, resume_text=None, job_description=None, chat_history=None):
    if not job_description:
        return (
            "To see your exact job match, paste the job description in the **Job Match** section "
            "of SmartHireAI — I'll show your match %, matched keywords, missing keywords, and specific suggestions.\n\n"
            "**The universal 'should I apply?' rule:**\n"
            "If you match 60–70% of the requirements, apply. Hiring managers post wishlists, not checklists. "
            "If you meet the top 3–4 required skills, you're a viable candidate.\n\n"
            "**Before applying:**\n"
            "1. Copy 5 exact keyword phrases from the JD into your resume bullets\n"
            "2. Mirror the JD's exact job title in your resume headline\n"
            "3. Address 'nice-to-have' skills you have but haven't mentioned\n"
            "4. Write one tailored cover letter sentence about this company specifically"
        )

    # Quick keyword analysis
    resume_words = set(re.findall(r'[a-zA-Z]{3,}', (resume_text or '').lower()))
    jd_words = set(re.findall(r'[a-zA-Z]{3,}', job_description.lower()))
    stop_words = {
        'and', 'the', 'is', 'in', 'to', 'with', 'for', 'a', 'of', 'on', 'as', 'an', 'are',
        'be', 'this', 'that', 'from', 'by', 'your', 'you', 'we', 'our', 'will', 'can', 'or',
        'at', 'have', 'has', 'it', 'not', 'all', 'skills', 'experience', 'work', 'job', 'team',
        'years', 'looking', 'role', 'must', 'strong', 'ability', 'knowledge', 'development',
        'design', 'working', 'using', 'required', 'preferred', 'should', 'would', 'could',
    }

    jd_keywords = jd_words - stop_words
    overlap = jd_keywords.intersection(resume_words)
    missing = jd_keywords - resume_words

    match_pct = min(int((len(overlap) / len(jd_keywords)) * 100), 100) if jd_keywords else 0
    verdict = "🟢 Strong match — apply immediately" if match_pct >= 70 else \
              "🟡 Moderate match — tailor resume first" if match_pct >= 50 else \
              "🔴 Below threshold — significant gaps to address"

    top_missing = sorted(missing, key=len, reverse=True)[:6]
    top_matched = list(overlap)[:8]

    response = (
        f"**Job Description Match Analysis:**\n\n"
        f"**Match Score: {match_pct}% — {verdict}**\n\n"
        f"✅ **Keywords you have:** {', '.join(top_matched) if top_matched else 'None detected'}\n\n"
        "❌ **Missing keywords (add these to your resume):**\n"
    )
    for kw in top_missing:
        response += f"- `{kw}` — integrate into a bullet or your Skills section\n"

    response += (
        "\n**Your 15-minute pre-apply checklist:**\n"
        "1. Add the missing keywords above into your resume bullets naturally\n"
        "2. Mirror the exact job title from the JD in your headline\n"
        "3. Write one tailored cover letter sentence about this company specifically\n"
        "4. Connect with 1 person at this company on LinkedIn before submitting"
    )
    return _trim_response(response)


def handle_unknown(message, resume_text=None):
    insight = _analyze_resume_text(resume_text)
    response = ""

    if insight:
        suggestions = []
        if not insight['has_metrics']:
            suggestions.append("**Add metrics** to every resume bullet — no numbers = no callbacks")
        if not insight['has_github']:
            suggestions.append("**Add your GitHub URL** to your resume contact section today")
        if not insight['has_projects']:
            suggestions.append("**Add a Projects section** — critical for any tech role")
        if suggestions:
            response = "**Based on your resume, here's what I'd prioritise:**\n\n"
            for s in suggestions:
                response += f"- {s}\n"
            response += "\n"

    response += (
        "**I can help you with any of these — just ask:**\n\n"
        "📄 **Resume** — `'Review my resume'` or `'Rewrite: [paste bullet]'`\n"
        "🎯 **Job Match** — `'Should I apply for this role?'`\n"
        "🛠️ **Skills** — `'What skills do I need for DevOps?'`\n"
        "💰 **Salary** — `'What's the salary for a Data Scientist in UAE?'`\n"
        "🎙️ **Interviews** — `'Prepare me for a Full Stack interview'`\n"
        "🔗 **LinkedIn** — `'How do I optimise my LinkedIn profile?'`\n"
        "📜 **Certifications** — `'What certs should I get for Cloud Engineering?'`\n"
        "🏢 **Companies** — `'Tell me about FAANG interviews'` or `'Top companies in Pakistan'`\n"
        "🌍 **Remote Work** — `'How do I get a remote job?'`\n"
        "🤝 **Networking** — `'How do I get a referral?'`\n"
        "📝 **Cover Letter** — `'Give me a cover letter structure'`\n"
        "💸 **Negotiation** — `'How do I negotiate my salary offer?'`\n"
        "📈 **Trending** — `'What skills are in demand in 2025?'`"
    )
    return response


# ============================================================
# MAIN ENTRY POINT
# ============================================================
def generate_intelligent_response(message, resume_text=None, job_description=None, chat_history=None):
    """
    Primary entry point. Fully rule-based — zero external API calls.
    Classifies intent and dispatches to the appropriate career knowledge handler.
    Always returns a non-empty, structured response.
    """
    print("[SmartHireAI Engine] Processing request — rule-based engine active")

    if not message or not message.strip():
        return handle_greeting(resume_text)

    intent = analyze_intent(message, chat_history)
    print(f"[SmartHireAI Engine] Intent detected: {intent}")

    dispatch = {
        'greeting':              lambda: handle_greeting(resume_text),
        'rewrite':               lambda: process_rewrite(message),
        'ats_score':             lambda: handle_ats_score(resume_text),
        'resume_improvement':    lambda: handle_resume_improvement(message, resume_text, chat_history),
        'skills_recommendation': lambda: handle_skills(message, resume_text, chat_history),
        'job_search':            lambda: handle_job_search(resume_text),
        'interview':             lambda: handle_interview(message, chat_history),
        'salary':                lambda: handle_salary(message, chat_history),
        'linkedin':              lambda: handle_linkedin(resume_text),
        'career_gap':            lambda: handle_career_gap(message, chat_history),
        'project':               lambda: handle_project(message, chat_history),
        'certification':         lambda: handle_certification(message, chat_history),
        'company':               lambda: handle_company(message),
        'cover_letter':          lambda: handle_cover_letter(resume_text),
        'networking':            lambda: handle_networking(),
        'freelancing':           lambda: handle_freelancing(),
        'remote_work':           lambda: handle_remote_work(),
        'negotiation':           lambda: handle_negotiation(),
        'trending':              lambda: handle_trending(),
        'jd_match':              lambda: handle_jd_match(message, resume_text, job_description, chat_history),
        'unknown':               lambda: handle_unknown(message, resume_text),
    }

    handler = dispatch.get(intent, lambda: handle_unknown(message, resume_text))

    try:
        response = handler()
        return response if response and response.strip() else handle_unknown(message, resume_text)
    except Exception as e:
        print(f"[SmartHireAI Engine] Handler error (intent={intent}): {e}")
        return handle_unknown(message, resume_text)
