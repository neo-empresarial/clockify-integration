import requests
import argparse
import sys
import click
from typing import List

sys.path.append("../")
from models import *


def valid_project_name(name: str, valid_initials: List[str]) -> bool:
    if len(name) < 4:
        return False
    if not (name[0].lower() in valid_initials):
        return False
    try:
        proj_int = int(name[1:])
        return True
    except:
        return False
    return True


@click.command()
@click.option("--name", prompt="Project name", help="The name for the project.")
def create_project(name: str) -> None:
    colors = {
        "e": "#69b39e",
        "t": "#09215d",
        "n": "#ff9800",
        "w": "#1b60ce",
        "c": "#8bc34a",
    }

    if not valid_project_name(name, colors.keys()):
        print(
            " A client cannot be assigned to a project with this name.\
        \n Please use format C###, in which C is the company initial\
        \n and ### the project number, completed with zeros to the left if necessary."
        )
        return

    client = Client.where("name", "like", f"{name[0].lower()}%").first()
    project_name = name.upper()
    default_activities = Project.find(0).activities

    proj_data = {
        "name": project_name,
        "isPublic": "true",  # On Clockify this means the project is visible to the whole team
        "billable": "true",
        "color": colors.get(project_name[0].lower(), "#ffffff"),
        "tasks": [{"name": activity.name} for activity in default_activities.all()],
        "clientId": client.clockify_id,
    }

    proj_response = requests.post(
        f"{V1_API_URL}/workspaces/{WORKSPACE_ID}/projects",
        json=proj_data,
        headers=HEADERS,
    )

    if proj_response.status_code != 201:
        print(f"Project {project_name} could not be created in Clockify. Aborting.")
        return
    print(f"Project {project_name} created in Clockify.")
    proj_clockify_id = proj_response.json().get("id")
    try:
        new_proj = Project.create(
            name=project_name.lower(), clockify_id=proj_clockify_id
        )
        new_proj.activities().sync(default_activities.map(lambda x: x.id).all())

        print(f"Project {project_name} created in {os.getenv('ENVIRONMENT')} database.")
    except:
        print(
            f"Project {project_name} could not be created in {os.getenv('ENVIRONMENT')} database."
        )
    pass


if __name__ == "__main__":
    create_project()
