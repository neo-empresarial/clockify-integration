from .client import Client
from .activity import Activity
from .member import Member
from .project import Project
from .time_entry import TimeEntry
import os

V1_API_URL = "https://api.clockify.me/api/v1"
WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
API_URL = "https://api.clockify.me/api/"
HEADERS = {"X-Api-Key": os.getenv("CLOCKIFY_API_KEY")}
