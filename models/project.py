from orator import Model
from .config import V1_API_URL, WORKSPACE_ID, HEADERS
import requests


class Project(Model):

    __table__ = "project"
    __fillable__ = ["clockify_id", "name"]
    __primary_key__ = "clockify_id"

    @classmethod
    def save_from_clockify(cls):
        """Check if all projects in clockify are register as projects in the database.
        Create a new project if necessary."""
        projects = cls.fetch_all_projects()
        for project in projects:
            Project.update_or_create({"clockify_id":project["clockify_id"]},
                                     {"name":project["name"]})
        return projects

    @staticmethod
    def fetch_all_projects():
        """Find all projects on NEO's workspace.

        Returns list of dictionaries containing "name", "clockify_id"
        for every project."""

        url = "{}/workspaces/{}/projects".format(V1_API_URL, WORKSPACE_ID)
        responses = requests.get(url, headers=HEADERS)
        return [
            {"name": project["name"], "clockify_id": project["id"]}
            for project in responses.json()
        ]
