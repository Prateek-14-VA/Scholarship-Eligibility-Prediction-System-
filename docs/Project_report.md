# Scholarship Eligibility Prediction System
## Project Report

**Submitted by:** Prateek Veeresh Aggimath
**Course:** Master of Computer Applications (MCA)
**College:** Acharya Institute of Technology
**Year:** 2025–2026
**Email:** prateekvaggimath@gmail.com

---

## 1. Abstract

Scholarships provide vital financial assistance to deserving students, enabling them to continue their education without interruption. Educational institutions and government bodies receive a large volume of scholarship applications every year, and manually verifying each applicant's academic performance, family income, attendance, and category details is a slow and error-prone process.

The Scholarship Eligibility Prediction System addresses this challenge by using machine learning to analyze student information and predict scholarship eligibility. By learning patterns from historical application data, the system classifies students as **Eligible** or **Not Eligible** and generates a probability-based eligibility score.

In addition, the system recommends specific Indian scholarship portals (UGC, AICTE, NSP) for which the candidate qualifies, along with the estimated award amount. The predictions, recommendations, and supporting analytics are presented through an interactive web dashboard.

---

## 2. Introduction

Scholarships play a crucial role in supporting students who cannot fully bear the cost of their education. Eligibility is typically determined by academic performance, family income, attendance percentage, and category-based reservation criteria.

Every year, schools, colleges, and government agencies receive thousands of applications. The conventional approach of collecting forms, verifying mark sheets and income certificates, checking attendance records, and cross-referencing against eligibility rules consumes significant time and effort.

Machine learning offers an effective solution by learning patterns from historical data. This system uses a trained classification model to predict eligibility and assign a confidence score. It then maps the student's profile against a curated database of Indian scholarship schemes (UGC, AICTE, NSP) to recommend the exact scholarships the student qualifies for.

---

## 3. Problem Statement

Educational institutions face several challenges in scholarship evaluation:

- Manual verification is slow and labor-intensive
- Delayed decisions cause students to miss application windows
- Inconsistent evaluations due to human error
- Rule-based systems cannot capture complex eligibility patterns
- No recommendation for students to identify which schemes they qualify for
- No analytics for institutions to understand eligibility trends

There is a clear need for a system that can:
- Accurately evaluate student information
- Classify applicants as Eligible or Not Eligible
- Generate a quantifiable eligibility score
- Recommend relevant Indian scholarship portals with award amounts
- Present data through meaningful visualizations

---

## 4. Objectives

1. Develop a machine learning-based system that analyzes student information such as academic marks, family income, attendance, and category criteria to predict scholarship eligibility accurately.
2. Automate the scholarship evaluation process by classifying students and generating a probability-based eligibility score.
3. Build an interactive web-based dashboard that displays eligibility predictions and analytics through charts and graphs.
4. Recommend specific Indian scholarship portals (UGC, AICTE, NSP, central/state schemes) along with the estimated award amount.
5. Store every prediction in a database for audit, history, and administrative review.

---

## 5. Methodology

### 5.1 Data Collection

Generated a synthetic dataset of 2000 student records with realistic distributions:
- **Age:** 17–30
- **Gender:** Male / Female / Other
- **Category:** General, OBC, SC, ST, EWS, Minority
- **Disability:** Yes / No
- **Education:** UG, PG, Technical, Professional
- **Marks:** 35–100 (with 2% missing values)
- **Attendance:** 40–100 (with 2% missing values)
- **Income:** ₹30,000–₹15,00,000
- **Target (eligible):** Yes / No (49.1% / 50.9% balanced)

Rules were derived from actual Indian scholarship schemes (NSP, UGC, AICTE, Post-Matric).

### 5.2 Data Preprocessing

- Filled missing values with median (marks, attendance)
- Encoded categorical variables using one-hot encoding
- Scaled numeric features with StandardScaler
- Split into train (80%) and test (20%) with stratification

### 5.3 Exploratory Data Analysis

Generated 7 charts:
1. Eligibility distribution
2. Marks distribution by eligibility
3. Income distribution by eligibility
4. Attendance distribution by eligibility
5. Eligibility by category
6. Eligibility by education level
7. Correlation heatmap

### 5.4 Model Training and Evaluation

Trained 4 classification algorithms:
- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)

Evaluated with accuracy, precision, recall, F1-score, and confusion matrix.

### 5.5 Prediction Pipeline

Built `predict_student()` function that:
- Accepts raw student input
- Encodes and scales features
- Returns eligibility label + probability score (0–100%)

### 5.6 Scholarship Recommendation Engine

Curated a database of 14 Indian scholarship schemes (UGC, AICTE, NSP).
Rule-based matching by: education, category, gender, disability, income, marks.

