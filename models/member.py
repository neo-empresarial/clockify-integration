from orator import Model
from models import API_URL, WORKSPACE_ID, HEADERS
import requests


class Member(Model):

    __table__ = "member"
    __fillable__ = ["clockify_id", "acronym", "email"]
    __primary_key__ = "clockify_id"

    @classmethod
    def save_from_clockify(cls):
        """Check if all users in clockify are register as members in the database.
        Create a new member if necessary."""
        users = cls.get_all_users()
        for user in users:
            member = Member.where("clockify_id", user["clockify_id"]).first()
            if member is None:
                Member.create(
                    clockify_id=user["clockify_id"],
                    acronym=user["acronym"],
                    email=user["email"],
                )
        return users

    @staticmethod
    def get_all_users():
        """Find all users from Clockify on NEO's workspace.

        Returns list of dictionaries containing "acronym", "clockify_id" and "email"
        of every user."""

        url = "{}/workspace/{}/users".format(API_URL, WORKSPACE_ID)
        responses = requests.get(url, headers=HEADERS)
        users = []
        for user in responses.json():
            acronym = user["name"]
            clockify_id = user["id"]
            email = user["email"]
            user_dict = {"acronym": acronym, "clockify_id": clockify_id, "email": email}
            users.append(user_dict)
        return users
