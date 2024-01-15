import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import environ
import requests

env = environ.Env()

def send_email_smtp(subject, body, recipient_email):
    sender_email = env.str("EMAIL")
    password = env.str("EMAIL_PASSWORD")

    print(env.int("SMTP_PORT"))

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Create server object with SSL option
    server = smtplib.SMTP(env.str("SMTP_SERVER"), env.int("SMTP_PORT"))
    server.login(sender_email, password)

    # Send email
    server.send_message(msg)
    server.quit()

def send_email_api(subject, body, recipient_email):
    
    email_params = {
        "apikey": env.str("MAIL_API_KEY"),
        "from": env.str("EMAIL"),
        "to": recipient_email,
        "subject": subject,
        "body": body,
        "isTransactional": True,
    }

    response = requests.post(
        "https://api.elasticemail.com/v2/email/send",
        data=email_params,
    )

    return response
