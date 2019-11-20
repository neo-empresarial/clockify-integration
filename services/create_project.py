import requests
import argparse
import sys
import click
from typing import AnyStr

sys.path.append("../")
from models import *


@click.command()
@click.option("--name", prompt="Project name", help="The name for the project.")
def create_project(name: AnyStr) -> None:
    colors = {
        "e": "#69b39e",
        "t": "#09215d",
        "n": "#ff9800",
        "w": "#1b60ce",
        "c": "#8bc34a",
    }

    def valid_project_name(name: AnyStr) -> bool:
        if len(name) < 4:
            return False
        if not (name[0].lower() in colors.keys()):
            return False
        try:
            proj_int = int(name[1:])
            return True
        except:
            return False
        return True

    if not valid_project_name(name):
        print(
            "A client cannot be assigned to a project with this name.\
        \n Please use format C###, in which C is the company initial\
        \n and ### the project number, completed with zeros to the left if necessary.)"
        )
        return

    client = Client.where("name", "like", f"{name[0]}%").first()

    project_name = name.upper()

    default_activities = Project.find(0).activities
    import pdb

    pdb.set_trace()
    proj_data = {
        "name": project_name,
        "isPublic": "true",  # On Clockify this means the project is visible to the whole team
        "billable": "true",
        "color": colors.get(project_name[0], "#ffffff"),
        "tasks": [{"name": activity.name} for activity in default_activities.all()],
        "clientId": client.clockify_id,
    }

    proj_response = requests.post(
        f"{V1_API_URL}/workspaces/{WORKSPACE_ID}/projects",
        json=proj_data,
        headers=HEADERS,
    )
    proj_clockify_id = proj_response.json().get("id")

    new_proj = Project.create(name=project_name, clockify_id=proj_clockify_id)
    new_proj.activities().sync(default_activities.map(lambda x: x.id).all())

    print(f"Project {project_name} created.")
    pass


if __name__ == "__main__":
    create_project()
