from azurejira import app
from flask import request, jsonify
import logging
from .utils import download_excel_file, display_excel_file, create_jira_ticket
from msal import ConfidentialClientApplication
import os
import sys
import requests
from .ms_auth import get_access_token
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]  # Output logs to stdout for Render
)

# @app.route('/log_event', methods=['POST'])
# def log_event():
#     event_data = request.json
#     file_name = event_data['resourceData']['name']
#     event_time = event_data['subscriptionExpirationDateTime']
#     uploader = event_data.get('uploader', 'Unknown')

#     logging.info(f"File uploaded: {file_name}")
#     logging.info(f"Event time: {event_time}")
#     logging.info(f"Uploader: {uploader}")

#     return jsonify({"message": "Event logged successfully"})


@app.route('/log_event', methods=['POST'])
def log_event():
    try:
        event_data = request.json
        logging.info(f"Received event: {event_data}")

        if event_data['resource'] == f"/me/drive/root:/{os.getenv('FILE_NAME')}":
            file_info = requests.get(
                f"https://graph.microsoft.com/v1.0/me/drive/root:/{os.getenv('FILE_NAME')}",
                headers={'Authorization': f'Bearer {get_access_token()}'}
            ).json()
            logging.info(f"File details: {file_info}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def index():
    return {
        "status":200,
        "message":"APIs working properly"
    }

# @app.route('/create_jira_tickets', methods=['POST'])
# def create_jira_tickets():
#     event_data = request.json
#     file_id = event_data['resourceData']['id']  # Get the file ID from the event
#     file_name = event_data['resourceData']['name']

#     if not file_name.endswith('.xlsx'):
#         logging.warning(f"Uploaded file is not an Excel file: {file_name}")
#         return jsonify({"message": "File is not an Excel file"}), 400

#     # Download the file from Microsoft 365
#     download_excel_file(file_id)

#     # Extract data and create Jira tickets
#     display_excel_file(file_name)

#     return jsonify({"message": "File processed successfully"}), 200