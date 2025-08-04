import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into the environment

# ==== CONFIGURATION ====
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
SUBTASK_ISSUE_TYPE_ID = "10056"  # Replace with the actual ID from your JIRA setup

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def create_subtask(summary, parent_key):
    url = f"{JIRA_URL}/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": parent_key.split("-")[0]},
            "parent": {"key": parent_key},
            "summary": summary,
            "issuetype": {"id": SUBTASK_ISSUE_TYPE_ID}
        }
    }

    response = requests.post(
        url,
        headers=HEADERS,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
        json=payload
    )

    if response.status_code == 201:
        return f"✅ Sub-task '{summary}' created under {parent_key}"
    else:
        return f"❌ Failed to create sub-task '{summary}' under {parent_key}. Reason: {response.status_code} {response.text}"

def create_subtasks(df):
    logs = []
    required_columns = {"Summary", "Parent"}

    if not required_columns.issubset(df.columns):
        raise KeyError(f"Expected columns: {required_columns}")

    for _, row in df.iterrows():
        summary = str(row["Summary"]).strip()
        parent_key = str(row["Parent"]).strip()

        if summary and parent_key:
            result = create_subtask(summary, parent_key)
            logs.append(result)
        else:
            logs.append(f"⚠️ Skipped row with missing data: Summary={summary}, Parent={parent_key}")

    return "\n".join(logs)
