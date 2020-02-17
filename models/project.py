from models import *
from orator.orm import belongs_to_many
import requests
import datetime


class Project(Model):

    __table__ = "project"
    __fillable__ = ["clockify_id", "name", "archived"]
    __primary_key__ = "id"
    __incrementing__ = True

    @belongs_to_many("project_activity", "project_id", "activity_id")
    def activities(self):
        from models import Activity

        return Activity

    @staticmethod
    def archive_project_clockify(project_clockify_id):
        """Archive a Project in clockify workspace.
           Returns the request response."""
        url_archive = "{}/workspaces/{}/projects/{}/archive".format(
            V0_API_URL, WORKSPACE_ID, project_clockify_id
        )
        return requests.get(url_archive, headers=HEADERS)

    @classmethod
    def check_and_change_to_archived(
        cls, project, last_time_entry, change_on_clockify=False, days_threshold=100
    ):
        """Given a project and its last time entry check if it should be archived in
           our database and, if change_on_clockify=True, in Clockify as well"""
        if last_time_entry is not None:
            diff = datetime.datetime.now() - last_time_entry.end
            if diff.days >= days_threshold:
                project.archived = True
                project.save()
                if change_on_clockify:
                    cls.update_project_clockify(project.clockify_id)
                return True

        return False

    @classmethod
    def archive_inactive_projects(cls):
        """Change all projects inactive with a time entry older than 100 days
           to archived in our database and in Clockify"""
        from models import TimeEntry

        projects = (
            Project.where("archived", "=", False).where("clockify_id", "!=", "").get()
        )
        for project in projects:
            time_entry = (
                TimeEntry.where("project_id", "=", project.id)
                .order_by("start", "desc")
                .first()
            )
            cls.check_and_change_to_archived(
                project, time_entry, change_on_clockify=True
            )

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
