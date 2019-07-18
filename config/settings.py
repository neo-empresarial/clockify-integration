from orator import DatabaseManager, Model
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

config = {
    "neo_data": {
        "driver": "postgres",
        "host": DB_HOSTNAME,
        "database": DB_NAME,
        "user": DB_USERNAME,
        "password": DB_PASSWORD,
        "prefix": "",
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)
