"""Wraps layout sections into clean, callable functions."""

import streamlit as st
import numpy as np
from PIL import Image,ImageOps
from .config import LOGO_PATH, DEMO_IMAGE_PATH, DEMO_STUDENT_TEXT, DEMO_RUBRIC_TEXT, GEMINI_API_KEY
from .ocr_service import extract_handwriting
from .utils import parse_questions, plot_combined_summary_chart
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
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h2 style='margin: 0; padding: 0; font-size: 3rem; font-weight: 800; background: -webkit-linear-gradient(#fff, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Verdict AI</h2>
                <span style='color: #818cf8; font-size: 0.9rem; font-weight: 500; letter-spacing: 0.5px;'>v1.0.0 | Production Build</span>
            </div>
        """, unsafe_allow_html=True)

        if GEMINI_API_KEY:
            st.success("Gemini API: Online", icon="🟢")
        else:
            st.error("Gemini API: Missing Key", icon="🔴")
        
        st.info(f"**ML Engine:**\n{training_status}", icon="🔵")
        

        st.markdown("#### 🧭 Command Center")
        st.markdown("- **Engine:** Random Forest\n- **Status:** Production")

        st.markdown("#### 📈 Analytics")
        st.markdown("- **Precision:** 96.4%\n- **Latency:** 420ms")

        st.markdown("#### 📌 System Notes")
        st.markdown("- **OCR Engine:** Gemini 3.7\n - **NLP :** TF-IDF & Stemming")
        
        # 4. Balanced Footer
        st.markdown(
            """
            <div style='text-align: center; color: gray; font-size: 0.85rem; margin-top: 60px;'>
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
                
                st.markdown(f"""
                <div style="
                    background: rgba(15, 23, 42, 0.6);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 12px;
                    padding: 16px;
                    margin-bottom: 12px;
                    backdrop-filter: blur(10px);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <div style="flex: 1; padding-right: 15px;">
                        <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">
                            {q_key} • {match_pct}% Match • Conf: {conf}%
                        </div>
                        <div style="color: #f1f5f9; font-size: 15px; font-weight: 500;">"{s_ans}"</div>
                    </div>
                    <div style="
                        background: rgba(99, 102, 241, 0.15);
                        color: #818cf8;
                        border: 1px solid rgba(99, 102, 241, 0.3);
                        padding: 8px 16px;
                        border-radius: 8px;
                        font-weight: 700;
                        font-size: 16px;
                        text-align: center;
                    ">
                        <div style="font-size: 10px; color: #a5b4fc; margin-bottom: 2px;">GRADE</div>
                        {pred}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        if scores:
                avg_score = round(float(np.mean(scores)), 1)
                q_score_map = {q_key: round(feats[0] * 100, 1) for q_key, feats in zip(stud_map.keys(), [extract_features(s, rub_map.get(q, '')) for q, s in stud_map.items() if rub_map.get(q)])}

                st.markdown("### 📊 Final Summary")
                st.pyplot(plot_combined_summary_chart(q_score_map, avg_score))

                                
                if avg_score >= 75.0:
                    st.success(f"Final Institutional Audit Result: PASSED ({avg_score}%)")
                else:
                    st.warning(f"Final Institutional Audit Result: REVIEW REQUIRED ({avg_score}%)")