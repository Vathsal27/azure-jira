from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    """
    Acquires an access token for Microsoft Graph API using MSAL library.

    Returns:
        str: Access token on success, None on failure.
    """
    # Configure the application
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    authority = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"
    scopes = ["https://graph.microsoft.com/.default"]  # Use the correct scope

    try:
        # Create a confidential client application
        app = ConfidentialClientApplication(
            client_id=client_id,
            authority= authority,
            client_credential=client_secret
        )

        # Acquire a token
        result = app.acquire_token_for_client(scopes=scopes)
        if result:
            return result['access_token']
        else:
            return None

    except Exception as e:
        print(f"Failed to obtain access token: {e}")
        return None

# def get_access_token():
#     client_id = os.getenv("AZURE_CLIENT_ID")
#     tenant_id = os.getenv("AZURE_TENANT_ID")
#     authority = f"https://login.microsoftonline.com/{tenant_id}"
#     scopes = ["https://graph.microsoft.com/.default"]

#     app = PublicClientApplication(client_id, authority=authority)
    
#     # Try to acquire token silently
#     accounts = app.get_accounts()
#     if accounts:
#         result = app.acquire_token_silent(scopes, account=accounts[0])
#         if result:
#             return result['access_token']

#     # Acquire token interactively if silent acquisition fails
#     result = app.acquire_token_interactive(scopes)
#     return result['access_token']