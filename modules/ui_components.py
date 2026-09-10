"""Wraps layout sections into clean, callable functions."""

import streamlit as st
import numpy as np
from PIL import Image,ImageOps
from .config import LOGO_PATH, DEMO_IMAGE_PATH, DEMO_STUDENT_TEXT, DEMO_RUBRIC_TEXT, GEMINI_API_KEY
from .ocr_service import extract_handwriting
from .utils import parse_questions, plot_score_chart
from .ml_engine import extract_features
import re

def reset_extracted_text():
    st.session_state['student_text'] = ""

def render_header():
    col_logo, col_text = st.columns([1, 3], vertical_alignment="center")
    with col_logo:
        st.image(LOGO_PATH, width=140)
    with col_text:
        st.markdown(
        """
        <div style="text-align: left;">
        <h1 style="text-align: left; margin-bottom: 0px; padding-bottom: 0px;">Verdict.ai</h1>
        <p style="text-align: left; font-size: 1rem; color: gray; margin-top: 4px;">
        Automated Handwritten Assignment Grading Platform
        </p>
        </div>
        """,
        unsafe_allow_html=True
        )
        return st.toggle("⚡ Offline Demo Mode", value=False, key="demo_toggle", on_change=reset_extracted_text)
        

import streamlit as st
from .config import LOGO_PATH, GEMINI_API_KEY

def render_sidebar(training_status):
    with st.sidebar:
        # 1. Compact Branding
        st.image(LOGO_PATH, width=150)
        st.title("Verdict.ai")
        st.caption("v1.0.0 | Production Build")

        if GEMINI_API_KEY:
            st.success("Gemini API: Online", icon="🟢")
        else:
            st.error("Gemini API: Missing Key", icon="🔴")
        
        st.info(f"**ML Engine:**\n{training_status}", icon="🔵")
        
        # 3. Portfolio Tech Stack
        with st.header("🛠️ Architecture & Tech Stack"):
            st.markdown(
                """
                * **Frontend:** Streamlit
                * **OCR Engine:** Gemini 3.7-flash
                * **ML Classifier:** Scikit-learn (Random Forest)
                * **NLP:** TF-IDF & Stemming
                """
            )
        
        # 4. Balanced Footer (Using controlled top margin instead of hard breaks)
        st.markdown(
            """
            <div style='text-align: center; color: gray; font-size: 0.85rem; margin-top: 40px;'>
                Developed by <b>Abhishek Kumar</b><br>
                Automated ASAG System
            </div>
            """, 
            unsafe_allow_html=True
        )

def render_ocr_section(demo_mode):
    st.subheader("1. Submission & OCR Inspection")
    uploaded_file = st.file_uploader("Upload Handwritten Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file or demo_mode:
        c_img, c_txt = st.columns([1, 1])
        with c_img:
            if demo_mode: 
                demo_img = Image.open(DEMO_IMAGE_PATH)
                demo_img = ImageOps.exif_transpose(demo_img)
                st.image(demo_img, width=350, caption="Demo Mode")
                
            elif uploaded_file: 
                uploaded_img = Image.open(uploaded_file)
                uploaded_img = ImageOps.exif_transpose(uploaded_img)
                st.image(uploaded_img, width=350)


        with c_txt:
            if not demo_mode and st.button("Run OCR Extraction", width="stretch") and uploaded_file:
                with st.spinner("Extracting via Gemini..."):
                    try:
                        st.session_state['student_text'] = extract_handwriting(Image.open(uploaded_file))
                    except Exception as e:
                        err_str = str(e)
                        match = re.search(r'(?:429|503|RESOURCE_EXHAUSTED|OVERLOADED|INVALID_ARGUMENT)[^\.]*', err_str)
                        if match:
                            clean_msg = match.group(0).strip()
                        else:
                            clean_msg = err_str[:60] + "..."
                        st.error(f"OCR Error : { clean_msg}.")


            if demo_mode:
                st.session_state['student_text'] = DEMO_STUDENT_TEXT
                
            if st.session_state['student_text']:
                st.session_state['student_text'] = st.text_area("Extracted Text:", st.session_state['student_text'], height=350)

def render_evaluation_section(model, demo_mode):
    st.divider()
    st.subheader("2. Automated Granular Evaluation")
    reference = st.text_area("Master Rubric (Use (Q1) tags):", DEMO_RUBRIC_TEXT if demo_mode else "", height=150)
    
    if st.button("Evaluate & Grade", width="stretch"):
        if not reference.strip(): return st.error("Provide an answer key.")
        
        with st.spinner("Grading..."):
            stud_map, rub_map = parse_questions(st.session_state['student_text']), parse_questions(reference)
            scores = []
            
            for q_key, s_ans in stud_map.items():
                r_ans = rub_map.get(q_key, "")
                if not r_ans: continue
                
                feats = extract_features(s_ans, r_ans)
                match_pct = round(feats[0] * 100, 1)
                scores.append(match_pct)
                pred, conf = model.predict([feats])[0], round(np.max(model.predict_proba([feats])[0]) * 100, 1)
                
                st.markdown(f"#### 📌 `{q_key}`")
                c1, c2, c3 = st.columns(3)
                c1.metric("Match", f"{match_pct}%")
                c2.metric("Grade", pred)
                c3.metric("Confidence", f"{conf}%")
                st.divider()
                
            if scores:
                st.markdown("### 📊 Final Summary")
                st.pyplot(plot_score_chart(round(float(np.mean(scores)), 1)))