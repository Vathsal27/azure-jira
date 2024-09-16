from azurejira import app
from flask import request, jsonify
import logging
from .utils import download_excel_file, display_excel_file, create_jira_ticket

@app.route('/log_event', methods=['POST'])
def log_event():
    event_data = request.json
    file_name = event_data['resourceData']['name']
    event_time = event_data['subscriptionExpirationDateTime']
    uploader = event_data.get('uploader', 'Unknown')

    logging.info(f"File uploaded: {file_name}")
    logging.info(f"Event time: {event_time}")
    logging.info(f"Uploader: {uploader}")

    return jsonify({"message": "Event logged successfully"})

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