# 🎓 Scholarship Eligibility Prediction System

A machine learning-powered web application that predicts scholarship eligibility for Indian students and recommends relevant government scholarship schemes with estimated award amounts.

---

## 📌 Overview

Educational institutions receive thousands of scholarship applications every year. Manual verification of academic marks, family income, attendance, and category is slow, error-prone, and often results in deserving students being overlooked.

This system uses a trained machine learning model to:
- **Predict** whether a student is Eligible or Not Eligible
- **Score** the prediction with a confidence percentage
- **Recommend** specific Indian scholarship schemes (UGC, AICTE, NSP) the student qualifies for
- **Visualize** eligibility trends through an interactive dashboard

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 ML-based Prediction | Random Forest classifier with ~92% accuracy |
| 📊 Eligibility Score | Probability-based confidence (0–100%) |
| 🎯 Scholarship Recommendation | Matches profile against 14 Indian schemes |
| 💰 Award Estimation | Total potential award amount per year |
| 📈 Interactive Dashboard | 5 Plotly charts showing eligibility trends |
| 💾 MySQL Database | Saves every prediction for audit and history |
| 📜 History Page | View all past predictions with names |
| 🔧 Admin Panel | Aggregate stats (total, eligible %, avg score) |
| 🖨️ Print/PDF Export | Save individual results |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10**
- **Flask 3.1** — Web framework
- **Scikit-learn** — Machine learning
- **Pandas, NumPy** — Data processing
- **MySQL 8.0** — Database
- **mysql-connector-python** — DB driver

### Frontend
- **HTML5, CSS3**
- **Bootstrap 5** — UI framework
- **Plotly.js** — Interactive charts
- **Jinja2** — Template engine

### ML Model
- **Algorithm:** Random Forest Classifier
- **Features:** age, gender, category, disability, education, marks, attendance, income
- **Target:** eligible (Yes/No)
- **Accuracy:** ~92%

---

## 📁 Project Structure
Project-MCA/
├── app.py
├── requirements.txt
├── README.md
├── data/
├── models/
├── scripts/
├── templates/
├── static/
└── docs/

---

## 🚀 Quick Start

### 1. Install dependencies
pip install -r requirements.txt

### 2. Setup MySQL database
Update `scripts/setup_database.py` and `scripts/db.py` with your MySQL password, then run:
python scripts/setup_database.py

### 3. Run the Flask app
python app.py

### 4. Open in browser
http://127.0.0.1:5000

---

## 📊 Model Performance

| Model | Accuracy | F1 Score |
|-------|----------|----------|
| **Random Forest** | **91.75%** | **91.77%** |
| Decision Tree | 90.75% | 90.82% |
| SVM | 85.00% | 85.44% |
| Logistic Regression | 82.50% | 82.93% |

---

## 🎓 Scholarship Schemes Included

- National Scholarship for Post Graduate Studies (UGC/NSP)
- PG Scholarship for Professional Courses – SC/ST (UGC)
- PG Indira Gandhi Scholarship for Single Girl Child (UGC)
- PG Scholarship for University Rank Holders (UGC)
- AICTE Pragati Scholarship
- AICTE Saksham Scholarship
- PM-USP Central Sector Scholarship
- PM YASASVI – Top Class Education
- Post-Matric Scholarship for Students with Disabilities
- Central Sector Scholarship – Top Class Education for SC/ST

---

## 🔮 Future Enhancements

- OCR-based document verification
- Live NSP/UGC/AICTE API integration
- Multi-language support
- Mobile app
- Explainable AI

---

## 📄 License

Academic project (MCA final year).

---

## 👤 Author

Prateek Veeresh Aggimath
MCA Student
Acharya Institute of Technology
prateekvaggimath@gmail.com

## 🌐 Live Demo

**URL:** https://scholarship-eligibility-prediction-system.onrender.com

> ⚠️ **Note:** The app runs on Render's free tier. First load after inactivity takes 30–60 seconds.

### Pages
- **Home** — Check a student's eligibility
- **Scholarships** — Browse all 14 schemes
- **Dashboard** — Analytics charts
- **History** — Past predictions
- **Admin** — Aggregate stats
- **About** — System information