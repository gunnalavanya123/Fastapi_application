import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import Optional

def send_email(subject: str, recipient_email: str, body: str, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str, sender_email: Optional[str] = None):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email or smtp_user
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
