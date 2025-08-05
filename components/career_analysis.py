import streamlit as st
from utils import session_manager
from services.api_client import n8n_client

def process_career_request():
    """Process career analysis request"""
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.spinner("Generating career recommendations..."):
        try:
            # Get student info and report data
            student_info = session_manager.get_student_info()
            report_data = session_manager.get_report_data()
            
            # Prepare career analysis request
            career_request_data = {
                "studentInfo": {
                    "name": student_info.get('name', 'Student'),
                    "age": student_info.get('age', 'Unknown'),
                    "grade": student_info.get('grade', 'Unknown')
                },
                "editedTestData": report_data.get("testData", {}),
                "editedInsights": report_data.get("insightLines", [])
            }
            
            # Send request to career analysis webhook
            career_data = n8n_client.request_career_analysis(career_request_data)
            
            # Store the career data
            session_manager.store_career_data(career_data)
            
            st.success("Career analysis completed!")
            
            # Small delay to show completion, then rerun
            import time
            time.sleep(1)
            st.rerun()
            
        except Exception as e:
            st.error(f"Failed to generate career recommendations: {e}")
            # Reset the request flag on error
            st.session_state.career_analysis_requested = False

def render_career_section():
    """Render the career analysis section with edit functionality"""
    
    career_data = session_manager.get_career_data()
    if not career_data:
        return
    
    st.markdown('<div class="career-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="career-title">Career Pathways & Recommendations</h1>', unsafe_allow_html=True)
    
    # Display career success/warning message
    if career_data.get("userMessage"):
        msg = career_data["userMessage"]
        if msg["type"] == "success":
            st.success(f"**{msg['title']}**: {msg['message']}")
        elif msg["type"] == "warning":
            st.warning(f"**{msg['title']}**: {msg['message']}")
        else:
            st.info(f"**{msg['title']}**: {msg['message']}")
    
    # Core Identity Summary Section
    if career_data.get("summary"):
        render_career_summary(career_data["summary"])
    
    # Career Fields Section
    if career_data.get("careerFields"):
        render_career_fields(career_data["careerFields"])
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_career_summary(summary_data):
    """Render the career summary section"""
    
    st.markdown('<h2 style="font-size: 25px; font-weight: 600; margin-top: 40px; margin-bottom: 8px; color: #202124;">Summary</h2>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 17px; color: #5f6368; margin-bottom: 20px; line-height: 1.5;">Key characteristics based on comprehensive psychometric analysis</div>', unsafe_allow_html=True)
    
    if session_manager.is_edit_mode():
        render_editable_summary(summary_data)
    else:
        render_readonly_summary(summary_data)

def render_editable_summary(summary_data):
    """Render editable summary section"""
    
    st.write("**Edit Summary:**")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Category**")
    with col2:
        st.write("**Key Characteristics**")
    
    # Core Drive
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_input("Category", value="Core Drive", key="summary_cat_1", disabled=True, label_visibility="collapsed")
    with col2:
        new_core_drive = st.text_area(
            "Core Drive", 
            value=summary_data.get("coreDriver", "Analysis pending"),
            key="summary_core_drive",
            height=80,
            label_visibility="collapsed"
        )
        # Update in session state
        career_data = session_manager.get_career_data()
        if career_data:
            career_data["summary"]["coreDriver"] = new_core_drive
    
    # Personality
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_input("Category", value="Personality", key="summary_cat_2", disabled=True, label_visibility="collapsed")
    with col2:
        new_personality = st.text_area(
            "Personality", 
            value=summary_data.get("personality", "Analysis pending"),
            key="summary_personality",
            height=80,
            label_visibility="collapsed"
        )
        career_data = session_manager.get_career_data()
        if career_data:
            career_data["summary"]["personality"] = new_personality
    
    # Work Style
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_input("Category", value="Work Style", key="summary_cat_3", disabled=True, label_visibility="collapsed")
    with col2:
        new_work_style = st.text_area(
            "Work Style", 
            value=summary_data.get("workStyle", "Analysis pending"),
            key="summary_work_style",
            height=80,
            label_visibility="collapsed"
        )
        career_data = session_manager.get_career_data()
        if career_data:
            career_data["summary"]["workStyle"] = new_work_style
    
    # Learning Style
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_input("Category", value="Learning Style", key="summary_cat_4", disabled=True, label_visibility="collapsed")
    with col2:
        new_learning_style = st.text_area(
            "Learning Style", 
            value=summary_data.get("learningStyle", "Analysis pending"),
            key="summary_learning_style",
            height=80,
            label_visibility="collapsed"
        )
        career_data = session_manager.get_career_data()
        if career_data:
            career_data["summary"]["learningStyle"] = new_learning_style

