import re
import pandas as pd
import numpy as np
import streamlit as st
from nltk.stem import SnowballStemmer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .config import DATASET_PATH

# Initialize Stemmer
stemmer = SnowballStemmer("english")

def normalize_text(text):
    """Lowercases, strips punctuation, and stems words to root form."""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = [stemmer.stem(w) for w in text.split()]
    return " ".join(words)

def extract_features(student_text, reference_text):
    """Extracts features for live inference using stemmed tokens with empty vocabulary protection."""
    norm_student = normalize_text(student_text)
    norm_reference = normalize_text(reference_text)
    
    if not norm_student.strip() or not norm_reference.strip():
        return [0.0, 0.0, 0.0, 0.0]
        
    try:
        # No stop words used to preserve full sentence context
        vectorizer = TfidfVectorizer()
        cleaned_docs = [norm_student, norm_reference]
        if all(not doc.strip() for doc in cleaned_docs):
            return [0.0, 0.0, 0.0, 0.0]
            
        vectors = vectorizer.fit_transform(cleaned_docs)
        sim_score = cosine_similarity(vectors[0], vectors[1])[0][0]
        
        s_words = len(student_text.split())
        r_words = len(reference_text.split())
        length_ratio = min(s_words / max(r_words, 1), 2.0)
        
        unique_ratio = len(set(norm_student.split())) / max(s_words, 1)
        
        ref_words = set(norm_reference.split())
        stud_words = set(norm_student.split())
        overlap = len(ref_words.intersection(stud_words)) / max(len(ref_words), 1)
        
        return [sim_score, length_ratio, unique_ratio, overlap]
    except ValueError:
        return [0.0, 0.0, 0.0, 0.0]
    except Exception:
        return [0.0, 0.0, 0.0, 0.0]

@st.cache_resource
def train_model_from_dataset():
    """Loads raw dataset, maps columns, converts marks to letter grades, and trains Random Forest."""
    try:
        df = pd.read_csv(DATASET_PATH)
        X_features = []
        y_labels = []

        for _, row in df.iterrows():
            raw_student = str(row['student_answer'])
            raw_reference = str(row['model_answer'])
            
            try:
                pct = (float(row['teacher_marks']) / float(row['total_marks'])) * 100
                if pct >= 85: grade_label = 'A'
                elif pct >= 70: grade_label = 'B'
                elif pct >= 50: grade_label = 'C'
                elif pct >= 35: grade_label = 'D'
                else: grade_label = 'F'
            except Exception:
                grade_label = 'C'

            if not raw_student.strip() or not raw_reference.strip():
                continue

            norm_student = normalize_text(raw_student)
            norm_reference = normalize_text(raw_reference)

            if not norm_student.strip() or not norm_reference.strip():
                continue

            # Feature Extraction safely guarded against ValueError
            try:
                vectorizer = TfidfVectorizer()
                vectors = vectorizer.fit_transform([norm_student, norm_reference])
                sim_score = cosine_similarity(vectors[0], vectors[1])[0][0]
            except ValueError:
                sim_score = 0.0

            s_words = len(raw_student.split())
            r_words = len(raw_reference.split())
            length_ratio = min(s_words / max(r_words, 1), 2.0)

            unique_ratio = len(set(norm_student.split())) / max(s_words, 1)

            ref_words = set(norm_reference.split())
            stud_words = set(norm_student.split())
            overlap = len(ref_words.intersection(stud_words)) / max(len(ref_words), 1)

            X_features.append([sim_score, length_ratio, unique_ratio, overlap])
            y_labels.append(grade_label)

        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(np.array(X_features), np.array(y_labels))
        return clf, f"Model Trained on {len(X_features)} rows!"

    except FileNotFoundError:
        fallback_clf = RandomForestClassifier(n_estimators=10, random_state=42)
        X_mock = np.array([[0.9, 0.95, 0.6, 0.8], [0.2, 0.3, 0.2, 0.1]])
        y_mock = np.array(["A", "F"])
        fallback_clf.fit(X_mock, y_mock)
        return fallback_clf, "⚠️ Using Fallback Model (Dataset missing)"