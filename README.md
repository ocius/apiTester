# Overview

This lambda function is used to test the availability and validity of OCIUS Api. If a single test fails an email is sent to the recipients defined in SES.py.

| API Endpoint                                                    | Testing Depth                      |
| --------------------------------------------------------------- | ---------------------------------- |
| https://api.ocius.com.au/drones                                 | Checks the API provides valid data |
| https://usvna.ocius.com.au/usvna/oc_server?mavstatus&nodeflate  | checks the response status is 200  |
| https://usvna.ocius.com.au/usvna/oc_server?listrobots&nodeflate | checks the response status is 200  |


# Development
## Architecture
### Lambda Function.py
Contains the main program, requests data from all the endpoints, validates the responses using test.py. If a single test has failed SES.py is used to send a summary report.

### SES.py
Defines how emails are sent using AWS's Boto3. Contains hardcoded email subject, recipients, AWS region and sender informaiton.
### Test.py
Defines the various tests for Ocius's drone API and Ocius 

### APIConstants.py
Defines the harcoded endpoints to test


# Deployment

## AWS Lambda (updating existing lambda)

1. Edit the code
2. Add any additional dependencies to bundle.sh
3. Run `sh bundle.sh`
4. upload lambda.zip to AWS Lambda

## AWS Lambda (creating a new lambda)

1. Check the email address kevin.chan@ocius.com.au is a verified SES email
2. Install into AWS Lambda using the IAM.json policy (to allow access to SES)
3. Create a rule in cloudwatch to execute this lambda function every hour
4. Profit

## Locally

Install the necessary packages with pipenv

```
pipenv install
```

and then run the tests with the below command

```
python3 LambdaFunction.py
```

This will print a test summary in terminal every hour

```
04/27, 21:05:23
-----------  ------
Test         Status
API Online   PASSED
Name         Bruce
Basic        PASSED
Coordinates  PASSED
Cameras      PASSED
Name         Bob
Basic        PASSED
Coordinates  PASSED
Cameras      PASSED
-----------  ------
```

## Cost

https://aws.amazon.com/ses/pricing/
AWS SES charges $0.10 every 1000 emails. At worst case, 1 email a day for a month will send a maximum of (24\*30) 720 emails < $0.10