def render_readonly_summary(summary_data):
    """Render read-only summary table"""
    
    summary_html = '''
    <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 17px; font-family: Inter, sans-serif; background-color: #f8f9fa; border-radius: 4px;">
        <tr><th style="background-color: #f8f9fa; border: 1px solid #dadce0; padding: 12px; text-align: left; font-weight: 500; color: #202124; font-size: 17px;">Category</th><th style="background-color: #f8f9fa; border: 1px solid #dadce0; padding: 12px; text-align: left; font-weight: 500; color: #202124; font-size: 17px;">Key Characteristics</th></tr>
    '''
    
    summary_items = [
        ("Core Drive", summary_data.get("coreDriver", "Analysis pending")),
        ("Personality", summary_data.get("personality", "Analysis pending")),
        ("Work Style", summary_data.get("workStyle", "Analysis pending")),
        ("Learning Style", summary_data.get("learningStyle", "Analysis pending"))
    ]
    
    for category, characteristic in summary_items:
        summary_html += f'<tr><td style="border: 1px solid #dadce0; padding: 12px; vertical-align: top; color: #202124; font-size: 17px;">{category}</td><td style="border: 1px solid #dadce0; padding: 12px; vertical-align: top; color: #202124; font-size: 17px;">{characteristic}</td></tr>'
    
    summary_html += '</table>'
    st.markdown(summary_html, unsafe_allow_html=True)

