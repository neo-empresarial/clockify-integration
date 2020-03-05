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
                time_entries = requests.get(
                    url_get, headers=HEADERS, stream=False
                ).json()
                if len(time_entries) != 0:
                    df_te = json_normalize(time_entries, record_prefix="te.")
                    cols_to_keep = [
                        "id",
                        "description",
                        "billable",
                        "userId",
                        "projectId",
                        "project.name",
                        "project.clientId",
                        "project.archived",
                        "project.clientName",
                        "project.note",
                        "timeInterval.start",
                        "timeInterval.end",
                        "task.id",
                        "task.name",
                        "tags",
                    ]
                    df_te = df_te[cols_to_keep]
                    df_te["member_id"] = member.id
                    data.append(df_te)
        return pd.concat(data, sort=False)

    @classmethod
    def process_time_entry(cls, time_entry):
        """Check and correct time entry data before sending to database"""
        if not pd.isna(time_entry["timeInterval.end"]):
            clockify_id = time_entry["id"]
            member_id = Member.where("clockify_id", time_entry["userId"]).first().id
            if not pd.isna(time_entry["projectId"]):
                project_id = (
                    Project.where("clockify_id", time_entry["projectId"]).first().id
                )
            else:
                print("Time entry sem projeto")
                return
            if not pd.isna(time_entry["task.name"]):
                activity_id = (
                    Activity.where("name", time_entry["task.name"].lower()).first().id
                )
            else:
                print("No task in Time Entry {}".format(clockify_id))
                # Send report to member
                return
            try:
                client_id = time_entry["client_id"]
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
        clients_dict = Client.map_all_clients()
        time_entries = cls.fetch_all_time_entries(start)
        time_entries["client_id"] = time_entries["project.clientId"].apply(
            lambda client_clockify_id: clients_dict.get(client_clockify_id).get("id")
        )
        time_entries.apply(
            lambda time_entry: cls.process_time_entry(time_entry), axis=1
        )
        return
