## Cross-account IAM Roles and policy permission
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Action": [
                "iam:ListAccessKeys",
                "iam:UpdateAccessKey",
                "iam:ListUsers",
                "iam:GetAccessKeyLastUsed"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
## Lambda Permission

### LambdaStsAssumeRole
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sts:AssumeRole",
            "Resource": "*"
        }
    ]
}
```

### S3-PutObject-Lambda
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3-object-lambda:*",
                "s3:PutObject"
            ],
            "Resource": "*"
        }
    ]
}
```
### SNS-Push-Message

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "sns:Publish"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```
