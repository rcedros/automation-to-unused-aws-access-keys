# Automation to unused AWS Access Keys

This article describes the methodology for automating the deactivation of access keys in all AWS accounts that have not been used for more than 90 days, taking advantage of a set of AWS services: Lambda, Python, SNS, S3, EventBridge and IAM Roles.


# Architecture
1. IAM Roles: Roles to access all AWS Accounts and services.
2. Lambda: Run the Python code.
3. Language: Python 3.10.
4. SNS: Send a email of access keys are deactivate.
5. EventBridge: Invoke and schedule automation.
6. S3: Save csv file with results in a bucket (optional).
