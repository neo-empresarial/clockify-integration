import boto3
import os
from models import Activity, Client, Member, Project, TimeEntry
from services import EmailSender

# from services import EmailSender
tasks = ["users", "projects", "activities", "tags", "time_entries"]


def periodic_handler(event, context):
    sns_publisher(event, context, "time_entries")


def sns_publisher(event, context, task):
    sns = boto3.client("sns")

    context_parts = context.invoked_function_arn.split(":")
    topic_name = os.getenv("sns_topic_name")
    topic_arn = "arn:aws:sns:{region}:{account_id}:{topic}".format(
        region=context_parts[3], account_id=context_parts[4], topic=topic_name
    )

    sns.publish(
        TopicArn=topic_arn,
        Message="T",
        MessageAttributes={"task": {"DataType": "String", "StringValue": task}},
    )


def update_users(event, context):
    try:
        Member.save_from_clockify()
    except Exception:
        sns_publisher(event, context, "time_entries")


def update_projects(event, context):
    try:
        Project.save_from_clockify()
    except Exception:
        sns_publisher(event, context, "time_entries")


def update_activities(event, context):
    try:
        Activity.save_from_clockify()
    except Exception:
        sns_publisher(event, context, "time_entries")


def update_tags(event, context):
    try:
        Client.save_from_clockify()
    except Exception:
        sns_publisher(event, context, "time_entries")


def update_time_entries(event, context):
    try:
        TimeEntry.save_from_clockify()
    except Exception:
        for task in tasks[:-1]:
            sns_publisher(event, context, task)


def email_on_success(event, context):
    return EmailSender(["lab@certi.org.br", "jnr@certi.org.br"]).send()
