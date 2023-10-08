from datetime import datetime
from aws_list_accounts import accounts
from aws_iam_assumed_roles import assume_role_and_get_client
from aws_alerts import send_sns_email
from aws_s3_bucket_upload import upload_file
import csv

def get_all_users(iam_client):
    """Return all IAM users."""
    response = iam_client.list_users()
    return response['Users']

def get_user_access_keys(iam_client, user_name):
    """Return access keys for a specific IAM user."""
    paginator = iam_client.get_paginator('list_access_keys')
    for page in paginator.paginate(UserName=user_name):
        for key_metadata in page['AccessKeyMetadata']:
            yield key_metadata

def get_all_user_access_keys(iam_client):
    """Return access keys for all IAM users."""
    for user in get_all_users(iam_client):
        for access_key in get_user_access_keys(iam_client, user['UserName']):
            yield access_key

def get_last_used_info(iam_client, access_key_id):
    """Return the last used date for a specific access key."""
    response = iam_client.get_access_key_last_used(AccessKeyId=access_key_id)
    return response['AccessKeyLastUsed']

def format_datetime_to_date(date_obj):
    """Convert a datetime object to a string in the format 'YYYY-M-D'."""
    return date_obj.strftime('%Y-%m-%d')

def get_access_key_summary(iam_client, account_name):
    """Generate a summary for all access keys including last used date."""
    summary = []
    for access_key in get_all_user_access_keys(iam_client):
        last_used_info = get_last_used_info(iam_client, access_key['AccessKeyId'])
        
        # Extract details from access_key and last_used_info
        user_name = access_key['UserName']
        access_key_id = access_key['AccessKeyId']
        status = access_key['Status']
        create_date = format_datetime_to_date(access_key['CreateDate'])
        
        if 'LastUsedDate' in last_used_info:
            last_used_date = last_used_info['LastUsedDate']
            formatted_last_used_date = format_datetime_to_date(last_used_date)
        else:
            last_used_date = datetime.now()
            formatted_last_used_date = 'N/A'

        days_difference = (datetime.now().date() - last_used_date.date()).days
        service_name = last_used_info.get('ServiceName', 'N/A')
        region = last_used_info.get('Region', 'N/A')
        
        summary_entry = (
            account_name,
            user_name,
            access_key_id,
            create_date,
            formatted_last_used_date,
            str(days_difference),
            service_name,
            region,
            status  # Include status here
        )
        summary.append(summary_entry)
    return summary

def disable_access_key(iam_client, user_name, access_key_id):
    """Disable the specified IAM access key."""
    try:
        response = iam_client.update_access_key(
            UserName=user_name,
            AccessKeyId=access_key_id,
            Status='Inactive'
        )
        print(f"Disabled access key {access_key_id} for user {user_name}")
        return user_name, access_key_id
    except Exception as e:
        print(f"Error disabling access key {access_key_id} for user {user_name}: {str(e)}")
        return None, None


def lambda_handler(event, context):
    # Use the /tmp directory to save the temporary file
    file_path = '/tmp/disabled_access_keys.csv'
    
    # List to store details of disabled access keys
    disabled_keys_list = []
    
    for account_role_arn in accounts:
        account_id = account_role_arn.split(":")[4]
        iam_client = assume_role_and_get_client(account_role_arn, "AssumedSession")
        results = get_access_key_summary(iam_client, account_id)
        
        for result in results:
            _, user_name, access_key_id, _, _, days_diff, _, _, status = result  # Unpack the result tuple
            
            if int(days_diff) >= 90 and status == "Active":  # Check if the key is active before disabling
                disabled_user, disabled_key = disable_access_key(iam_client, user_name, access_key_id)
                
                if disabled_key:
                    # Add account_id, user_name, access_key_id, and days_diff to the list
                    disabled_keys_list.append((account_id, disabled_user, disabled_key, days_diff))
    
    # Write disabled keys to CSV
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the header with updated columns
        header = ["account_id", "user_account", "disabled_access_key_id", "days_diff"]
        csv_writer.writerow(header)
        
        # Write the disabled keys
        for entry in disabled_keys_list:
            csv_writer.writerow(entry)
    
    # Upload the file from /tmp to S3
    upload_file(file_path, 'disabled-access-key-accounts', 'disabled_access_keys.csv')

   # Construct a message based on the disabled keys
    if len(disabled_keys_list) == 0:
        message = "No access keys were altered."
    else:
        message = "List of disabled access keys:\n\n"
        for entry in disabled_keys_list:
            message += f"Account ID: {entry[0]}, User: {entry[1]}, Access Key: {entry[2]}, Days: {entry[3]}\n"

    # Send the message using SNS
    topic_arn = "arn:aws:sns:us-east-1:44444444444:AccessKeyAlerts"
    subject = "Access Keys Disabled Report"
    send_sns_email(topic_arn, subject, message)


