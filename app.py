import streamlit as st
import pandas as pd
import spacy
import plotly.express as px

# 1. UI Configuration (Must be first)
st.set_page_config(page_title="JD Decoder", layout="wide", page_icon="🔍", initial_sidebar_state="expanded")

# 2. Ultra-Modern Styling with Advanced Effects
st.markdown("""
    <style>
    /* Root Variables */
    :root {
        --primary: #0066ff;
        --secondary: #00d9ff;
        --dark: #0a0e27;
        --light: #f8f9fa;
        --success: #00d084;
        --warning: #ffa500;
    }
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(-45deg, #0a0e27, #1a1f4b, #0f0f2e, #1a0a3e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: white;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main title with enhanced gradient */
    .main-title {
        background: linear-gradient(90deg, #00d9ff 0%, #0066ff 25%, #00d9ff 50%, #0066ff 75%, #00d9ff 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5em;
        font-weight: 900;
        margin-bottom: 15px;
        letter-spacing: -2px;
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    /* Subtitle styling */
    .subtitle {
        color: #a0d9ff !important;
        font-size: 1.1em;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* Advanced Glassmorphic card */
    .card {
        background: rgba(20, 30, 80, 0.4);
        border: 2px solid rgba(0, 217, 255, 0.2);
        border-radius: 20px;
        padding: 28px;
        backdrop-filter: blur(20px) saturate(180%);
        margin: 20px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37), 
                    inset 0 0 20px rgba(0, 217, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .card:hover {
        border-color: rgba(0, 217, 255, 0.5);
        box-shadow: 0 12px 48px 0 rgba(0, 217, 255, 0.2),
                    inset 0 0 30px rgba(0, 217, 255, 0.08);
        transform: translateY(-5px);
    }
    
    .card:hover::before {
        left: 100%;
    }
    
    /* Text styling */
    .stMarkdown p, .stMarkdown span, .stMarkdown li {
        color: #e8ecf1 !important;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Sidebar styling with gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(26, 31, 75, 0.95) 0%, rgba(15, 15, 46, 0.95) 100%);
        border-right: 2px solid rgba(0, 217, 255, 0.15);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #00d9ff !important;
        font-weight: 800;
        font-size: 1.3em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] .stMarkdown span {
        color: #c5cfe0 !important;
        font-size: 0.95em;
    }
    
    /* Enhanced Textarea */
    .stTextArea textarea {
        background: rgba(15, 25, 70, 0.6) !important;
        border: 2px solid rgba(0, 217, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #e8ecf1 !important;
        font-size: 15px !important;
        padding: 16px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(165, 180, 210, 0.6) !important;
    }
    
    .stTextArea textarea:focus {
        border: 2px solid #00d9ff !important;
        box-shadow: 0 0 30px rgba(0, 217, 255, 0.3),
                    inset 0 0 20px rgba(0, 217, 255, 0.05) !important;
        background: rgba(15, 25, 70, 0.8) !important;
    }
    
    /* Premium button with advanced effects */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0066ff 0%, #00d9ff 100%);
        color: white !important;
        border-radius: 12px;
        border: none;
        padding: 14px 40px;
        font-weight: 700;
        font-size: 1.1em;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(0, 102, 255, 0.5),
                    0 0 20px rgba(0, 217, 255, 0.2);
        width: 100%;
        position: relative;
        overflow: hidden;
        letter-spacing: 0.5px;
    }
    
    div.stButton > button:first-child::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    div.stButton > button:first-child:hover {
        box-shadow: 0 10px 35px rgba(0, 102, 255, 0.6),
                    0 0 30px rgba(0, 217, 255, 0.3);
        transform: translateY(-3px);
    }
    
    div.stButton > button:first-child:hover::before {
        left: 100%;
    }
    
    div.stButton > button:first-child:active {
        transform: translateY(-1px);
    }
    
    /* Success box enhanced */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 208, 132, 0.15) 0%, rgba(0, 255, 150, 0.08) 100%) !important;
        border: 2px solid rgba(0, 208, 132, 0.4) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 24px rgba(0, 208, 132, 0.15) !important;
        padding: 20px !important;
    }
    
    .stSuccess p {
        color: #00ff9e !important;
        font-weight: 600;
    }
    
    /* Warning box enhanced */
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 165, 0, 0.15) 0%, rgba(255, 180, 20, 0.08) 100%) !important;
        border: 2px solid rgba(255, 165, 0, 0.4) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 24px rgba(255, 165, 0, 0.15) !important;
        padding: 20px !important;
    }
    
    .stWarning p {
        color: #ffb300 !important;
        font-weight: 600;
    }
    
    /* Error box enhanced */
    .stError {
        background: linear-gradient(135deg, rgba(255, 68, 68, 0.15) 0%, rgba(255, 100, 100, 0.08) 100%) !important;
        border: 2px solid rgba(255, 68, 68, 0.4) !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 24px rgba(255, 68, 68, 0.15) !important;
        padding: 20px !important;
    }
    
    /* Header styling */
    .stSubheader {
        color: #00ffff !important;
        font-weight: 800 !important;
        font-size: 1.3em !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Glossary items with hover effect */
    .glossary-item {
        background: rgba(0, 102, 255, 0.12);
        border-left: 4px solid #00d9ff;
        padding: 14px;
        margin: 10px 0;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .glossary-item:hover {
        background: rgba(0, 102, 255, 0.2);
        border-left-color: #00ffff;
        transform: translateX(8px);
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.2);
    }
    
    /* Tool badges with glow */
    .tool-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(0, 102, 255, 0.25), rgba(0, 217, 255, 0.25));
        border: 2px solid rgba(0, 217, 255, 0.6);
        padding: 8px 18px;
        border-radius: 25px;
        margin: 6px;
        font-weight: 600;
        color: #00ffff;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.15);
        cursor: default;
    }
    
    .tool-badge:hover {
        background: linear-gradient(135deg, rgba(0, 102, 255, 0.4), rgba(0, 217, 255, 0.4));
        border-color: #00ffff;
        box-shadow: 0 8px 20px rgba(0, 217, 255, 0.3);
        transform: scale(1.05);
    }
    
    /* Metric cards styling */
    [data-testid="metric-container"] {
        background: rgba(20, 30, 80, 0.4) !important;
        border: 2px solid rgba(0, 217, 255, 0.2) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(20px) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: rgba(0, 217, 255, 0.5) !important;
        box-shadow: 0 8px 24px rgba(0, 217, 255, 0.2) !important;
        transform: translateY(-3px) !important;
    }
    
    /* Smooth scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #0066ff, #00d9ff);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #00d9ff, #0066ff);
    }
    </style>
    """, unsafe_allow_html=True)

