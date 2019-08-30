import models
import config.settings
import requests
import os
from models import TimeEntry, Activity, Client, Member, Project
from scripts import get_all_users, get_all_tasks, parse_all_projects, parse_all_tags

WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
BASE_API_URL = "https://api.clockify.me/api/"
HEADER = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}


def fetch_members():
    """Check if all users in clockify are register as members in the database.
       Create a new member if necessary."""
    users = get_all_users()
    for user in users:
        member = Member.where("clockify_id", user["clockify_id"]).first()
        if member is None:
            Member.create(
                clockify_id=user["clockify_id"],
                acronym=user["acronym"],
                email=user["email"],
            )
    return users


def fetch_activities():
    """Check if all tasks in clockify are register as activities in the database.
       Create a new activity if necessary."""
    tasks = get_all_tasks()
    for task in tasks:
        activity = Activity.where("name", task).first()
        if activity is None:
            Activity.create(name=task)
    return tasks


def fetch_projects():
    """Check if all projects in clockify are register as projects in the database.
       Create a new project if necessary."""
    projects = parse_all_projects()
    for project in projects:
        db_project = Project.where("clockify_id", project["clockify_id"]).first()
        if db_project is None:
            Project.create(clockify_id=project["clockify_id"], name=project["name"])
    return projects


def fetch_clients():
    """Check if all tags in clockify are register as clients in the database.
       Create a new client if necessary."""
    tags = parse_all_tags()
    for tag in tags:
        client = Client.where("clockify_id", tag["clockify_id"]).first()
        if client is None:
            Client.create(clockify_id=tag["clockify_id"], name=tag["name"])
    return tags


def fetch_users_time_entries(users):
    API_URL = "https://api.clockify.me/api/v1"
    for user in users:
        url = "{}/workspaces/{}/user/{}/time-entries?hydrated=true&page-size=1000&start=2019-08-05T00:00:01Z".format(
            API_URL, WORKSPACE_ID, user["clockify_id"]
        )
        time_entries = requests.get(url, headers=HEADER)
        for time_entry in time_entries.json():
            db_time_entry = TimeEntry.where("clockify_id", time_entry["id"]).first()
            if db_time_entry is None:
                try:
                    if time_entry["timeInterval"]["end"] is not None:
                        TimeEntry.create(
                            clockify_id=time_entry["id"],
                            member_id=time_entry["userId"],
                            project_id=time_entry["projectId"],
                            activity_id=Activity.where(
                                "name", time_entry["task"]["name"]
                            )
                            .first()
                            .id,
                            client_id=time_entry["tags"][0]["id"],
                            start=time_entry["timeInterval"]["start"],
                            end=time_entry["timeInterval"]["end"],
                            description=time_entry["description"],
                        )
                    else:
                        print("No end time")
                        print(time_entry)
                except TypeError:
                    print("No task")
                    print(time_entry)
                except IndexError:
                    print("no tag")
                    print(time_entry)


def fetch_time_entries():
    for page in range(200):
        url = "{}workspaces/{}/timeEntries/?page={}".format(
            BASE_API_URL, WORKSPACE_ID, page
        )
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


if __name__ == "__main__":
    users = fetch_members()
    activities = fetch_activities()
    projects = fetch_projects()
    clients = fetch_clients()
    fetch_users_time_entries(users)
