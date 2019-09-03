import os

V1_API_URL = "https://api.clockify.me/api/v1"
WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
HEADERS = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}
