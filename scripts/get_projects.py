import requests
import os
from dotenv import load_dotenv

load_dotenv()

WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
BASE_API_URL = "https://api.clockify.me/api/v1"
HEADER = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}


def parse_all_projects():
    """Find all projects on NEO's workspace.

    Returns list of dictionaries containing "name", "clockify_id"
    for every project."""

    url = "{}/workspaces/{}/projects".format(BASE_API_URL, WORKSPACE_ID)
    responses = requests.get(url, headers=HEADER)
    return [
        {"name": project["name"], "clockify_id": project["id"]}
        for project in responses.json()
    ]
