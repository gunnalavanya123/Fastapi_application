import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random 
import string
import os

class EmailService():
    def send_email(self, to_email, subject, body):
        EMAIL_SERVER = os.getenv("EMAIL_SERVER")
        EMAIL_PORT = int(os.getenv("EMAIL_PORT"))  # Ensure the port is an integer
        EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = to_email 
        msg['Subject'] = subject 
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                server.send_message(msg)
            return "Email sent successfully."
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")