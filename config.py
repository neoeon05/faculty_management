# Configuration File for Faculty Management System
# Edit these values to customize the application

# Application Settings
APP_TITLE = "Faculty Management System"
APP_ICON = "👨‍🏫"
LAYOUT = "wide"  # Options: "centered", "wide"

# Default Admin Credentials (Change these for security!)
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"  # Will be hashed automatically

# Gender Options (Add or remove as needed)
GENDER_OPTIONS = ["Male", "Female", "Other"]

# Feedback Questions (Customize as needed)
FEEDBACK_QUESTIONS = {
    "relevance": "Relevance of topic to work situation",
    "knowledge": "Knowledge of the speaker (clarity of concepts)",
    "practical_linking": "Ability to link theory with practice",
    "coverage": "Comprehensive coverage of topics",
    "presentation_style": "Structuring and style of presentation",
    "audibility": "Audibility and expression while speaking",
    "interaction": "Interaction with audience",
    "response": "Response to questions and comments",
    "teaching_aids": "Use of examples, teaching aids, and case studies",
    "pace": "Pace (speed) of presentation"
}

# Field Lengths
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 100
MAX_BATCH_LENGTH = 100
MAX_SESSION_NAME_LENGTH = 200
MAX_BIODATA_LENGTH = 1000
MAX_RECOMMENDATION_LENGTH = 500

# Numeric Constraints
MIN_FEEDBACK_SCORE = 0.0
MAX_FEEDBACK_SCORE = 10.0
FEEDBACK_STEP = 0.01
MIN_DURATION = 0.5
MAX_DURATION = 24.0
DURATION_STEP = 0.5

# Currency Symbol
CURRENCY_SYMBOL = "₹"  # Change to "$", "€", etc. as needed

# Data Storage
DATA_DIRECTORY = "data"
USERS_FILENAME = "users.json"
FACULTIES_FILENAME = "faculties.json"
SESSIONS_FILENAME = "sessions.json"

# ID Prefixes
FACULTY_ID_PREFIX = "FAC"
SESSION_ID_PREFIX = "SES"
ID_PADDING = 4  # Number of digits (e.g., 4 = 0001, 0002, etc.)

# Dashboard Settings
RECENT_SESSIONS_LIMIT = 10  # Number of recent sessions to show on dashboard
TOP_FACULTIES_LIMIT = 10  # Number of top faculties to show in reports

# Date Format
DATE_FORMAT = "%Y-%m-%d"  # ISO format, change if needed
DISPLAY_DATE_FORMAT = "%B %d, %Y"  # Human-readable format

# Password Requirements
MIN_PASSWORD_LENGTH = 6
REQUIRE_SPECIAL_CHAR = False
REQUIRE_NUMBER = False
REQUIRE_UPPERCASE = False

# Feature Flags (Enable/Disable Features)
ENABLE_REGISTRATION = True  # Allow new user registration
ENABLE_EXPORT = True  # Allow data export
ENABLE_IMPORT = True  # Allow data import
ENABLE_REPORTS = True  # Show reports section
ENABLE_BATCH_FIELD = True  # Show batch field in forms

# UI Theme Colors (Streamlit default, can be customized in .streamlit/config.toml)
# See: https://docs.streamlit.io/library/advanced-features/configuration

# Report Settings
EXPORT_DATE_FORMAT = "%Y%m%d_%H%M%S"  # Format for export filenames

# Session Settings
DEFAULT_SESSION_DURATION = 1.0  # Default duration in hours
DEFAULT_HONORARIUM = 0.0  # Default honorarium value

# Validation Settings
VALIDATE_EMAIL = True  # Validate email format
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Notes:
# - Restart the application after changing this file
# - Some changes may require code modifications in app.py
# - Keep DEFAULT_ADMIN_PASSWORD secure and change it after first login
# - Backup this file before making changes
