import os

DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASES = {
    "production": {
        "driver": "postgres",
        "host": DB_HOSTNAME,
        "database": DB_NAME,
        "user": DB_USERNAME,
        "password": DB_PASSWORD,
        "prefix": "",
    }
}
