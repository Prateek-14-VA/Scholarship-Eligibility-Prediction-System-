# User Manual
## Scholarship Eligibility Prediction System

**Author:** Prateek Veeresh Aggimath
**Version:** 1.0
**Date:** 2026

---

## 1. Introduction

The Scholarship Eligibility Prediction System is a web application that helps students and institutions determine scholarship eligibility using machine learning. It also recommends relevant Indian scholarship schemes and shows the total award amount a student can receive.

---

## 2. System Requirements

### For Users (Students / Staff)
- Any modern web browser (Chrome, Firefox, Edge)
- Internet connection (for Bootstrap/Plotly CDN)

### For Administrators (Running the App)
- Python 3.10 or higher
- MySQL 8.0
- Windows / Linux / macOS
- 4 GB RAM minimum

---

## 3. Installation

### Step 1: Install Python Dependencies

Open PowerShell in the project folder:
cd C:\Project-MCA
pip install -r requirements.txt


### Step 2: Setup MySQL Database

1. Start MySQL service
2. Open `scripts/setup_database.py`
3. Update the password in `DB_CONFIG`
4. Run:
python scripts/setup_database.py


### Step 3: Start the Application
python app.py


You should see:
Running on http://127.0.0.1:5000

---

## 4. Using the Application

### 4.1 Home Page

Open your browser and go to:
http://127.0.0.1:5000

You'll see a form with the following fields:

| Field | Description |
|-------|-------------|
| Student Name | Full name |
| Age | Between 15 and 60 |
| Gender | Male / Female / Other |
| Category | General / OBC / SC / ST / EWS / Minority |
| Disability | Yes / No |
| Education Level | UG / PG / Technical / Professional |
| Marks | 0 to 100 |
| Attendance | 0 to 100 |
| Family Income | Annual income in rupees |

### 4.2 Submit the Form

1. Fill in all fields
2. Click **Check Eligibility**
3. Wait for the spinner (analyzing...)
4. You'll be redirected to the result page

### 4.3 Result Page

The result page shows:

1. **Student Profile** — All the entered details
2. **Eligibility Badge** — ✓ Eligible (green) or ✗ Not Eligible (red)
3. **Eligibility Score** — Confidence percentage (0–100%)
4. **Recommended Scholarships** — Table with:
   - Scholarship name
   - Provider (UGC / AICTE / NSP)
   - Award amount
   - Apply link
5. **Total Estimated Award** — Sum of all eligible scholarships
6. **Buttons:**
   - Check Another Student
   - Print / Save as PDF

---

## 5. Navigation

The top navbar has these pages:

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Enter student details |
| Scholarships | `/scholarships` | Browse all 14 schemes |
| Dashboard | `/dashboard` | View analytics charts |
| History | `/history` | See all past predictions |
| Admin | `/admin` | Aggregate statistics |
| About | `/about` | System information |

---

## 6. Dashboard

The dashboard shows:

### Summary Cards
- **Total Students** — Total predictions made
- **Eligible** — Count and percentage
- **Not Eligible** — Count and percentage

### Interactive Charts
1. Eligibility by Category
2. Eligibility by Education Level
3. Marks Distribution
4. Income Brackets
5. Eligibility by Gender

**How to interact:**
- **Hover** — see exact values
- **Click legend** — toggle series
- **Drag** — zoom into a region
- **Camera icon** — download chart as PNG

---

## 7. History Page

The history page lists all past predictions with:
- Name
- Date and time
- Age, gender, category, education
- Marks, income
- Eligibility result (badge)
- Score

Sorted by most recent first.

---

## 8. Admin Panel

The admin panel shows:
- Total predictions
- Eligible count
- Not eligible count
- Average score

Plus quick links to History and Dashboard.

---

## 9. Troubleshooting

| Problem | Solution |
|---------|----------|
| Page not loading | Check Flask is running (`python app.py`) |
| Database error | Start MySQL service, check password in `db.py` |
| Charts blank | Check internet connection (Plotly CDN) |
| Form not submitting | Check all required fields are filled |
| Port 5000 in use | Change port in `app.py` |
| Slow response | First prediction is slow (model loading), later ones are fast |

---

## 10. Stopping the Application

Press `Ctrl + C` in the PowerShell window where Flask is running.

---

## 11. Sample Walkthrough

**Input:**
- Name: Priya Sharma
- Age: 24
- Gender: Female
- Category: SC
- Disability: No
- Education: Professional
- Marks: 75
- Attendance: 85
- Income: 200000

**Expected Output:**
- Eligibility: **Eligible**
- Score: **~91%**
- Scholarships:
  - PG Scholarship for Professional Courses – SC/ST (UGC) — ₹78,000
  - AICTE Pragati Scholarship (AICTE) — ₹30,000
- Total Award: **₹1,08,000/year**

---

## 12. Support

For issues, contact:
**Prateek Veeresh Aggimath**
prateekvaggimath@gmail.com