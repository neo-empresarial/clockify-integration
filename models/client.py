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
                {"clockify_id": client["clockify_id"]}, {"name": client["name"]}
            )
        return clients

    @staticmethod
    def fetch_all_clients(archived=None):
        """Find all clients from Clockify on NEO's workspace.

        Returns list of dictionaries containing "clockify_id" and "name"
        of every client."""

        url = "{}/workspaces/{}/clients".format(V1_API_URL, WORKSPACE_ID)
        responses = requests.get(url, headers=HEADERS)
        return [
            {"clockify_id": client["id"], "name": client["name"].lower()}
            for client in responses.json()
        ]

    @staticmethod
    def map_all_clients():
        """Returns a dictionary of all clients in database. Dictionary key is client
           clockify id. This should be used to reduce Queries to our DB in other functions."""

        clients_map = {}
        for client in Client.all():
            clients_map[client.clockify_id] = {"id": client.id, "name": client.name}
        return clients_map
