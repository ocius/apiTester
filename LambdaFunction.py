from Tests import run_tests
from SES import send_email
from jinja2 import Template

TEMPLATE='''
<!DOCTYPE html>
<html>
<meta charset="UTF-8">
<head> </head>
    <body>
        <h1> Ocius API Tests Failed </h1>
       {% for test_group, tests in test_groups.items() %}
            <h2> {{test_group}} </h2>
            <table style="font-family: 'Arial'; border-collapse: collapse; border: 1px solid #eee; border-bottom: 2px solid rgb(18, 81, 146); box-shadow: 0px 0px 20px rgba(0,0,0,0.10), 0px 10px 20px rgba(0,0,0,0.05), 0px 20px 20px rgba(0,0,0,0.05), 0px 30px 20px rgba(0,0,0,0.05);">
                <tr>
                    <th style="background: rgb(18, 81, 146); color: #fff;">
                        Test
                    </th>
                    <th style="background: rgb(18, 81, 146); color: #fff;">
                        Status
                    </th>
                </tr>
           {% for title, status in tests %}
                <tr>
               {% if not title == 'Name' %}
                    <td style="border: 1px solid #eee; padding: 12px 35px; border-collapse: collapse;">
                        {{title}}
                    </td>
                    <td style="border: 1px solid #eee; padding: 12px 35px; border-collapse: collapse;">
                        {{status}}
                    </td>
               {% else %}
                    <td style="border: 1px solid #eee; padding: 12px 35px; border-collapse: collapse; font-weight: bold;">
                        {{status}}
                    </td>
               {% endif %}
                </tr>
           {% endfor %}
            </table>
       {% endfor %}
        <p> To manually check the response, copy and paste the below into a pretty printer</p>
        <pre>
            {{response}}
        </pre>
    </body>
</html>
'''


def format_message_html(test_groups, response):
    tm = Template(TEMPLATE)
    return tm.render(test_groups=test_groups, response=response)


def handler(event, context):
    '''
    Main lambda event handler
    This checks the API and sends an email if a test does not
    return PASSED
    '''
    test_groups, API_response = run_tests()
    for test_group in test_groups:
        for test, status in test_groups[test_group]:
            if not test == 'Name' and status != 'PASSED':
                message_html = format_message_html(test_groups, API_response.json())
                send_email(message_html, message_html)
                return {'message': API_response.json()}
    return {'message': 'All tests passed'}


if __name__ == "__main__":
    test_groups, API_response = run_tests()
    message_html = format_message_html(test_groups, API_response.json())
    with open('email.html', 'w') as f:
        f.write(message_html)
    print({'message': 'All tests passed'})