### 5.7 Web Application

- Flask backend with 7 routes
- 8 HTML templates with Bootstrap 5
- Plotly.js interactive charts
- MySQL database for persistence

---

## 6. System Architecture
User → Browser
↓
Flask App (app.py)
↓
┌────┼────┐
↓ ↓ ↓
predict recommend db
.py .py .py
↓ ↓ ↓
ML scholarship MySQL
Model database
↓ ↓ ↓
└────┼────┘
↓
result.html


---

## 7. Modules

| Module | Purpose |
|--------|---------|
| Student Data Input | Accept 9 fields via HTML form |
| Data Preprocessing | Clean, encode, scale |
| Feature Selection | Identify relevant attributes |
| ML Model | Random Forest prediction |
| Eligibility Prediction | Classify Eligible / Not Eligible |
| Eligibility Score | Confidence percentage |
| Scholarship Recommendation | Match profile against schemes |
| Student Analytics | Charts and trends |
| Dashboard | Visual presentation |
| History | View past predictions |
| Admin Panel | Aggregate statistics |
| Database | MySQL persistence |

---

## 8. Results

### 8.1 Model Performance

| Model | Accuracy | Precision | Recall | F1 Score |
|-------|----------|-----------|--------|----------|
| **Random Forest** | **91.75%** | 89.76% | 93.88% | **91.77%** |
| Decision Tree | 90.75% | 88.41% | 93.37% | 90.82% |
| SVM | 85.00% | 81.48% | 89.80% | 85.44% |
| Logistic Regression | 82.50% | 79.44% | 86.73% | 82.93% |

**Best model:** Random Forest with 91.77% F1 score.

### 8.2 Sample Prediction

**Student:** Priya Sharma, 24, Female, SC, No disability, Professional
**Marks:** 75% | **Attendance:** 85% | **Income:** ₹2,00,000

**Output:**
- Eligibility: **Eligible**
- Score: **91.66%**
- Recommended Scholarships: 2
- Total Award: **₹1,08,000/year**

---

## 9. Tools and Technologies

- **Programming Language:** Python 3.10
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Algorithms:** Logistic Regression, Decision Tree, Random Forest, SVM
- **Web Framework:** Flask
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Charts:** Plotly, Matplotlib
- **Database:** MySQL 8.0
- **IDE:** Visual Studio Code
- **Version Control:** Git, GitHub

---

## 10. Expected Outcome

The expected outcome is a fully functional Scholarship Eligibility Prediction Portal that:
- Evaluates student information using machine learning
- Classifies each applicant as Eligible or Not Eligible
- Generates a confidence score
- Recommends specific Indian scholarship schemes with award amounts
- Presents results through an interactive dashboard
- Saves every prediction to a database for audit
- Reduces manual effort and evaluation errors
- Makes scholarship selection faster, fairer, and more transparent

---

## 11. Scope and Future Enhancements

- **Database Integration:** Connect to college databases for automatic record retrieval
- **Automated Document Verification:** OCR for income certificates and mark sheets
- **Explainable AI:** Show feature importance per prediction
- **Mobile Application:** Android/iOS app for students
- **Live Portal Integration:** NSP/UGC/AICTE APIs for real-time updates
- **Multi-Language Support:** Interface in regional languages
- **Email/SMS Notifications:** Alert students when new schemes match

---

## 12. Conclusion

The Scholarship Eligibility Prediction System successfully automates scholarship evaluation through machine learning. It predicts eligibility, assigns a confidence score, recommends specific Indian scholarship portals with award amounts, and presents results through an interactive web dashboard.

By automating scholarship evaluation and recommendation, the system reduces administrative workload, minimizes errors, and ensures a fairer selection process. It demonstrates how machine learning and web technologies can be combined to make scholarship distribution more efficient, transparent, and accessible — ultimately helping more deserving students continue their education.

---

## 13. References

1. Pedregosa et al., "Scikit-learn: Machine Learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.
2. L. Breiman, "Random Forests," Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.
3. M. Grinberg, "Flask Web Development: Developing Web Applications with Python," 2nd ed., O'Reilly Media, 2018.
4. W. McKinney, "Data Structures for Statistical Computing in Python," Proceedings of the 9th Python in Science Conference (SciPy), 2010, pp. 56–61.
5. National Scholarship Portal (NSP), Government of India. [Online]. Available: https://scholarships.gov.in
6. University Grants Commission (UGC) Scholarship Schemes. [Online]. Available: https://ugc.gov.in
7. All India Council for Technical Education (AICTE) Scholarships. [Online]. Available: https://aicte-india.org
8. T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," Proceedings of the 22nd ACM SIGKDD, 2016, pp. 785–794.