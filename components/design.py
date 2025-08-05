import streamlit as st

def apply_styling():
    """Apply all CSS styling to the Streamlit app"""
    
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global styles */
        .main > div {
            max-width: 8.5in;
            margin: 0 auto;
            padding: 1in 1in;
            background-color: white;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #202124;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Document container */
        .doc-container {
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin: 20px auto;
            padding: 0;
        }
        
        /* Title styles */
        .doc-title {
            font-size: 28px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 8px;
            color: #202124;
            border-bottom: none;
        }
        
        .doc-subtitle {
            font-size: 18px;
            font-weight: 400;
            text-align: center;
            margin-bottom: 40px;
            color: #5f6368;
        }
        
        /* Student info header */
        .student-header {
            border-bottom: 1px solid #dadce0;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .student-name {
            font-size: 25px !important;
            font-weight: 600;
            margin-bottom: 5px;
            color: #202124;
        }
        
        .student-details {
            font-size: 17px;
            color: #5f6368;
            margin-bottom: 10px;
        }
        
        .personality-type {
            font-size: 18px;
            font-weight: 500;
            color: #1a73e8;
            margin-top: 10px;
        }
        
        /* Section headers */
        .section-title {
            font-size: 25px !important;
            font-weight: 600;
            margin-top: 40px;
            margin-bottom: 8px;
            color: #202124;
        }
        
        .section-subtitle {
            font-size: 17px;
            color: #5f6368;
            margin-bottom: 20px;
            font-style: normal;
            line-height: 1.5;
        }
        
        /* Table styles */
        .doc-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 17px;
        }
        
        .doc-table th {
            background-color: #f8f9fa;
            border: 1px solid #dadce0;
            padding: 12px;
            text-align: left;
            font-weight: 500;
            color: #202124;
        }
        
        .doc-table td {
            border: 1px solid #dadce0;
            padding: 12px;
            vertical-align: top;
            color: #202124;
        }
        
        .doc-table tr:nth-child(even) {
            background-color: #fafafa;
        }
        
        /* Insight boxes */
        .insight-box {
            background-color: #f8f9fa;
            border-left: 4px solid #1a73e8;
            padding: 16px;
            margin: 20px 0;
            font-style: normal;
            color: #5f6368;
            font-size: 17px;
        }
        
        .insight-label {
            font-weight: 500;
            color: #202124;
            font-style: normal;
        }
        
        /* Edit mode styles */
        .edit-notice {
            background-color: #fff3e0;
            border: 1px solid #ffb74d;
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 4px;
            font-size: 17px;
            color: #e65100;
        }
        
        /* Button styles */
        .stButton > button {
            background-color: #1a73e8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
            font-size: 17px;
        }
        
        .stButton > button:hover {
            background-color: #1557b0;
        }
        
        /* Google Export Button */
        .google-export-btn {
            background-color: #4285f4 !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 12px 24px !important;
            font-weight: 500 !important;
            font-size: 17px !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        
        .google-export-btn:hover {
            background-color: #3367d6 !important;
        }
        
        /* Google Auth Status */
        .auth-status {
            background-color: #e8f5e8;
            border: 1px solid #4caf50;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
            font-size: 17px;
            color: #2e7d32;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .auth-status.disconnected {
            background-color: #fff3e0;
            border: 1px solid #ff9800;
            color: #e65100;
        }
        
        /* Form styles */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-family: 'Inter', sans-serif;
            font-size: 17px;
        }
        
        /* Career section */
        .career-section {
            margin-top: 50px;
            border-top: 2px solid #dadce0;
            padding-top: 30px;
        }
        
        .career-title {
            font-size: 25px;
            font-weight: 600;
            margin-bottom: 30px;
            color: #202124;
            text-align: center;
        }
        
        .career-field {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #dadce0;
            border-radius: 4px;
            font-size: 17px;
        }
        
        .career-field-title {
            font-size: 25px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #202124;
        }
        
        .alignment-high { 
            color: #137333; 
            font-weight: 500; 
            font-size: 17px;
        }
        
        .alignment-moderate { 
            color: #ea8600; 
            font-weight: 500; 
            font-size: 17px;
        }
        
        .alignment-low { 
            color: #d93025; 
            font-weight: 500; 
            font-size: 17px;
        }
        
        .career-role {
            margin: 15px 0;
            padding: 12px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        
        .career-role-title {
            font-weight: 500;
            color: #202124;
            margin-bottom: 4px;
            font-size: 17px;
        }
        
        .career-role-desc {
            color: #5f6368;
            font-size: 17px;
        }

        .less-aligned-item {
            background-color: #fef7e0;
            border-left: 4px solid #f9ab00;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 4px;
        }
        
        
        /* Loading states */
        .stSpinner {
            text-align: center;
        }
        
        /* Summary table styles */
        .summary-table {
            margin: 20px 0;
            background-color: #f8f9fa;
            border-radius: 4px;
            padding: 20px;
        }
        
        /* Export section */
        .export-section {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid #dadce0;
            background-color: #f8f9fa;
            padding: 30px;
            border-radius: 4px;
        }
        
        .export-title {
            font-size: 25px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #202124;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
