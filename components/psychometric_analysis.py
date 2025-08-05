import streamlit as st
import pandas as pd
import requests
from utils import session_manager
from services.api_client import n8n_client

# ─── TEST CONFIGURATIONS ──────────────────────────────
TEST_CONFIGS = [
    {
        "key": "test16PersonalityData",
        "title": "MBTI-style Personality Type",
        "subtitle": "Categorizes people into 16 personality types based on 5 preferences: how you gain energy (Introvert/Extravert), how you process information (Intuitive/Observant), how you make decisions (Thinking/Feeling), how you approach life (Judging/Prospecting), and how you see yourself (Assertive/Turbulent).",
        "headers": ["Preference", "Score", "Meaning"]
    },
    {
        "key": "high5Data",
        "title": "HIGH5 Strengths Themes",
        "subtitle": "Identifies your top 5 natural strengths from 20 possible talents (like Empathizer, Brainstormer, Deliverer). Focuses on what energizes you and where you have the greatest potential for success.",
        "headers": ["Strength", "Domain", "Meaning"]
    },
    {
        "key": "bigFiveData",
        "title": "Big Five Personality Traits (OCEAN)",
        "subtitle": "Measures 5 core personality dimensions: Openness (creativity), Conscientiousness (organization), Extraversion (sociability), Agreeableness (cooperation), Neuroticism (emotional stability).",
        "headers": ["Trait", "Score", "Meaning"]
    },
    {
        "key": "riasecData",
        "title": "RIASEC Career Interest Themes",
        "subtitle": "Assesses career interests across 6 work personality types: Realistic (hands-on), Investigative (analytical), Artistic (creative), Social (helping others), Enterprising (leading), Conventional (organized tasks).",
        "headers": ["Theme", "Score", "Meaning"]
    }
]

