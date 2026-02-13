# 🎓 Faculty Management System v2.0

A comprehensive faculty and session management application built with Python and Streamlit, now with advanced features!

## 🌟 NEW Features in v2.0

### ✨ Advanced Filtering
- Multi-criteria filtering for sessions
- Filter by date range, faculty, batch, honorarium range, and feedback scores
- Export filtered results to Excel
- Real-time statistics on filtered data

### 📅 Calendar View
- Interactive monthly calendar showing all sessions
- Visual indicators for session count per day
- Month and year selection
- Highlighted sessions in calendar grid

### 📥 Bulk Import from Excel/CSV
- Import multiple sessions at once
- **Auto-create missing faculties** with default values
- Column mapping for flexible file formats
- Feedback score normalization (0-5 to 0-10 scale)

### 👤 User Profile Management
- Update full name and email
- Change password securely
- View account information

### 🔑 Password Reset
- Forgot password workflow
- Secure password reset
- Change password from profile

### 📊 Excel Export
- Export faculties to Excel
- Export sessions with all feedback
- Export filtered results
- Professional formatting

## 🚀 Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

**Default Login:** `admin` / `admin123`

## 📥 Bulk Import Guide

1. Go to "📥 Bulk Import"
2. Upload Excel/CSV file
3. Map columns (Date, Faculty, Topic required)
4. Click "Import Sessions"
5. System auto-creates missing faculties!

### Auto-Faculty Creation
- Automatically creates faculty if not found
- Default gender: "Other"
- Auto-generated email
- Can be edited later

## 📅 Calendar View

1. Select year and month
2. View sessions in calendar grid
3. Blue highlights = sessions that day
4. Click to view details

## 🔍 Advanced Filtering

Filter sessions by:
- Date range
- Faculty
- Batch
- Honorarium range
- Minimum feedback score

Export filtered results to Excel!

## 📊 Excel Exports

All export buttons now generate professional Excel files:
- Faculty list with all details
- Session list with feedback scores
- Filtered session results
- Faculty-specific session reports

## 🔐 Security

- Password hashing (SHA-256)
- User data isolation
- Admin full access
- Password reset functionality

**Version**: 2.0.0  
**Built with**: Python + Streamlit
