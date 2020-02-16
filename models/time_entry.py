from models import *
from orator.orm import belongs_to
import re
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
    __primary_key__ = "id"

    @belongs_to("member_id", "id")
    def member(self):
        return Member

    @belongs_to("project_id", "id")
    def project(self):
        return Project

    @belongs_to("activity_id", "id")
    def activity(self):
        return Activity

    @belongs_to("client_id", "id")
    def client(self):
        return Client

    @staticmethod
    def find_company(project_name):
        """Returns clockify_id from company based on the project name"""
        if project_name[0] == "c":
            return Client.where("name", "certi").first()
        elif project_name[0] == "e":
            return Client.where("name", "embraco").first()
        elif project_name[0] == "n":
            return Client.where("name", "neo").first()
        elif project_name[0] == "t":
            return Client.where("name", "tupy").first()
        elif project_name[0] == "w":
            return Client.where("name", "weg").first()
        else:
            print(project_name)
            raise ReferenceError("No client starts with this letter")

    @staticmethod
    def tag_is_empty(time_entry):
        """Check if the time entry has an empty tag"""
        try:
            tag_id = time_entry["tags"][0]["id"]
            return False
        except IndexError:
            return True

    @staticmethod
    def is_company_project(project_name):
        """Check if this is a company project.
           Company projects starts with a letter followed by numbers (e.g. 'W101')"""
        return bool(re.search("^([a-z])\d+", project_name))

    @staticmethod
    def update_tag_clockify(time_entry, tag_clockify_id):
        """Update a Time Entry tag in clockify workspace.
           Returns the request response."""
        url_update = "{}/workspaces/{}/time-entries/{}".format(
            V1_API_URL, WORKSPACE_ID, time_entry["id"]
        )

        update_time_entry = {
            "start": time_entry["timeInterval"]["start"],
            "billable": time_entry["billable"],
            "description": time_entry["description"],
            "projectId": time_entry["projectId"],
            "taskId": time_entry["task"]["id"],
            "end": time_entry["timeInterval"]["start"],
            "tagIds": [tag_clockify_id],
        }
        return requests.put(url_update, json=update_time_entry, headers=HEADERS)

    @classmethod
    def correct_empty_or_wrong_tag(cls, time_entry):
        """Check if the tag is empty and if the time entry is for a company project.
           With that it can sometimes correct the tag."""
        project_name = (
            Project.where("clockify_id", time_entry["projectId"]).first().name
        )
        tag_is_empty = cls.tag_is_empty(time_entry)
        is_company_project = cls.is_company_project(project_name)

        if tag_is_empty and is_company_project:
            # Send report to user
            company = cls.find_company(project_name)
            cls.update_tag_clockify(time_entry, company.clockify_id)
            print(
                "Time Entry {}, in project {} has empty tag. Assuming tagName is {}".format(
                    time_entry["id"], project_name, company.name
                )
            )
            return company.id
        elif tag_is_empty and not is_company_project:
            # Send report to user;
            print(
                "Time Entry {}, in project {} has empty tag. Assuming tagName is neo".format(
                    time_entry["id"], project_name
                )
            )
            neo = Client.where("name", "neo").first()
            cls.update_tag_clockify(time_entry, neo.clockify_id)
            return neo.id

        company_tag = (
            Client.where("clockify_id", time_entry["tags"][0]["id"]).first().id
        )

        if not tag_is_empty and is_company_project:
            expected_company = cls.find_company(project_name)
            if company_tag != expected_company.id:
                # Send report to user
                cls.update_tag_clockify(time_entry, expected_company.clockify_id)
                print(
                    "Time Entry {}, in project {} has a wrong tag. Assuming tagName is {}".format(
                        time_entry["id"], project_name, expected_company.name
                    )
                )
            return expected_company.id

        elif not tag_is_empty and not is_company_project:
            # Here we could check alot of stuff
            # like Neócio or if the task of the time entry can have this task.
            return company_tag

    @staticmethod
    def check_to_long_time_entry(parameter_list):
        pass

    @classmethod
    def save_from_clockify(cls, start="2019-08-05T00:00:01Z"):
        for member in Member.all():
            if member.clockify_id is not None:
                url_get = "{}/workspaces/{}/user/{}/time-entries?hydrated=true&page-size=1000&start={}".format(
                    V1_API_URL, WORKSPACE_ID, member.clockify_id, start
                )
                time_entries = requests.get(url_get, headers=HEADERS)
                for time_entry in time_entries.json():
                    if time_entry["timeInterval"]["end"] is not None:
                        clockify_id = time_entry["id"]
                        member_id = (
                            Member.where("clockify_id", time_entry["userId"]).first().id
                        )
                        try:
                            project_id = (
                                Project.where("clockify_id", time_entry["projectId"])
                                .first()
                                .id
                            )
                        except AttributeError:
                            print("Time entry sem projeto")
                            continue
                        try:
                            activity_id = (
                                Activity.where(
                                    "name", time_entry["task"]["name"].lower()
                                )
                                .first()
                                .id
                            )
                        except TypeError:
                            print("No task in Time Entry {}".format(clockify_id))
                            # Send report to member
                            continue
                        try:
                            client_id = cls.correct_empty_or_wrong_tag(time_entry)
                        except ReferenceError:
                            print(time_entry)
                            print("New Company, code needs to be updated")
                            continue
                        start = time_entry["timeInterval"]["start"]
                        end = time_entry["timeInterval"]["end"]
                        description = time_entry["description"]
                        TimeEntry.update_or_create(
                            {"clockify_id": clockify_id},
                            {
                                "member_id": member_id,
                                "project_id": project_id,
                                "activity_id": activity_id,
                                "client_id": client_id,
                                "start": start,
                                "end": end,
                                "description": description,
                            },
                        )
                    else:
                        print("No end time")
