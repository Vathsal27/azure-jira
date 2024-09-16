import requests
from .ms_auth import get_access_token
import os
import logging
import pandas as pd

def download_excel_file(file_id):
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
    headers = {
        "Authorization": f"Bearer {get_access_token()}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Save the Excel file locally
        file_path = os.path.join('files', f"{file_id}.xlsx")
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path
    else:
        logging.error(f"Failed to download file: {response.status_code}")
        raise Exception("File download failed")

def process_excel_file(file_name):
    # Load the Excel file into a Pandas DataFrame
    file_path = os.path.join('files', file_name)
    xls = pd.ExcelFile(file_path)

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Process each row to create Jira tickets
        for index, row in df.iterrows():
            create_jira_ticket(row)

def display_excel_file(file_name):
    # Load the Excel file into a Pandas DataFrame
    file_path = os.path.join('files', file_name)
    xls = pd.ExcelFile(file_path)

    for sheet_name in xls.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Display each row instead of creating Jira tickets
        for index, row in df.iterrows():
            print(f"Row {index + 1}:")
            print(row)
            print("-----------------------")

def create_jira_ticket(row):
    url = f"{os.getenv('JIRA_BASE_URL')}/rest/api/3/issue"
    headers = {
        "Authorization": f"Basic {os.getenv('JIRA_USER')}:{os.getenv('JIRA_API_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    # Construct the issue data from the Excel row
    issue_data = {
        "fields": {
            "project": {"key": os.getenv('JIRA_PROJECT_KEY')},
            "summary": row['Summary'],  # Assuming 'Summary' is a column in the Excel file
            "description": row['Description'],
            "issuetype": {"name": "Task"},
            "assignee": {"emailAddress": row['Assignee']}
        }
    }
    
    response = requests.post(url, json=issue_data, headers=headers)
    
    if response.status_code == 201:
        logging.info(f"Created Jira ticket: {response.json()['key']}")
    else:
        logging.error(f"Failed to create Jira ticket: {response.content}")

