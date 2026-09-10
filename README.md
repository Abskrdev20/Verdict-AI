# Verdict.ai ⚖️🤖

> An automated, production-ready Automated Short Answer Grading (ASAG) platform powered by Scikit-learn and Google Gemini Vision.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-RandomForest-orange)
![Gemini AI](https://img.shields.io/badge/Google-Gemini_API-purple)

---

## 🚀 Overview
**Verdict.ai** is an intelligent web application designed to grade handwritten student short answers against a master reference rubric. By combining computer vision OCR (Gemini Vision) with classical machine learning (Random Forest classification over TF-IDF vectors, length ratios, and keyword overlap density), the system automates granular, question-by-question academic evaluations.

---

## 🛠️ Tech Stack & Architecture
The project follows a clean, highly modular architecture to maximize maintainability and scalability:

* **Frontend:** Streamlit (Custom UI layouts & state controls)
* **OCR Service:** Google GenAI SDK (`gemini-3.7-flash`) with exponential backoff fault tolerance
* **ML Engine:** Scikit-learn (`RandomForestClassifier`), `TfidfVectorizer`, and `NLTK` (Snowball Stemming)
* **Project Structure:**
  ```text
  Verdict-AI/
  ├── app.py                # Main execution entry point
  ├── modules/              # Core business logic packages
  │   ├── config.py         # Global variables & static texts
  │   ├── ml_engine.py      # Feature extraction & Random Forest pipeline
  │   ├── ocr_service.py    # Gemini API wrapper with retry logic
  │   ├── ui_components.py  # Modular Streamlit view blocks
  │   └── utils.py          # Helpers (Text parsing, styling, charting)
  ├── Training_Dataset/     # Reference dataset (`train.csv`)
  └── requirements.txt      # Project dependencies

## ✨ Key Features
* Granular Question Tagging: Dynamically parses assignments using (Q1), (Q2) tags to score individual questions independently.

* Robust NLP Pipeline: Bypasses stop-word deletion to preserve critical student negations (e.g., "not" vs. "is"), safeguarded against empty vocabulary errors.

* Offline Demo Mode: Allows recruiters and reviewers to test evaluation metrics instantly without hitting cloud API rate limits or incurring latency delays.

* Fault-Resilient OCR: Integrates exponential backoff logic to handle API capacity constraints (503/429 limits) gracefully.

### Step 3: Initialize Git and Push to GitHub
Open your terminal inside the `Verdict-AI` root folder and run these standard commands to upload your project:

```bash
git git clone https://github.com/Abskrdev20/Verdict-AI.git
cd Verdict-AI
pip install -r requirements.txt
streamlit run app.py
```

## 👨‍💻 Author
Developed by Abhishek Kumar