def render_career_fields(career_fields):
    """Render career fields section"""
    
    for field_index, (field_key, field_data) in enumerate(career_fields.items()):
        st.markdown('<div class="career-field">', unsafe_allow_html=True)
        
        if session_manager.is_edit_mode():
            render_editable_career_field(field_data, field_key, field_index)
        else:
            render_readonly_career_field(field_data)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_readonly_career_field(field_data):
    """Render read-only career field - UPDATED for spaces and lessAligned"""
    
    st.markdown(f'<h3 class="career-field-title">{field_data.get("title", "Career Field")}</h3>', unsafe_allow_html=True)
    
    # Alignment indicator with color coding
    alignment = field_data.get("alignment", "Unknown")
    if alignment.lower() == "high":
        alignment_class = "alignment-high"
    elif "moderate" in alignment.lower():
        alignment_class = "alignment-moderate"
    else:
        alignment_class = "alignment-low"
    
    st.markdown(f'<p style="font-size: 17px;"><strong>Alignment:</strong> <span class="{alignment_class}">{alignment}</span></p>', unsafe_allow_html=True)
    
    # Description
    description = field_data.get("description", "Analysis in progress")
    st.markdown(f'<p style="font-size: 17px; color: #202124;">{description}</p>', unsafe_allow_html=True)
    
    # Career Spaces (changed from roles)
    spaces = field_data.get("spaces", [])
    if spaces:
        st.markdown('<h4 style="font-size: 17px; font-weight: 600; color: #202124; margin-bottom: 15px;">Career Spaces to Explore:</h4>', unsafe_allow_html=True)
        for space in spaces:
            space_title = space.get("title", "Career Space")
            space_description = space.get("description", "Description pending")
            st.markdown(f'''
            <div class="career-role">
                <div class="career-role-title">{space_title}</div>
                <div class="career-role-desc">{space_description}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Less Aligned Areas (NEW SECTION)
    less_aligned = field_data.get("lessAligned", [])
    if less_aligned:
        st.markdown('<h4 style="font-size: 17px; font-weight: 600; color: #202124; margin-bottom: 15px; margin-top: 25px;">Less Aligned Areas:</h4>', unsafe_allow_html=True)
        for item in less_aligned:
            area_name = item.get("area", "Area")
            reason = item.get("reason", "Reason pending")
            st.markdown(f'''
            <div class="less-aligned-item" style="background-color: #fef7e0; border-left: 4px solid #f9ab00; padding: 12px; margin-bottom: 8px; border-radius: 4px;">
                <div style="font-weight: 500; color: #202124; margin-bottom: 4px;">{area_name}</div>
                <div style="color: #5f6368; font-size: 15px;">{reason}</div>
            </div>
            ''', unsafe_allow_html=True)

def render_editable_career_field(field_data, field_key, field_index):
    """Render editable career field - UPDATED for spaces and lessAligned"""
    
    st.write(f"**Edit Career Field {field_index + 1}:**")
    
    # Title
    new_title = st.text_input(
        "Field Title",
        value=field_data.get("title", "Career Field"),
        key=f"career_title_{field_index}",
        label_visibility="collapsed"
    )
    career_data = session_manager.get_career_data()
    if career_data:
        career_data["careerFields"][field_key]["title"] = new_title
    
    # Alignment
    alignment_options = ["High", "Moderate", "Low"]
    current_alignment = field_data.get("alignment", "Unknown")
    new_alignment = st.selectbox(
        "Alignment",
        alignment_options,
        index=alignment_options.index(current_alignment) if current_alignment in alignment_options else 0,
        key=f"career_alignment_{field_index}"
    )
    if career_data:
        career_data["careerFields"][field_key]["alignment"] = new_alignment
    
    # Description
    new_description = st.text_area(
        "Description",
        value=field_data.get("description", "Analysis in progress"),
        key=f"career_desc_{field_index}",
        height=100,
        label_visibility="collapsed"
    )
    if career_data:
        career_data["careerFields"][field_key]["description"] = new_description
    
    # Career Spaces (changed from roles)
    spaces = field_data.get("spaces", [])
    if spaces:
        st.write("**Edit Career Spaces:**")
        for space_index, space in enumerate(spaces):
            col1, col2 = st.columns([1, 2])
            with col1:
                new_space_title = st.text_input(
                    f"Space {space_index + 1} Title",
                    value=space.get("title", "Career Space"),
                    key=f"space_title_{field_index}_{space_index}",
                    label_visibility="collapsed"
                )
            with col2:
                new_space_desc = st.text_area(
                    f"Space {space_index + 1} Description",
                    value=space.get("description", "Description pending"),
                    key=f"space_desc_{field_index}_{space_index}",
                    height=80,
                    label_visibility="collapsed"
                )
            
            # Update in session state
            if career_data:
                career_data["careerFields"][field_key]["spaces"][space_index]["title"] = new_space_title
                career_data["careerFields"][field_key]["spaces"][space_index]["description"] = new_space_desc
    
    # Less Aligned Areas (NEW SECTION)
    less_aligned = field_data.get("lessAligned", [])
    if less_aligned:
        st.write("**Edit Less Aligned Areas:**")
        for less_index, item in enumerate(less_aligned):
            col1, col2 = st.columns([1, 2])
            with col1:
                new_area_name = st.text_input(
                    f"Less Aligned {less_index + 1} Area",
                    value=item.get("area", "Area"),
                    key=f"less_area_{field_index}_{less_index}",
                    label_visibility="collapsed"
                )
            with col2:
                new_area_reason = st.text_area(
                    f"Less Aligned {less_index + 1} Reason",
                    value=item.get("reason", "Reason pending"),
                    key=f"less_reason_{field_index}_{less_index}",
                    height=70,
                    label_visibility="collapsed"
                )
            
            # Update in session state
            if career_data:
                career_data["careerFields"][field_key]["lessAligned"][less_index]["area"] = new_area_name
                career_data["careerFields"][field_key]["lessAligned"][less_index]["reason"] = new_area_reason
