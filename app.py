"""
Streamlit Web Application
Interactive UI for Medicine & Health Recommendation System
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from recommendation_engine import HealthRecommendationEngine
import time
import textwrap
import os
import ast
from fpdf import FPDF

# Page configuration
st.set_page_config(
    page_title="Health Recommendation System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Remove excessive top spacing in sidebar and main area */
    .block-container {
        padding-top: 2rem;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 1rem !important;
    }
    section[data-testid="stSidebar"] h3:first-of-type {
        margin-top: 0rem;
        padding-top: 0rem;
    }
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        border-radius: 10px;
        padding: 0.45rem 0.6rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button[kind="primary"] {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(76, 175, 80, 0.3);
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(76, 175, 80, 0.4);
    }
    .stButton>button[kind="secondary"] {
        width: auto;
        background-color: #eef1f4;
        color: #2c3e50;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.25rem 0.5rem;
        transition: all 0.2s ease;
    }
    .stButton>button[kind="secondary"]:hover {
        background-color: #e2e6ea;
        transform: scale(1.05);
    }
    .prediction-box {
        padding: 20px;
        border-radius: 15px;
        background-color: #f0f8ff;
        border-left: 5px solid #4CAF50;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .prediction-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .severity-high {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .severity-moderate {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
    }
    .severity-low {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
    }
    .recommendation-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: all 0.3s ease;
        border: 1px solid #e0e0e0;
    }
    .recommendation-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        border-color: #4CAF50;
    }
    h1 {
        color: #2c3e50;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h2 {
        color: #34495e;
    }
    h3 {
        color: #7f8c8d;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
    }
    .stCheckbox {
        padding: 2px 0;
        margin: 0px 0;
    }
    .stCheckbox > label {
        padding: 2px 6px;
        border-radius: 3px;
        transition: background-color 0.2s ease;
        margin: 0px 0;
        font-size: 14px;
    }
    .stCheckbox > label:hover {
        background-color: #f0f0f0;
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .st-emotion-cache-tn0cau {
        display: flex;
        gap: 0rem;
        width: 100%;
        max-width: 100%;
        height: auto;
        min-width: 1rem;
        flex-flow: column;
        flex: 1 1 0%;
        -webkit-box-align: stretch;
        align-items: stretch;
        -webkit-box-pack: start;
        justify-content: start;
    }
    .st-emotion-cache-wfksaw {
        display: flex;
        gap: 0rem;
        width: 100%;
        max-width: 100%;
        height: 100%;
        min-width: 1rem;
        flex-flow: column;
        flex: 1 1 0%;
        -webkit-box-align: stretch;
        align-items: stretch;
        -webkit-box-pack: start;
        justify-content: start;
    }

    section[data-testid="stSidebar"] [data-testid="stElementToolbar"],
    section[data-testid="stSidebar"] [data-testid="stDataFrameToolbar"],
    section[data-testid="stSidebar"] [data-testid="stColumnHeaderDropdown"],
    section[data-testid="stSidebar"] .stDataEditorToolbarContainer {
        display: none;
    }

    /* Sticky Sidebar Component Logic */
    div[data-testid="stSidebarUserContent"] > div:first-child {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: inherit;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = None
    st.session_state.model_loaded = False
    st.session_state.selected_symptoms = {}
    st.session_state.report = None
    st.session_state.diagnosis_generated_once = False
    st.session_state.history = []
    st.session_state.active_view = 'diagnosis'

@st.cache_resource
def load_engine():
    """Load the recommendation engine (cached)"""
    engine = HealthRecommendationEngine()
    
    if engine.load_model() and engine.load_recommendation_data():
        return engine
    return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_filtered_symptoms(_all_symptoms, search_term):
    """Cache filtered symptoms for better search performance"""
    if search_term:
        return [s for s in _all_symptoms if search_term.lower() in s.lower()]
    return _all_symptoms

@st.cache_data
def load_bmi_data():
    """Cache loading of BMI wellness dataset"""
    try:
        path = os.path.join("datasets", "bmi_wellness.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Pre-parse string lists
            for col in ["Diet", "Routines", "Recipes"]:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
            return df
    except Exception as e:
        st.error(f"Error loading BMI dataset: {e}")
    return None

@st.cache_data
def generate_bmi_pdf_report(data):
    """Cached PDF generation for BMI report"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "BMI & WELLNESS PLAN REPORT", ln=True, align='C')
    pdf.line(10, 20, 200, 20)
    pdf.ln(10)
    
    def safe_print(text, is_disclaimer=False):
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        for line in textwrap.wrap(safe_text, width=90):
            pdf.cell(0, 5 if is_disclaimer else 6, line, ln=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "PATIENT BODY METRICS", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, f"Gender: {data['gender']}", ln=True)
    pdf.cell(0, 6, f"Height: {data['height']} cm", ln=True)
    pdf.cell(0, 6, f"Weight: {data['weight']} kg", ln=True)
    pdf.cell(0, 6, f"Calculated BMI: {data['bmi']:.1f}", ln=True)
    pdf.cell(0, 6, f"Category: {data['cat']}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "DIETARY GUIDELINES", ln=True)
    pdf.set_font("Arial", '', 11)
    for d in data['diet']:
        safe_print(f"- {d}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "DAILY ROUTINES", ln=True)
    pdf.set_font("Arial", '', 11)
    for r in data['routines']:
        safe_print(f"- {r}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "HEALTHY RECIPES", ln=True)
    pdf.set_font("Arial", '', 11)
    for r in data['recipes']:
        safe_print(f"- {r}")
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 9)
    safe_print("DISCLAIMER: This is an AI-generated health report. Please consult with a healthcare professional before making any drastic dietary or physical lifestyle changes.", is_disclaimer=True)
    
    return bytes(pdf.output())

@st.fragment
def display_main_bmi_dashboard():
    """Display BMI Dashboard in Main Content Area (Isolated Fragment)"""
    st.markdown("## ⚖️ BMI & Wellness Dashboard")
    st.markdown("Calculate your Body Mass Index and get personalized wellness recommendations.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
    with col2:
        height = st.number_input("Height (cm)", min_value=50.0, max_value=300.0, value=170.0, step=0.1)
    with col3:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
    with col3:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
    if st.button("Calculate BMI & Generate Plan", type="primary"):
        bmi = weight / ((height/100)**2)
        if bmi < 18.5:
            cat, color = "Underweight", "#FFC107"
        elif bmi < 25:
            cat, color = "Normal", "#4CAF50"
        elif bmi < 30:
            cat, color = "Overweight", "#FF9800"
        else:
            cat, color = "Obese", "#F44336"
            
        bmi_df = load_bmi_data()
        if bmi_df is not None:
            try:
                cat_row = bmi_df[bmi_df["Category"] == cat].iloc[0]
                diet = cat_row["Diet"]
                routines = cat_row["Routines"]
                recipes = cat_row["Recipes"]
            except Exception as e:
                st.error(f"Error processing BMI recommendations: {e}")
                diet, routines, recipes = [], [], []
        else:
            diet, routines, recipes = [], [], []
            
        st.session_state.bmi_calc_data = {
            "bmi": bmi, "cat": cat, "color": color, "diet": diet,
            "routines": routines, "recipes": recipes,
            "height": height, "weight": weight, "gender": gender
        }
            
    if st.session_state.get('bmi_calc_data'):
        data = st.session_state.bmi_calc_data
        
        st.markdown("---")
        st.markdown(f"""
            <div style='padding: 20px; border-radius: 12px; background-color: #f8f9fa; border-left: 8px solid {data['color']}; margin-top: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h2 style='margin: 0; color: #2c3e50;'>Your BMI: {data['bmi']:.1f}</h2>
                <h3 style='margin: 10px 0 0 0; color: {data['color']}; font-weight: bold;'>Category: {data['cat']}</h3>
                <p style='color: #7f8c8d; margin-top: 10px;'>Calculated for a {data['height']}cm, {data['weight']}kg {data['gender']}.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Recommended Action Plan")
        tab1, tab2, tab3 = st.tabs(["🥗 Dietary Guidelines", "🏃 Daily Routines", "🍳 Healthy Recipes"])
        
        with tab1:
            for item in data['diet']:
                st.info(f"✓ {item}")
        with tab2:
            for item in data['routines']:
                st.success(f"✓ {item}")
        with tab3:
            for item in data['recipes']:
                st.warning(f"✓ {item}")

        # Download report button
        st.markdown("---")
        st.markdown("### 📥 Export Plan")
        pdf_bytes = generate_bmi_pdf_report(data)
        st.download_button(
            label="📄 Download BMI Wellness Plan (PDF)",
            data=pdf_bytes,
            file_name=f"bmi_wellness_plan_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

def display_session_history():
    """Display session history in sidebar"""
    st.sidebar.markdown("---")
    if 'history' in st.session_state and st.session_state.history:
        with st.sidebar.expander("🕒 Recent Activity", expanded=False):
            for item in reversed(st.session_state.history[-5:]):
                st.markdown(f"**{item['time']}**")
                st.markdown(f"Diagnosed: *{item['disease']}* ({item['symptoms']} symptoms)")
                st.markdown("---")

def display_header():
    """Display application header"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
            <h1 style='text-align: center; color: #2c3e50;'>
                🏥 Intelligent Medicine & Health Recommendation System
            </h1>
            <p style='text-align: center; color: #7f8c8d; font-size: 18px;'>
                AI-Powered Disease Prediction & Personalized Healthcare Recommendations
            </p>
        """, unsafe_allow_html=True)
        st.markdown("---")

@st.fragment
def voice_assistant_interface(engine):
    """Voice Assistant for selecting symptoms using Gemini AI (Isolated Fragment)"""
    if not st.session_state.get('voice_mode_enabled', False):
        return
        
    st.markdown("### 🎙️ Voice Assistant")
    try:
        from streamlit_mic_recorder import speech_to_text
        import google.generativeai as genai
        
        # Configure Gemini API (key stored in Streamlit Secrets)
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            st.error("⚠️ Gemini API key not configured. Add GEMINI_API_KEY in app Settings → Secrets.")
            return
        genai.configure(api_key=api_key)
        
        text = speech_to_text(language='en', start_prompt="🔴 Start Voice Recognition", stop_prompt="⏹ Speak Now (Auto-stops on pause)", just_once=False, key='stt')
        if text:
            st.success(f'Heard: "{text}"')
            
            with st.spinner("🧠 Mapping symptoms with Gemini AI..."):
                try:
                    all_symptoms = engine.get_all_symptoms()
                    symptom_set = set(all_symptoms)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    prompt = f"""
                    You are a highly capable medical parsing AI. 
                    The patient reported the following physical issues: "{text}"
                    
                    Here is the strict dataset of valid system symptoms:
                    {all_symptoms}
                    
                    Task: Map the patient's colloquial symptoms to the exact string variables from the dataset.
                    Return ONLY a comma-separated list of the exact string dataset symptoms that correctly match.
                    Do not include any conversational text, explanations, code blocks, bullet points, or symptoms not in the list.
                    If nothing clearly matches, return an empty response.
                    """
                    response = model.generate_content(prompt)
                    
                    matched = []
                    if response.text and response.text.strip():
                        # Parse the comma-separated list
                        extracted = [s.strip() for s in response.text.split(',')]
                        for s in extracted:
                            # Verify the exact system matched correctly
                            if s in symptom_set and s not in matched:
                                matched.append(s)
                
                    if matched:
                        new_found = False
                        st.info(f"Gemini AI extracted: {', '.join([s.replace('_', ' ') for s in matched])}")
                        for s in matched:
                            if s not in st.session_state.selected_symptoms:
                                st.session_state.selected_symptoms[s] = True
                                new_found = True
                        st.session_state.report = None
                        if new_found:
                            st.rerun()
                    else:
                        st.warning("No valid matching symptoms were detected by the AI from your phrase.")
                except Exception as e:
                    st.error(f"Gemini API Processing Error: {e}")
    except Exception as e:
        st.error(f"Voice and AI packages missing. Error: {e}")

def symptom_selection_interface(engine, top_container=None):
    """Create symptom selection interface"""
    target = top_container if top_container else st.sidebar
    
    # Get all symptoms (already sorted from engine)
    all_symptoms = engine.get_all_symptoms()

    def clear_all_selections(symptoms):
        st.session_state.selected_symptoms = {}
        st.session_state.report = None
        st.session_state.symptom_search = ""

        st.session_state.pop("available_symptoms_editor", None)
        st.session_state.pop("selected_symptoms_editor", None)

        if st.session_state.diagnosis_generated_once:
            st.session_state.auto_diagnose = True
    
    with target:
        st.header("🔍 Symptom Selection")
        # Search functionality
        search_term = st.text_input(
            "🔎 Search Symptoms",
            placeholder="Type to search...",
            help="Search for symptoms by name",
            key="symptom_search"
        )
    
    # Filter symptoms based on search (using cached function)
    filtered_symptoms = get_filtered_symptoms(all_symptoms, search_term)
    
    st.sidebar.markdown(f"**Found {len(filtered_symptoms)} symptoms**")
    
    selected_symptoms = {symptom: 1 for symptom in st.session_state.selected_symptoms.keys()}

    available_symptoms = [s for s in filtered_symptoms if s not in st.session_state.selected_symptoms]

    st.sidebar.markdown("### Available Symptoms")
    if available_symptoms:
        available_df = pd.DataFrame(
            {
                "Symptom": [s.replace('_', ' ').title() for s in available_symptoms],
                "Add": [False] * len(available_symptoms),
            },
            index=available_symptoms,
        )

        edited_available_df = st.sidebar.data_editor(
            available_df,
            hide_index=True,
            disabled=["Symptom"],
            num_rows="fixed",
            height=260,
            key="available_symptoms_editor",
        )

        symptoms_to_add = list(edited_available_df[edited_available_df["Add"]].index)
        if symptoms_to_add:
            changed = False
            for symptom in symptoms_to_add:
                if symptom not in st.session_state.selected_symptoms:
                    st.session_state.selected_symptoms[symptom] = True
                    changed = True

            if changed and st.session_state.diagnosis_generated_once:
                st.session_state.auto_diagnose = True
                st.session_state.report = None

            st.rerun()
    else:
        st.caption("No available symptoms (adjust search or remove selected).")
    
    # Display selected count with visual badge
    selected_count = sum(1 for v in selected_symptoms.values() if v == 1)
    badge_color = "#4CAF50" if selected_count > 0 else "#6c757d"
    st.sidebar.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 15px;'>
            <span style='font-weight: bold; margin-right: 10px;'>✅ Selected:</span>
            <span style='background-color: {badge_color}; color: white; padding: 4px 12px; 
                   border-radius: 20px; font-weight: bold; font-size: 14px;'>
                {selected_count} symptoms
            </span>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### Selected Symptoms")
    selected_list = sorted(st.session_state.selected_symptoms.keys())
    if selected_list:
        selected_df = pd.DataFrame(
            {
                "Symptom": [s.replace('_', ' ').title() for s in selected_list],
                "Remove": [False] * len(selected_list),
            },
            index=selected_list,
        )

        edited_selected_df = st.sidebar.data_editor(
            selected_df,
            hide_index=True,
            disabled=["Symptom"],
            num_rows="fixed",
            height=220,
            key="selected_symptoms_editor",
        )

        symptoms_to_remove = list(edited_selected_df[edited_selected_df["Remove"]].index)
        if symptoms_to_remove:
            for symptom in symptoms_to_remove:
                st.session_state.selected_symptoms.pop(symptom, None)

            if st.session_state.diagnosis_generated_once:
                st.session_state.auto_diagnose = True
                st.session_state.report = None

            st.rerun()
    else:
        st.caption("No symptoms selected.")
    
    # Clear button
    st.sidebar.button(
        "🗑️ Clear All Selections",
        on_click=clear_all_selections,
        args=(all_symptoms,)
    )
    
    return selected_symptoms

def display_prediction_results(report):
    """Display prediction results"""
    st.markdown("## 🎯 Diagnosis Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='prediction-box'>
                <h3 style='color: #2c3e50; margin-bottom: 10px;'>Predicted Disease</h3>
                <h2 style='color: #4CAF50; margin: 0;'>{report['prediction']['disease']}</h2>
                <p style='color: #7f8c8d; margin-top: 10px;'>
                    Confidence: {report['prediction']['confidence']:.1%}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        severity_class = f"severity-{report['severity']['level'].lower()}"
        st.markdown(f"""
            <div class='prediction-box {severity_class}'>
                <h3 style='color: #2c3e50; margin-bottom: 10px;'>Severity Level</h3>
                <h2 style='margin: 0;'>{report['severity']['level']}</h2>
                <p style='color: #7f8c8d; margin-top: 10px;'>
                    Score: {report['severity']['score']}/7
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='prediction-box'>
                <h3 style='color: #2c3e50; margin-bottom: 10px;'>Symptoms Count</h3>
                <h2 style='color: #3498db; margin: 0;'>{report['symptoms']['count']}</h2>
                <p style='color: #7f8c8d; margin-top: 10px;'>
                    Active symptoms detected
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Confidence chart
    st.markdown("### 📊 Top 3 Possible Diagnoses")
    
    top_3 = report['prediction']['top_3_predictions']
    diseases = [pred['disease'] for pred in top_3]
    probabilities = [pred['probability'] * 100 for pred in top_3]
    
    fig = go.Figure(data=[
        go.Bar(
            x=probabilities,
            y=diseases,
            orientation='h',
            marker=dict(
                color=['#4CAF50', '#2196F3', '#FFC107'],
                line=dict(color='rgba(0,0,0,0.3)', width=1)
            ),
            text=[f"{p:.1f}%" for p in probabilities],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Prediction Confidence Comparison",
        xaxis_title="Confidence (%)",
        yaxis_title="Disease",
        height=300,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_disease_description(report):
    """Display disease description"""
    st.markdown("## 📖 Disease Information")
    
    st.markdown(f"""
        <div class='recommendation-card'>
            <h3 style='color: #2c3e50;'>{report['prediction']['disease']}</h3>
            <p style='font-size: 16px; line-height: 1.6; color: #34495e;'>
                {report['description']}
            </p>
        </div>
    """, unsafe_allow_html=True)

def display_recommendations(report):
    """Display all recommendations"""
    st.markdown("## 💡 Personalized Recommendations")
    
    # Create tabs for different recommendations
    tab1, tab2, tab3, tab4 = st.tabs([
        "💊 Medications", 
        "🥗 Diet Plan", 
        "🏃 Lifestyle & Exercise", 
        "⚕️ Precautions"
    ])
    
    with tab1:
        st.markdown("### Recommended Medications")
        if report['medications']:
            for i, med in enumerate(report['medications'], 1):
                st.markdown(f"""
                    <div class='recommendation-card'>
                        <strong>{i}. {med}</strong>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific medication recommendations available.")
        
        st.warning("⚠️ **Important:** Always consult with a healthcare professional before taking any medication.")
    
    with tab2:
        st.markdown("### Dietary Recommendations")
        if report['diet']:
            col1, col2 = st.columns(2)
            for i, diet in enumerate(report['diet']):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                        <div class='recommendation-card'>
                            ✓ {diet}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No specific diet recommendations available.")
    
    with tab3:
        st.markdown("### Lifestyle & Exercise Recommendations")
        if report['workouts']:
            for i, workout in enumerate(report['workouts'], 1):
                st.markdown(f"{i}. {workout}")
        else:
            st.info("No specific workout recommendations available.")
    
    with tab4:
        st.markdown("### Important Precautions")
        if report['precautions']:
            for i, precaution in enumerate(report['precautions'], 1):
                st.markdown(f"""
                    <div class='recommendation-card' style='background-color: #fff3cd; border-left: 5px solid #ffc107;'>
                        <strong>{i}. {precaution}</strong>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific precautions available.")

def display_active_symptoms(report):
    """Display active symptoms"""
    with st.expander("📋 View Active Symptoms", expanded=False):
        symptoms = report['symptoms']['active_symptoms']
        
        # Display in columns
        cols = st.columns(3)
        for i, symptom in enumerate(symptoms):
            with cols[i % 3]:
                st.markdown(f"• {symptom.replace('_', ' ').title()}")

@st.cache_data
def generate_pdf_report(report):
    """Cached PDF generation for Health report"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "HEALTH RECOMMENDATION REPORT", ln=True, align='C')
    pdf.line(10, 20, 200, 20)
    pdf.ln(10)
    
    def safe_print(text, is_disclaimer=False):
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        # Use width 80 for reasonable wrapping, or a bit more
        for line in textwrap.wrap(safe_text, width=90):
            pdf.cell(0, 5 if is_disclaimer else 6, line, ln=True)
            
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "DIAGNOSIS", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 6, f"Predicted Disease: {report['prediction']['disease']}", ln=True)
    pdf.cell(0, 6, f"Confidence: {report['prediction']['confidence']:.1%}", ln=True)
    pdf.cell(0, 6, f"Severity Level: {report['severity']['level']}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "MEDICATIONS", ln=True)
    pdf.set_font("Arial", '', 11)
    for m in report['medications']:
        safe_print(f"- {m}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "DIET RECOMMENDATIONS", ln=True)
    pdf.set_font("Arial", '', 11)
    for d in report['diet']:
        safe_print(f"- {d}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "LIFESTYLE & EXERCISE", ln=True)
    pdf.set_font("Arial", '', 11)
    for w in report['workouts'][:10]:
        safe_print(f"- {w}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "PRECAUTIONS", ln=True)
    pdf.set_font("Arial", '', 11)
    for p in report['precautions']:
        safe_print(f"- {p}")
        
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 9)
    safe_print("DISCLAIMER: This is an AI-generated report. Please consult with a healthcare professional before making any medical decisions.", is_disclaimer=True)
    
    return bytes(pdf.output())

def main():
    """Main application function"""
    display_header()
    
    # Load engine
    if st.session_state.engine is None:
        # Full-screen premium loading splash
        st.markdown("""
            <style>
            @keyframes pulse { 0%,100% { opacity: 0.4; } 50% { opacity: 1; } }
            @keyframes spin { to { transform: rotate(360deg); } }
            .loading-container {
                display: flex; flex-direction: column; align-items: center;
                justify-content: center; padding: 80px 20px; text-align: center;
            }
            .loading-ring {
                width: 80px; height: 80px; border: 6px solid #e0e0e0;
                border-top: 6px solid #4CAF50; border-radius: 50%;
                animation: spin 1s linear infinite; margin-bottom: 30px;
            }
            .loading-title {
                font-size: 1.8rem; font-weight: 800; color: #2c3e50;
                margin-bottom: 10px; letter-spacing: 1px;
            }
            .loading-sub {
                font-size: 1.05rem; color: #7f8c8d; margin-bottom: 35px;
            }
            .loading-steps { display: flex; flex-direction: column; gap: 12px; align-items: flex-start; }
            .loading-step {
                display: flex; align-items: center; gap: 12px;
                font-size: 1rem; color: #34495e; animation: pulse 1.5s ease-in-out infinite;
            }
            .loading-step:nth-child(2) { animation-delay: 0.3s; }
            .loading-step:nth-child(3) { animation-delay: 0.6s; }
            .loading-step:nth-child(4) { animation-delay: 0.9s; }
            .step-icon {
                width: 32px; height: 32px; border-radius: 50%; display: flex;
                align-items: center; justify-content: center; font-size: 1rem;
                background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
                color: white; box-shadow: 0 2px 8px rgba(76,175,80,0.3);
            }
            </style>
            <div class="loading-container">
                <div class="loading-ring"></div>
                <div class="loading-title">⚕️ ALEIHMS</div>
                <div class="loading-sub">Initializing AI Health Engine — please wait...</div>
                <div class="loading-steps">
                    <div class="loading-step"><div class="step-icon">🧠</div> Loading ML Disease Predictor</div>
                    <div class="loading-step"><div class="step-icon">📊</div> Preparing Medical Datasets</div>
                    <div class="loading-step"><div class="step-icon">💊</div> Indexing Recommendation Engine</div>
                    <div class="loading-step"><div class="step-icon">✅</div> Finalizing System Diagnostics</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.session_state.engine = load_engine()

        if st.session_state.engine is None:
            st.error("❌ Failed to load the model. Please ensure the model is trained.")
            st.info("Run `python model_training.py` to train the model first.")
            st.stop()
        else:
            st.session_state.model_loaded = True
            st.rerun()
    
    engine = st.session_state.engine
    
    sticky_nav = st.sidebar.container()
    with sticky_nav:
        st.markdown("""
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <div style='background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); padding: 10px 14px; border-radius: 12px; margin-right: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                    <h2 style='margin: 0; color: white; line-height: 1; font-size: 1.8rem;'>⚕️</h2>
                </div>
                <h2 style='margin: 0; color: #2c3e50; font-weight: 800; letter-spacing: 1.5px; font-size: 2rem;'>ALEIHMS</h2>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("### 🧭 Navigation")
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔮 AI Health Diagnosis", use_container_width=True):
                st.session_state.active_view = 'diagnosis'
        with col2:
            st.session_state.voice_mode_enabled = st.toggle("🎙️", key="voice_mode_nav", help="Enable Voice Mode")
            
        if st.button("⚖️ BMI & Wellness Dashboard", use_container_width=True):
            st.session_state.active_view = 'bmi'
        
    if st.session_state.active_view == 'bmi':
        display_session_history()
        display_main_bmi_dashboard()
        return
    
    # Symptom selection
    selected_symptoms = symptom_selection_interface(engine, top_container=sticky_nav)
    display_session_history()
    
    # Voice Assistant and Diagnosis in main display area
    voice_assistant_interface(engine)
    st.markdown("---")
    
    # Predict button (always show when symptoms are selected)
    if selected_symptoms:
        if st.button("🔮 Get Diagnosis & Recommendations", type="primary"):
            with st.spinner("🧠 Analyzing symptoms and generating recommendations..."):
                # Generate report
                report = engine.generate_comprehensive_report(selected_symptoms)
                st.session_state.report = report
                st.session_state.diagnosis_generated_once = True
                
                # Append to session history
                st.session_state.history.append({
                    "time": pd.Timestamp.now().strftime("%I:%M %p"),
                    "disease": report['prediction']['disease'],
                    "symptoms": report['symptoms']['count']
                })
        
        # Auto-diagnosis after symptom removal (only if diagnosis was generated once)
        if st.session_state.get("auto_diagnose", False) and st.session_state.diagnosis_generated_once:
            with st.spinner("🔄 Updating diagnosis..."):
                report = engine.generate_comprehensive_report(selected_symptoms)
                st.session_state.report = report
                st.session_state.auto_diagnose = False
    
    # Main content area
    if st.session_state.report:
        # Display results if available
        report = st.session_state.report
        
        # Display all sections
        display_prediction_results(report)
        display_active_symptoms(report)
        st.markdown("---")
        display_disease_description(report)
        st.markdown("---")
        display_recommendations(report)
        
        # Download report button
        st.markdown("---")
        st.markdown("### 📥 Export Report")
        
        # Create PDF report
        pdf_bytes = generate_pdf_report(report)
        
        st.download_button(
            label="📄 Download Professional Report (PDF)",
            data=pdf_bytes,
            file_name=f"health_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
        
        # Disclaimer
        st.markdown("---")
        st.warning("""
            **⚠️ Medical Disclaimer:** This system is designed for educational and informational 
            purposes only. It should not be used as a substitute for professional medical advice, 
            diagnosis, or treatment. Always seek the advice of your physician or other qualified 
            health provider with any questions you may have regarding a medical condition.
        """)
    else:
        # Welcome screen (shown when no report exists, even if symptoms are selected)
        st.markdown("""
            <div style='text-align: center; padding: 50px;'>
                <h2 style='color: #2c3e50; margin-bottom: 20px;'>👋 Welcome to the Health Recommendation System</h2>
                <p style='font-size: 18px; color: #7f8c8d; margin-bottom: 30px;'>
                    Select your symptoms from the sidebar to get started with AI-powered diagnosis
                    and personalized health recommendations.
                </p>
                <div style='display: flex; justify-content: center; gap: 40px; margin-top: 40px;'>
                    <div style='text-align: center; padding: 20px; border-radius: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1); transition: transform 0.3s ease;'>
                        <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>🔍</h1>
                        <h4 style='margin-bottom: 5px;'>Search Symptoms</h4>
                        <p style='font-size: 14px; opacity: 0.9;'>Find symptoms easily</p>
                    </div>
                    <div style='text-align: center; padding: 20px; border-radius: 15px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1); transition: transform 0.3s ease;'>
                        <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>🎯</h1>
                        <h4 style='margin-bottom: 5px;'>AI Diagnosis</h4>
                        <p style='font-size: 14px; opacity: 0.9;'>Get accurate predictions</p>
                    </div>
                    <div style='text-align: center; padding: 20px; border-radius: 15px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.1); transition: transform 0.3s ease;'>
                        <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>💊</h1>
                        <h4 style='margin-bottom: 5px;'>Recommendations</h4>
                        <p style='font-size: 14px; opacity: 0.9;'>Personalized health advice</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Display system statistics with enhanced styling
        st.markdown("---")
        st.markdown("### 📊 System Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div style='text-align: center; padding: 20px; border-radius: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                    <h1 style='font-size: 2rem; margin-bottom: 5px;'>📋</h1>
                    <h4 style='margin-bottom: 10px;'>Available Symptoms</h4>
                    <h2 style='margin: 0; font-size: 1.8rem;'>""" + str(len(engine.get_all_symptoms())) + """</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='text-align: center; padding: 20px; border-radius: 12px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                    <h1 style='font-size: 2rem; margin-bottom: 5px;'>🏥</h1>
                    <h4 style='margin-bottom: 10px;'>Disease Database</h4>
                    <h2 style='margin: 0; font-size: 1.8rem;'>41</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div style='text-align: center; padding: 20px; border-radius: 12px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                    <h1 style='font-size: 2rem; margin-bottom: 5px;'>🎯</h1>
                    <h4 style='margin-bottom: 10px;'>Model Accuracy</h4>
                    <h2 style='margin: 0; font-size: 1.8rem;'>95%+</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div style='text-align: center; padding: 20px; border-radius: 12px; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                    <h1 style='font-size: 2rem; margin-bottom: 5px;'>💡</h1>
                    <h4 style='margin-bottom: 10px;'>Recommendations</h4>
                    <h2 style='margin: 0; font-size: 1.8rem;'>4 Types</h2>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
