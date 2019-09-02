from orator import Model
from orator.orm import belongs_to
from models import Activity, Client, Member, Project
from .config import V1_API_URL, WORKSPACE_ID, HEADERS
import requests


class TimeEntry(Model):
    __table__ = "time_entry"
    __fillable__ = [
        "clockify_id",
        "member_id",
        "project_id",
        "activity_id",
        "client_id",
        "start",
        "end",
        "description",
        "created_at",
        "updated_at",
    ]
    __primary_key__ = "clockify_id"

    @belongs_to("member_id", "clockify_id")
    def member(self):
        return Member

    @belongs_to("project_id", "clockify_id")
    def project(self):
        return Project

    @belongs_to("activity_id", "id")
    def activity(self):
        return Activity

    @belongs_to("client_id", "clockify_id")
    def client(self):
        return Client

    @staticmethod
    def save_from_clockify():
        for member in Member.all():
            url = "{}/workspaces/{}/user/{}/time-entries?hydrated=true&page-size=1000&start=2019-08-05T00:00:01Z".format(
                V1_API_URL, WORKSPACE_ID, member["clockify_id"]
            )
            time_entries = requests.get(url, headers=HEADERS)
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
