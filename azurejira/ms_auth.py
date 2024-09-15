import msal
from .config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, SCOPES

def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=SCOPES)
    return result['access_token']