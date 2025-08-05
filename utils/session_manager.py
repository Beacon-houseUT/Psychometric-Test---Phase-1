import streamlit as st

def initialize_session():
    """Initialize all session state variables"""
    
    # Form and processing states
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if 'report_data' not in st.session_state:
        st.session_state.report_data = None
    if 'original_data' not in st.session_state:
        st.session_state.original_data = None
    
    # Edit mode
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    
    # Career analysis
    if 'career_data' not in st.session_state:
        st.session_state.career_data = None
    if 'career_analysis_requested' not in st.session_state:
        st.session_state.career_analysis_requested = False
    if 'original_career_data' not in st.session_state:
        st.session_state.original_career_data = None
    
    # Google export
    if 'google_authenticated' not in st.session_state:
        st.session_state.google_authenticated = False
    if 'export_requested' not in st.session_state:
        st.session_state.export_requested = False

# ─── STATE CHECKERS ──────────────────────────────
def is_form_submitted():
    """Check if form has been submitted"""
    return st.session_state.form_submitted

def has_report_data():
    """Check if report data exists"""
    return st.session_state.report_data is not None

def has_career_data():
    """Check if career data exists"""
    return st.session_state.career_data is not None

def is_edit_mode():
    """Check if in edit mode"""
    return st.session_state.edit_mode

def is_processing_career_analysis():
    """Check if career analysis is being processed"""
    return st.session_state.career_analysis_requested and not st.session_state.career_data

def is_google_authenticated():
    """Check if Google is authenticated"""
    return st.session_state.google_authenticated

# ─── FORM DATA MANAGEMENT ──────────────────────────
def store_form_data(name, age, grade, uploaded_files):
    """Store form data in session state"""
    st.session_state.name = name
    st.session_state.age = age
    st.session_state.grade = grade
    st.session_state.uploaded_files = uploaded_files
    st.session_state.form_submitted = True

def get_form_data():
    """Get stored form data"""
    return {
        'name': getattr(st.session_state, 'name', ''),
        'age': getattr(st.session_state, 'age', 0),
        'grade': getattr(st.session_state, 'grade', ''),
        'uploaded_files': getattr(st.session_state, 'uploaded_files', [])
    }

# ─── REPORT DATA MANAGEMENT ──────────────────────────
def store_report_data(data):
    """Store report data and create backup"""
    st.session_state.report_data = data
    st.session_state.original_data = data.copy()

def get_report_data():
    """Get current report data"""
    return st.session_state.report_data

def get_student_info():
    """Get student info from report data or form data"""
    if st.session_state.report_data:
        return st.session_state.report_data.get("studentInfo", {
            "name": getattr(st.session_state, 'name', 'Unknown'),
            "age": getattr(st.session_state, 'age', 'Unknown'),
            "grade": getattr(st.session_state, 'grade', 'Unknown'),
        })
    else:
        return {
            "name": getattr(st.session_state, 'name', 'Unknown'),
            "age": getattr(st.session_state, 'age', 'Unknown'),
            "grade": getattr(st.session_state, 'grade', 'Unknown'),
        }

# ─── CAREER DATA MANAGEMENT ──────────────────────────
def store_career_data(data):
    """Store career data and create backup"""
    st.session_state.career_data = data
    if data:  # Only create backup if data exists
        st.session_state.original_career_data = data.copy()
    st.session_state.career_analysis_requested = False

def get_career_data():
    """Get current career data"""
    return st.session_state.career_data

def request_career_analysis():
    """Request career analysis"""
    st.session_state.career_analysis_requested = True

def request_career_reanalysis():
    """Request career reanalysis"""
    st.session_state.career_data = None
    st.session_state.career_analysis_requested = True

# ─── EDIT MODE MANAGEMENT ──────────────────────────
def toggle_edit_mode():
    """Toggle edit mode on/off"""
    st.session_state.edit_mode = not st.session_state.edit_mode

def reset_changes():
    """Reset all changes to original data"""
    if st.session_state.original_data:
        st.session_state.report_data = st.session_state.original_data.copy()
    
    if hasattr(st.session_state, 'original_career_data') and st.session_state.original_career_data:
        st.session_state.career_data = st.session_state.original_career_data.copy()

def save_changes():
    """Save current changes as new original"""
    if st.session_state.report_data:
        st.session_state.original_data = st.session_state.report_data.copy()
    
    if st.session_state.career_data:
        st.session_state.original_career_data = st.session_state.career_data.copy()
    
    st.session_state.edit_mode = False

# ─── GOOGLE EXPORT MANAGEMENT ──────────────────────────
def set_google_authenticated(status):
    """Set Google authentication status"""
    st.session_state.google_authenticated = status

def request_export():
    """Request export to Google Docs"""
    st.session_state.export_requested = True

# ─── RESET FUNCTIONS ──────────────────────────────
def reset_all():
    """Reset entire application state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def reset_form():
    """Reset form submission state"""
    st.session_state.form_submitted = False
