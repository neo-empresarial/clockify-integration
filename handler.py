import boto3
import json
import datetime
from datetime import timezone
from services import EmailSender


def periodic_handler(event, context):
    sns = boto3.client("sns")

    context_parts = context.invoked_function_arn.split(":")
    topic_name = "clockify"
    topic_arn = "arn:aws:sns:{region}:{account_id}:{topic}".format(
        region=context_parts[3], account_id=context_parts[4], topic=topic_name
    )

    sns.publish(
        TopicArn=topic_arn,
        Message="test",
        MessageAttributes={"task": {"DataType": "String", "StringValue": "users"}},
    )


def update_users(event, context):
    print(event)


def update_projects(event, context):
    pass


def update_activities(event, context):
    pass


def update_tags(event, context):
    pass


def update_time_entries(event, context):
    pass


def email_on_success(event, context):
    return EmailSender(["lab@certi.org.br", "jnr@certi.org.br"]).send()
