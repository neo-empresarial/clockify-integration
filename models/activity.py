from itertools import chain
from orator import Model
from models import API_URL, WORKSPACE_ID, HEADERS
import requests


class Activity(Model):

    __table__ = "activity"
    __fillable__ = ["name"]
    __primary_key__ = "id"

    @classmethod
    def save_from_clockify(cls):
        """Check if all tasks in clockify are register as activities in the database.
        Create a new activity if necessary."""
        tasks = cls.get_all_tasks()
        for task in tasks:
            activity = Activity.where("name", task).first()
            if activity is None:
                Activity.create(name=task)
        return tasks

    @classmethod
    def get_all_tasks(cls):
        """Get all unique tasks from clockify"""
        projects_ids = [x["clockify_id"] for x in cls.get_all_projects_id()]
        tasks = list(map(cls.get_all_project_tasks, projects_ids))
        unique_tasks = list(set(chain.from_iterable(tasks)))
        return unique_tasks

    @staticmethod
    def get_all_project_tasks(project_id):
        """Find all tasks from one project of Clockify on NEO's workspace.

        Returns list of dictionaries containing "name" of every task."""

        url = "{}/workspaces/{}/projects/{}/tasks".format(
            API_URL, WORKSPACE_ID, project_id
        )
        responses = requests.get(url, headers=HEADERS)
        return [task["name"] for task in responses.json()]

    @staticmethod
    def get_all_projects_id():
        """Get all projects ids from clockify.

        This is used later to get all workspaces tasks"""

        url = "{}/workspaces/{}/projects".format(API_URL, WORKSPACE_ID)
        responses = requests.get(url, headers=HEADERS)
        return [
            {"clockify_id": project["id"], "name": project["name"]}
            for project in responses.json()
        ]
