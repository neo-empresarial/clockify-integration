from models import *
from orator.orm import belongs_to_many
import requests


class Project(Model):

    __table__ = "project"
    __fillable__ = ["clockify_id", "name", "archived"]
    __primary_key__ = "id"
    __incrementing__ = True

    @belongs_to_many("project_activity", "project_id", "activity_id")
    def activities(self):
        from models import Activity

        return Activity

    @classmethod
    def create_default(cls, name):
        """Create project with default activities"""
        template = Project.first()
        try:
            cls.create({"name": name})
        except:
            pass

    @classmethod
    def save_from_clockify(cls):
        """Check if all projects in clockify are register as projects in the database.
        Create a new project if necessary."""
        projects = cls.fetch_all_projects()
        for project in projects:
            Project.update_or_create(
                {"clockify_id": project["clockify_id"]}, {"name": project["name"]}
            )
        return projects

    @staticmethod
    def fetch_all_projects(archived=0):
        """Find all projects on NEO's workspace.
        Use the parameter archived="" to retrieve all projects.
        Use the parameter archived=0 to retrieve all active projects.
        Use the parameter archived=1 to retrieve all archived projects.
        Returns list of dictionaries containing "name", "clockify_id"
        for every project."""

        url = "{}/workspaces/{}/projects?page-size=100&archived={}"
        url = url.format(V1_API_URL, WORKSPACE_ID, archived)
        responses = requests.get(url, headers=HEADERS)
        return [
            {"name": project["name"].lower(), "clockify_id": project["id"]}
            for project in responses.json()
        ]
