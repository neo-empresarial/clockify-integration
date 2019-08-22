import requests
import os
from dotenv import load_dotenv
from itertools import chain

load_dotenv()

WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
BASE_API_URL = "https://api.clockify.me/api/v1"
HEADER = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}

def get_all_project_tasks(project_id):
    """Find all tasks from one project of Clockify on NEO's workspace.

    Returns list of dictionaries containing "name" of every task."""

    url = "{}/workspaces/{}/projects/{}/tasks".format(BASE_API_URL, WORKSPACE_ID, project_id)
    responses = requests.get(url, headers=HEADER)
    return [
        task["name"]
        for task in responses.json()
    ]

def get_all_projects_id():
    """Get all projects ids from clockify.

    This is used later to get all workspaces tasks"""

    url = "{}/workspaces/{}/projects".format(BASE_API_URL, WORKSPACE_ID)
    responses = requests.get(url, headers=HEADER)
    return [
        {"clockify_id": project["id"], "name": project["name"]}
        for project in responses.json()
    ]

def get_all_tasks():
    """Get all unique tasks from clockify"""
    projects_ids = [x["clockify_id"] for x in get_all_projects_id()]
    tasks = list(map(get_all_project_tasks, projects_ids))
    unique_tasks = list(set(chain.from_iterable(tasks)))
    return unique_tasks
