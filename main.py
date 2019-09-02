from models import TimeEntry, Activity
import requests
import os

WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
API_URL = "https://api.clockify.me/api/"
HEADER = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}


def deprecated_fetch_time_entries():
    for page in range(200):
        url = "{}workspaces/{}/timeEntries/?page={}".format(API_URL, WORKSPACE_ID, page)
        responses = requests.get(url, headers=HEADER)
        for response in responses.json():
            r = response
            if r["tags"] and Activity.where("name", r["task"]["name"]).first():
                TimeEntry.create(
                    start=r["timeInterval"]["start"],
                    end=r["timeInterval"]["end"],
                    description=r["description"],
                    activity_id=Activity.where("name", r["task"]["name"]).first().id,
                    project_id=r["project"]["id"],
                    member_id=r["user"]["id"],
                    client_id=r["tags"][0]["id"],
                    clockify_id=r["id"],
                )
