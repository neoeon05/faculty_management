# 📚 New Features Guide - v2.0

## Table of Contents
1. [Bulk Import from Excel](#bulk-import-from-excel)
2. [Advanced Filtering](#advanced-filtering)
3. [Calendar View](#calendar-view)
4. [User Profile Management](#user-profile-management)
5. [Password Reset](#password-reset)
6. [Excel Export](#excel-export)

---

## 📥 Bulk Import from Excel

### Overview
Import multiple sessions at once from Excel or CSV files. The system will automatically create faculty profiles for any faculty members that don't exist in your database.

### Step-by-Step Guide

#### 1. Prepare Your Excel File
Your Excel file should have these columns (column names can vary):
- **Date** - Session date (required)
- **Speaker/Faculty** - Faculty name (required)
- **Topic/Session Name** - Session title (required)
- **Batch** - Student batch (optional)
- **Duration** - Hours (optional, defaults to 2.0)
- **Honorarium** - Payment amount (optional, defaults to 0)
- **Feedback columns** - Various feedback scores (optional)

#### 2. Upload the File
1. Navigate to **📥 Bulk Import** from the sidebar
2. Click on the file uploader
3. Select your Excel (.xlsx, .xls) or CSV (.csv) file
4. For Excel files, select the appropriate sheet

#### 3. Map Columns
The system will show you a preview of your data. Map your columns:

**Required Mappings:**
- **Date Column**: Select the column containing session dates
- **Faculty/Speaker Column**: Select the column with faculty names
- **Session/Topic Column**: Select the column with session titles

**Optional Mappings:**
- **Batch Column**: Student batch information
- **Duration Column**: Session duration in hours
- **Honorarium Column**: Payment amount
- **Feedback Columns**: System auto-detects feedback columns

#### 4. Import Sessions
1. Click **"Import Sessions"** button
2. Watch the progress bar
3. Review the import summary:
   - Total sessions imported
   - Rows skipped (invalid data)
   - New faculties created

### Auto-Faculty Creation

When a faculty name in your import file doesn't exist in the database:

**What the system does:**
- Creates a new faculty profile automatically
- Sets Name from your import file
- Sets Gender to "Other" (default)
- Generates email: `[name]@faculty.edu`
- Adds biodata: "Auto-created from bulk import"
- Tracks who created it (your username)

**What you should do after import:**
1. Go to **Manage Faculties**
2. Find auto-created faculties
3. Edit to add correct:
   - Gender
   - Email address
   - Batch information
   - Biodata

### Feedback Score Normalization

The system automatically handles different feedback scales:

| Your Scale | System Converts To |
|------------|-------------------|
| 0-5 | 0-10 (multiplied by 2) |
| 0-10 | 0-10 (no change) |

**Example:**
- Your file has score: 4.5 (on 0-5 scale)
- System converts to: 9.0 (on 0-10 scale)

### Common Issues

**Issue**: Import shows "0 sessions imported"
- **Solution**: Check that Date, Faculty, and Topic columns are mapped correctly

**Issue**: "Skipped X rows"
- **Solution**: These rows have missing required data (date, faculty, or topic)

**Issue**: Too many auto-created faculties
- **Solution**: Ensure faculty names in your Excel match existing faculty names exactly (including spacing and spelling)

---

## 🔍 Advanced Filtering

### Overview
Filter sessions using multiple criteria and export the results to Excel.

### Step-by-Step Guide

#### 1. Access Advanced Filter
Navigate to **🔍 Advanced Filter** from the sidebar

#### 2. Set Filter Criteria

**Date Range:**
- **From Date**: Start of date range (optional)
- **To Date**: End of date range (optional)
- Leave blank to include all dates

**Faculty & Batch:**
- **Faculty**: Select specific faculty or "All"
- **Batch**: Select specific batch or "All"
- Batch filter uses partial matching (e.g., "2024" matches "MBA 2024")

**Honorarium Range:**
- **Min Honorarium**: Minimum amount (default: 0)
- **Max Honorarium**: Maximum amount (default: 100,000)
- Set to 0 and 100,000 to include all

**Feedback Score:**
- **Min Avg Feedback Score**: Minimum average score (0-10 scale)
- Use slider to set threshold
- Only sessions with avg feedback ≥ this value will be shown

#### 3. Apply Filters
Click **"Apply Filters"** button

#### 4. View Results

The results show:
- **Session Count**: Number of matching sessions
- **Data Table**: All matching sessions with details
- **Statistics Cards**:
  - Total sessions
  - Total honorarium
  - Average honorarium
  - Average feedback score

#### 5. Export Filtered Results
Click **"📥 Download as Excel"** to export the filtered results

### Use Cases

**Find high-performing sessions:**
```
- Min Avg Feedback Score: 8.5
- All other filters: default
```

**Budget analysis for a specific period:**
```
- From Date: 2024-01-01
- To Date: 2024-12-31
- Min Honorarium: 5000
```

**Faculty performance review:**
```
- Faculty: Select specific faculty
- All other filters: default
```

**Batch-specific sessions:**
```
- Batch: Enter batch name (e.g., "2024")
- All other filters: default
```

---

## 📅 Calendar View

### Overview
Visual monthly calendar showing all sessions at a glance.

### Step-by-Step Guide

#### 1. Access Calendar
Navigate to **📅 Calendar View** from the sidebar

#### 2. Select Month and Year
- **Year Dropdown**: Select year (current year ± 2 years)
- **Month Dropdown**: Select month (January - December)

#### 3. View Calendar

**Calendar Grid:**
- Days with sessions are highlighted in **blue**
- Session count is shown: "📚 X session(s)"
- Empty days show just the date number

**Below Calendar:**
- All sessions for the month are listed by date
- Click on any session to expand details
- Click **"View Details"** to see full session information

### Use Cases

**Planning future sessions:**
- Check which days already have sessions
- Avoid scheduling conflicts
- Balance session distribution across the month

**Monthly review:**
- See all sessions at a glance
- Quickly identify busy periods
- Review session frequency

**Quick access:**
- Find sessions by date
- Navigate to session details
- View faculty assignments for the month

---

## 👤 User Profile Management

### Overview
Manage your account information and change your password.

### Step-by-Step Guide

#### 1. Access Profile
Click **👤 Profile** from the sidebar

#### 2. Update Profile Information

**Edit Profile:**
1. Enter new **Full Name**
2. Enter new **Email** (must include @)
3. Click **"Update Profile"**
4. See success message

**Account Information Shown:**
- Username (cannot be changed)
- Role (User or Admin)

#### 3. Change Password

**Security Note**: Always use a strong password (min 6 characters)

**Steps:**
1. Enter your **Current Password**
2. Enter your **New Password**
3. Enter **Confirm New Password** (must match)
4. Click **"Change Password"**

**Requirements:**
- Current password must be correct
- New password must be at least 6 characters
- New password and confirmation must match

### Common Issues

**Issue**: "Current password is incorrect"
- **Solution**: Double-check your current password. If you've forgotten it, logout and use "Forgot Password"

**Issue**: "New passwords do not match"
- **Solution**: Ensure both password fields have identical text

**Issue**: Profile update fails
- **Solution**: Ensure email is valid (contains @)

---

## 🔑 Password Reset

### Overview
Reset your password if you've forgotten it or want to change it without logging in.

### Method 1: Forgot Password (Not Logged In)

#### Step-by-Step:
1. On login page, click **"Forgot Password?"**
2. Enter your **Username**
3. Enter your registered **Email**
4. Click **"Request Password Reset"**
5. If username and email match, you'll be redirected to reset page
6. Enter your **New Password**
7. Enter **Confirm New Password**
8. Click **"Reset Password"**
9. Login with your new password

### Method 2: Change Password (Logged In)

See [User Profile Management](#user-profile-management) section above.

### Security Notes

- Password reset requires both username AND registered email
- Passwords are hashed and cannot be recovered (only reset)
- Always use a unique, strong password
- Change your password regularly
- Don't share your password with anyone

### Common Issues

**Issue**: "Invalid username or email"
- **Solution**: 
  - Check spelling of username
  - Ensure email matches the one you registered with
  - Contact admin if you can't remember your email

**Issue**: Reset page doesn't load
- **Solution**: Make sure username and email match exactly before clicking "Request Password Reset"

---

## 📊 Excel Export

### Overview
Export your data to professional Excel format for analysis, backup, or sharing.

### Available Exports

#### 1. Export All Faculties
**Location**: Manage Faculties → View/Edit Faculties tab

**Includes:**
- Faculty ID
- Name
- Gender  
- Email
- Batch
- Biodata
- Created By
- Created At

**How to Export:**
1. Go to **👥 Manage Faculties**
2. Click **View/Edit Faculties** tab
3. Click **"📥 Export All to Excel"**
4. File downloads as: `faculties_YYYYMMDD.xlsx`

#### 2. Export All Sessions
**Location**: Manage Sessions → View/Edit Sessions tab

**Includes:**
- Session ID
- Date
- Session Name
- Faculty
- Batch
- Duration
- Honorarium
- All 10 feedback scores
- Recommendation text
- Created By
- Created At

**How to Export:**
1. Go to **📚 Manage Sessions**
2. Click **View/Edit Sessions** tab
3. Click **"📥 Export All to Excel"**
4. File downloads as: `sessions_YYYYMMDD.xlsx`

#### 3. Export Filtered Sessions
**Location**: Advanced Filter page

**Includes:**
- All session data matching your filter criteria
- Summary statistics

**How to Export:**
1. Go to **🔍 Advanced Filter**
2. Set your filter criteria
3. Click **"Apply Filters"**
4. Click **"📥 Download as Excel"**
5. File downloads as: `filtered_sessions_YYYYMMDD.xlsx`

#### 4. Export Faculty-Specific Sessions
**Location**: Faculty Sessions view

**Includes:**
- All sessions for a specific faculty
- Session dates, names, batches
- Duration and honorarium

**How to Export:**
1. Go to **👥 Manage Faculties**
2. Click **🔍 Search Faculty** tab
3. Find your faculty
4. Click **"View Sessions"**
5. Click **"📥 Export to Excel"**
6. File downloads as: `FacultyName_sessions_YYYYMMDD.xlsx`

#### 5. Export Faculty Performance Report
**Location**: Reports → Faculty Performance tab

**Includes:**
- Faculty name, email
- Total sessions, duration
- Total honorarium
- Average feedback score

**How to Export:**
1. Go to **📈 Reports**
2. Click **Faculty Performance** tab
3. Click **"📥 Download Report (Excel)"**
4. File downloads as: `faculty_performance_YYYYMMDD.xlsx`

### Excel File Format

All exported Excel files feature:
- **Professional formatting**: Clean, readable layout
- **Column headers**: Clear, descriptive names
- **Data types**: Proper formatting for dates, numbers, text
- **No index column**: Clean data without row numbers
- **Timestamp**: Filename includes export date

### Use Cases

**Data Analysis:**
- Open in Excel, Google Sheets, or other tools
- Create pivot tables
- Generate charts and graphs
- Perform calculations

**Reporting:**
- Share with management
- Include in presentations
- Create reports for stakeholders

**Backup:**
- Regular exports for data safety
- Archive historical data
- Migrate to another system

**Bulk Editing:**
- Export, edit in Excel
- Re-import using Bulk Import feature
- Update multiple records at once

### Tips

**For Best Results:**
1. Export regularly for backup
2. Use descriptive filter criteria for focused exports
3. Keep exports organized by date
4. Use filtered exports for specific analysis
5. Combine multiple exports for comprehensive reporting

**File Organization:**
```
My Documents/
  Faculty Management/
    Exports/
      Faculties/
        faculties_20260213.xlsx
      Sessions/
        sessions_20260213.xlsx
        filtered_sessions_20260213.xlsx
      Reports/
        faculty_performance_20260213.xlsx
```

---

## 🎯 Quick Reference Card

### Bulk Import
1. 📥 Bulk Import
2. Upload file
3. Map columns
4. Import ✅

### Advanced Filter
1. 🔍 Advanced Filter
2. Set criteria
3. Apply
4. Export ✅

### Calendar View
1. 📅 Calendar View
2. Select month/year
3. View sessions
4. Click for details

### Profile
1. 👤 Profile
2. Update info
3. Change password
4. Save ✅

### Excel Export
1. Find export button
2. Click 📥
3. Download file ✅

---

**Need more help?** Check the main README.md or contact your system administrator.

**Version**: 2.0.0  
**Last Updated**: February 2026
