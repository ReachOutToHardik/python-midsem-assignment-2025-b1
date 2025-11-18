# Smart Attendance Analyzer

<div align="center">

## MID-SEMESTER ASSIGNMENT

### Bachelor of Computer Applications (BCA)
### 3rd Semester

**Submitted by:**  
Hardik Joshi [243501062]

**Submitted to:**  
Poja Mam
Department of Computer Applications

**Academic Year:** 2025-26  
**Date of Submission:** November 18, 2025

</div>

---

## Project Overview

The **Smart Attendance Analyzer** is a menu-driven terminal application designed to manage and analyze student attendance records efficiently. It provides comprehensive attendance tracking, statistical analysis, and visualization capabilities.

## Features

- **Record Management**: Add and store attendance records in CSV format
- **Data Validation**: Automatic data cleaning and validation
- **Deduplication**: Remove duplicate attendance entries
- **Statistical Analysis**: Calculate attendance percentages for individual students
- **Defaulter Identification**: Automatically identify students with attendance below 75%
- **Visual Reports**: Generate graphical charts for attendance analysis
  - Top students by attendance percentage
  - Daily attendance rate trends
- **Sample Data Generation**: Built-in demo data generator for testing

## Technical Specifications

- **Language**: Python 3
- **Data Storage**: CSV file format
- **Visualization**: Matplotlib library
- **File Structure**:
  - `attendance_analyzer.py` - Main application
  - `data/attendance.csv` - Attendance records
  - `data/top_students.png` - Generated chart
  - `data/daily_rate.png` - Generated chart

## How to Run

```bash
python attendance_analyzer.py
```

## Menu Options

1. **Add Record** - Enter new attendance entry
2. **Analyze & Show Summary** - View statistics and generate charts
3. **Save Cleaned Data** - Remove duplicates and save
4. **Generate Sample Data** - Create demo records for testing
5. **Exit** - Close the application

## Data Format

Attendance records are stored with the following fields:
- Student ID
- Student Name
- Date (YYYY-MM-DD)
- Status (P=Present, A=Absent, L=Leave, H=Holiday)

## Analysis Capabilities

- Individual student attendance percentage
- Present/Total days calculation
- Identification of students below 75% attendance threshold
- Daily attendance rate tracking
- Visual representation of attendance patterns

---

<div align="center">

**END OF DOCUMENT**

</div>
