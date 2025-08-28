import requests
import time
import streamlit as st

class N8NClient:
    """Client for communicating with N8N webhooks"""
    
    def __init__(self):
        self.base_url = "https://techbh.app.n8n.cloud/webhook"
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.headers.update({
            'User-Agent': 'StreamlitApp/1.0',
            'Connection': 'close'
        })
    
    def upload_psychometric_data(self, form_data, files, max_retries=3):
        """
        Upload form data and files to psychometric analysis webhook
        
        Args:
            form_data (dict): Form data with name, age, grade, fileCount
            files (list): List of file tuples for upload
            max_retries (int): Maximum retry attempts
        
        Returns:
            dict: Parsed response from webhook
        """
        
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = self.session.post(
                    f"{self.base_url}/google-report-upload",
                    data=form_data,
                    files=files,
                    timeout=(30, 180),  # (connection timeout, read timeout)
                    stream=False
                )
                response.raise_for_status()
                
                # Parse JSON response
                try:
                    payload = response.json()
                except ValueError:
                    text_response = response.text
                    raise Exception(f"Invalid JSON response: {text_response[:500]}...")
                
                # Validate response
                if not payload:
                    raise Exception("Empty response received from server")
                
                # Unwrap list response if needed
                if isinstance(payload, list) and payload:
                    payload = payload[0]
                
                return payload
                
            except (requests.exceptions.ConnectionError, 
                    requests.exceptions.ChunkedEncodingError,
                    requests.exceptions.Timeout) as e:
                retry_count += 1
                if retry_count < max_retries:
                    st.write(f"Connection issue, retrying... (attempt {retry_count + 1})")
                    time.sleep(2)  # Wait before retry
                    # Reset files for retry (files might be consumed)
                    for file_tuple in files:
                        if hasattr(file_tuple[1], 'seek'):
                            file_tuple[1].seek(0)
                else:
                    raise e
    
    def request_career_analysis(self, career_request_data):
        """
        Request career analysis from webhook
        
        Args:
            career_request_data (dict): Career analysis request data
        
        Returns:
            dict: Parsed career analysis response
        """
        
        try:
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
            
            response = self.session.post(
                f"{self.base_url}/google-career-analysis",
                json=career_request_data,
                timeout=(30, 120)
            )
            response.raise_for_status()
            
            # Parse career response
            career_data = response.json()
            if isinstance(career_data, list) and career_data:
                career_data = career_data[0]
            
            # Extract the actual career analysis from n8n structure
            if career_data.get("reportData") and career_data["reportData"].get("careerAnalysis"):
                return career_data["reportData"]["careerAnalysis"]
            else:
                # Fallback to direct structure
                return career_data
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to generate career recommendations: {e}")
        except Exception as e:
            raise Exception(f"An error occurred during career analysis: {e}")

    def request_google_export(self, payload):
        """
        Request Google Docs export from N8N workflow
        
        Args:
            payload (dict): Combined psychometric and career data
                           {"psychometricData": {...}, "careerData": {...}}
        
        Returns:
            dict: Export response with success status and document URL
        """
        
        try:
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
            
            response = self.session.post(
                f"{self.base_url}/google-export",  # Updated endpoint name
                json=payload,
                timeout=(30, 120)
            )
            response.raise_for_status()
            
            # Parse export response
            result = response.json()
            if isinstance(result, list) and result:
                result = result[0]
            
            return result
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to export to Google Docs: {e}")
        except Exception as e:
            raise Exception(f"An error occurred during export: {e}")

# Create singleton instance
n8n_client = N8NClient()
