from models import *
from orator.orm import belongs_to_many, belongs_to
import requests


class Project(Model):

    __table__ = "project"
    __fillable__ = ["clockify_id", "client_id", "name"]
    __primary_key__ = "id"
    __incrementing__ = True

    @belongs_to("client_id", "id")
    def client(self):
        return Client

    @belongs_to_many("project_activity", "project_id", "activity_id")
    def activities(self):
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
    def save_from_clockify(cls, archived=0):
        """Check if all projects in clockify are register as projects in the database.
           Create a new project if necessary.
           Use the parameter archived="" to retrieve all projects.
           Use the parameter archived=0 to retrieve all active projects.
           Use the parameter archived=1 to retrieve all archived projects."""
        projects = cls.fetch_all_projects(archived)
        clients_dict = Client.map_all_clients()
        for project in projects:
            Project.update_or_create(
                {"clockify_id": project["clockify_id"]},
                {
                    "client_id": clients_dict[project["client_id"]]["id"],
                    "name": project["name"],
                },
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
            {
                "name": project["name"].lower(),
                "clockify_id": project["id"],
                "client_id": project["clientId"],
            }
            for project in responses.json()
        ]

    @staticmethod
    def map_all_projects():
        """Returns a dictionary of all projects in database. Dictionary key is project
           clockify id. This should be used to reduce Queries to our DB in other functions."""

        projects_map = {}
        for project in Project.all():
            projects_map[project.clockify_id] = {
                "id": project.id,
                "name": project.name,
                "client_id": project.client_id,
            }
        return projects_map
