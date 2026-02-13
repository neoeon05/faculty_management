import streamlit as st
import pandas as pd
import json
from datetime import datetime, date, timedelta
import hashlib
import os
from pathlib import Path
import io
import re

# Set page configuration
st.set_page_config(
    page_title="Faculty Management System",
    page_icon="👨‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File paths for data storage
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
FACULTIES_FILE = DATA_DIR / "faculties.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'reset_token' not in st.session_state:
    st.session_state.reset_token = None

# Utility functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_json(filepath, default=None):
    if default is None:
        default = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def initialize_data():
    # Initialize users with default admin account
    if not os.path.exists(USERS_FILE):
        users = {
            "admin": {
                "password": hash_password("admin123"),
                "is_admin": True,
                "email": "admin@system.com",
                "full_name": "System Administrator"
            }
        }
        save_json(USERS_FILE, users)
    
    # Initialize faculties
    if not os.path.exists(FACULTIES_FILE):
        save_json(FACULTIES_FILE, {})
    
    # Initialize sessions
    if not os.path.exists(SESSIONS_FILE):
        save_json(SESSIONS_FILE, {})

# Load data
initialize_data()

def get_user_faculties(username, is_admin):
    faculties = load_json(FACULTIES_FILE, {})
    if is_admin:
        return faculties
    return {k: v for k, v in faculties.items() if v.get('created_by') == username}

def get_user_sessions(username, is_admin):
    sessions = load_json(SESSIONS_FILE, {})
    if is_admin:
        return sessions
    return {k: v for k, v in sessions.items() if v.get('created_by') == username}

def get_faculty_by_name(faculty_name):
    """Get faculty by name, return faculty_id or None"""
    faculties = load_json(FACULTIES_FILE, {})
    for fid, faculty in faculties.items():
        if faculty['name'].lower() == faculty_name.lower():
            return fid, faculty
    return None, None

def create_faculty_from_name(faculty_name, created_by="system"):
    """Create a new faculty with default values from just a name"""
    faculties = load_json(FACULTIES_FILE, {})
    faculty_id = f"FAC{len(faculties) + 1:04d}"
    
    # Extract email from name (simple approach)
    email_name = faculty_name.lower().replace(" ", ".").replace("sh.", "").replace("dr.", "").replace("prof.", "").strip()
    email = f"{email_name}@faculty.edu"
    
    faculties[faculty_id] = {
        'id': faculty_id,
        'name': faculty_name,
        'gender': 'Other',  # Default
        'email': email,
        'designation': 'Faculty',  # Default designation
        'batch': '',
        'biodata': 'Auto-created from bulk import',
        'created_by': created_by,
        'created_at': datetime.now().isoformat()
    }
    
    save_json(FACULTIES_FILE, faculties)
    return faculty_id

# Login Page
def login_page():
    st.title("🎓 Faculty Management System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("Login", type="primary", key="login_btn"):
                users = load_json(USERS_FILE)
                if username in users and users[username]['password'] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.is_admin = users[username].get('is_admin', False)
                    st.session_state.page = 'home'
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        with col_btn2:
            if st.button("Register", key="register_btn"):
                st.session_state.page = 'register'
                st.rerun()
        
        with col_btn3:
            if st.button("Forgot Password?", key="forgot_btn"):
                st.session_state.page = 'forgot_password'
                st.rerun()

# Registration Page
def register_page():
    st.title("🎓 Faculty Management System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Register New Account")
        new_username = st.text_input("Username", key="reg_username")
        full_name = st.text_input("Full Name", key="reg_fullname")
        email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Register", type="primary", key="reg_submit_btn"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif new_username == "" or full_name == "" or email == "":
                    st.error("All fields are required")
                elif '@' not in email:
                    st.error("Please enter a valid email address")
                else:
                    users = load_json(USERS_FILE)
                    if new_username in users:
                        st.error("Username already exists")
                    else:
                        users[new_username] = {
                            "password": hash_password(new_password),
                            "is_admin": False,
                            "email": email,
                            "full_name": full_name
                        }
                        save_json(USERS_FILE, users)
                        st.success("Registration successful! Please login.")
                        st.session_state.page = 'login'
                        st.rerun()
        
        with col_btn2:
            if st.button("Back to Login", key="reg_back_btn"):
                st.session_state.page = 'login'
                st.rerun()

# Forgot Password Page
def forgot_password_page():
    st.title("🎓 Faculty Management System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Reset Password")
        username = st.text_input("Username", key="forgot_username")
        email = st.text_input("Email", key="forgot_email")
        
        if st.button("Request Password Reset", type="primary", key="forgot_submit_btn"):
            users = load_json(USERS_FILE)
            if username in users and users[username].get('email') == email:
                # Generate reset token (simplified - in production use secure tokens)
                st.session_state.reset_token = {
                    'username': username,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.page = 'reset_password'
                st.rerun()
            else:
                st.error("Invalid username or email")
        
        if st.button("Back to Login", key="forgot_back_btn"):
            st.session_state.page = 'login'
            st.rerun()

# Reset Password Page
def reset_password_page():
    if not st.session_state.reset_token:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    st.title("🎓 Faculty Management System")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Set New Password")
        st.info(f"Resetting password for: {st.session_state.reset_token['username']}")
        
        new_password = st.text_input("New Password", type="password", key="reset_password")
        confirm_password = st.text_input("Confirm New Password", type="password", key="reset_confirm")
        
        if st.button("Reset Password", type="primary", key="reset_submit_btn"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                users = load_json(USERS_FILE)
                username = st.session_state.reset_token['username']
                users[username]['password'] = hash_password(new_password)
                save_json(USERS_FILE, users)
                st.success("Password reset successful! Please login with your new password.")
                st.session_state.reset_token = None
                st.session_state.page = 'login'
                st.rerun()

# User Profile Management Page
def user_profile_page():
    st.title("👤 User Profile")
    
    users = load_json(USERS_FILE)
    user_data = users.get(st.session_state.username, {})
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Profile Information")
        with st.form("profile_form"):
            full_name = st.text_input("Full Name", value=user_data.get('full_name', ''))
            email = st.text_input("Email", value=user_data.get('email', ''))
            
            st.markdown("**Account Information:**")
            st.markdown(f"- Username: `{st.session_state.username}`")
            st.markdown(f"- Role: `{'Admin' if st.session_state.is_admin else 'User'}`")
            
            if st.form_submit_button("Update Profile", type="primary"):
                if full_name and email and '@' in email:
                    users[st.session_state.username]['full_name'] = full_name
                    users[st.session_state.username]['email'] = email
                    save_json(USERS_FILE, users)
                    st.success("Profile updated successfully!")
                    st.rerun()
                else:
                    st.error("Please fill all fields with valid information")
    
    with col2:
        st.subheader("Change Password")
        with st.form("password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password", type="primary"):
                if hash_password(current_password) != user_data['password']:
                    st.error("Current password is incorrect")
                elif new_password != confirm_password:
                    st.error("New passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    users[st.session_state.username]['password'] = hash_password(new_password)
                    save_json(USERS_FILE, users)
                    st.success("Password changed successfully!")
                    st.rerun()

# User Management Page (Admin Only)
def user_management_page():
    st.title("👥 User Management")
    
    if not st.session_state.is_admin:
        st.error("Access denied. This page is for administrators only.")
        return
    
    users = load_json(USERS_FILE)
    
    tab1, tab2 = st.tabs(["➕ Add User", "📋 Manage Users"])
    
    with tab1:
        st.subheader("Create New User")
        with st.form("create_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username *", max_chars=50)
                full_name = st.text_input("Full Name *", max_chars=100)
                email = st.text_input("Email *", max_chars=100)
            
            with col2:
                new_password = st.text_input("Password *", type="password")
                confirm_password = st.text_input("Confirm Password *", type="password")
                is_admin = st.checkbox("Grant Admin Rights")
            
            submitted = st.form_submit_button("Create User", type="primary")
            
            if submitted:
                if not new_username or not full_name or not email or not new_password:
                    st.error("Please fill all mandatory fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif '@' not in email:
                    st.error("Please enter a valid email address")
                elif new_username in users:
                    st.error("Username already exists")
                else:
                    users[new_username] = {
                        "password": hash_password(new_password),
                        "is_admin": is_admin,
                        "email": email,
                        "full_name": full_name,
                        "created_at": datetime.now().isoformat(),
                        "created_by": st.session_state.username
                    }
                    save_json(USERS_FILE, users)
                    st.success(f"User '{new_username}' created successfully!")
                    st.rerun()
    
    with tab2:
        st.subheader("All Users")
        
        if len(users) == 0:
            st.info("No users found.")
        else:
            # Display users in a table format
            user_data = []
            for username, user_info in users.items():
                user_data.append({
                    'Username': username,
                    'Full Name': user_info.get('full_name', 'N/A'),
                    'Email': user_info.get('email', 'N/A'),
                    'Role': 'Admin' if user_info.get('is_admin', False) else 'User',
                    'Created At': user_info.get('created_at', 'N/A')[:10] if user_info.get('created_at') else 'N/A'
                })
            
            df_users = pd.DataFrame(user_data)
            st.dataframe(df_users, hide_index=True)
            
            st.markdown("---")
            st.subheader("Edit/Delete Users")
            
            for username, user_info in users.items():
                with st.expander(f"👤 {username} ({user_info.get('full_name', 'N/A')})"):
                    with st.form(f"edit_user_{username}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_full_name = st.text_input("Full Name *", value=user_info.get('full_name', ''), key=f"fname_{username}")
                            edit_email = st.text_input("Email *", value=user_info.get('email', ''), key=f"email_{username}")
                            edit_is_admin = st.checkbox("Admin Rights", value=user_info.get('is_admin', False), key=f"admin_{username}")
                        
                        with col2:
                            st.markdown(f"**Username:** `{username}`")
                            st.markdown(f"**Created At:** {user_info.get('created_at', 'N/A')[:10] if user_info.get('created_at') else 'N/A'}")
                            st.markdown(f"**Created By:** {user_info.get('created_by', 'N/A')}")
                        
                        st.markdown("---")
                        st.markdown("**Reset Password (optional)**")
                        new_pwd = st.text_input("New Password (leave blank to keep current)", type="password", key=f"pwd_{username}")
                        confirm_pwd = st.text_input("Confirm New Password", type="password", key=f"cpwd_{username}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            update_btn = st.form_submit_button("Update User", type="primary")
                        with col_btn2:
                            # Don't allow deleting your own account or last admin
                            can_delete = username != st.session_state.username
                            if user_info.get('is_admin', False):
                                admin_count = sum(1 for u in users.values() if u.get('is_admin', False))
                                can_delete = can_delete and admin_count > 1
                            
                            delete_btn = st.form_submit_button("Delete User", type="secondary", disabled=not can_delete)
                        
                        if update_btn:
                            if not edit_full_name or not edit_email:
                                st.error("Please fill all mandatory fields")
                            elif '@' not in edit_email:
                                st.error("Please enter a valid email address")
                            elif new_pwd and new_pwd != confirm_pwd:
                                st.error("New passwords do not match")
                            elif new_pwd and len(new_pwd) < 6:
                                st.error("Password must be at least 6 characters")
                            else:
                                users[username]['full_name'] = edit_full_name
                                users[username]['email'] = edit_email
                                users[username]['is_admin'] = edit_is_admin
                                
                                if new_pwd:
                                    users[username]['password'] = hash_password(new_pwd)
                                
                                save_json(USERS_FILE, users)
                                st.success(f"User '{username}' updated successfully!")
                                st.rerun()
                        
                        if delete_btn:
                            del users[username]
                            save_json(USERS_FILE, users)
                            st.success(f"User '{username}' deleted successfully!")
                            st.rerun()


# Home/Dashboard Page
def home_page():
    st.title("📊 Dashboard")
    
    faculties = get_user_faculties(st.session_state.username, st.session_state.is_admin)
    sessions = get_user_sessions(st.session_state.username, st.session_state.is_admin)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Faculties", len(faculties))
    
    with col2:
        st.metric("Total Sessions", len(sessions))
    
    with col3:
        total_honorarium = sum(s.get('honorarium_paid', 0) for s in sessions.values())
        st.metric("Total Honorarium", f"₹{total_honorarium:,.2f}")
    
    with col4:
        if sessions:
            # Calculate average based on 'overall_performance' score only (out of 5)
            overall_scores = []
            for session in sessions.values():
                feedback = session.get('feedback', {})
                overall_perf = feedback.get('overall_performance')
                if overall_perf and isinstance(overall_perf, (int, float)) and overall_perf > 0:
                    overall_scores.append(overall_perf)
            if overall_scores:
                st.metric("Avg Feedback Score", f"{sum(overall_scores)/len(overall_scores):.2f}/5")
            else:
                st.metric("Avg Feedback Score", "N/A")
        else:
            st.metric("Avg Feedback Score", "N/A")
    
    st.markdown("---")
    
    # Recent Sessions
    if sessions:
        st.subheader("📅 Recent Sessions")
        sessions_list = []
        for sid, session in sessions.items():
            sessions_list.append({
                'Date': session.get('date'),
                'Session Name': session.get('session_name'),
                'Faculty': session.get('faculty_name'),
                'Batch': session.get('batch', 'N/A'),
                'Honorarium': f"₹{session.get('honorarium_paid', 0):,.2f}"
            })
        
        df = pd.DataFrame(sessions_list)
        df = df.sort_values('Date', ascending=False).head(10)
        st.dataframe(df, hide_index=True)

# Advanced Filtering for Sessions
def apply_session_filters(sessions, filter_config):
    """Apply advanced filters to sessions"""
    filtered = sessions.copy()
    
    # Date range filter
    if filter_config.get('start_date') and filter_config.get('end_date'):
        filtered = {
            sid: s for sid, s in filtered.items()
            if filter_config['start_date'] <= datetime.strptime(s['date'], '%Y-%m-%d').date() <= filter_config['end_date']
        }
    
    # Faculty filter
    if filter_config.get('faculty'):
        filtered = {
            sid: s for sid, s in filtered.items()
            if s.get('faculty_name') == filter_config['faculty']
        }
    
    # Batch filter
    if filter_config.get('batch'):
        filtered = {
            sid: s for sid, s in filtered.items()
            if filter_config['batch'].lower() in s.get('batch', '').lower()
        }
    
    # Honorarium range
    if filter_config.get('min_honorarium') is not None:
        filtered = {
            sid: s for sid, s in filtered.items()
            if s.get('honorarium_paid', 0) >= filter_config['min_honorarium']
        }
    
    if filter_config.get('max_honorarium') is not None:
        filtered = {
            sid: s for sid, s in filtered.items()
            if s.get('honorarium_paid', 0) <= filter_config['max_honorarium']
        }
    
    # Feedback score filter
    if filter_config.get('min_feedback') is not None:
        filtered_by_feedback = {}
        for sid, s in filtered.items():
            feedback = s.get('feedback', {})
            scores = [v for k, v in feedback.items() if k != 'recommend_again' and isinstance(v, (int, float)) and v > 0]
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score >= filter_config['min_feedback']:
                    filtered_by_feedback[sid] = s
        filtered = filtered_by_feedback
    
    return filtered

# Calendar View for Sessions
def calendar_view_page():
    st.title("📅 Calendar View")
    
    sessions = get_user_sessions(st.session_state.username, st.session_state.is_admin)
    
    if not sessions:
        st.info("No sessions to display. Add some sessions first!")
        return
    
    # Month selector
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        current_year = datetime.now().year
        year = st.selectbox("Year", range(current_year - 2, current_year + 2), index=2)
    
    with col2:
        month = st.selectbox("Month", range(1, 13), 
                            format_func=lambda x: datetime(2000, x, 1).strftime('%B'),
                            index=datetime.now().month - 1)
    
    # Filter sessions for selected month
    month_sessions = {}
    for sid, session in sessions.items():
        try:
            session_date = datetime.strptime(session['date'], '%Y-%m-%d')
            if session_date.year == year and session_date.month == month:
                day = session_date.day
                if day not in month_sessions:
                    month_sessions[day] = []
                month_sessions[day].append(session)
        except:
            continue
    
    st.markdown("---")
    
    # Create calendar grid
    import calendar
    cal = calendar.monthcalendar(year, month)
    
    # Display calendar
    st.subheader(f"{datetime(year, month, 1).strftime('%B %Y')}")
    
    # Header row
    cols = st.columns(7)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"**{day}**")
    
    # Calendar rows
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown("&nbsp;")
                else:
                    # Check if there are sessions on this day
                    if day in month_sessions:
                        session_count = len(month_sessions[day])
                        st.markdown(f"""
                        <div style='background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #2196f3;'>
                            <strong style='font-size: 18px;'>{day}</strong><br>
                            <span style='color: #1976d2; font-size: 12px;'>📚 {session_count} session{'s' if session_count > 1 else ''}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='padding: 10px;'><span style='font-size: 18px;'>{day}</span></div>", unsafe_allow_html=True)
    
    # Show session details below calendar
    if month_sessions:
        st.markdown("---")
        st.subheader("Sessions This Month")
        
        for day in sorted(month_sessions.keys()):
            st.markdown(f"### {datetime(year, month, day).strftime('%B %d, %Y')}")
            for session in month_sessions[day]:
                with st.expander(f"📚 {session['session_name']} - {session['faculty_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Duration:** {session.get('duration', 'N/A')} hours")
                        st.markdown(f"**Batch:** {session.get('batch', 'N/A')}")
                    with col2:
                        st.markdown(f"**Honorarium:** ₹{session.get('honorarium_paid', 0):,.2f}")
                        if st.button(f"View Details", key=f"view_{session['id']}"):
                            st.session_state.selected_session = session['id']
                            st.session_state.page = 'session_details'
                            st.rerun()

# Bulk Import Page
def bulk_import_page():
    st.title("📥 Bulk Import")
    
    st.markdown("""
    ### Import Sessions from Excel/CSV
    
    Upload an Excel or CSV file with session data. The system will:
    - Import all sessions from the file
    - Auto-create missing faculties with default values
    - Skip invalid or duplicate rows
    
    **Required columns:**
    - Date
    - Faculty/Speaker Name
    - Session/Topic Name
    - Batch (optional)
    - Feedback scores (optional)
    """)
    
    uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=['xlsx', 'xls', 'csv'])
    
    if uploaded_file is not None:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                # Show sheet selector for Excel
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_name = st.selectbox("Select Sheet", xl_file.sheet_names)
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            
            st.subheader("Preview Data")
            st.dataframe(df.head(10))
            
            st.markdown("---")
            st.subheader("Column Mapping")
            st.markdown("Map your Excel columns to system fields:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                date_col = st.selectbox("Date Column", options=[''] + list(df.columns), 
                                       index=list(df.columns).index('DA1:O1ate') + 1 if 'DA1:O1ate' in df.columns else 0)
                faculty_col = st.selectbox("Faculty/Speaker Column", options=[''] + list(df.columns),
                                          index=list(df.columns).index('Speaker') + 1 if 'Speaker' in df.columns else 0)
                topic_col = st.selectbox("Session/Topic Column", options=[''] + list(df.columns),
                                        index=list(df.columns).index('Topic') + 1 if 'Topic' in df.columns else 0)
                batch_col = st.selectbox("Batch Column (optional)", options=[''] + list(df.columns),
                                        index=list(df.columns).index('Batch') + 1 if 'Batch' in df.columns else 0)
            
            with col2:
                duration_col = st.selectbox("Duration Column (optional)", options=[''] + list(df.columns))
                honorarium_col = st.selectbox("Honorarium Column (optional)", options=[''] + list(df.columns))
                
                st.markdown("**Feedback Columns (optional):**")
                # Map feedback columns
                feedback_mapping = {}
                feedback_fields = [
                    ('relevance', 'Relevance'),
                    ('knowledge', 'Clarity/Knowledge'),
                    ('practical_linking', 'Practical Linking'),
                    ('coverage', 'Coverage'),
                    ('presentation_style', 'Presentation Style'),
                    ('audibility', 'Audibility'),
                    ('interaction', 'Interaction/Discussion'),
                    ('response', 'Response to Questions'),
                    ('teaching_aids', 'Teaching Aids'),
                    ('pace', 'Pace/Speed'),
                    ('overall_performance', 'Overall Performance')
                ]
                
                # Auto-detect feedback columns
                for key, label in feedback_fields:
                    matching_cols = [c for c in df.columns if any(word in c.lower() for word in label.lower().split())]
                    if matching_cols:
                        feedback_mapping[key] = matching_cols[0]
            
            if st.button("Import Sessions", type="primary"):
                if not date_col or not faculty_col or not topic_col:
                    st.error("Please map at least Date, Faculty, and Topic columns")
                else:
                    imported_count = 0
                    skipped_count = 0
                    created_faculties = []
                    
                    sessions = load_json(SESSIONS_FILE, {})
                    faculties = load_json(FACULTIES_FILE, {})
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, row in df.iterrows():
                        try:
                            # Skip empty rows
                            if pd.isna(row[date_col]) or pd.isna(row[faculty_col]) or pd.isna(row[topic_col]):
                                skipped_count += 1
                                continue
                            
                            # Parse date
                            try:
                                if isinstance(row[date_col], pd.Timestamp):
                                    session_date = row[date_col].strftime('%Y-%m-%d')
                                else:
                                    session_date = pd.to_datetime(str(row[date_col])).strftime('%Y-%m-%d')
                            except:
                                skipped_count += 1
                                continue
                            
                            # Get faculty name
                            faculty_name = str(row[faculty_col]).strip()
                            
                            # Check if faculty exists, create if not
                            faculty_id, faculty = get_faculty_by_name(faculty_name)
                            if not faculty_id:
                                faculty_id = create_faculty_from_name(faculty_name, st.session_state.username)
                                created_faculties.append(faculty_name)
                            
                            # Get other fields
                            session_name = str(row[topic_col]).strip()
                            batch = str(row[batch_col]).strip() if batch_col and not pd.isna(row.get(batch_col)) else ''
                            
                            # Duration
                            duration = 2.0  # Default
                            if duration_col and not pd.isna(row.get(duration_col)):
                                try:
                                    duration = float(row[duration_col])
                                except:
                                    pass
                            
                            # Honorarium
                            honorarium = 0.0
                            if honorarium_col and not pd.isna(row.get(honorarium_col)):
                                try:
                                    honorarium = float(row[honorarium_col])
                                except:
                                    pass
                            
                            # Feedback scores - normalize to proper max marks
                            feedback = {}
                            # Define max marks for each field
                            field_max_marks = {
                                'relevance': 4.0,
                                'knowledge': 5.0,
                                'practical_linking': 5.0,
                                'coverage': 5.0,
                                'presentation_style': 5.0,
                                'audibility': 5.0,
                                'interaction': 5.0,
                                'response': 5.0,
                                'teaching_aids': 5.0,
                                'pace': 3.0,
                                'overall_performance': 5.0
                            }
                            
                            for key, col in feedback_mapping.items():
                                if key in field_max_marks:
                                    max_mark = field_max_marks[key]
                                    if col in df.columns and not pd.isna(row.get(col)):
                                        try:
                                            score = float(row[col])
                                            # Ensure score doesn't exceed max marks
                                            feedback[key] = round(min(score, max_mark), 2)
                                        except:
                                            feedback[key] = 0.0
                                    else:
                                        feedback[key] = 0.0
                            
                            feedback['recommend_again'] = ''
                            
                            # Create session
                            session_id = f"SES{len(sessions) + 1:04d}"
                            sessions[session_id] = {
                                'id': session_id,
                                'date': session_date,
                                'duration': duration,
                                'faculty_name': faculty_name,
                                'session_name': session_name,
                                'batch': batch,
                                'honorarium_paid': honorarium,
                                'feedback': feedback,
                                'created_by': st.session_state.username,
                                'created_at': datetime.now().isoformat(),
                                'imported': True
                            }
                            
                            imported_count += 1
                            
                        except Exception as e:
                            st.warning(f"Error importing row {idx + 1}: {str(e)}")
                            skipped_count += 1
                        
                        # Update progress
                        progress = (idx + 1) / len(df)
                        progress_bar.progress(progress)
                        status_text.text(f"Processing row {idx + 1} of {len(df)}")
                    
                    # Save data
                    save_json(SESSIONS_FILE, sessions)
                    
                    # Show results
                    st.success(f"""
                    ✅ Import Complete!
                    - **Imported:** {imported_count} sessions
                    - **Skipped:** {skipped_count} rows
                    - **New Faculties Created:** {len(created_faculties)}
                    """)
                    
                    if created_faculties:
                        with st.expander("View Auto-Created Faculties"):
                            for fname in created_faculties:
                                st.markdown(f"- {fname}")
        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.exception(e)

# Export to Excel
def export_to_excel(data, filename, sheet_name="Data"):
    """Export data to Excel format"""
    output = io.BytesIO()
    
    if isinstance(data, dict):
        # Convert dict to DataFrame
        if data:
            df = pd.DataFrame(data.values())
        else:
            df = pd.DataFrame()
    else:
        df = data
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return output.getvalue()

# Advanced Filtering Page for Sessions
def advanced_filter_page():
    st.title("🔍 Advanced Session Filtering")
    
    sessions = get_user_sessions(st.session_state.username, st.session_state.is_admin)
    faculties = get_user_faculties(st.session_state.username, st.session_state.is_admin)
    
    if not sessions:
        st.info("No sessions to filter. Add some sessions first!")
        return
    
    st.markdown("### Filter Options")
    
    # Create filter form
    with st.form("filter_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Date Range**")
            start_date = st.date_input("From Date", value=None)
            end_date = st.date_input("To Date", value=None)
        
        with col2:
            st.markdown("**Faculty & Batch**")
            faculty_list = sorted(set(s['faculty_name'] for s in sessions.values() if s.get('faculty_name')))
            selected_faculty = st.selectbox("Faculty", ['All'] + faculty_list)
            
            batch_list = sorted(set(s.get('batch', '') for s in sessions.values() if s.get('batch')))
            selected_batch = st.selectbox("Batch", ['All'] + batch_list)
        
        with col3:
            st.markdown("**Honorarium Range**")
            min_honorarium = st.number_input("Min Honorarium", min_value=0.0, value=0.0, step=100.0)
            max_honorarium = st.number_input("Max Honorarium", min_value=0.0, value=100000.0, step=100.0)
            
            st.markdown("**Feedback Score**")
            min_feedback = st.slider("Min Avg Feedback Score", 0.0, 10.0, 0.0, 0.1)
        
        apply_filter = st.form_submit_button("Apply Filters", type="primary")
    
    if apply_filter or 'filter_config' in st.session_state:
        filter_config = {
            'start_date': start_date,
            'end_date': end_date,
            'faculty': selected_faculty if selected_faculty != 'All' else None,
            'batch': selected_batch if selected_batch != 'All' else None,
            'min_honorarium': min_honorarium if min_honorarium > 0 else None,
            'max_honorarium': max_honorarium if max_honorarium < 100000 else None,
            'min_feedback': min_feedback if min_feedback > 0 else None
        }
        
        st.session_state.filter_config = filter_config
        
        # Apply filters
        filtered_sessions = apply_session_filters(sessions, filter_config)
        
        st.markdown("---")
        st.subheader(f"📊 Results: {len(filtered_sessions)} sessions found")
        
        if filtered_sessions:
            # Create display DataFrame
            sessions_data = []
            for sid, session in filtered_sessions.items():
                # Calculate avg feedback
                feedback = session.get('feedback', {})
                scores = [v for k, v in feedback.items() if k != 'recommend_again' and isinstance(v, (int, float)) and v > 0]
                avg_feedback = sum(scores) / len(scores) if scores else 0
                
                sessions_data.append({
                    'ID': session['id'],
                    'Date': session['date'],
                    'Session Name': session['session_name'],
                    'Faculty': session['faculty_name'],
                    'Batch': session.get('batch', ''),
                    'Duration (hrs)': session.get('duration', 0),
                    'Honorarium': session.get('honorarium_paid', 0),
                    'Avg Feedback': round(avg_feedback, 2)
                })
            
            df = pd.DataFrame(sessions_data)
            df = df.sort_values('Date', ascending=False)
            
            # Display table
            st.dataframe(df, hide_index=True)
            
            # Export button
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                excel_data = export_to_excel(df, "filtered_sessions.xlsx")
                st.download_button(
                    label="📥 Download as Excel",
                    data=excel_data,
                    file_name=f"filtered_sessions_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_filtered_sessions_{len(filtered_sessions)}",
                    use_container_width=True
                )
            
            # Statistics
            st.markdown("---")
            st.subheader("📈 Filtered Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Sessions", len(filtered_sessions))
            with col2:
                total_hon = sum(s.get('honorarium_paid', 0) for s in filtered_sessions.values())
                st.metric("Total Honorarium", f"₹{total_hon:,.2f}")
            with col3:
                avg_hon = total_hon / len(filtered_sessions) if filtered_sessions else 0
                st.metric("Avg Honorarium", f"₹{avg_hon:,.2f}")
            with col4:
                all_scores = []
                for s in filtered_sessions.values():
                    fb = s.get('feedback', {})
                    scores = [v for k, v in fb.items() if k != 'recommend_again' and isinstance(v, (int, float)) and v > 0]
                    all_scores.extend(scores)
                avg_fb = sum(all_scores) / len(all_scores) if all_scores else 0
                st.metric("Avg Feedback", f"{avg_fb:.2f}/10")

# Manage Faculties Page with Excel Export
def manage_faculties_page():
    st.title("👥 Manage Faculties")
    
    tab1, tab2, tab3 = st.tabs(["📝 Add Faculty", "📋 View/Edit Faculties", "🔍 Search Faculty"])
    
    with tab1:
        st.subheader("Add New Faculty")
        with st.form("add_faculty_form"):
            name = st.text_input("Name *", max_chars=100)
            gender = st.selectbox("Gender *", ["", "Male", "Female", "Other"])
            email = st.text_input("Email *", max_chars=100)
            designation = st.text_input("Designation *", max_chars=100, placeholder="e.g., Professor, Assistant Professor, Lecturer")
            batch = st.text_input("Batch", max_chars=50)
            biodata = st.text_area("Biodata", max_chars=1000)
            
            submitted = st.form_submit_button("Add Faculty", type="primary")
            
            if submitted:
                if not name or not gender or not email or not designation:
                    st.error("Please fill all mandatory fields (Name, Gender, Email, Designation)")
                elif '@' not in email:
                    st.error("Please enter a valid email address")
                else:
                    faculties = load_json(FACULTIES_FILE, {})
                    faculty_id = f"FAC{len(faculties) + 1:04d}"
                    
                    faculties[faculty_id] = {
                        'id': faculty_id,
                        'name': name,
                        'gender': gender,
                        'email': email,
                        'designation': designation,
                        'batch': batch,
                        'biodata': biodata,
                        'created_by': st.session_state.username,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    save_json(FACULTIES_FILE, faculties)
                    st.success(f"Faculty '{name}' added successfully! (ID: {faculty_id})")
                    st.rerun()
    
    with tab2:
        st.subheader("All Faculties")
        faculties = get_user_faculties(st.session_state.username, st.session_state.is_admin)
        
        if not faculties:
            st.info("No faculties found. Add a faculty to get started.")
        else:
            # Export button
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                faculty_df = pd.DataFrame([
                    {
                        'ID': f['id'],
                        'Name': f['name'],
                        'Gender': f['gender'],
                        'Email': f['email'],
                        'Designation': f.get('designation', 'Faculty'),
                        'Batch': f.get('batch', ''),
                        'Biodata': f.get('biodata', ''),
                        'Created By': f.get('created_by', ''),
                        'Created At': f.get('created_at', '')
                    }
                    for f in faculties.values()
                ])
                
                excel_data = export_to_excel(faculty_df, "faculties.xlsx")
                st.download_button(
                    label="📥 Export All to Excel",
                    data=excel_data,
                    file_name=f"faculties_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_all_faculties_{len(faculties)}",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            for fid, faculty in faculties.items():
                with st.expander(f"🎓 {faculty['name']} ({faculty['id']})"):
                    with st.form(f"edit_faculty_{fid}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            name = st.text_input("Name *", value=faculty['name'], key=f"name_{fid}")
                            gender = st.selectbox("Gender *", ["Male", "Female", "Other"], 
                                                index=["Male", "Female", "Other"].index(faculty['gender']), 
                                                key=f"gender_{fid}")
                            email = st.text_input("Email *", value=faculty['email'], key=f"email_{fid}")
                            designation = st.text_input("Designation *", value=faculty.get('designation', 'Faculty'), key=f"designation_{fid}")
                        
                        with col2:
                            batch = st.text_input("Batch", value=faculty.get('batch', ''), key=f"batch_{fid}")
                            st.markdown("**Created By:** " + faculty.get('created_by', 'Unknown'))
                            st.markdown("**Created At:** " + faculty.get('created_at', 'Unknown')[:10])
                        
                        biodata = st.text_area("Biodata", value=faculty.get('biodata', ''), key=f"biodata_{fid}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            update_btn = st.form_submit_button("Update Faculty", type="primary")
                        with col_btn2:
                            delete_btn = st.form_submit_button("Delete Faculty", type="secondary")
                        
                        if update_btn:
                            if not name or not gender or not email or not designation:
                                st.error("Please fill all mandatory fields")
                            else:
                                all_faculties = load_json(FACULTIES_FILE, {})
                                all_faculties[fid].update({
                                    'name': name,
                                    'gender': gender,
                                    'email': email,
                                    'designation': designation,
                                    'batch': batch,
                                    'biodata': biodata
                                })
                                save_json(FACULTIES_FILE, all_faculties)
                                st.success("Faculty updated successfully!")
                                st.rerun()
                        
                        if delete_btn:
                            all_faculties = load_json(FACULTIES_FILE, {})
                            del all_faculties[fid]
                            save_json(FACULTIES_FILE, all_faculties)
                            st.success("Faculty deleted successfully!")
                            st.rerun()
    
    with tab3:
        st.subheader("Search Faculty")
        search_term = st.text_input("Search by name or email", key="search_faculty")
        
        faculties = get_user_faculties(st.session_state.username, st.session_state.is_admin)
        
        if search_term:
            filtered_faculties = {
                fid: f for fid, f in faculties.items() 
                if search_term.lower() in f['name'].lower() or search_term.lower() in f['email'].lower()
            }
        else:
            filtered_faculties = faculties
        
        if filtered_faculties:
            for fid, faculty in filtered_faculties.items():
                with st.container():
                    st.markdown(f"### 🎓 {faculty['name']}")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**ID:** {faculty['id']}")
                        st.markdown(f"**Gender:** {faculty['gender']}")
                        st.markdown(f"**Email:** {faculty['email']}")
                        st.markdown(f"**Designation:** {faculty.get('designation', 'Faculty')}")
                    
                    with col2:
                        st.markdown(f"**Batch:** {faculty.get('batch', 'N/A')}")
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button(f"View Sessions", key=f"view_sessions_{fid}"):
                                st.session_state.selected_faculty = faculty['name']
                                st.session_state.page = 'faculty_sessions'
                                st.rerun()
                        with col_btn2:
                            # Prepare faculty data for export
                            faculty_export_df = pd.DataFrame([{
                                'ID': faculty['id'],
                                'Name': faculty['name'],
                                'Gender': faculty['gender'],
                                'Email': faculty['email'],
                                'Designation': faculty.get('designation', 'Faculty'),
                                'Batch': faculty.get('batch', ''),
                                'Biodata': faculty.get('biodata', ''),
                                'Created By': faculty.get('created_by', ''),
                                'Created At': faculty.get('created_at', '')[:10] if faculty.get('created_at') else ''
                            }])
                            excel_data = export_to_excel(faculty_export_df, f"{faculty['name']}.xlsx")
                            st.download_button(
                                label="📥 Download",
                                data=excel_data,
                                file_name=f"{faculty['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_faculty_{fid}",
                                use_container_width=True
                            )
                    
                    if faculty.get('biodata'):
                        st.markdown(f"**Biodata:** {faculty['biodata']}")
                    
                    st.markdown("---")
        else:
            st.info("No faculties found matching your search.")

# Manage Sessions Page with Excel Export
def manage_sessions_page():
    st.title("📚 Manage Sessions")
    
    tab1, tab2 = st.tabs(["📝 Add Session", "📋 View/Edit Sessions"])
    
    faculties = get_user_faculties(st.session_state.username, st.session_state.is_admin)
    faculty_names = [f['name'] for f in faculties.values()]
    
    with tab1:
        st.subheader("Add New Session")
        
        if not faculty_names:
            st.warning("Please add at least one faculty before creating a session.")
        else:
            with st.form("add_session_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    session_date = st.date_input("Date *", value=date.today())
                    duration = st.number_input("Duration (hours) *", min_value=0.5, max_value=24.0, value=1.0, step=0.5)
                    faculty_name = st.selectbox("Faculty Name *", [""] + faculty_names)
                    session_name = st.text_input("Session Name *", max_chars=200)
                
                with col2:
                    batch = st.text_input("Batch", max_chars=100)
                    honorarium = st.number_input("Honorarium Paid (₹)", min_value=0.0, value=0.0, step=100.0)
                
                st.markdown("### 📊 Feedback Scores (Optional)")
                st.markdown("*Enter scores as per maximum marks mentioned for each parameter*")
                
                col1, col2 = st.columns(2)
                
                feedback_fields = [
                    ("Relevance of topic to work situation", 4.0, "relevance"),
                    ("Knowledge of speaker (clarity of concepts)", 5.0, "knowledge"),
                    ("Ability to link classroom with real work", 5.0, "practical_linking"),
                    ("Comprehensive coverage of topics", 5.0, "coverage"),
                    ("Structuring and style of presentation", 5.0, "presentation_style"),
                    ("Audibility and expression while speaking", 5.0, "audibility"),
                    ("Interaction with audience", 5.0, "interaction"),
                    ("Response to questions and comments", 5.0, "response"),
                    ("Use of examples, teaching aids, case studies", 5.0, "teaching_aids"),
                    ("Pace (speed) of presentation", 3.0, "pace"),
                    ("Overall Performance", 5.0, "overall_performance")
                ]
                
                feedback_values = {}
                for i, (field, max_marks, key) in enumerate(feedback_fields):
                    with col1 if i % 2 == 0 else col2:
                        feedback_values[key] = st.number_input(
                            f"{i+1}. {field} (Max: {max_marks})", 
                            min_value=0.0, 
                            max_value=max_marks, 
                            value=0.0, 
                            step=0.01,
                            format="%.2f",
                            key=f"feedback_{key}"
                        )
                
                recommend_again = st.text_area("11. Would you recommend this faculty again?", max_chars=500)
                
                submitted = st.form_submit_button("Add Session", type="primary")
                
                if submitted:
                    if not session_date or not duration or not faculty_name or not session_name:
                        st.error("Please fill all mandatory fields (Date, Duration, Faculty Name, Session Name)")
                    else:
                        sessions = load_json(SESSIONS_FILE, {})
                        session_id = f"SES{len(sessions) + 1:04d}"
                        
                        sessions[session_id] = {
                            'id': session_id,
                            'date': str(session_date),
                            'duration': duration,
                            'faculty_name': faculty_name,
                            'session_name': session_name,
                            'batch': batch,
                            'honorarium_paid': honorarium,
                            'feedback': {
                                'relevance': feedback_values['relevance'],
                                'knowledge': feedback_values['knowledge'],
                                'practical_linking': feedback_values['practical_linking'],
                                'coverage': feedback_values['coverage'],
                                'presentation_style': feedback_values['presentation_style'],
                                'audibility': feedback_values['audibility'],
                                'interaction': feedback_values['interaction'],
                                'response': feedback_values['response'],
                                'teaching_aids': feedback_values['teaching_aids'],
                                'pace': feedback_values['pace'],
                                'overall_performance': feedback_values['overall_performance'],
                                'recommend_again': recommend_again
                            },
                            'created_by': st.session_state.username,
                            'created_at': datetime.now().isoformat()
                        }
                        
                        save_json(SESSIONS_FILE, sessions)
                        st.success(f"Session '{session_name}' added successfully! (ID: {session_id})")
                        st.rerun()
    
    with tab2:
        st.subheader("All Sessions")
        sessions = get_user_sessions(st.session_state.username, st.session_state.is_admin)
        
        if not sessions:
            st.info("No sessions found. Add a session to get started.")
        else:
            # Export button
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                sessions_export = []
                for sid, s in sessions.items():
                    fb = s.get('feedback', {})
                    sessions_export.append({
                        'ID': s['id'],
                        'Date': s['date'],
                        'Session Name': s['session_name'],
                        'Faculty': s['faculty_name'],
                        'Batch': s.get('batch', ''),
                        'Duration (hrs)': s.get('duration', 0),
                        'Honorarium': s.get('honorarium_paid', 0),
                        'Relevance': fb.get('relevance', 0),
                        'Knowledge': fb.get('knowledge', 0),
                        'Practical Linking': fb.get('practical_linking', 0),
                        'Coverage': fb.get('coverage', 0),
                        'Presentation Style': fb.get('presentation_style', 0),
                        'Audibility': fb.get('audibility', 0),
                        'Interaction': fb.get('interaction', 0),
                        'Response': fb.get('response', 0),
                        'Teaching Aids': fb.get('teaching_aids', 0),
                        'Pace': fb.get('pace', 0),
                        'Recommendation': fb.get('recommend_again', ''),
                        'Created By': s.get('created_by', ''),
                        'Created At': s.get('created_at', '')
                    })
                
                session_df = pd.DataFrame(sessions_export)
                excel_data = export_to_excel(session_df, "sessions.xlsx")
                st.download_button(
                    label="📥 Export All to Excel",
                    data=excel_data,
                    file_name=f"sessions_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_all_sessions_{len(sessions)}",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Sort sessions by date (most recent first)
            sorted_sessions = sorted(sessions.items(), key=lambda x: x[1].get('date', ''), reverse=True)
            
            for sid, session in sorted_sessions:
                with st.expander(f"📚 {session['session_name']} - {session['date']} ({session['id']})"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Faculty:** {session['faculty_name']}")
                        st.markdown(f"**Date:** {session['date']}")
                        st.markdown(f"**Duration:** {session['duration']} hours")
                        st.markdown(f"**Batch:** {session.get('batch', 'N/A')}")
                        st.markdown(f"**Honorarium:** ₹{session.get('honorarium_paid', 0):,.2f}")
                    
                    with col2:
                        if st.button("View Full Details", key=f"view_{sid}"):
                            st.session_state.selected_session = sid
                            st.session_state.page = 'session_details'
                            st.rerun()
                        
                        if st.button("Delete Session", key=f"del_{sid}", type="secondary"):
                            all_sessions = load_json(SESSIONS_FILE, {})
                            del all_sessions[sid]
                            save_json(SESSIONS_FILE, all_sessions)
                            st.success("Session deleted successfully!")
                            st.rerun()

# Faculty Sessions View
def faculty_sessions_page():
    if 'selected_faculty' not in st.session_state:
        st.session_state.page = 'manage_faculties'
        st.rerun()
    
    faculty_name = st.session_state.selected_faculty
    st.title(f"📚 Sessions by {faculty_name}")
    
    if st.button("← Back to Faculties"):
        st.session_state.page = 'manage_faculties'
        st.rerun()
    
    st.markdown("---")
    
    sessions = get_user_sessions(st.session_state.username, st.session_state.is_admin)
    faculty_sessions = {sid: s for sid, s in sessions.items() if s.get('faculty_name') == faculty_name}
    
    if not faculty_sessions:
        st.info(f"No sessions found for {faculty_name}")
    else:
        # Create a table view
        sessions_data = []
        for sid, session in faculty_sessions.items():
            sessions_data.append({
                'Session ID': sid,
                'Date': session.get('date'),
                'Session Name': session.get('session_name'),
                'Batch': session.get('batch', 'N/A'),
                'Duration (hrs)': session.get('duration'),
                'Honorarium': f"₹{session.get('honorarium_paid', 0):,.2f}"
            })
        
        df = pd.DataFrame(sessions_data)
        df = df.sort_values('Date', ascending=False)
        
        st.markdown(f"**Total Sessions:** {len(faculty_sessions)}")
        st.markdown(f"**Total Honorarium:** ₹{sum(s.get('honorarium_paid', 0) for s in faculty_sessions.values()):,.2f}")
        
        # Export button
        excel_data = export_to_excel(df, f"{faculty_name}_sessions.xlsx")
        st.download_button(
            label="📥 Export to Excel",
            data=excel_data,
            file_name=f"{faculty_name.replace(' ', '_')}_sessions_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_faculty_sessions_{st.session_state.get('selected_faculty_id', 'default')}"
        )
        
        st.markdown("---")
        st.subheader("Sessions List")
        st.dataframe(df, hide_index=True)
        
        st.markdown("---")
        st.subheader("Click on a session to view details")
        
        for sid, session in sorted(faculty_sessions.items(), key=lambda x: x[1].get('date', ''), reverse=True):
            if st.button(f"📖 {session['session_name']} - {session['date']}", key=f"btn_{sid}"):
                st.session_state.selected_session = sid
                st.session_state.page = 'session_details'
                st.rerun()

# Session Details View
def session_details_page():
    if 'selected_session' not in st.session_state:
        st.session_state.page = 'manage_sessions'
        st.rerun()
    
    sessions = load_json(SESSIONS_FILE, {})
    session_id = st.session_state.selected_session
    
    if session_id not in sessions:
        st.error("Session not found")
        st.session_state.page = 'manage_sessions'
        st.rerun()
    
    session = sessions[session_id]
    
    st.title(f"📖 Session Details: {session['session_name']}")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            if 'selected_faculty' in st.session_state:
                st.session_state.page = 'faculty_sessions'
            else:
                st.session_state.page = 'manage_sessions'
            st.rerun()
    
    st.markdown("---")
    
    # Basic Information
    st.subheader("📋 Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Session ID:** {session['id']}")
        st.markdown(f"**Session Name:** {session['session_name']}")
        st.markdown(f"**Faculty:** {session['faculty_name']}")
        st.markdown(f"**Date:** {session['date']}")
    
    with col2:
        st.markdown(f"**Duration:** {session['duration']} hours")
        st.markdown(f"**Batch:** {session.get('batch', 'N/A')}")
        st.markdown(f"**Honorarium Paid:** ₹{session.get('honorarium_paid', 0):,.2f}")
    
    # Feedback Section
    st.markdown("---")
    st.subheader("📊 Feedback Scores")
    
    feedback = session.get('feedback', {})
    
    feedback_labels = {
        'relevance': ('1. Relevance of topic to work situation', 4.0),
        'knowledge': ('2. Knowledge of speaker (clarity of concepts)', 5.0),
        'practical_linking': ('3. Ability to link classroom with real work', 5.0),
        'coverage': ('4. Comprehensive coverage of topics', 5.0),
        'presentation_style': ('5. Structuring and style of presentation', 5.0),
        'audibility': ('6. Audibility and expression while speaking', 5.0),
        'interaction': ('7. Interaction with audience', 5.0),
        'response': ('8. Response to questions and comments', 5.0),
        'teaching_aids': ('9. Use of examples, teaching aids, case studies', 5.0),
        'pace': ('10. Pace (speed) of presentation', 3.0),
        'overall_performance': ('11. Overall Performance', 5.0)
    }
    
    # Calculate total score and percentage
    total_obtained = sum(feedback.get(k, 0) for k in feedback_labels.keys() if isinstance(feedback.get(k, 0), (int, float)))
    total_max = sum(max_marks for _, max_marks in feedback_labels.values())
    percentage = (total_obtained / total_max * 100) if total_max > 0 else 0
    
    st.markdown(f"### Total Score: **{total_obtained:.2f} / {total_max:.0f}** ({percentage:.1f}%)")
    
    # Display scores in a nice format
    col1, col2 = st.columns(2)
    
    for i, (key, (label, max_marks)) in enumerate(feedback_labels.items()):
        score = feedback.get(key, 0)
        with col1 if i % 2 == 0 else col2:
            st.metric(label, f"{score:.2f} / {max_marks:.0f}")
    
    st.markdown("---")
    
    # Recommendation
    if feedback.get('recommend_again'):
        st.subheader("💬 Recommendation")
        st.info(feedback['recommend_again'])
    
    # Edit Button
    st.markdown("---")
    if st.button("✏️ Edit Session", type="primary"):
        st.session_state.editing_session = session_id
        st.session_state.page = 'edit_session'
        st.rerun()

# Edit Session Page (keeping from original)
def edit_session_page():
    if 'editing_session' not in st.session_state:
        st.session_state.page = 'manage_sessions'
        st.rerun()
    
    sessions = load_json(SESSIONS_FILE, {})
    session_id = st.session_state.editing_session
    
    if session_id not in sessions:
        st.error("Session not found")
        st.session_state.page = 'manage_sessions'
        st.rerun()
    
    session = sessions[session_id]
    
    st.title(f"✏️ Edit Session: {session['session_name']}")
    
    if st.button("← Back to Details"):
        st.session_state.selected_session = session_id
        st.session_state.page = 'session_details'
        del st.session_state.editing_session
        st.rerun()
    
    st.markdown("---")
    
    faculties = get_user_faculties(st.session_state.username, st.session_state.is_admin)
    faculty_names = [f['name'] for f in faculties.values()]
    
    with st.form("edit_session_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            session_date = st.date_input("Date *", value=datetime.strptime(session['date'], '%Y-%m-%d').date())
            duration = st.number_input("Duration (hours) *", min_value=0.5, max_value=24.0, value=session['duration'], step=0.5)
            current_faculty_index = faculty_names.index(session['faculty_name']) if session['faculty_name'] in faculty_names else 0
            faculty_name = st.selectbox("Faculty Name *", faculty_names, index=current_faculty_index)
            session_name = st.text_input("Session Name *", value=session['session_name'], max_chars=200)
        
        with col2:
            batch = st.text_input("Batch", value=session.get('batch', ''), max_chars=100)
            honorarium = st.number_input("Honorarium Paid (₹)", min_value=0.0, value=session.get('honorarium_paid', 0), step=100.0)
        
        st.markdown("### 📊 Feedback Scores")
        
        col1, col2 = st.columns(2)
        
        feedback_fields = [
            ("relevance", "Relevance of topic to work situation", 4.0),
            ("knowledge", "Knowledge of speaker (clarity of concepts)", 5.0),
            ("practical_linking", "Ability to link classroom with real work", 5.0),
            ("coverage", "Comprehensive coverage of topics", 5.0),
            ("presentation_style", "Structuring and style of presentation", 5.0),
            ("audibility", "Audibility and expression while speaking", 5.0),
            ("interaction", "Interaction with audience", 5.0),
            ("response", "Response to questions and comments", 5.0),
            ("teaching_aids", "Use of examples, teaching aids, case studies", 5.0),
            ("pace", "Pace (speed) of presentation", 3.0),
            ("overall_performance", "Overall Performance", 5.0)
        ]
        
        feedback_values = {}
        feedback = session.get('feedback', {})
        
        for i, (key, label, max_marks) in enumerate(feedback_fields):
            with col1 if i % 2 == 0 else col2:
                feedback_values[key] = st.number_input(
                    f"{i+1}. {label} (Max: {max_marks})", 
                    min_value=0.0, 
                    max_value=max_marks, 
                    value=float(feedback.get(key, 0.0)), 
                    step=0.01,
                    format="%.2f",
                    key=f"edit_feedback_{key}"
                )
        
        recommend_again = st.text_area("Would you recommend this faculty again?", 
                                       value=feedback.get('recommend_again', ''), 
                                       max_chars=500)
        
        submitted = st.form_submit_button("Update Session", type="primary")
        
        if submitted:
            if not session_date or not duration or not faculty_name or not session_name:
                st.error("Please fill all mandatory fields")
            else:
                sessions[session_id].update({
                    'date': str(session_date),
                    'duration': duration,
                    'faculty_name': faculty_name,
                    'session_name': session_name,
                    'batch': batch,
                    'honorarium_paid': honorarium,
                    'feedback': {
                        **feedback_values,
                        'recommend_again': recommend_again
                    }
                })
                
                save_json(SESSIONS_FILE, sessions)
                st.success("Session updated successfully!")
                st.session_state.selected_session = session_id
                st.session_state.page = 'session_details'
                del st.session_state.editing_session
                st.rerun()

# Reports Page (keeping from original with minor updates)
def reports_page():
    st.title("📈 Reports & Analytics")
    
    faculties = get_user_faculties(st.session_state.username, st.session_state.is_admin)
    sessions = get_user_sessions(st.session_state.username, st.session_state.is_admin)
    
    if not sessions:
        st.info("No data available for reports. Add some sessions first.")
        return
    
    tab1, tab2, tab3 = st.tabs(["Faculty Performance", "Session Analytics", "Financial Summary"])
    
    with tab1:
        st.subheader("🎓 Faculty Performance Report")
        
        faculty_data = {}
        for fid, faculty in faculties.items():
            fname = faculty['name']
            faculty_sessions = [s for s in sessions.values() if s.get('faculty_name') == fname]
            
            if faculty_sessions:
                total_sessions = len(faculty_sessions)
                total_duration = sum(s.get('duration', 0) for s in faculty_sessions)
                total_honorarium = sum(s.get('honorarium_paid', 0) for s in faculty_sessions)
                
                # Calculate average based on 'overall_performance' score only
                overall_scores = []
                for session in faculty_sessions:
                    feedback = session.get('feedback', {})
                    overall_perf = feedback.get('overall_performance')
                    if overall_perf and isinstance(overall_perf, (int, float)) and overall_perf > 0:
                        overall_scores.append(overall_perf)
                
                avg_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0
                
                faculty_data[fname] = {
                    'Faculty Name': fname,
                    'Total Sessions': total_sessions,
                    'Total Duration (hrs)': f"{total_duration:.1f}",
                    'Total Honorarium': total_honorarium,
                    'Avg Feedback Score': round(avg_score, 2),
                    'Email': faculty['email']
                }
        
        if faculty_data:
            df = pd.DataFrame(faculty_data.values())
            st.dataframe(df, hide_index=True)
            
            # Download button
            excel_data = export_to_excel(df, "faculty_performance.xlsx")
            st.download_button(
                label="📥 Download Report (Excel)",
                data=excel_data,
                file_name=f"faculty_performance_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"download_faculty_performance_{len(faculty_data)}",
                use_container_width=True
            )
        else:
            st.info("No faculty performance data available.")
    
    with tab2:
        st.subheader("📊 Session Analytics")
        
        # Monthly sessions
        session_dates = []
        for s in sessions.values():
            try:
                session_dates.append(datetime.strptime(s['date'], '%Y-%m-%d'))
            except:
                continue
        
        if session_dates:
            df_dates = pd.DataFrame({'Date': session_dates})
            df_dates['Month'] = df_dates['Date'].dt.to_period('M').astype(str)
            monthly_counts = df_dates['Month'].value_counts().sort_index()
            
            st.markdown("**Sessions per Month**")
            st.bar_chart(monthly_counts)
        
        # Batch-wise sessions
        batch_sessions = {}
        for session in sessions.values():
            batch = session.get('batch', 'Not Specified')
            if batch:
                batch_sessions[batch] = batch_sessions.get(batch, 0) + 1
        
        if batch_sessions:
            st.markdown("---")
            st.markdown("**Sessions by Batch**")
            df_batch = pd.DataFrame(list(batch_sessions.items()), columns=['Batch', 'Sessions'])
            st.dataframe(df_batch, hide_index=True)
    
    with tab3:
        st.subheader("💰 Financial Summary")
        
        total_honorarium = sum(s.get('honorarium_paid', 0) for s in sessions.values())
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Honorarium Paid", f"₹{total_honorarium:,.2f}")
        with col2:
            avg_honorarium = total_honorarium / len(sessions) if sessions else 0
            st.metric("Avg per Session", f"₹{avg_honorarium:,.2f}")
        with col3:
            st.metric("Total Sessions", len(sessions))
        
        # Monthly expenses
        st.markdown("---")
        st.markdown("**Monthly Honorarium Expenses**")
        
        monthly_expenses = {}
        for session in sessions.values():
            try:
                date_obj = datetime.strptime(session['date'], '%Y-%m-%d')
                month_key = date_obj.strftime('%Y-%m')
                monthly_expenses[month_key] = monthly_expenses.get(month_key, 0) + session.get('honorarium_paid', 0)
            except:
                continue
        
        if monthly_expenses:
            df_expenses = pd.DataFrame(list(monthly_expenses.items()), columns=['Month', 'Honorarium'])
            df_expenses = df_expenses.sort_values('Month')
            st.bar_chart(df_expenses.set_index('Month'))

# Main App Logic
def main():
    if not st.session_state.logged_in:
        if st.session_state.page == 'register':
            register_page()
        elif st.session_state.page == 'forgot_password':
            forgot_password_page()
        elif st.session_state.page == 'reset_password':
            reset_password_page()
        else:
            login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.title("🎓 Faculty Management")
            st.markdown(f"**User:** {st.session_state.username}")
            if st.session_state.is_admin:
                st.markdown("**Role:** 🔐 Admin")
            else:
                st.markdown("**Role:** 👤 User")
            
            st.markdown("---")
            
            # Navigation
            if st.button("🏠 Dashboard"):
                st.session_state.page = 'home'
                st.rerun()
            
            if st.button("👥 Manage Faculties"):
                st.session_state.page = 'manage_faculties'
                st.rerun()
            
            if st.button("📚 Manage Sessions"):
                st.session_state.page = 'manage_sessions'
                st.rerun()
            
            if st.button("🔍 Advanced Filter"):
                st.session_state.page = 'advanced_filter'
                st.rerun()
            
            if st.button("📅 Calendar View"):
                st.session_state.page = 'calendar_view'
                st.rerun()
            
            if st.button("📥 Bulk Import"):
                st.session_state.page = 'bulk_import'
                st.rerun()
            
            if st.button("📈 Reports"):
                st.session_state.page = 'reports'
                st.rerun()
            
            st.markdown("---")
            
            if st.button("👤 Profile"):
                st.session_state.page = 'user_profile'
                st.rerun()
            
            # Admin-only: User Management
            if st.session_state.is_admin:
                if st.button("👥 User Management"):
                    st.session_state.page = 'user_management'
                    st.rerun()
            
            if st.button("🚪 Logout", type="secondary"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.is_admin = False
                st.session_state.page = 'login'
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 💡 Quick Stats")
            faculties = get_user_faculties(st.session_state.username, st.session_state.is_admin)
            sessions = get_user_sessions(st.session_state.username, st.session_state.is_admin)
            st.markdown(f"**Faculties:** {len(faculties)}")
            st.markdown(f"**Sessions:** {len(sessions)}")
        
        # Main content area
        if st.session_state.page == 'home':
            home_page()
        elif st.session_state.page == 'manage_faculties':
            manage_faculties_page()
        elif st.session_state.page == 'manage_sessions':
            manage_sessions_page()
        elif st.session_state.page == 'faculty_sessions':
            faculty_sessions_page()
        elif st.session_state.page == 'session_details':
            session_details_page()
        elif st.session_state.page == 'edit_session':
            edit_session_page()
        elif st.session_state.page == 'reports':
            reports_page()
        elif st.session_state.page == 'advanced_filter':
            advanced_filter_page()
        elif st.session_state.page == 'calendar_view':
            calendar_view_page()
        elif st.session_state.page == 'bulk_import':
            bulk_import_page()
        elif st.session_state.page == 'user_profile':
            user_profile_page()
        elif st.session_state.page == 'user_management':
            user_management_page()

if __name__ == "__main__":
    main()
