import requests
import os
from dotenv import load_dotenv

load_dotenv()

WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
BASE_API_URL = "https://api.clockify.me/api/v1"
HEADER = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}


def get_all_users():
    """Find all users from Clockify on NEO's workspace.

    Returns list of dictionaries containing "acronym", "clockify_id" and "email"
    of every user."""

    url = "{}/workspace/{}/users".format(BASE_API_URL, WORKSPACE_ID)
    responses = requests.get(url, headers=HEADER)
    users = []
    for user in responses.json():
        acronym = user["name"]
        clockify_id = user["id"]
        email = user["email"]
        user_dict = {"acronym": acronym, "clockify_id": clockify_id, "email": email}
        users.append(user_dict)
    return users
