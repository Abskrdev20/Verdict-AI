"""Pure helper functions that do not render major UI blocks."""

import re
import matplotlib.pyplot as plt
import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            /* 1. Import Premium Google Font */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            /* Force Font Everywhere */
            html, body, [class*="css"], .stMarkdown, .stText {
                font-family: 'Inter', sans-serif !important;
            }

            /* 2. Ultra-Modern Mesh Gradient Background */
            .stApp {
                background-color: #030712;
                background-image: 
                    radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%), 
                    radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
                    radial-gradient(at 50% 100%, rgba(56, 189, 248, 0.1) 0px, transparent 50%);
                background-attachment: fixed;
                color: #f8fafc;
            }

            /* Make the top Streamlit header completely transparent */
            header[data-testid="stHeader"] { 
                background: transparent !important;
                background-color: transparent !important;
                visibility: visible !important;
            }
            
            div[data-testid="stImage"] {
             display: flex; justify-content: center; margin: auto; }

            /* 4. Glassmorphism Sidebar (Apple-style) */
            [data-testid="stSidebar"] {
                background: rgba(10, 15, 30, 0.4) !important;
                backdrop-filter: blur(24px) !important;
                -webkit-backdrop-filter: blur(24px) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
            }

            /* 5. Glowing Magic Primary Button */
            button[kind="primary"] {
                background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
                border-radius: 12px !important;
                box-shadow: 0 4px 20px rgba(124, 58, 237, 0.3) !important;
                color: white !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                letter-spacing: 0.5px !important;
                padding: 0.75rem !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }
            button[kind="primary"]:hover {
                transform: translateY(-3px) scale(1.01) !important;
                box-shadow: 0 10px 25px rgba(124, 58, 237, 0.5) !important;
                border-color: rgba(255,255,255,0.3) !important;
            }

            /* 6. Stunning File Uploader Dropzone */
            [data-testid="stFileUploader"] {
                background: rgba(30, 41, 59, 0.3) !important;
                border: 2px dashed rgba(99, 102, 241, 0.4) !important;
                border-radius: 16px !important;
                padding: 2rem !important;
                backdrop-filter: blur(10px) !important;
                transition: all 0.3s ease !important;
            }
            [data-testid="stFileUploader"]:hover {
                border-color: rgba(99, 102, 241, 0.8) !important;
                background: rgba(99, 102, 241, 0.05) !important;
            }
            
            [data-testid="stFileUploader"] button {
                border-radius: 8px !important;
                background-color: rgba(255,255,255,0.05) !important;
                border: 1px solid rgba(255,255,255,0.1) !important;
            }

            /* 7. Text Areas / Inputs */
            .stTextArea > div > div > textarea {
                background-color: rgba(15, 23, 42, 0.6) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 12px !important;
                color: #e2e8f0 !important;
                padding: 1rem !important;
                font-size: 14px !important;
            }
            .stTextArea > div > div > textarea:focus {
                border-color: #6366f1 !important;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
            }

            /* 8. Container Spacing Fix */
            [data-testid="stVerticalBlock"] > div.element-container {
                margin-bottom: 0.3rem !important;
            }
            
            /* 9. Sleek Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: transparent;
            }
            ::-webkit-scrollbar-thumb {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            /* 10. Metric Cards */
            [data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                border-radius: 16px !important;
                padding: 1.5rem !important;
                backdrop-filter: blur(10px) !important;
            }
        </style>
    """, unsafe_allow_html=True)

def parse_questions(text):
    pattern = r'\(Q(\d+)\)'
    splits = re.split(pattern, text)
    if len(splits) <= 1:
        return {"Overall": text.strip()} if text.strip() else {}
    return {f"Q{splits[i]}": splits[i+1].strip() for i in range(1, len(splits), 2) if splits[i+1].strip()}



def plot_combined_summary_chart(question_scores_dict, overall_avg):
    """
    Generates a chart depicting individual question scores alongside the overall average benchmark.
    """
    questions = list(question_scores_dict.keys())
    scores = list(question_scores_dict.values())

    fig, ax = plt.subplots(figsize=(6, 2.6))
    
    # Color-code individual question bars based on passing status (75%)
    colors = ['#4caf50' if s >= 75.0 else '#f59e0b' for s in scores]
    bars = ax.bar(questions, scores, color=colors, width=0.45, alpha=0.85)
    
    ax.set_ylim(0, 105)
    ax.set_ylabel('Score (%)', fontsize=9, color='#cbd5e1')
    ax.set_title('Question Breakdown & Overall Average', fontsize=10, fontweight='bold', color='#f8fafc', pad=10)
    
    # FIX: Use 'none' instead of 'transparent' for Matplotlib compatibility
    ax.set_facecolor('none')
    fig.patch.set_facecolor('none')
    
    ax.tick_params(colors='#94a3b8', labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#334155')
    ax.spines['bottom'].set_color('#334155')
    
    # Horizontal line representing the overall average benchmark
    ax.axhline(overall_avg, color='#818cf8', linestyle='-', linewidth=1.5, label=f'Overall Average: {overall_avg}%')
    ax.legend(loc='upper right', fontsize=7, facecolor='#0f172a', edgecolor='#334155', labelcolor='#cbd5e1')

    # Data labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2, f'{height}%',
                ha='center', va='bottom', fontsize=8, fontweight='bold', color='#f8fafc')

    plt.tight_layout()
    return fig