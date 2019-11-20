from models import *


import requests


class Client(Model):

    __table__ = "client"
    __fillable__ = ["clockify_id", "name"]
    __primary_key__ = "id"
    __incrementing__ = True

    @classmethod
    def save_from_clockify(cls):
        """Check if all clients in clockify are register as clients in the database.
        Create a new client if necessary."""
        clients = cls.fetch_all_clients()
        for client in clients:
            Client.update_or_create(
                {"name": client["name"]}, {"clockify_id": client["clockify_id"]}
            )
        return clients

    @staticmethod
    def fetch_all_clients():
        """Find all clients from Clockify on NEO's workspace.
        Returns list of dictionaries containing 'clockify_id' and 'name'
        of every client."""
        responses = requests.get(
            f"{V1_API_URL}/workspaces/{WORKSPACE_ID}/clients", headers=HEADERS
        )
        return [
            {"clockify_id": client["id"], "name": client["name"].lower()}
            for client in responses.json()
        ]
