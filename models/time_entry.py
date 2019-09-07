from orator import Model
from orator.orm import belongs_to
import re
import requests
from models import Activity, Client, Member, Project
from .config import V1_API_URL, WORKSPACE_ID, HEADERS


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

    @classmethod
    def check_company_project(cls, match):
        if match[0][0] == "C":
            return Client.where("name", "CERTI").first().clockify_id
        elif match[0][0] == "E":
            return Client.where("name", "Embraco").first().clockify_id
        elif match[0][0] == "N":
            return Client.where("name", "NEO").first().clockify_id
        elif match[0][0] == "T":
            return Client.where("name", "Tupy").first().clockify_id
        elif match[0][0] == "W":
            return Client.where("name", "WEG").first().clockify_id
        else:
            print(match)
            raise ReferenceError("No client starts with this letter")

    @classmethod
    def correct_empty_wrong_tag(cls, time_entry):
        try:
            client_id = time_entry["tags"][0]["id"]
            project_name = Project.where("clockify_id", time_entry["projectId"]).first().name
            match = re.search("^([A-Z])\d+", project_name)
            if match is None:
                return client_id
            else:
                project_client_id = cls.check_company_project(match)
                if project_client_id != client_id:
                    # Change on clockify
                    print("client different than expected")
                    print(time_entry)
                return project_client_id
        except IndexError:
            print("No tag")
            project_name = Project.where("clockify_id", time_entry["projectId"]).first().name
            match = re.search("^([A-Z])\d+", project_name)
            if match is None:
                # Change on clockify and send report to member
                print("This is not a company project")
                print(time_entry)
                return Client.where("name", "NEO").first().clockify_id
            else:
                # Change on clockify
                print("This is a company project")
                print(time_entry)
                return cls.check_company_project(match)

    @classmethod
    def check_to_long_time_entry(parameter_list):
        pass

    @classmethod
    def save_from_clockify(cls, start="2019-08-05T00:00:01Z"):
        for member in Member.all():
            url = "{}/workspaces/{}/user/{}/time-entries?hydrated=true&page-size=1000&start={}".format(
                V1_API_URL, WORKSPACE_ID, member.clockify_id, start
            )
            time_entries = requests.get(url, headers=HEADERS)
            for time_entry in time_entries.json():
                if time_entry["timeInterval"]["end"] is not None:
                    clockify_id = time_entry["id"]
                    member_id = time_entry["userId"]
                    project_id = time_entry["projectId"]
                    try:
                        activity_id = Activity.where("name", time_entry["task"]["name"]).first().id
                    except TypeError:
                        print("No task")
                        print(time_entry)
                        # Send report to member
                        continue
                    try:
                        client_id = cls.correct_empty_wrong_tag(time_entry)
                    except ReferenceError:
                        print(time_entry)
                        print("New Company, code needs to be updated")
                        continue
                    start = time_entry["timeInterval"]["start"]
                    end = time_entry["timeInterval"]["end"]
                    description = time_entry["description"]
                    TimeEntry.update_or_create({"clockify_id": clockify_id},
                                               {"member_id": member_id,
                                                "project_id": project_id,
                                                "activity_id": activity_id,
                                                "client_id": client_id,
                                                "start": start,
                                                "end": end,
                                                "description": description})
                else:
                    print("No end time")
                    print(time_entry)
