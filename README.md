# expense-tracker-line-bot
I built this to try out LINE Messaging API. 
This simple AWS + MongoDB LINE bot might serve as a template.

# Example
For context, this bot caps my meal expenses :)
<img width="510" alt="Screenshot 2567-12-16 at 01 21 22" src="https://github.com/user-attachments/assets/3198d34f-c301-4aac-8886-a25c537b62b7" />


# Prerequisites
1. AWS: install and set up AWS CLI + create AWSLambdaBasicExecutionRole
2. [LINE](https://developers.line.biz/en/docs/messaging-api/getting-started/)
3. MongoDB cluster
4. Docker

# Quick Start
1. Refer to cmd.sh for command templates for building a docker image for a lambda function and pushing it to an ECR repository.
My architecture is arm_64 and my Python is of version 3.12; adjust accordingly.

2. These should be your environment variables in the local .env and the lambda function configuration
```bash
LINE_CHANNEL_ACCESS_TOKEN=
LINE_CHANNEL_SECRET=
MDB_URI=
```

# Diagram
<img width="624" alt="Screenshot 2567-12-15 at 23 46 54" src="https://github.com/user-attachments/assets/b5be7a2b-9e62-4304-a660-bf7779aeffee" />
