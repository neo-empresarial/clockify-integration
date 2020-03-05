from models import *
from orator.orm import belongs_to
import re
import requests
import pandas as pd
from pandas import json_normalize
from models import *


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
        return pd.isna(time_entry["tag.id"])

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
            "start": time_entry["timeInterval.start"],
            "billable": time_entry["billable"],
            "description": time_entry["description"],
            "projectId": time_entry["projectId"],
            "taskId": time_entry["task.id"],
            "end": time_entry["timeInterval.end"],
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
            Client.where("clockify_id", time_entry["tag.id"]).first().id
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

    @staticmethod
    def fetch_all_time_entries(start):
        """Return time entries from all members that started after the specified start 
           datetime from clockify in a pandas dataframe"""
        data = []
        for member in Member.all():
            if member.clockify_id is not None:
                url_get = "{}/workspaces/{}/user/{}/time-entries?hydrated=true&in-progress=0&page-size=1000&start={}".format(
                    V1_API_URL, WORKSPACE_ID, member.clockify_id, start
                )
                time_entries = requests.get(url_get, headers=HEADERS, stream=False).json()
                if len(time_entries) != 0:
                    df_te = json_normalize(time_entries, record_prefix='te.')
                    df_tags = json_normalize(time_entries, ["tags"], ['id'],
                                           record_prefix='tag.', meta_prefix='te.', errors='ignore')
                    df_all = pd.merge(df_te, df_tags, left_on='id', right_on='te.id', how='left')
                    cols_to_keep = ['id','description','billable','userId','projectId',
                                    'project.name','project.clientId','project.archived',
                                    'project.clientName','project.note','timeInterval.start',
                                    'timeInterval.end','task.id','task.name','tag.id',
                                    'tag.name',
                                   ]
                    df_all = df_all[cols_to_keep]
                    df_all["member_id"] = member.id
                    data.append(df_all)
        return pd.concat(data, sort=False)

    @classmethod
    def process_time_entry(cls, time_entry):
        """Check and correct time entry data before sending to database"""
        if not pd.isna(time_entry["timeInterval.end"]):
            clockify_id = time_entry["id"]
            member_id = (
                Member.where("clockify_id", time_entry["userId"]).first().id
            )
            if not pd.isna(time_entry["projectId"]):
                project_id = (
                    Project.where("clockify_id", time_entry["projectId"])
                    .first()
                    .id
                )
            else:
                print("Time entry sem projeto")
                return
            if not pd.isna(time_entry["task.name"]):
                activity_id = (
                    Activity.where("name", time_entry["task.name"].lower())
                    .first()
                    .id
                )
            else:
                print("No task in Time Entry {}".format(clockify_id))
                # Send report to member
                return
            try:
                client_id = cls.correct_empty_or_wrong_tag(time_entry)
            except ReferenceError:
                print("New Company, code needs to be updated")
                return
            start = time_entry["timeInterval.start"]
            end = time_entry["timeInterval.end"]
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

    @classmethod
    def save_from_clockify(cls, start="2020-01-01T00:00:01Z"):
        """Save all time entries from all members that started after the specified start
           datetime from clockify in the database"""
        time_entries = cls.fetch_all_time_entries(start)
        time_entries.apply(lambda time_entry: cls.process_time_entry(time_entry), axis=1)
        return
