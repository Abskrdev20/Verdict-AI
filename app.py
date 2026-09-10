import os
import sys
import warnings
import streamlit as st

# 1. Path Configuration: Bind the root folder so 'modules' resolves correctly as a package
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.utils import apply_custom_css
from modules.ml_engine import train_model_from_dataset
from modules.ui_components import render_header, render_sidebar, render_ocr_section, render_evaluation_section

warnings.filterwarnings("ignore")

# 2. UI Setup
st.set_page_config(
    page_title="Verdict.ai | Assignment Grader", 
    layout="centered",
)
apply_custom_css()

if 'student_text' not in st.session_state:
    st.session_state['student_text'] = ""

# 3. Boot Engine
grading_model, training_status = train_model_from_dataset()

# 4. Render Dashboard
demo_mode = render_header()
render_sidebar(training_status)
render_ocr_section(demo_mode)

# 5. Render Evaluation 
if st.session_state['student_text']:
    render_evaluation_section(grading_model, demo_mode)