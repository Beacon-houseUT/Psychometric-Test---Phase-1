import requests

N8N_WEBHOOK_URL = "https://uttarika.app.n8n.cloud/webhook/google-export"  # Replace with your actual webhook if different

def request_google_export(payload: dict) -> dict:
    """
    Sends a POST request to the n8n webhook to export the report to Google Docs.

    Args:
        payload (dict): The complete data structure containing psychometricData and careerData

    Returns:
        dict: A dictionary with either {"success": True, "documentUrl": "..."} or {"success": False, "error": "..."}
    """
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Assume the n8n workflow returns { documentUrl: "...", ... }
        if "documentUrl" in data:
            return {
                "success": True,
                "documentUrl": data["documentUrl"]
            }
        else:
            return {
                "success": False,
                "error": "No document URL returned from n8n"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }
