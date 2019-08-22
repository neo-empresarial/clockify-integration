import requests
import os
from dotenv import load_dotenv

load_dotenv()

WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
BASE_API_URL = "https://api.clockify.me/api/v1"
HEADER = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}


def parse_all_tags():
    """Find all tags from Clockify on NEO's workspace.

    Returns list of dictionaries containing "clockify_id" and "name"
    of every tag."""

    url = "{}/workspaces/{}/tags".format(BASE_API_URL, WORKSPACE_ID)
    responses = requests.get(url, headers=HEADER)
    return [
        {"clockify_id": client["id"], "name": client["name"]}
        for client in responses.json()
    ]
