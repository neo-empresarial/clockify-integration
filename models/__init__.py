from orator import DatabaseManager, Model
import os

V1_API_URL = "https://api.clockify.me/api/v1"
WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")
HEADERS = {
    "X-Api-Key": os.getenv("CLOCKIFY_API_KEY"),
    "content-type": "application/json",
}

DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

CONFIG = {
    "default": os.getenv("ENVIRONMENT"),
    "production": {
        "driver": "postgres",
        "host": DB_HOSTNAME,
        "database": DB_NAME,
        "user": DB_USERNAME,
        "password": DB_PASSWORD,
        "prefix": "",
    },
    "development": {
        "driver": "postgres",
        "host": "localhost",
        "database": "neo-data",
        "user": "neo",
        "password": "neoempresarial",
        "prefix": "",
    },
}


db = DatabaseManager(CONFIG)
Model.set_connection_resolver(db)

from .client import Client
from .activity import Activity
from .member import Member
from .project import Project
from .time_entry import TimeEntry
from .indicator import Indicator
from .indicator_consolidation import IndicatorConsolidation
