from azurejira import app
from flask import request, jsonify
import logging
from logging.handlers import RotatingFileHandler
from .utils import get_access_token
import sys
from .config import *

# Your secret client state from the subscription
CLIENT_STATE = 'secretClientValue'

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)  # Set the log level to INFO or as needed
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Ensure that Flask's default logging configuration does not override
app.logger.setLevel(logging.INFO)

@app.route('/microsoft365-webhook', methods=['POST'])
def microsoft365_webhook():
    # Log the incoming request
    app.logger.info("Webhook triggered with data: %s", request.json)

    data = request.json

    # Microsoft validation check
    if 'validationToken' in data:
        app.logger.info("Validation token received")
        return data['validationToken'], 200

    # Verify the subscription clientState
    if data['value'][0]['clientState'] != CLIENT_STATE:
        app.logger.warning("Client state mismatch")
        return "Client state mismatch", 400

    try:
        access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, TENANT_ID)
    except Exception as e:
        return app.logger.warning(f"Failed to get access token: {e}")

    # Handle the file change notifications
    for notification in data['value']:
        resource = notification['resource']
        event_type = notification['changeType']
        app.logger.info(f"File change detected: {resource} with event type: {event_type}")
        
        # Add your custom logic here (e.g., process file upload)

    app.logger.info("Webhook processed successfully")
    return jsonify({"status": "success"}), 200