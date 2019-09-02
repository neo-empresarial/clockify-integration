import requests
import os
from dotenv import load_dotenv
from itertools import chain

load_dotenv()

class FetchDataClockify():
    def __init__(self):

        self.WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
        self.BASE_API_URL = "https://api.clockify.me/api/v1"
        self.HEADERS = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}


    def fetch_all(self):
        """Find all users, project, tags and tasks from Clockify"""
        return [
            self.fetch_all_users(),
            self.fetch_all_projects(),
            self.fetch_all_tags(),
            self.fetch_all_tasks()
        ]


    def fetch_all_users(self):
        """Find all users from Clockify on NEO's workspace.

        Returns list of dictionaries containing "acronym", "clockify_id" and "email"
        of every user."""

        url = "{}/workspace/{}/users".format(self.BASE_API_URL, self.WORKSPACE_ID)
        responses = requests.get(url, headers=self.HEADERS)
        return [
            {"acronym": user["name"], "clockify_id": user["id"], "email": user["email"]}
            for user in responses.json()
        ]


    def fetch_all_projects(self):
        """Find all projects on NEO's workspace.

        Returns list of dictionaries containing "name", "clockify_id"
        for every project."""

        url = "{}/workspaces/{}/projects".format(self.BASE_API_URL, self.WORKSPACE_ID)
        responses = requests.get(url, headers=self.HEADERS)
        return [
            {"name": project["name"], "clockify_id": project["id"]}
            for project in responses.json()
        ]


    def fetch_project_tasks(self, project_id):
        """Find all tasks from one project of Clockify on NEO's workspace.

        Returns list of dictionaries containing "name" of every task."""

        url = "{}/workspaces/{}/projects/{}/tasks".format(self.BASE_API_URL, self.WORKSPACE_ID, project_id)
        responses = requests.get(url, headers=self.HEADERS)
        return [
            task["name"]
            for task in responses.json()
        ]


    def fetch_all_tasks(self):
        """Find all unique tasks from all project of Clockify on NEO's workspace.

        Returns list of dictionaries containing "name" of every task."""

        projects_ids = [project["clockify_id"] for project in self.fetch_all_projects()]
        tasks = list(map(self.fetch_project_tasks, projects_ids))
        unique_tasks = list(set(chain.from_iterable(tasks)))
        return unique_tasks


    def fetch_all_tags(self):
        """Find all tags from Clockify on NEO's workspace.

        Returns list of dictionaries containing "clockify_id" and "name"
        of every tag."""

        url = "{}/workspaces/{}/tags".format(self.BASE_API_URL, self.WORKSPACE_ID)
        responses = requests.get(url, headers=self.HEADERS)
        return [
            {"clockify_id": client["id"], "name": client["name"]}
            for client in responses.json()
        ]
