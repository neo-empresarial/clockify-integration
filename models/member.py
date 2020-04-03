from models import *

import requests


class Member(Model):

    __table__ = "member"
    __fillable__ = [
        "clockify_id",
        "acronym",
        "email",
        "is_clt",
        "is_active",
        "date_deactivated",
    ]
    __primary_key__ = "id"
    __incrementing__ = True

    @classmethod
    def save_from_clockify(cls):
        """Check if all users in clockify are register as members in the database.
        Create a new member if necessary."""
        users = cls.fetch_all_users()

        for user in users:
            Member.update_or_create(
                {"clockify_id": user["clockify_id"]},
                {"acronym": user["acronym"], "email": user["email"]},
            )
        return users

    @staticmethod
    def fetch_all_users():
        """Find all users from Clockify on NEO's workspace.

        Returns list of dictionaries containing "acronym", "clockify_id" and "email"
        of every user."""
        url = "{}/workspace/{}/users".format(V1_API_URL, WORKSPACE_ID)
        responses = requests.get(url, headers=HEADERS)
        return [
            {
                "acronym": user["name"].lower(),
                "clockify_id": user["id"],
                "email": user["email"].lower(),
            }
            for user in responses.json()
        ]

    @staticmethod
    def map_all_members():
        """Returns a dictionary of all members in database. Dictionary key is member
           clockify id. This should be used to reduce Queries to our DB in other functions."""

        members_map = {}
        for member in Member.all():
            members_map[member.clockify_id] = {
                "id": member.id,
                "acronym": member.acronym,
                "email": member.email,
            }
        return members_map
