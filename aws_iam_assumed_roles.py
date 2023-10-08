import boto3

def assume_role_and_get_client(role_arn, session_name):
    """
    Assume a role and return an IAM client using the assumed role's credentials.
    """
    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
    )

    credentials = assumed_role_object['Credentials']

    iam_client = boto3.client(
        'iam',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

    return iam_client