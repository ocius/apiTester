from Tests import *
from time import sleep
from SES import send_email
from jinja2 import Template
from tabulate import tabulate
from datetime import datetime

TEMPLATE='''<html>
	<head></head>
	<body>
		<h1>Ocius API Tests Failed</h1>
		<table>
			<tr>
				<th>Test</th>
				<th>Status</th>
			</tr>
            {% for title, status in tests %}
			<tr>
                {% if not title == 'Name' %}
				<td>{{title}}</td>
                {% endif %}
				<td>{{status}}</td>
			</tr>
            {% endfor %}
		</table>
	</body>
</html>'''

def format_message_text(tests):
    tests.insert(0,('Test', 'Status'))
    return tabulate(tests)

def format_message_html(tests):
    tm=Template(TEMPLATE)
    return tm.render(tests=tests)

def handler(event, context):
    ''' 
    Main lambda event handler
    This checks the API and sends an email if a test does not
    return PASSED
    '''
    test_results = run_tests()
    for test, status in test_results:
        if not test == 'Name' and status != 'PASSED':
            message = format_message(tests)
            send_email(message)

if __name__ == '__main__':
    '''
    Run this locally to get hourly terminal updates
    '''
    while True:
        test_results = run_tests()
        print(datetime.now().strftime("%m/%d, %H:%M:%S"))
        print(format_message_text(test_results))
        sleep(60*60)

