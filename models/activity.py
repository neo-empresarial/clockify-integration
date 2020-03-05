from models import *
from itertools import chain

from orator.orm import belongs_to_many

import requests


class Activity(Model):

    __table__ = "activity"
    __fillable__ = ["clockify_id", "name"]
    __primary_key__ = "id"
    __incrementing__ = True

    @belongs_to_many("project_activity", "activity_id", "project_id")
    def projects(self):
        from models import Project

        return Project

    @classmethod
    def save_from_clockify(cls):
        """Check if all tasks in clockify are register as activities in the database.
        Create a new activity if necessary."""
        tasks = cls.fetch_all_task()
        for task in tasks:
            Activity.first_or_create(name=task)
        return tasks

    @classmethod
    def fetch_all_task(cls):
        """Find all unique tasks from all project of Clockify on NEO's workspace.

        Returns list of dictionaries containing "name" of every task."""
        projects_ids = [project["clockify_id"] for project in cls.get_all_projects_id()]
        tasks = list(map(cls.fetch_project_tasks, projects_ids))
        unique_tasks = list(set(chain.from_iterable(tasks)))
        return unique_tasks

    @staticmethod
    def fetch_project_tasks(project_id):
        """Find all tasks from one project of Clockify on NEO's workspace.

        Returns list of dictionaries containing "name" of every task."""

        url = "{}/workspaces/{}/projects/{}/tasks".format(
            V1_API_URL, WORKSPACE_ID, project_id
        )
        responses = requests.get(url, headers=HEADERS)
        return [task["name"].lower() for task in responses.json()]

    @staticmethod
    def get_all_projects_id():
        """Get all projects ids from clockify.

        This is used later to get all workspaces tasks"""

        url = "{}/workspaces/{}/projects".format(V1_API_URL, WORKSPACE_ID)
        responses = requests.get(url, headers=HEADERS)
        return [
            {"clockify_id": project["id"], "name": project["name"].lower()}
            for project in responses.json()
        ]

    @staticmethod
    def map_all_activities():
        """Returns a dictionary of all activities in database. Dictionary key is activity
           name. This should be used to reduce Queries to our DB in other functions."""

        activities_map = {}
        for activity in Activity.all():
            activities_map[activity.name] = {"id": activity.id}
        return activities_map
