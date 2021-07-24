from django.core.mail import EmailMessage
from synergyDB.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_PASSWORD
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def message_notification(r_email,first_name,last_name):

	msg1 = f'Welcome { first_name } to Synergy management & Consultants.'
	msg2 = f'If you have not received your login credentials please contact the administration.'
	message = Mail(
	    from_email=DEFAULT_FROM_EMAIL,
	    to_emails=r_email,
	    subject='Welcome Mail',
	    html_content='<h4>'+ msg1 +'</h4>' + '<br><br>' + ' Please visit <a href="http://206.189.234.28/">http://206.189.234.28/</a> to Log In to the system. <br><br>' + msg2 )
	try:
	    sg = SendGridAPIClient(EMAIL_HOST_PASSWORD)
	    response = sg.send(message)
	    print(response.status_code)
	    print(response.body)
	    print(response.headers)
	except Exception as e:
	    print(f'{e} : Error!')