"""Pure helper functions that do not render major UI blocks."""

import re
import matplotlib.pyplot as plt
import streamlit as st

def apply_custom_css():
    st.markdown(
        """
        <style>
        h1, h2, h3 { text-align: left; }
        .stCaption, p { text-align: left; }
        div[data-testid="stImage"] { display: flex; justify-content: center; margin: auto; }
        div[data-testid="stMetric"] { background-color: rgba(28, 131, 246, 0.05); border: 1px solid rgba(28, 131, 246, 0.2); padding: 15px; border-radius: 10px; text-align: center; }
        div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] { display: flex; justify-content: center; text-align: center; }
        div[data-testid="stToggle"] { background: transparent !important; display: flex; justify-content: center; }
        </style>
        """,
        unsafe_allow_html=True
    )

def parse_questions(text):
    pattern = r'\(Q(\d+)\)'
    splits = re.split(pattern, text)
    if len(splits) <= 1:
        return {"Overall": text.strip()} if text.strip() else {}
    return {f"Q{splits[i]}": splits[i+1].strip() for i in range(1, len(splits), 2) if splits[i+1].strip()}

def plot_score_chart(score):
    fig, ax = plt.subplots(figsize=(6, 2.2))
    bars = ax.barh(['Passing Target', 'Student Score'], [75.0, score], 
                   color=['#ff9999', '#4caf50' if score >= 75 else '#ff9800'], height=0.45)
    ax.set_xlim(0, 100)
    ax.set_xlabel('Percentage (%)')
    ax.set_title('Performance Benchmark Comparison', fontsize=11, fontweight='bold')
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1.5, bar.get_y() + bar.get_height()/2, f'{width}%', 
                va='center', ha='left', fontsize=9, fontweight='bold')
    plt.tight_layout()
    return fig