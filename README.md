[![Maintainability](https://api.codeclimate.com/v1/badges/b8c97fe0cb9760a0a19c/maintainability)](https://codeclimate.com/github/neo-empresarial/clockify-integration/maintainability)

# Clockify Integration

Hey NEOson, welcome to the Clockify Integration repository! The main purpose of this program is to get the data from Clockify so we can replace the Excel timesheet for something better. 

## How it works

We use [AWS Lambda](https://aws.amazon.com/lambda/) to run a python script every day that uses [Clockify API](https://clockify.me/developers-api) to fetch all projects, members, activities, clients and time entries. We process all this data and save on the right format in a database. After that, we use [Metabase](https://www.metabase.com/) to analyze the data saved in the database. By doing all of that we have live data and metrics about every NEOson that is readily available to anyone at NEO.

## Installation

### PostgreSQL

If you are using **Ubuntu**, you can install [PostgreSQL](https://www.postgresql.org/) by running:

```bash
$ sudo apt-get install postgresql-11
```

Or on **macOS** (assuming you have homebrew installed):

```bash
$ brew install postgresql
```

### Python requirements

We recommend to use pyenv to install python 3.7.4 locally and then use pipenv to install the requirements with:

```
$ pipenv install && pipenv shell
```

### .env file

Using the `.template.env` fill the missing keys and save it as a **new** copy with the name `.env` at the root directory of the project. Pipenv will use this file to load the environment variables.

### Migrate database

After installing postgres we can create a database and default database user you'll use in your development environment.

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

Now we must give user 'neo' the privileges needed to access the database we just created.
You can do this by opening the PostgreSQL CLI in your preferred command line shell. This can be done through running:

```bash
$ psql
```

and you'll be inside the Postgres interface. Now we want to grant access to the recently created database. You can do so by running:

```bash
GRANT ALL PRIVILEGES ON DATABASE "neo-data" TO neo;
```
inside your session. After this, if you want quit the Postgres client, simply type `\q`

--- 

With the database created and python requirements installed we can migrate the tables. We will use the `orator_config.py` file to migrate, run the following command:

```bash
$ orator migrate -c orator_config.py
```
And then run the seeds with:

```bash
$ orator db:seed -c orator_config.py
```

If you want to begin a new database, you can run this SQL query:

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

and run the migrations and seeds again.
