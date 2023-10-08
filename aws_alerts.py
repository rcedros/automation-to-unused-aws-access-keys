import boto3

def send_sns_email(topic_arn, subject, message):
    """Send an email using Amazon SNS"""
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )

