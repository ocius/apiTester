'''
Uses AWS SES to send an email
Code from https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
'''
import boto3
from botocore.exceptions import ClientError
from APIConstants import *

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "kevin.chan@ocius.com.au"

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENTS = ["kevin.chan@ocius.com.au", "tom@ocius.com.au"]

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
# CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "ap-southeast-2"

# The subject line for the email.
SUBJECT = "Ocius drone API report"

# The character encoding for the email.
CHARSET = "UTF-8"
# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)

# Try to send the email.


def send_email(message_html, message_text):
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENTS,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': message_html,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': message_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