def render_upload_form():
    """Render the initial upload form"""
    
    st.markdown('<h1 class="doc-title">Psychometric Assessment Upload</h1>', unsafe_allow_html=True)
    
    with st.form("upload_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name = st.text_input("Child's Name", placeholder="Enter full name")
        with col2:
            age = st.number_input("Age", min_value=5, max_value=18, step=1)
        with col3:
            grade = st.text_input("Grade", placeholder="e.g., 5th grade")
        
        uploaded_files = st.file_uploader(
            "Upload Test Screenshots (1-4 images)",
            accept_multiple_files=True,
            type=["jpg", "jpeg", "png"],
            help="Upload screenshots of the test results"
        )
        
        submit = st.form_submit_button("Generate Report", type="primary", use_container_width=True)
    
    if submit:
        if not (name and age and grade and uploaded_files):
            st.error("Please complete all fields and upload at least one image.")
        else:
            # Store form data and trigger processing
            session_manager.store_form_data(name, age, grade, uploaded_files)
            st.rerun()

def process_uploaded_data():
    """Process uploaded data using N8N API"""
    
    form_data_dict = session_manager.get_form_data()
    student_name = form_data_dict['name']
    
    with st.spinner(f"Analyzing test results for {student_name}..."):
        progress = st.progress(0)
        status = st.empty()
        
        status.text("Uploading images...")
        progress.progress(20)
        
        # Prepare form data
        form_data = {
            "name": form_data_dict['name'],
            "age": str(form_data_dict['age']),
            "grade": form_data_dict['grade'],
            "fileCount": str(len(form_data_dict['uploaded_files'])),
        }
        
        # Prepare files
        files = []
        for i, f in enumerate(form_data_dict['uploaded_files']):
            f.seek(0)
            files.append((f"data{i}", (f.name, f.read(), f.type)))
        
        try:
            status.text("Processing test data...")
            progress.progress(50)
            
            # Upload to N8N
            payload = n8n_client.upload_psychometric_data(form_data, files)
            
            status.text("Generating insights...")
            progress.progress(80)
            
            # Store the results
            session_manager.store_report_data(payload)
            
            progress.progress(100)
            status.text("Report ready!")
            
            # Small delay to show completion, then rerun
            import time
            time.sleep(1)
            st.rerun()
            
        except requests.exceptions.Timeout:
            st.error("Request timed out. The server may be busy. Please try again.")
            session_manager.reset_form()
            st.stop()
            
        except requests.exceptions.ConnectionError:
            st.error("Connection failed. Please check your internet connection and try again.")
            session_manager.reset_form()
            st.stop()
            
        except requests.exceptions.HTTPError as e:
            st.error(f"Server error: {e}")
            session_manager.reset_form()
            st.stop()
            
        except Exception as e:
            st.error(f"Could not generate report: {e}")
            st.error("Please try uploading fewer or smaller images, or try again later.")
            session_manager.reset_form()
            st.stop()

def render_report():
    """Render the complete psychometric report (assumes data is already processed)"""
    
    payload = session_manager.get_report_data()
    student_info = session_manager.get_student_info()
    
    # Header Section
    st.markdown('<h1 class="doc-title">Psychometric Assessment Report</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="student-header">', unsafe_allow_html=True)
    st.markdown(f'''
        <div>
            <div class="student-name">{student_info.get("name", "N/A")}</div>
            <div class="student-details">Age: {student_info.get("age", "N/A")} | Grade: {student_info.get("grade", "N/A")}</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Show edit mode indicator
    if session_manager.is_edit_mode():
        st.markdown(
            '<div class="edit-notice"><strong>EDIT MODE:</strong> You can now modify the report data. Click "Save Changes" to confirm or "Reset Changes" to revert.</div>',
            unsafe_allow_html=True
        )
    
    # Display test sections
    test_data = payload.get("testData", {})
    insights = payload.get("insightLines", [])
    
    for i, config in enumerate(TEST_CONFIGS):
        rows = test_data.get(config["key"], [])
        if not rows:
            continue
        
        st.markdown(f'<h2 class="section-title">{config["title"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-subtitle">{config["subtitle"]}</div>', unsafe_allow_html=True)
        
        # Show editable or read-only table based on mode
        if session_manager.is_edit_mode():
            render_editable_table(config, rows, i)
        else:
            render_read_only_table(config, rows)
        
        # Add insight if available
        if i < len(insights):
            render_insight(insights[i], i)

def render_editable_table(config, rows, test_index):
    """Render an editable table for a specific test type"""
    
    if config["key"] == "high5Data":
        # Show column headers
        col1, col2, col3 = st.columns([1, 1, 3])
        col1.write("**Strength**")
        col2.write("**Domain**")
        col3.write("**Meaning**")
        
        # HIGH5 has different structure (no score field)
        for j, row in enumerate(rows):
            col1, col2, col3 = st.columns([1, 1, 3])
            
            with col1:
                new_preference = st.text_input(
                    f"Strength {j+1}",
                    value=row.get("preference", ""),
                    key=f"{config['key']}_pref_{j}",
                    label_visibility="collapsed"
                )
            
            with col2:
                new_domain = st.text_input(
                    f"Domain {j+1}",
                    value=row.get("domain", ""),
                    key=f"{config['key']}_domain_{j}",
                    label_visibility="collapsed"
                )
            
            with col3:
                new_meaning = st.text_area(
                    f"Meaning {j+1}",
                    value=row.get("meaning", ""),
                    key=f"{config['key']}_meaning_{j}",
                    height=80,
                    label_visibility="collapsed"
                )
            
            # Update the data in session state
            report_data = session_manager.get_report_data()
            report_data["testData"][config["key"]][j].update({
                "preference": new_preference,
                "domain": new_domain,
                "meaning": new_meaning
            })
    
    else:
        # Show column headers
        col1, col2, col3 = st.columns([1, 1, 3])
        col1.write("**Preference**")
        col2.write("**Score**")
        col3.write("**Meaning**")
        
        # Standard structure for other tests
        for j, row in enumerate(rows):
            col1, col2, col3 = st.columns([1, 1, 3])
            
            with col1:
                if config["key"] == "test16PersonalityData":
                    # For 16 personalities, preference is read-only
                    st.text_input(
                        f"Preference {j+1}",
                        value=row.get("preference", ""),
                        key=f"{config['key']}_pref_{j}_readonly",
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    new_preference = row.get("preference", "")
                else:
                    new_preference = st.text_input(
                        f"Preference {j+1}",
                        value=row.get("preference", ""),
                        key=f"{config['key']}_pref_{j}",
                        label_visibility="collapsed"
                    )
            
            with col2:
                new_score = st.text_input(
                    f"Score {j+1}",
                    value=row.get("score", ""),
                    key=f"{config['key']}_score_{j}",
                    label_visibility="collapsed"
                )
            
            with col3:
                new_meaning = st.text_area(
                    f"Meaning {j+1}",
                    value=row.get("meaning", ""),
                    key=f"{config['key']}_meaning_{j}",
                    height=80,
                    label_visibility="collapsed"
                )
            
            # Update the data in session state
            report_data = session_manager.get_report_data()
            report_data["testData"][config["key"]][j].update({
                "preference": new_preference,
                "score": new_score,
                "meaning": new_meaning
            })

def render_read_only_table(config, rows):
    """Render a read-only table using Google Docs styling"""
    
    if config["key"] == "high5Data":
        # HIGH5 special display - only show preference, domain, meaning
        table_data = []
        for row in rows:
            table_data.append([
                row.get("preference", ""),
                row.get("domain", ""),
                row.get("meaning", "")
            ])
        
        headers = ["Strength", "Domain", "Meaning"]
        df = pd.DataFrame(table_data, columns=headers)
    else:
        # Standard display - show preference, score, meaning
        table_data = []
        for row in rows:
            table_data.append([
                row.get("preference", ""),
                row.get("score", ""),
                row.get("meaning", "")
            ])
        
        df = pd.DataFrame(table_data, columns=config["headers"])
    
    # Convert to HTML for custom styling
    html_table = df.to_html(index=False, escape=False)
    html_table = html_table.replace('<td>', '<td style="padding: 12px; border: 1px solid #dadce0; vertical-align: top; color: #202124; font-size: 17px; font-family: Inter, sans-serif;">')
    html_table = html_table.replace('<th>', '<th style="background-color: #f8f9fa; border: 1px solid #dadce0; padding: 12px; text-align: left; font-weight: 500; color: #202124; font-size: 17px; font-family: Inter, sans-serif;">')
    html_table = html_table.replace('<table border="1" class="dataframe">', '<table class="doc-table" style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 17px; font-family: Inter, sans-serif;">')
    
    st.markdown(html_table, unsafe_allow_html=True)

def render_insight(insight_text, insight_index):
    """Render insight section (editable or read-only)"""
    
    if session_manager.is_edit_mode():
        st.write("**Insight:**")
        new_insight = st.text_area(
            "Edit insight",
            value=insight_text.replace("INSIGHT: ", ""),
            key=f"insight_{insight_index}",
            height=100,
            label_visibility="collapsed"
        )
        # Update insight in session state
        report_data = session_manager.get_report_data()
        report_data["insightLines"][insight_index] = f"INSIGHT: {new_insight}"
    else:
        clean_insight = insight_text.replace("INSIGHT: ", "")
        st.markdown(
            f'<div class="insight-box"><span class="insight-label">Insight:</span> {clean_insight}</div>',
            unsafe_allow_html=True
        )
