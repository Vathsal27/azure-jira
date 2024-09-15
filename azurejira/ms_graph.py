import requests
from .ms_auth import get_access_token

def subscribe_to_folder():
    url = "https://graph.microsoft.com/v1.0/subscriptions"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    data = {
        "changeType": "created",
        "notificationUrl": "https://yourapp.com/log_event",  # Replace with your actual URL
        "resource": "/me/drive/root:/Jira Tasks:/children",
        "expirationDateTime": "2024-12-31T11:00:00.000Z",
        "clientState": "secretClientValue"  # Optional, can be omitted
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
