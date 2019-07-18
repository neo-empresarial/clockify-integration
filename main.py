import models
import config.settings
import requests
import os 
from models import TimeEntry, Activity

workspace_id = os.getenv("CLOCKIFY_WORKSPACE_ID")

base_api_url = "https://api.clockify.me/api/"
headers = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}

def fetch_time_entries():
    for page in range(200):
        url = "{}workspaces/{}/timeEntries/?page={}".format(base_api_url, workspace_id, page)
        responses = requests.get(url, headers=headers)
        for response in responses.json():
            r = response
            if r['tags'] and Activity.where('name', r['task']['name']).first():
                TimeEntry.create(
                        start= r['timeInterval']['start'],
                        end= r['timeInterval']['end'],
                        description= r['description'],
                        activity_id= Activity.where('name', r['task']['name']).first().id ,
                        project_id= r['project']['id'],
                        member_id= r['user']['id'],
                        client_id= r['tags'][0]['id'],
                        clockify_id= r['id'] 
                )

if __name__ == "__main__":
    test()