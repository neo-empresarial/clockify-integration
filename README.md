# Clockify Integration

Hey NEOson, welcome to the Clockify Integration repository! The main purpose of this program is to get the data from Clockify so we can replace the Excel timesheet for something better. 

# How does it work?

We use [AWS Lambda](https://aws.amazon.com/lambda/) to run a python script every day that uses [Clockify API](https://clockify.me/developers-api) to fetch all projects, members, activities, clients and time entries. We process all this data and save on the right format in a database. After that, we use [Metabase](https://www.metabase.com/) to analyze the data saved in the database. By doing all of that we have live data and metrics for every NEOson to use without much technical knowledge needed.

# Installation

## PostgreSQL

If you'r using **Ubuntu** you can install [PostgreSQL](https://www.postgresql.org/) with:

```bash
$ sudo apt-get install postgresql-11
```

Or on **MacOs** with:

```bash
$ brew install postgresql
```

---

After installing postgres we can create the default user and database we use for the development database.

```bash
sudo -u postgres -i
```

Now we can run commands as the PostgresSQL superuser. To create a user, type the following command:

```
$ createuser --interactive --pwprompt
Enter name of role to add: neo
Enter password for new role: neoempresarial
Enter it again: neoempresarial
Shall the new role be a superuser? y
```

Then create a database with:

```bash
$ createdb -O neo "neo-data"
```

Now lets give neo user privileges to this database and exit postgres shell with:

```
$ psql
# GRANT ALL PRIVILEGES ON DATABASE "neo-data" TO neo;
# \q
$ exit
```

--- 

With the development database created we can migrate the tables. To do so we need to create a file called `orator.py` with the following lines:

```python
DATABASES = {
    'development': {
        'driver': 'postgres',
        'host': 'localhost',
        'database': 'neo-data',
        'user': 'neo',
        'password': 'neoempresarial',
        'prefix': ''
    }
}
```

Before we can migrate you need to install the python requirements first.

## Python requirements

We recommend to use pyenv to install python 3.7.4 locally and then use pipenv to install the requirements with:

```
$ pipenv install && pipenv shell
```

## Migrate database

With the `orator.py` file created and the python requirements installed run te following command:

```bash
$ orator migrate
```

After running the command delete the `orator.py` file. 

If you want to recreate a fresh database. Just delete all the tables from the database and repeat the steps above. 

## .env file

Create .env file inside config folder with the following keys:

```
DB_HOSTNAME=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_PORT=5432
DB_URI=
ENVIRONMENT=production
CLOCKIFY_API_KEY=
CLOCKIFY_WORKSPACE_ID=
SENDGRID_API_KEY=
AWS_DEFAULT_REGION=
SNS_TOPIC_NAME=
```