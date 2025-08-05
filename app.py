import streamlit as st
from components import design, psychometric_analysis, career_analysis,google_export
from utils import session_manager

# ─── PAGE CONFIG ──────────────────────────────────
st.set_page_config(page_title="Psychometric Report", layout="centered")

# ─── INITIALIZE APPLICATION ─────────────────────────
def main():
    """Main application controller"""
    
    # Apply styling
    design.apply_styling()
    
    # Initialize session state
    session_manager.initialize_session()
    
    # Route to appropriate component based on state
    if not session_manager.is_form_submitted():
        # Show upload form
        psychometric_analysis.render_upload_form()
    
    elif session_manager.is_form_submitted() and not session_manager.has_report_data():
        # Show processing screen for psychometric analysis
        psychometric_analysis.process_uploaded_data()
    
    elif session_manager.is_processing_career_analysis():
        # Process career analysis request
        career_analysis.process_career_request()  # Correct function name
    
    else:
        # Display main report (this covers the case where we have report data)
        render_main_report()

def render_main_report():
    """Render the complete report with all sections"""
    
    # Render psychometric analysis
    psychometric_analysis.render_report()
    
    # Render career analysis if available
    if session_manager.has_career_data():
        career_analysis.render_career_section()
    
    # Render action buttons
    render_action_buttons()

def render_action_buttons():
    """Render all action buttons at the bottom"""
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Edit Report button - always visible
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        edit_label = "View Report" if session_manager.is_edit_mode() else "Edit Report"
        if st.button(edit_label, use_container_width=True):
            session_manager.toggle_edit_mode()
            st.rerun()
    
    # Edit mode controls
    if session_manager.is_edit_mode():
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Reset Changes", use_container_width=True):
                session_manager.reset_changes()
                st.rerun()
        
        with col3:
            if st.button("Save Changes", use_container_width=True):
                session_manager.save_changes()
                st.success("Changes saved!")
                st.rerun()
    
    # Main action buttons (only if not processing career analysis)
    if not session_manager.is_processing_career_analysis():
        st.markdown("<br>", unsafe_allow_html=True)
        
        if session_manager.has_career_data():
            # Show Career Reanalysis | Export to Google Docs | New Assessment
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("Career Reanalysis", use_container_width=True):
                    session_manager.request_career_reanalysis()
                    st.rerun()
            
            with col2:
                if st.button("Export to Google Docs", use_container_width=True):
                    request_google_export()
            
            with col3:
                if st.button("New Assessment", use_container_width=True):
                    session_manager.reset_all()
                    st.rerun()
        else:
            # Show Generate Career Pathways + New Assessment
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if not session_manager.is_edit_mode():
                    if st.button("Generate Career Pathways", use_container_width=True):
                        session_manager.request_career_analysis()
                        st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("New Assessment", use_container_width=True):
                    session_manager.reset_all()
                    st.rerun()

def request_google_export():
    """Request Google Docs export via N8N backend"""
    
    with st.spinner("Exporting to Google Docs..."):
        try:
            # Prepare the payload exactly as specified
            payload = {
                "psychometricData": session_manager.get_report_data(),
                "careerData": session_manager.get_career_data()
            }
            
            # Send to N8N export workflow
            result = google_export.request_google_export(payload)

            
            if result.get("success"):
                st.success("✅ Report exported to Google Docs successfully!")
                if result.get("documentUrl"):
                    st.markdown(f"📄 [Open Google Doc]({result['documentUrl']})")
                    st.markdown(f'''
                    <script>
                    window.open('{result["documentUrl"]}', '_blank');
                    </script>
                    ''', unsafe_allow_html=True)
            else:
                st.error(f"❌ Export failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")

if __name__ == "__main__":
    main()
