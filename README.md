# Running locally
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

# Deployment
1. Check the email address kevin.chan@ocius.com.au is a verified SES email
2. Install into AWS Lambda using the IAM.json policy (to allow access to SES)
3. Create a rule in cloudwatch to execute this lambda function every hour
4. Profit
 
## Cost
https://aws.amazon.com/ses/pricing/
AWS SES charges $0.10 every 1000 emails. At worst case, 1 email a day for a month will send a maximum of (24*30) 720 emails < $0.10
