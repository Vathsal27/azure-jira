import requests
from .ms_auth import get_access_token
import os
import datetime

def subscribe_to_folder():
    url = "https://graph.microsoft.com/v1.0/subscriptions"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "changeType": "created",
        "notificationUrl": "https://yourapp.com/log_event",  # Replace with your actual URL
        "resource": f"/me/drive/root:/{os.getenv('FILE_NAME')}:/children",
        "expirationDateTime": datetime.datetime.utcnow() + datetime.timedelta(days=2*365)
        # "expirationDateTime": "2024-12-31T11:00:00.000Z"
        # "clientState": "secretClientValue"  # Optional, can be omitted
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()