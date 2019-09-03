from orator import Model
from .config import V1_API_URL, WORKSPACE_ID, HEADERS
import requests


class Client(Model):

    __table__ = "client"
    __fillable__ = ["clockify_id", "name"]
    __primary_key__ = "clockify_id"

    @classmethod
    def save_from_clockify(cls):
        """Check if all tags in clockify are register as clients in the database.
        Create a new client if necessary."""
        tags = cls.fetch_all_tags()
        for tag in tags:
            Client.update_or_create({"clockify_id":tag["clockify_id"]},
                                    {"name":tag["name"]})
        return tags

    @staticmethod
    def fetch_all_tags():
        """Find all tags from Clockify on NEO's workspace.

        Returns list of dictionaries containing "clockify_id" and "name"
        of every tag."""

        url = "{}/workspaces/{}/tags".format(V1_API_URL, WORKSPACE_ID)
        responses = requests.get(url, headers=HEADERS)
        return [
            {"clockify_id": client["id"], "name": client["name"]}
            for client in responses.json()
        ]
