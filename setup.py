import boto3
import os


def create_sns_topic():
    sns = boto3.client("sns", region_name='us-east-1')
    return sns.create_topic(Name="neo-data")


if __name__ == "__main__":
    create_sns_topic()
