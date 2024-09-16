import os
import requests

def get_access_token():
    # OAuth 2.0 client credentials flow to get an access token
    data = {
        "client_id": os.getenv('AZURE_CLIENT_ID'),
        "scope": " ".join(os.getenv('SCOPES', "").split()),
        "client_secret": os.getenv('CLIENT_SECRET'),
        "grant_type": "client_credentials"
    }

    response = requests.post(f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}/oauth2/v2.0/token", data=data)
    
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        raise Exception(f"Failed to obtain access token: {response.content}")