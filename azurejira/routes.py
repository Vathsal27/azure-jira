from azurejira import app
from flask import request, jsonify
import logging

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

# @app.route('/')
# def index():
#     return {"status":200}