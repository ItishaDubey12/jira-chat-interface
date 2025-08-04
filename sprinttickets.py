import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into the environment

//Config

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def create_sprint_tickets(df):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    auth = (JIRA_EMAIL, JIRA_API_TOKEN)

    created_issues = []
    errors = []

    for index, row in df.iterrows():
        try:
            summary = str(row['Summary']).strip()
            project_key = str(row['Project']).strip()
            issue_type = str(row['Issue Type']).strip()
            description = str(row['Description']).strip()

            payload = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": description
                                    }
                                ]
                            }
                        ]
                    },
                    "issuetype": {"name": issue_type}
                }
            }

            response = requests.post(f"{JIRA_URL}/rest/api/3/issue", 
                                     json=payload, 
                                     headers=headers, 
                                     auth=auth)

            if response.status_code == 201:
                issue_key = response.json().get('key')
                created_issues.append(issue_key)
            else:
                error_text = response.text
                errors.append(f"Row {index + 1}: {response.status_code} - {error_text}")

        except Exception as e:
            errors.append(f"Row {index + 1}: Exception - {str(e)}")

    if created_issues:
        return f"✅ Tickets created: {', '.join(created_issues)}"
    else:
        return f"❌ No tickets created. Errors: {errors}"