# Load NLP model
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()

# --- REFINED LOGIC ---
def decode_jd(text):
    doc = nlp(text)
    must_haves = []
    nice_to_haves = []
    
    must_triggers = ['proficiency', 'requirement', 'skills', 'experience', 'ability', 'degree', 'develop', 'maintain']
    plus_triggers = ['plus', 'preferred', 'nice to have', 'bonus', 'ideal', 'exposure', 'advantage']
    ignore_list = ['google is', 'we are committed', 'please do not', 'equal opportunity', 'privacy policy']

    sentences = [sent.text.strip() for sent in doc.sents]
    
    for sent in sentences:
        low_sent = sent.lower()
        
        if any(ignore in low_sent for ignore in ignore_list):
            continue
            
        if any(p in low_sent for p in plus_triggers):
            nice_to_haves.append(sent)
        elif any(m in low_sent for m in must_triggers):
            must_haves.append(sent)

    # Enhanced blacklist with common non-tech terms
    blacklist = ['Google', 'India', 'Interns', 'Internship', 'Policy', 'Local', 'Social', 'CVs', 'Ads',
                 'Accommodations', 'Equal', 'Opportunity', 'Employer', 'Background', 'Check', 'Microsoft',
                 'Careers', 'Interview', 'Application', 'Position', 'Company', 'Team', 'Office', 'Work']
    
    # Tech keywords to whitelist (to ensure we catch real tech)
    tech_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'sql', 'aws', 
                     'docker', 'kubernetes', 'cloud', 'azure', 'gcp', 'git', 'api', 'rest', 'graphql',
                     'mongodb', 'postgres', 'mysql', 'redis', 'elasticsearch', 'kafka', 'hadoop', 'spark',
                     'tensorflow', 'pytorch', 'django', 'flask', 'spring', 'rust', 'golang', 'scala']
    
    tools = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT"]]
    clean_tools = list(set([t for t in tools if t not in blacklist and len(t) > 2 and t.lower() not in blacklist]))
    
    # Additional filtering: keep only if it looks like tech
    tech_patterns = ['js', 'sql', 'api', 'db', 'framework', 'library', 'platform', 'tool', 'service']
    filtered_tools = [t for t in clean_tools if any(pattern in t.lower() for pattern in tech_patterns) or 
                      any(keyword in t.lower() for keyword in tech_keywords)]
    
    # If we filtered too aggressively, return the original clean list with just blacklist removed
    final_tools = filtered_tools if filtered_tools else clean_tools
    
    return must_haves, nice_to_haves, final_tools

