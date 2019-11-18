import requests
import argparse
import sys
import click
from typing import AnyStr

sys.path.append("../")
from models import *


def create_client(name: AnyStr) -> None:
    proj_response = requests.post(
        f"{V1_API_URL}/workspaces/{WORKSPACE_ID}/clients",
        json={"name": name},
        headers=HEADERS,
    )
    print(f"Client {name} created.")
    pass


@click.command()
@click.option("--name", prompt="Project name", help="The name for the project.")
# @click.option("--client", prompt="Client name", help="The client name for the project.")
def create_project(name: AnyStr) -> None:
    colors = {
        "e": "#69b39e",
        "t": "#09215d",
        "n": "#FF9800",
        "w": "#1b60ce",
        "c": "#8BC34A",
    }
    project_name = name.upper()
    default_activities = Project.find(0).activities
    proj_data = {
        "name": project_name,
        "isPublic": "false",
        "billable": "true",
        "color": colors[name[0]],
    }
    proj_response = requests.post(
        f"{V1_API_URL}/workspaces/{WORKSPACE_ID}/projects",
        json=proj_data,
        headers=HEADERS,
    )
    proj_clockify_id = proj_response.json().get("id")

    for activity in default_activities.all():
        ac_data = {"name": activity.name, "projectId": proj_clockify_id}
        requests.post(
            f"{V1_API_URL}/workspaces/{WORKSPACE_ID}/projects/{proj_clockify_id}/tasks",
            json=ac_data,
            headers=HEADERS,
        )

    new_proj = Project.create(name=project_name, clockify_id=proj_clockify_id)
    new_proj.activities().sync(default_activities.map(lambda x: x.id).all())
    print(f"Project {project_name} created.")
    pass


if __name__ == "__main__":
    create_project()
