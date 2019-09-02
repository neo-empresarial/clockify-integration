import models
import config.settings
import requests
import os
from models import TimeEntry, Activity, Client, Member, Project
from scripts import FetchDataClockify

WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
BASE_API_URL = "https://api.clockify.me/api/"
HEADER = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}

def update_or_create_members():
    """Check if all users in clockify are register as members in the database.
       Create a new member if necessary."""
    users = FetchDataClockify().fetch_all_users()
    for user in users:
        Member.update_or_create({"clockify_id":user["clockify_id"]},
                                {"acronym":user["acronym"],
                                 "email":user["email"]})
    return users


def first_or_create_activities():
    """Check if all tasks in clockify are register as activities in the database.
       Create a new activity if necessary."""
    tasks = FetchDataClockify().fetch_all_tasks()
    for task in tasks:
        Activity.first_or_create(name=task)
    return tasks


def update_or_create_projects():
    """Check if all projects in clockify are register as projects in the database.
       Create a new project if necessary."""
    projects = FetchDataClockify().fetch_all_projects()
    for project in projects:
        Project.update_or_create({"clockify_id":project["clockify_id"]},
                                 {"name":project["name"]})
    return projects


def update_or_create_clients():
    """Check if all tags in clockify are register as clients in the database.
       Create a new client if necessary."""
    tags = FetchDataClockify().fetch_all_tags()
    for tag in tags:
        Client.update_or_create({"clockify_id":tag["clockify_id"]},
                                {"name":tag["name"]})
    return tags


def update_or_create_users_time_entries(users):
    """Check if all time entries in clockify are register in the database.
       Create a new time entry if necessary."""
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
                            activity_id=Activity.where("name", time_entry["task"]["name"]).first().id,
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


if __name__ == "__main__":
    users = update_or_create_members()
    activities = first_or_create_activities()
    projects = update_or_create_projects()
    clients = update_or_create_clients()
    update_or_create_users_time_entries(users)
