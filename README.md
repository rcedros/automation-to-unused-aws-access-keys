# Automation to unused AWS Access Keys

This article describes the methodology for automating the deactivation of access keys in all AWS accounts that have not been used for more than N's days, taking advantage of a set of AWS services: Lambda, Python, SNS, S3, EventBridge and IAM Roles.

In this project, I’ve set up an AWS Organization comprising four distinct accounts: Production, Homologation, Development, and Security. Within each of these accounts, I’ve established an IAM Role. This role grants the Lambda function (located in the Security Account) the necessary permissions to access the other accounts.

Its primary task is to identify and disable any access keys that have remained unused for more than N’s days. Once an access key is deactivated, an email alert is sent via SNS detailing which specific keys were deactivated.

To automate this process, I’ve configured EventBridge to invoke this Lambda function on a weekly schedule.

<<< If you want to know more details on how to implement it, please visit my [article on Medium](https://rcedros.medium.com/automation-and-management-unused-aws-access-keys-50d9dadf8e2b) >>> 

## Architecture
1. **IAM Roles**: Roles to access all AWS Accounts and services.
2. **Lambda**: Run the Python code.
3. **Language**: Python 3.10.
4. **SNS**: Send a email of access keys are deactivate.
5. **EventBridge**: Invoke and schedule automation.
6. **S3**: Save csv file with results in a bucket (optional).

![image](https://user-images.githubusercontent.com/12600917/278735475-79f48b9c-3465-4804-a398-7c36e75a8a20.png)

## Setup
1. Creating a cross-account IAM Role in all AWS Accounts and give IAM permissions to desactivate AccessKeys.
3. Create a Lambda Function, upload this github file in .zip format and give their role permissions.
4. Create alert using Simple Notification Service (SNS).
5. Create Schedule with AWS EventBridge.

## Files configuration
1. Update [aws_list_accounts.py](https://github.com/rcedros/automation-to-unused-aws-access-keys/blob/main/aws_list_accounts.py) with cross-accounts IAM Roles that were created.
2. Update [main.py](https://github.com/rcedros/automation-to-unused-aws-access-keys/blob/main/main.py) with number of the days disared disabled access keys.
3. Update [main.py](https://github.com/rcedros/automation-to-unused-aws-access-keys/blob/main/main.py) with SNS topic that will send email.
4. Copy/paste [iam_roles_permissions.md](https://github.com/rcedros/automation-to-unused-aws-access-keys/blob/main/iam_roles_permissions.md)

