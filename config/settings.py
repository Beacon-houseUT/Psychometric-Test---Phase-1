# config/settings.py
# Configuration settings for the psychometric app

# N8N Webhook URLs
N8N_BASE_URL = "https://techbh.app.n8n.cloud/webhook"
PSYCHOMETRIC_UPLOAD_ENDPOINT = "/google-report-upload"
CAREER_ANALYSIS_ENDPOINT = "/google-career-analysis"
GOOGLE_EXPORT_ENDPOINT = "/google-export"

# App Configuration
APP_TITLE = "Psychometric Assessment Report"
MAX_FILE_UPLOADS = None  # No limit - let users upload as many as needed
UPLOAD_HELP_TEXT = "Upload screenshots of the test results"
SUPPORTED_FILE_TYPES = ["jpg", "jpeg", "png"]
MIN_AGE = 5
MAX_AGE = 18

# Request Configuration
CONNECTION_TIMEOUT = 30
READ_TIMEOUT = 180
MAX_RETRIES = 3

# Test Configuration
TEST_TYPES = [
    "MBTI-style Personality Type",
    "HIGH5 Strengths Themes", 
    "Big Five Personality Traits (OCEAN)",
    "RIASEC Career Interest Themes"
]
