# Automation to unused AWS Access Keys

This article describes the methodology for automating the deactivation of access keys in all AWS accounts that have not been used for more than N's days, taking advantage of a set of AWS services: Lambda, Python, SNS, S3, EventBridge and IAM Roles.

<<< If you want to know more details on how to implement it, please visit my [article on Medium](https://rcedros.medium.com/automation-and-management-unused-aws-access-keys-50d9dadf8e2b) >>> 

## Architecture
1. **IAM Roles**: Roles to access all AWS Accounts and services.
2. **Lambda**: Run the Python code.
3. **Language**: Python 3.10.
4. **SNS**: Send a email of access keys are deactivate.
5. **EventBridge**: Invoke and schedule automation.
6. **S3**: Save csv file with results in a bucket (optional).

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