# --- SIDEBAR ---
GLOSSARY = {
    "fast-paced": "Expect frequent priority shifts and tight deadlines.",
    "self-starter": "You'll need to figure things out with minimal training.",
    "stakeholder": "People (tech or non-tech) who care about the project.",
    "scalability": "Making sure the app doesn't crash when millions use it.",
    "exposure": "You will see it/learn it, but you don't need to be an expert yet."
}

with st.sidebar:
    st.markdown("## 🧭 Jargon Buster")
    for word, meaning in GLOSSARY.items():
        st.markdown(f'<div class="glossary-item"><strong style="color: #00ffff;">{word.capitalize()}</strong><br><span style="color: #c5cfe0; font-size: 0.9em;">{meaning}</span></div>', unsafe_allow_html=True)

# --- MAIN UI ---
st.markdown('<div class="main-title">🔍 Job Description Skill Decoder</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform long job descriptions into actionable skill checklists</p>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
jd_input = st.text_area("📋 Paste the Job Description here:", height=300, placeholder="Copy-paste the entire job posting...")
st.markdown('</div>', unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])

with col_btn1:
    decode_pressed = st.button("🚀 Decode This Job", use_container_width=True)

if decode_pressed:
    if jd_input.strip():
        must, plus, tools = decode_jd(jd_input)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Success metrics with enhanced styling
        col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
        
        with col_metrics1:
            st.metric("✅ Must-Have Skills", len(must), delta="core requirements", delta_color="off")
        with col_metrics2:
            st.metric("🌟 Nice-to-Haves", len(plus), delta="bonus points", delta_color="off")
        with col_metrics3:
            st.metric("🛠️ Tech Stack", len(tools), delta="tools mentioned", delta_color="off")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.success("### ✅ Must-Have Skills")
            if must:
                for i, item in enumerate(must[:8], 1):
                    st.markdown(f"**{i}.** {item}")
            else:
                st.write("No mandatory skills detected.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.warning("### 🌟 Nice-to-Haves / Exposure")
            if plus:
                for i, item in enumerate(plus, 1):
                    st.markdown(f"**{i}.** {item}")
            else:
                st.write("No 'preferred' skills found. Everything listed seems mandatory.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🛠️ Tech & Platforms Mentioned")
        if tools:
            st.markdown(" ".join([f'<span class="tool-badge">{t}</span>' for t in sorted(tools)]), unsafe_allow_html=True)
        else:
            st.write("No specific technologies identified.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.error("⚠️ Please paste the job description first!")